#SMS_Project_Analyzers/git_analyzer.py
import subprocess
from pathlib import Path

from config import SMS_PROJECT_PATH
from database.db_utils import get_git_status

class GitAnalyzer:

        """
        Analyzes changes pushed to the remote Git repository.

        It compares the last processed commit stored in the database
        with the latest commit on the tracked remote branch and
        returns commit metadata and the paths of changed files.
        """

        def analyze(self, project_id):
            """
            Analyze the remote repository for new commits.

            Returns the latest commit hash, commit metadata,
            and the paths of files changed since the last
            processed commit stored in the database.
            """

            project_path = Path(SMS_PROJECT_PATH)

            try:

                git_status = get_git_status(project_id)

                if not git_status:
                    return {
                        "success": False,
                        "error": f"No Git configuration found for project_id={project_id}"
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
                    capture_output=True,
                    text=True,
                    check=True
                )

                result = subprocess.run(
                    [
                        "git",
                        "-C",
                        str(project_path),
                        "rev-parse",
                        f"origin/{branch}"
                    ],
                    capture_output=True,
                    text=True,
                    check=True
                )

                latest_commit = result.stdout.strip()

                # First run
                if last_processed_commit is None:

                    commits = self.get_commits(
                        project_path,
                        "",
                        latest_commit
                    )

                    result = subprocess.run(
                        [
                            "git",
                            "-C",
                            str(project_path),
                            "ls-files"
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    changed_files = [
                        line.strip()
                        for line in result.stdout.splitlines()
                        if line.strip()
                    ]

                    return {
                        "success": True,
                        "branch": branch,
                        "latest_commit": latest_commit,
                        "commits": commits,
                        "files": changed_files
                    }

                # Already synchronized
                if last_processed_commit == latest_commit:
                    return {
                        "success": True,
                        "branch": branch,
                        "latest_commit": latest_commit,
                        "commits": [],
                        "files": []
                    }

                changed_files = self.get_changed_files(
                    project_path,
                    last_processed_commit,
                    latest_commit
                )

                commits = self.get_commits(
                    project_path,
                    last_processed_commit,
                    latest_commit
                )

                return {
                    "success": True,
                    "branch": branch,
                    "latest_commit": latest_commit,
                    "commits": commits,
                    "files": changed_files
                }

            except subprocess.CalledProcessError as e:

                return {
                    "success": False,
                    "error": e.stderr
                } 

        def get_changed_files(self, project_path, old_commit, new_commit):

            """
            Return a list of files changed between two commits.
            """

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

        # def get_commits(self, project_path, old_commit, new_commit):
        #     """
        #     Return commit metadata between two commits.
        #     """

        #     result = subprocess.run(
        #         [
        #             "git",
        #             "-C",
        #             str(project_path),
        #             "log",
        #             "--pretty=format:%H|%an|%aI|%s",
        #             f"{old_commit}..{new_commit}"
        #         ],
        #         capture_output=True,
        #         text=True,
        #         check=True
        #     )

        #     commits = []

        #     for line in result.stdout.splitlines():

        #         if not line.strip():
        #             continue

        #         parts = line.split("|", 3)

        #         if len(parts) != 4:
        #             continue

        #         commit_hash, author, commit_date, commit_message = parts

        #         commits.append(
        #             {
        #                 "commit_hash": commit_hash,
        #                 "author": author,
        #                 "commit_date": commit_date,
        #                 "commit_message": commit_message
        #             }
        #         )

        #     return commits

        def get_commits(self, project_path, old_commit, new_commit):

            if old_commit:
                cmd = [
                    "git",
                    "-C",
                    str(project_path),
                    "log",
                    "--pretty=format:%H|%an|%aI|%s",
                    f"{old_commit}..{new_commit}"
                ]
            else:
                cmd = [
                    "git",
                    "-C",
                    str(project_path),
                    "log",
                    "--pretty=format:%H|%an|%aI|%s"
                ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

    


