#database/project_analysis_updater.py

from database.db_manager import get_connection
from database.git_status_updater import update_last_processed_commit


class ProjectAnalysisUpdater:


    def update(self, project_id, analysis, commit_hash):

        conn = get_connection()


        try:

            cur = conn.cursor()

            modules = analysis.get("modules", [])


            for module in modules:

                status = self.normalize_status(
                            module["status"]
                        )

                cur.execute("""
                    UPDATE project_modules
                    SET
                        status = %s,
                        progress = %s,
                        updated_at = NOW()
                    WHERE
                        project_id = %s
                    AND
                        module_name = %s
                """,
                (
                    status,
                    module["progress"],
                    project_id,
                    module["module_name"]
                ))

                print("Rows updated:", cur.rowcount)
                print(repr(module["module_name"]))

            # update overall progress

            cur.execute("""
                UPDATE projects
                SET
                    overall_progress = (
                        SELECT AVG(progress)
                        FROM project_modules
                        WHERE project_id = %s
                    ),
                    updated_at = NOW()
                WHERE id = %s
            """,
            (
                project_id,
                project_id
            ))


            conn.commit()


            # after successful DB update
            update_last_processed_commit(
                project_id,
                commit_hash
            )


            return {
                "success": True
            }


        except Exception as e:

            conn.rollback()

            return {
                "success": False,
                "error": str(e)
            }


        finally:

            cur.close()
            conn.close()

    def normalize_status(self, status):

        status = status.strip().lower()

        mapping = {
            "in_progress": "In Progress",
            "in progress": "In Progress",
            "completed": "Completed",
            "complete": "Completed",
            "updated": "In Progress",
            "started": "In Progress",
            "ongoing": "In Progress",
            "working": "In Progress",
            "not_started": "Not Started",
            "not started": "Not Started",
        }

        return mapping.get(
            status.lower(),
            status
        )

