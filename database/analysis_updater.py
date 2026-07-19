#database/analysis_updater.py
from database.db_manager import get_connection


def update_project_analysis(project_id, analysis):

    conn = get_connection()

    try:
        cur = conn.cursor()

        # ----------------------------
        # Update overall project progress
        # ----------------------------

        # cur.execute("""
        #     UPDATE projects
        #     SET
        #         overall_progress = %s,
        #         updated_at = NOW()
        #     WHERE id = %s
        # """, (
        #     analysis["overall_progress"],
        #     project_id
        # ))

        # ----------------------------
        # Update / Insert modules
        # ----------------------------

        for module in analysis["modules"]:

            cur.execute("""
                SELECT id
                FROM project_modules
                WHERE
                    project_id = %s
                    AND module_name = %s
            """, (
                project_id,
                module["module"]
            ))

            exists = cur.fetchone()

            if exists:

                cur.execute("""
                    UPDATE project_modules
                    SET
                        status = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (
                    module["status"],
                    exists[0]
                ))

            else:

                print(
                    f"Unknown module ignored: {module['module']}"
                )

        conn.commit()

    finally:
        cur.close()
        conn.close()


def calculate_project_progress(project_id):

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT status
            FROM project_modules
            WHERE project_id = %s
        """, (project_id,))

        modules = cur.fetchall()

        if not modules:
            return 0

        total = 0

        for (status,) in modules:

            if status == "Completed":
                total += 100

            elif status == "In Progress":
                total += 50

            elif status == "Not Started":      # Not Started
                total += 0

        progress = round(total / len(modules))

        cur.execute("""
            UPDATE projects
            SET
                overall_progress = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (progress, project_id))

        conn.commit()

        return progress

    finally:
        cur.close()
        conn.close()

