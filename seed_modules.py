# database/seed_database.py

from database.db_manager import get_connection


def seed():

    conn = get_connection()
    cur = conn.cursor()

    try:

        # -----------------------------------------------------
        # Project
        # -----------------------------------------------------

        cur.execute(
            """
            INSERT INTO projects
            (
                project_name,
                description,
                repository_url
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            RETURNING id;
            """,
            (
                "Student Management System",
                "AI-powered Student Management System built with Django REST Framework.",
                "https://github.com/ktoufee3/AI_Agent_For_Progress_Check.git"
            )
        )

        project_id = cur.fetchone()[0]

        # -----------------------------------------------------
        # Modules
        # -----------------------------------------------------

        modules = [
            "Project Setup",
            "Authentication",
            "Student Management",
            "Teacher Management",
            "Course Management",
            "Attendance",
            "Examinations",
            "Fee Management",
            "Notifications",
            "Reports",
            "REST API",
            "AI Progress Checker"
        ]

        for module in modules:

            cur.execute(
                """
                INSERT INTO project_modules
                (
                    project_id,
                    module_name
                )
                VALUES
                (
                    %s,
                    %s
                );
                """,
                (
                    project_id,
                    module
                )
            )

        # -----------------------------------------------------
        # Git Status
        # -----------------------------------------------------

        cur.execute(
            """
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
                NULL
            );
            """,
            (
                project_id,
                "master"
            )
        )

        conn.commit()

        print("Database seeded successfully.")

    except Exception as e:

        conn.rollback()
        raise e

    finally:

        cur.close()
        conn.close()


if __name__ == "__main__":
    seed()