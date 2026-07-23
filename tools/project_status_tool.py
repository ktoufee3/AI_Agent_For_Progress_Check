#tools/project_status_tool.py
from database.db_utils import (
    get_project,
    get_project_modules,
    calculate_overall_progress,
    get_last_commit,
    get_git_status
)
from tools.base_tool import BaseTool


class ProjectStatusTool(BaseTool):

    name = "ProjectStatusTool"

    description = "Provides the current status of a project."

    parameters = {}

    def execute(self):

        project = get_project()

        if project is None:
            return {
                "success": False,
                "error": "Project not found."
            }

        modules = get_project_modules(project["id"])

        project["overall_progress"] = calculate_overall_progress(modules)

        git_status = get_git_status(project['id'])

        last_commit = get_last_commit(project["id"])

        project["created_at"] = (
            project["created_at"].isoformat()
            if project["created_at"] else None
        )

        project["updated_at"] = (
            project["updated_at"].isoformat()
            if project["updated_at"] else None
        )

        return {
            "success": True,
            "data": {
                "project_info": project,
                "modules": modules,
                "git_status" : git_status,
                "last_commit": last_commit
            }
        }








