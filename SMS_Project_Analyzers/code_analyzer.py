# # #SMS_Project_Analyzers/code_analyzer.py
# import subprocess

# from config import SMS_PROJECT_PATH
# from SMS_Project_Analyzers.file_reader import FileReader


# class CodeAnalyzer:

#     def analyze(self):

#         changed_files = self.get_changed_files()

#         files = FileReader().read_files(changed_files)

#         return {
#             "success": True,
#             "files": files
#         }

#     def get_changed_files(self):

#         try:

#             print("Entering get_changed_files()")

#             print(f"SMS_PROJECT_PATH = {SMS_PROJECT_PATH}")

#             result = subprocess.run(
#                 [
#                     "git",
#                     "-C",
#                     SMS_PROJECT_PATH,
#                     "status",
#                     "--porcelain"
#                 ],
#                 capture_output=True,
#                 text=True,
#                 check=True
#             )

#             changed_files = []


#             print(f"Raw git status: {result.stdout}")

#             for line in result.stdout.splitlines():

#                 if not line.strip():
#                     continue

#                 # M  myapp/models.py
#                 # A  README.md
#                 # ?? new_file.py

#                 changed_files.append(line[3:].strip())

#             return changed_files

#         except subprocess.CalledProcessError as e:
#             print("Git command failed!")
#             print(e)
#             print(e.stdout)
#             print(e.stderr)
#             return []

#         except Exception as e:
#             print("Unexpected error:", e)
#             raise


# if __name__ == "__main__":

#     print(CodeAnalyzer().analyze())