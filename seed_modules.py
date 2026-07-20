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

# --------------------------------------------------
# Project
# --------------------------------------------------

cur.execute("""
    INSERT INTO projects
    (
        project_name,
        overall_progress,
        current_phase,
        status
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    RETURNING id
""", (
    "Student Management System",
    0,
    "Project Setup",
    "In Progress"
))

project_id = cur.fetchone()[0]

print(f"Project ID: {project_id}")

# --------------------------------------------------
# Git Status
# --------------------------------------------------

cur.execute("""
    INSERT INTO project_git_status
    (
        project_id,
        branch,
        last_processed_commit
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
""", (
    project_id,
    "master",
    None
))

# --------------------------------------------------
# Modules
# --------------------------------------------------

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
        VALUES
        (
            %s,
            %s,
            %s
        )
    """, (
        project_id,
        module,
        "Not Started"
    ))

conn.commit()

cur.close()
conn.close()

print("Database seeded successfully.")