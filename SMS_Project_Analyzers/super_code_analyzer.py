#SMS_Project_Analyzers/super_code_analyzer.py
from SMS_Project_Analyzers.code_analyzer import CodeAnalyzer
from SMS_Project_Analyzers.git_analyzer import GitAnalyzer
from SMS_Project_Analyzers.llm_code_analyzer import LLMCodeAnalyzer
from database.db_manager import get_connection
from database.project_analysis_updater import ProjectAnalysisUpdater

class SuperCodeAnalyzer:

    def get_project_modules(self, project_id):
        """
        Returns the list of module names for a project.
        """

        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT module_name
                FROM project_modules
                WHERE project_id = %s
                ORDER BY id
                """,
                (project_id,)
            )

            return [row[0] for row in cur.fetchall()]

        finally:
            cur.close()
            conn.close()

    def analyze(self, project_id):

        # Local changes
        local_result = CodeAnalyzer().analyze()

        # print("\nLOCAL RESULT:")
        # print(local_result)


        # Remote changes
        git_result = GitAnalyzer().analyze(project_id)

        # print("\nGIT RESULT:")
        # print(git_result)


        if not local_result["success"]:
            return local_result


        if not git_result["success"]:
            return git_result


        # ---------------------------------
        # Merge files
        # ---------------------------------

        files_map = {}


        # Remote committed changes first
        for file in git_result["files"]:
            files_map[file["path"]] = file


        # Local changes override remote
        for file in local_result["files"]:
            files_map[file["path"]] = file


        files = list(files_map.values())
        project_context = self.get_project_modules(project_id)

        analysis = LLMCodeAnalyzer().analyze(files, project_context)

        update_result = ProjectAnalysisUpdater().update(
            project_id,
            analysis,
            git_result["latest_commit"]
        )

        if not update_result["success"]:
            return update_result

        return {
            "success": True,
            "latest_commit": git_result["latest_commit"],
            "files": files,
            "analysis" : analysis
        }