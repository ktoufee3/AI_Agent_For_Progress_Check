import psycopg2
import config

conn = psycopg2.connect(
    host=config.db_host,
    port=config.db_port,
    database=config.db_name,
    user=config.db_user,
    password=config.db_password
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE project_commits (
    id SERIAL PRIMARY KEY,
    project_id INT,
    commit_hash TEXT UNIQUE,
    author TEXT,
    commit_message TEXT,
    commit_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
""")

conn.commit()      # Save changes
cur.close()        # Close cursor
conn.close()       # Close connection

print("Project inserted successfully.")