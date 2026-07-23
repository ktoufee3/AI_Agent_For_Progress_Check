#SMS_Project_Analyzers/git_history_analyzer
from pathlib import Path
import subprocess

from config import SMS_PROJECT_PATH


class GitHistoryAnalyzer:

    def __init__(self):
        self.project_path = Path(SMS_PROJECT_PATH)

    def _run_git(self, args):
        result = subprocess.run(
            ["git", "-C", str(self.project_path)] + args,
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    def get_latest_commit(self):
        output = self._run_git([
            "log",
            "-1",
            "--pretty=format:%H|%an|%aI|%s"
        ])

        commit_hash, author, commit_date, message = output.split("|", 3)

        return {
            "success": True,
            "commit": {
                "commit_hash": commit_hash,
                "author": author,
                "commit_date": commit_date,
                "commit_message": message,
            }
        }

    def get_changed_files(self, commit_hash="HEAD"):
        output = self._run_git([
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            commit_hash,
        ])

        files = [
            line.strip()
            for line in output.splitlines()
            if line.strip()
        ]

        return {
            "success": True,
            "commit_hash": commit_hash,
            "files": files,
        }

