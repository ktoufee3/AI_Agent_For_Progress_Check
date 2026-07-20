#agent/agent.py
import json

from llm.llm_client import LLMClient
from prompts.planner_prompt import build_planner_prompt
from prompts.responder_prompt import build_responder_prompt
from tools.registory import TOOL_REGISTRY, get_available_tools
from memory.conversation_memory import ConversationMemory

class Agent:

    def __init__(self):
        self.available_tools = get_available_tools()
        self.llm = LLMClient()
        self.memory = ConversationMemory()

    def run(self, user_question):

        history = self.memory.get()
        planner_prompt = build_planner_prompt(
            user_question,
            history,
            self.available_tools
        )

        planner_response = self.llm.generate(planner_prompt)

        plan = json.loads(planner_response)

        print(" Planner Output:")
        print(plan)

        tool = TOOL_REGISTRY[plan["selected_tool"]]

        tool_result = tool.execute(**plan["parameters"])

        print(" Tool Result:")
        print(tool_result)

        responder_prompt = build_responder_prompt(
            user_question,
            history,
            tool_result
        )

        answer = self.llm.generate(responder_prompt)
        self.memory.add("user", user_question)
        self.memory.add("assistant", answer)        

        return answer

        # return self.llm.generate(responder_prompt)