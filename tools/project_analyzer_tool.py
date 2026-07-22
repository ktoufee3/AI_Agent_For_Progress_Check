#tools/project_analyzer_tool.py
from SMS_Project_Analyzers.super_code_analyzer import SuperCodeAnalyzer
from tools.base_tool import BaseTool
from tools.project_status_tool import ProjectStatusTool

class ProjectAnalyzerTool(BaseTool):

    name = "ProjectAnalyzerTool"

    description = "Analyzes the Student Management System project."

    parameters = {}


    def execute(self, project_id=1):

        print("Starting project analysis...")

        analyzer = SuperCodeAnalyzer()

        result = analyzer.analyze(project_id)

        print("Analyzer result:")
        print(result)

        if not result["success"]:
            return result

        print("Returning updated status...")

        return ProjectStatusTool().execute()
    
if __name__ == "__main__":

    result = ProjectAnalyzerTool().execute()

    print(result)