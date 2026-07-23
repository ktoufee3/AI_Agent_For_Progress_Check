from tools.project_status_tool import ProjectStatusTool
from tools.project_analyzer_tool import ProjectAnalyzerTool
from tools.git_history_tool import GitHistoryTool

TOOL_REGISTRY = {
    ProjectStatusTool.name: ProjectStatusTool(),
    ProjectAnalyzerTool.name: ProjectAnalyzerTool(),
    # GitHistoryTool.name: GitHistoryTool()
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