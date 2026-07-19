import subprocess

from config import SMS_PROJECT_PATH


class GitAnalyzer:

    def get_changed_files(self):

        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    SMS_PROJECT_PATH,
                    "fetch",
                    "origin"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            changed_files = []

            for line in result.stdout.splitlines():

                # Example:
                # M myapp/models.py
                # A myapp/views.py

                status = line[:2].strip()
                file_path = line[3:]

                if status:
                    changed_files.append(file_path)

            return {
                "success": True,
                "changed_files": changed_files
            }

        except subprocess.CalledProcessError as e:

            return {
                "success": False,
                "error": str(e)
            }