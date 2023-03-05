product_table = """
    CREATE TABLE product (
         id BIGINT NOT NULL UNIQUE,
         name TINYTEXT NOT NULL,
         created DATETIME(6) DEFAULT NOW(6),
         SHARD KEY (id)
    );
"""
product_snapshot_table = """
    CREATE TABLE product_snapshot (
         id BIGINT NOT NULL AUTO_INCREMENT,
         product_id BIGINT NOT NULL,
         filename VARCHAR(10) NOT NULL,
         created DATETIME(6) DEFAULT NOW(6),
         approved_count SMALLINT DEFAULT 0,
         disapproved_count SMALLINT DEFAULT 0,
         KEY(id)
    );
"""
