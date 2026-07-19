#tools/project_status_tool.py
from psycopg2.extras import RealDictCursor

from database.db_manager import get_connection
from tools.base_tool import BaseTool


class ProjectStatusTool(BaseTool):

    name = "ProjectStatusTool"

    description = "Provides the current status of a project."

    # parameters = {
    #     "project_id": "integer"
    # }

    parameters = {}

    def execute(self):

        conn = get_connection()

        try:
            # RealDictCursor returns rows as dictionaries instead of tuples.
            cur = conn.cursor(cursor_factory=RealDictCursor)


            # cur.execute("""
            #     SELECT
            #         project_name,
            #         description,
            #         overall_progress,
            #         current_phase,
            #         status
            #     FROM projects
            #     WHERE id = %s
            # """, (project_id,))

            cur.execute("""
                SELECT
                    id,
                    project_name,
                    description,
                    overall_progress,
                    current_phase,
                    status
                FROM projects
                ORDER BY id DESC
                LIMIT 1
            """)



            project = cur.fetchone()

            if project is None:
                return {
                        "success": False,
                        "error": "Project not found."
                    }

            project_id = project["id"]

            cur.execute("""
                SELECT
                    module_name,
                    status,
                    progress
                FROM project_modules
                WHERE project_id = %s
            """, (project_id,))

            modules = cur.fetchall()

            cur.execute("""
                SELECT
                    milestone_name,
                    status
                FROM project_milestones
                WHERE project_id = %s
            """, (project_id,))

            milestones = cur.fetchall()

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


        # Convert RealDictRow objects to normal Python dictionaries
        project = dict(project)
        modules = [dict(module) for module in modules]
        milestones = [dict(milestone) for milestone in milestones]

        return {
                "success": True,
                "data": {
                    "project_info": project,
                    "modules": modules,
                    "milestones": milestones
                }
            }




