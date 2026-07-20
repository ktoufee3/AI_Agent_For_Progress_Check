import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import config


DB_NAME = "sms_progress_checker"


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
            overall_progress INTEGER DEFAULT 0,
            current_phase VARCHAR(255),
            status VARCHAR(50),
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

            progress INTEGER DEFAULT 0,

            status VARCHAR(50) DEFAULT 'Not Started',

            started_at TIMESTAMP,

            completed_at TIMESTAMP,

            updated_at TIMESTAMP DEFAULT NOW(),

            CONSTRAINT unique_project_module
                UNIQUE(project_id, module_name)
        );
    """)

    # ---------------------------------------------------------
    # project_milestones
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_milestones
        (
            id SERIAL PRIMARY KEY,

            project_id INTEGER NOT NULL
                REFERENCES projects(id)
                ON DELETE CASCADE,

            milestone_name VARCHAR(255) NOT NULL,

            description TEXT,

            status VARCHAR(50) DEFAULT 'Pending',

            due_date DATE,

            completed_at TIMESTAMP,

            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # ---------------------------------------------------------
    # project_git_status
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS project_git_status
        (
            id SERIAL PRIMARY KEY,

            project_id INTEGER NOT NULL UNIQUE
                REFERENCES projects(id)
                ON DELETE CASCADE,

            repository_url TEXT,

            branch VARCHAR(100) DEFAULT 'main',

            last_processed_commit VARCHAR(64),

            last_checked_at TIMESTAMP,

            created_at TIMESTAMP DEFAULT NOW(),

            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Tables created successfully.")


if __name__ == "__main__":

    create_database()

    create_tables()

    print("Database setup completed successfully.")