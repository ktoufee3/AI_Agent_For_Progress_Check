#SMS_Project_Analyzers/super_code_analyzer.py

from SMS_Project_Analyzers.local_code_analyzer import CodeAnalyzer
from SMS_Project_Analyzers.git_analyzer import GitAnalyzer
from SMS_Project_Analyzers.file_reader import FileReader
from SMS_Project_Analyzers.llm_code_analyzer import LLMCodeAnalyzer
# from database.db_manager import get_connection
from database.db_utils import update_project_analysis, get_project_modules,update_git_status
#update_project_analysis
from database.db_manager import get_connection
from database.db_utils import save_commits

class SuperCodeAnalyzer:



    def analyze(self, project_id):

        # Local uncommitted changes
        local_result = CodeAnalyzer().analyze()

        # Remote committed changes
        git_result = GitAnalyzer().analyze(project_id)

        print("commits")
        print(git_result["commits"])

        if not local_result["success"]:
            return local_result

        if not git_result["success"]:
            return git_result

        if git_result['commits']:
            # print(f"commit: {git_result['commit']}")

            conn = get_connection()

            cur = conn.cursor()

            try:
                save_commits(cur, project_id, git_result["commits"])
                conn.commit()

            except Exception as e:
                conn.rollback()
                return {
                    "success" : False,
                    "error" : str(e)
                }

            finally:
                cur.close()
                conn.close()


            git_update = update_git_status(
                project_id,
                git_result["latest_commit"]
            )

            if not git_update["success"]:
                return git_update

        # ---------------------------------
        # Merge file paths
        # ---------------------------------

        file_paths = set()

        # Files changed in remote commits
        file_paths.update(git_result["files"])

        # Files modified locally
        file_paths.update(local_result["files"])

        # ---------------------------------
        # Read latest local versions
        # ---------------------------------

        if not file_paths:
            return {
                "success": True,
                "latest_commit": git_result["latest_commit"],
                "commits": git_result["commits"],
                "files": [],
                "analysis": None,
                "message": "No code changes detected."
            }

        # if not file_paths:
        #     return {
        #         "success": True,
        #         "latest_commit": git_result["latest_commit"],
        #         "commits": [],
        #         "files": [],
        #         "analysis": None,
        #         "message": "No code changes detected."
        #     }

        files = FileReader().read_files(
            paths=sorted(file_paths)
        )

        project_context = get_project_modules(project_id)

        analysis = LLMCodeAnalyzer().analyze(
            files,
            project_context
        )

        update_result = update_project_analysis(
            project_id,
            analysis
        )

        if not update_result["success"]:
            return update_result

        # git_update = update_git_status(
        #     project_id=project_id,
        #     last_processed_commit=git_result["latest_commit"]
        # )

        if not git_update["success"]:
            return git_update


        return {
            "success": True,
            "latest_commit": git_result["latest_commit"],
            "commits": git_result["commits"],
            "files": files,
            "analysis": analysis
        }

