qa_snapshot_session_result_table = """
    CREATE TABLE qa_snapshot_session_result (
        session_id INT NOT NULL,
        snapshot_id BIGINT NOT NULL,
        is_match BOOLEAN,
        SHARD KEY (snapshot_id, session_id),
        CONSTRAINT qa_snapshot_session_result_uk UNIQUE (snapshot_id, session_id)
    );
"""

qa_snapshot_session_table = """
    CREATE ROWSTORE TABLE qa_snapshot_session (
        id INT NOT NULL AUTO_INCREMENT,
        username VARCHAR(14) NOT NULL,
        remaining_snapshots_quantity INT NOT NULL,
        created DATETIME(6) DEFAULT NOW(6),
        KEY(id)
    );
"""

qa_leaderboard_table = """
    CREATE ROWSTORE TABLE qa_leaderboard (
        username VARCHAR(14) NOT NULL UNIQUE,
        activity_points DECIMAL(2),
        accuracy_points DECIMAL(2),
        SHARD KEY (username)
    );
"""
