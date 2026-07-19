from tools.project_status_tool import ProjectStatusTool
from tools.project_analyzer_tool import ProjectAnalyzerTool

TOOL_REGISTRY = {
    ProjectStatusTool.name: ProjectStatusTool(),
    ProjectAnalyzerTool.name: ProjectAnalyzerTool()
}


def get_available_tools():
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
        for tool in TOOL_REGISTRY.values()
    ]