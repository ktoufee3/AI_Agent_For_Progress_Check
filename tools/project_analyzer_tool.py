#tools/project_analyzer_tool.py
from SMS_Project_Analyzers.super_code_analyzer import SuperCodeAnalyzer
from tools.base_tool import BaseTool
from SMS_Project_Analyzers.llm_code_analyzer import LLMCodeAnalyzer

from SMS_Project_Analyzers.super_code_analyzer import SuperCodeAnalyzer
from tools.base_tool import BaseTool


class ProjectAnalyzerTool(BaseTool):

    name = "ProjectAnalyzerTool"

    description = "Analyzes the Student Management System project."

    parameters = {}


    def execute(self):

        project_id = 1

        analyzer = SuperCodeAnalyzer()

        result = analyzer.analyze(
            project_id
        )

        return result
    
if __name__ == "__main__":

    result = ProjectAnalyzerTool().execute()

    print(result)