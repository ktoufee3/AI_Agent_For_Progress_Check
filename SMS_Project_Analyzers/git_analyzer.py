#SMS_Project_Analyzers/git_analyzer.py
import subprocess
from pathlib import Path

from config import SMS_PROJECT_PATH
from SMS_Project_Analyzers.file_reader import FileReader
from database.git_status_updater import get_git_status

class GitAnalyzer:

    """
    Analyzes changes pushed to the remote Git repository.

    It compares the last processed commit stored in the database
    with the latest commit on the tracked remote branch and
    returns the contents of files changed between those commits.
    """

    def analyze(self, project_id):

        project_path = Path(SMS_PROJECT_PATH)


        try:
            git_status = get_git_status(project_id)

            if not git_status:
                return {
                    "success" : False,
                    "error" : f"No Git configuration found for project_id={project_id}"
                }

            branch = git_status["branch"]
            last_processed_commit = git_status["last_processed_commit"]

            subprocess.run(
                [
                    "git",
                    "-C",
                    str(project_path),
                    "fetch",
                    "origin"
                ],
                check=True,
                capture_output=True,
                text=True
            )

            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(project_path),
                    "rev-parse",
                    f"origin/{branch}"
                ],
                check=True,
                capture_output=True,
                text=True
            )

            latest_commit = result.stdout.strip()

            if last_processed_commit is None:
                return {
                    "success": True,
                    "latest_commit": latest_commit,
                    "files": []
                }

            if last_processed_commit == latest_commit:
                return {
                    "success": True,
                    "latest_commit": latest_commit,
                    "files": []
                }

            changed_files = self.get_changed_files(
                project_path,
                last_processed_commit,
                latest_commit
            )

            files = FileReader.read_files(changed_files)

            return {
                "success": True,
                "initialzed" : True,
                "latest_commit": latest_commit,
                "files" : files,
            }

        except subprocess.CalledProcessError as e:

            return {
                "success": False,
                "error": e.stderr
            }
        

    def get_changed_files(self, project_path, old_commit, new_commit):

        result = subprocess.run(
            [
                "git",
                "-C",
                str(project_path),
                "diff",
                "--name-only",
                old_commit,
                new_commit
            ],
            capture_output=True,
            text=True,
            check=True
        )

        changed_files = []

        for line in result.stdout.splitlines():

            if line.strip():
                changed_files.append(line.strip())

        return changed_files

