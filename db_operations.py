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
INSERT INTO projects (
    project_name,
    description,
    overall_progress,
    current_phase,
    status
)
VALUES (
    'Student Management System',
    'AI-powered Student Management System built with Django REST Framework',
    35,
    'Attendance Module',
    'In Progress'
);
""")

conn.commit()      # Save changes
cur.close()        # Close cursor
conn.close()       # Close connection

print("Project inserted successfully.")