# Env setup

```shell
docker compose up -d
python db/migrations.py
python startup_scripts/fill_db.py
```

# Assumptions

- Snapshots and products are immutable

# Other comments

- I've decided to use SingleStore as a database because it has many cool features for ML/CV projects, and I've always wanted to try it :)
- Consistency should be enforced on the application side
- SingleStore might not be the best choice cause of poor integration with python ecosystem
- The images are going to be stored in S3 storage (minio)

# Areas of improvement

- Concurrency
- Move database queries to separate level