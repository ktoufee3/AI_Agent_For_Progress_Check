#SMS_Project_Analyzers/code_analyzer.py
from pathlib import Path

from config import SMS_PROJECT_PATH


class CodeAnalyzer:

    def analyze(self, changed_files):

        project_path = Path(SMS_PROJECT_PATH)

        if not project_path.exists():
            return {
                "success": False,
                "error": f"Project path not found: {project_path}"
            }

        analyzed_files = []

        for file in changed_files:

            full_path = project_path / file

            if not full_path.exists():
                continue

            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                analyzed_files.append({
                    "path": file,
                    "content": content
                })

            except Exception as e:
                analyzed_files.append({
                    "path": file,
                    "error": str(e)
                })

        return {
            "success": True,
            "files": analyzed_files
        }