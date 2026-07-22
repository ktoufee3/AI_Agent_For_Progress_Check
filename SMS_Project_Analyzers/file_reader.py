#SMS_Project_Analyzers/file_reader.py
from pathlib import Path

from config import (
    SMS_PROJECT_PATH,
    IGNORED_FILES,
    IGNORED_DIRECTORIES,
)


class FileReader:

    @staticmethod
    def read_files(paths):

        project_path = Path(SMS_PROJECT_PATH)

        analyzed_files = []

        for file in paths:

            path = Path(file)

            if path.name in IGNORED_FILES:
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

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

        return analyzed_files