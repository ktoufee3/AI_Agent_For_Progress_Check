#tools/project_analyzer_tool.py
from SMS_Project_Analyzers.super_code_analyzer import SuperCodeAnalyzer
from tools.base_tool import BaseTool
from tools.project_status_tool import ProjectStatusTool

from SMS_Project_Analyzers.git_analyzer import GitAnalyzer
import inspect

print("FILE:", inspect.getfile(GitAnalyzer))
print("--------------------------------")
print(inspect.getsource(GitAnalyzer.analyze))
print("--------------------------------")

class ProjectAnalyzerTool(BaseTool):

    name = "ProjectAnalyzerTool"

    description = "Analyzes the Student Management System project."

    parameters = {}

    def execute(self, project_id=1):

        print("Starting project analysis...")

        analyzer = SuperCodeAnalyzer()

        analysis_result = analyzer.analyze(project_id)

        print("Analyzer result:")
        print(analysis_result)

        if not analysis_result["success"]:
            return analysis_result

        print("Loading latest project status...")

        status = ProjectStatusTool().execute()

        if not status["success"]:
            return status

        # Add the latest Git/code analysis
        status["data"]["latest_analysis"] = analysis_result

        return status
    
if __name__ == "__main__":

    result = ProjectAnalyzerTool().execute()

    print(result)