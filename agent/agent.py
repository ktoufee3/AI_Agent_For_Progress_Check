import json

from llm import client
from prompts.planner_prompt import build_planner_prompt
from prompts.responder_prompt import build_responder_prompt
from tools.registory import TOOL_REGISTRY, get_available_tools


class Agent:

    def __init__(self):
        self.available_tools = get_available_tools()

    def run(self, user_question):

        planner_prompt = build_planner_prompt(
            user_question,
            self.available_tools
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": planner_prompt
                }
            ],
            temperature=0
        )

        plan = json.loads(response.choices[0].message.content)

        print("\nPlanner Output:")
        print(plan)

        tool = TOOL_REGISTRY[plan["selected_tool"]]

        tool_result = tool.execute(**plan["parameters"])

        print("\nTool Result:")
        print(tool_result)

        responder_prompt = build_responder_prompt(
            user_question,
            tool_result
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": responder_prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content