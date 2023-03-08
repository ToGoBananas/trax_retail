from db.queries.base import QueriesBase


class QALeaderboardQueries(QueriesBase):
    def get_accuracy_matches(self, username, max_reviews_count):
        sub_q = f"""
            SELECT COUNT(is_match = true) as c1, COUNT(is_match = false) as c2, 
            COUNT(is_match = true and username = '{username}') as c1_user,
            COUNT(is_match = false and username = '{username}') as c2_user 
            from qa_snapshot_session_result 
            JOIN qa_snapshot_session ON qa_snapshot_session.id = qa_snapshot_session_result.session_id 
            GROUP BY qa_snapshot_session_result.snapshot_id HAVING COUNT(is_match is not null) >= {max_reviews_count}"""
        q = f"""
            select sum(
            CASE
                WHEN c1 >= c2 and c1_user <> 0 THEN 1
                WHEN c2 >= c1 and c2_user <> 0 THEN 1
                else -1 END 
            ) as points from ({sub_q})
        """
        return self.db_client.fetch_one(q)["points"]

    def get_finished_sessions_count(self, username):
        return self.db_client.fetch_one(
            f"SELECT count(*) as points from qa_snapshot_session where username = '{username}' "
            f"and remaining_snapshots_quantity = 0;"
        )["points"]

    def update_leaderboard(self, username, points_for_activity, points_for_accuracy):
        return self.db_client.execute(
            f"""
                INSERT INTO qa_leaderboard (username, activity_points, accuracy_points)
                    VALUES ('{username}', '{str(points_for_activity)}', '{str(points_for_accuracy)}')
                ON DUPLICATE KEY UPDATE 
                    activity_points=VALUES(activity_points), accuracy_points=VALUES(accuracy_points);
            """
        )

    def get_leaderboard(self):
        return self.db_client.fetchall("SELECT * from qa_leaderboard order by activity_points + accuracy_points desc;")
