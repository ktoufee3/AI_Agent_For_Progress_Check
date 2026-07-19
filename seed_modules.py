#seed_modules.py
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

project_id = 2

modules = [
    "Project Setup",
    "Authentication",
    "Student Management",
    "Teacher Management",
    "Attendance",
    "Fees",
    "Results"
]

for module in modules:

    cur.execute("""
        INSERT INTO project_modules
        (
            project_id,
            module_name,
            status
        )
        VALUES (%s, %s, 'Not Started')
        ON CONFLICT (project_id, module_name) DO NOTHING
    """, (project_id, module))

conn.commit()

cur.close()
conn.close()

print("Modules inserted successfully.")

