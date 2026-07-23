# tools/git_history_tool.py

from tools.base_tool import BaseTool
from SMS_Project_Analyzers.git_history_analyzer import GitHistoryAnalyzer


class GitHistoryTool(BaseTool):

    name = "GitHistoryTool"

    description = (
        "Provides Git history, latest commits, and changed files."
    )

    parameters = {
        "operation": {
            "type": "string",
            "enum": [
                "latest_commit",
                "changed_files"
            ]
        },
        "commit_hash": {
            "type": "string",
            "required": False
        }
    }

    def execute(
        self,
        operation,
        commit_hash=None
    ):
        analyzer = GitHistoryAnalyzer()

        if operation == "latest_commit":
            return analyzer.get_latest_commit()

        if operation == "changed_files":
            return analyzer.get_changed_files(
                commit_hash or "HEAD"
            )

        return {
            "success": False,
            "error": f"Unknown operation: {operation}"
        }