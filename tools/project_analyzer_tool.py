#tools/project_analyzer_tool.py
from SMS_Project_Analyzers.code_analyzer import CodeAnalyzer
from tools.base_tool import BaseTool

changed_files = [
    "myapp/models.py",
    "myapp/views.py",
    "README.md"
]

class ProjectAnalyzerTool(BaseTool):

    name = "ProjectAnalyzerTool"

    description = "Analyzes the Student Management System project."

    parameters = {}

    def execute(self):

        analyzer = CodeAnalyzer()

        result = analyzer.analyze(changed_files)

        return result