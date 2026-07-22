# SMS_Project_Analyzers/local_code_analyzer.py

import subprocess

from config import SMS_PROJECT_PATH


class CodeAnalyzer:
    """
    Detect local Git changes that have not yet been committed.

    Returns the paths of modified, added, deleted and untracked files
    in the working tree.
    """

    def analyze(self):
        """
        Analyze the local repository and return changed file paths.
        """

        result = self.get_changed_files()

        if not result["success"]:
            return result


        return {
            "success": True,
            "files": result['files']
        }

    def get_changed_files(self):
        """
        Return paths of locally changed files.
        """

        try:

            result = subprocess.run(
                [
                    "git",
                    "-C",
                    SMS_PROJECT_PATH,
                    "status",
                    "--porcelain"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            changed_files = []

            for line in result.stdout.splitlines():

                if not line.strip():
                    continue

                changed_files.append(line[3:].strip())

            return {
                "success": True,
                "files": changed_files
            }

        except subprocess.CalledProcessError as e:

            return {
                "success": False,
                "error": e.stderr
            }

