from tools.registory import TOOL_REGISTRY


class ToolRunner:

    def execute(self, plan):

        tool_name = plan.get("selected_tool")

        if tool_name not in TOOL_REGISTRY:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        tool = TOOL_REGISTRY[tool_name]

        parameters = plan.get("parameters", {})

        return tool.execute(**parameters)