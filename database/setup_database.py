#setup_database
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import config

DB_NAME = config.db_name
def create_database():

    conn = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_password
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")

    if cur.fetchone():
        print(f"Database '{DB_NAME}' already exists.")
    else:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully.")

    cur.close()
    conn.close()


# def create_tables():

#     conn = psycopg2.connect(
#         host=config.db_host,
#         port=config.db_port,
#         database=DB_NAME,
#         user=config.db_user,
#         password=config.db_password
#     )

#     cur = conn.cursor()

#     # ---------------------------------------------------------
#     # projects
#     # ---------------------------------------------------------

#     cur.execute("""
#         CREATE TABLE projects
#         (
#             id SERIAL PRIMARY KEY,

#             project_name VARCHAR(255) NOT NULL,

#             description TEXT,

#             repository_url TEXT,

#             default_branch VARCHAR(100) DEFAULT 'main',

#             overall_progress NUMERIC(5,2) DEFAULT 0,

#             created_at TIMESTAMP DEFAULT NOW(),

#             updated_at TIMESTAMP DEFAULT NOW()
#         );
#     """)

#     # ---------------------------------------------------------
#     # project_modules
#     # ---------------------------------------------------------

#     cur.execute("""
#         CREATE TABLE project_modules
#         (
#             id SERIAL PRIMARY KEY,

#             project_id INTEGER NOT NULL
#                 REFERENCES projects(id)
#                 ON DELETE CASCADE,

#             module_name VARCHAR(255) NOT NULL,

#             description TEXT,

#             progress NUMERIC(5,2) DEFAULT 0,

#             status VARCHAR(50) DEFAULT 'Not Started',

#             started_at TIMESTAMP,

#             completed_at TIMESTAMP,

#             updated_at TIMESTAMP DEFAULT NOW(),

#             CONSTRAINT unique_project_module
#                 UNIQUE(project_id, module_name)
#         );
#     """)


#     # ---------------------------------------------------------
#     # project_git_status
#     # ---------------------------------------------------------

#     cur.execute("""
#         CREATE TABLE project_git_status
#         (
#             project_id INTEGER PRIMARY KEY
#                 REFERENCES projects(id)
#                 ON DELETE CASCADE,

#             last_processed_commit VARCHAR(40),

#             last_checked_at TIMESTAMP,

#             updated_at TIMESTAMP DEFAULT NOW()
#         );
#     """)

#     # project_commits
#     cur.execute("""
#         CREATE TABLE project_commits
#         (
#             id SERIAL PRIMARY KEY,

#             project_id INTEGER NOT NULL
#                 REFERENCES projects(id)
#                 ON DELETE CASCADE,

#             commit_hash VARCHAR(40) NOT NULL UNIQUE,

#             author VARCHAR(255),

#             commit_message TEXT,

#             commit_date TIMESTAMP,

#             created_at TIMESTAMP DEFAULT NOW()
#         );

#     """)





#     conn.commit()

#     cur.close()
#     conn.close()

#     print("Tables created successfully.")

# database/setup_database.py

import psycopg2

import config


DB_NAME = "sms_progress_checker"


def create_tables():

    conn = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=DB_NAME,
        user=config.db_user,
        password=config.db_password
    )

    cur = conn.cursor()

    # ---------------------------------------------------------
    # projects
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects
        (
            id SERIAL PRIMARY KEY,

            project_name VARCHAR(255) NOT NULL,

            description TEXT,

            repository_url TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT NOW(),

            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # ---------------------------------------------------------
    # project_modules
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_modules
        (
            id SERIAL PRIMARY KEY,

            project_id INTEGER NOT NULL
                REFERENCES projects(id)
                ON DELETE CASCADE,

            module_name VARCHAR(255) NOT NULL,

            description TEXT,

            progress NUMERIC(5,2) DEFAULT 0,

            status VARCHAR(50) DEFAULT 'Not Started',

            started_at TIMESTAMP,

            completed_at TIMESTAMP,

            updated_at TIMESTAMP DEFAULT NOW(),

            CONSTRAINT unique_project_module
                UNIQUE(project_id, module_name)
        );
    """)

    # ---------------------------------------------------------
    # project_git_status
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_git_status
        (
            project_id INTEGER PRIMARY KEY
                REFERENCES projects(id)
                ON DELETE CASCADE,

            branch VARCHAR(100) DEFAULT 'master',

            last_processed_commit VARCHAR(40),

            last_checked_at TIMESTAMP,

            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # ---------------------------------------------------------
    # project_commits
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_commits
        (
            id SERIAL PRIMARY KEY,

            project_id INTEGER NOT NULL
                REFERENCES projects(id)
                ON DELETE CASCADE,

            commit_hash VARCHAR(40) NOT NULL UNIQUE,

            author VARCHAR(255),

            commit_message TEXT,

            commit_date TIMESTAMP,

            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # ---------------------------------------------------------
    # Indexes
    # ---------------------------------------------------------

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_project_commits_project
        ON project_commits(project_id);
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_project_modules_project
        ON project_modules(project_id);
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Tables created successfully.")

def drop_all_tables():

    conn = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=DB_NAME,
        user=config.db_user,
        password=config.db_password
    )

    conn.set_session(autocommit=True)

    cur = conn.cursor()

    cur.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """)

    cur.close()
    conn.close()

    print("All database objects deleted successfully.")



if __name__ == "__main__":

    # drop_all_tables()

    # create_database()

    create_tables()

    print("Database setup completed successfully.")