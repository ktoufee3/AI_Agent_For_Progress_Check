#agent/agent.py
import json

from llm.llm_client import LLMClient
from prompts.planner_prompt import build_planner_prompt
from tools.registory import TOOL_REGISTRY, get_available_tools
from memory.conversation_memory import ConversationMemory

from agent.project_reasoner import ProjectReasoner
from agent.response_generator import ResponseGenerator
from agent.planner import Planner
from agent.tool_runner import ToolRunner
class Agent:

    def __init__(self):

        self.planner = Planner()

        self.available_tools = get_available_tools()

        self.memory = ConversationMemory()

        self.tool_runner = ToolRunner()

        self.reasoner = ProjectReasoner()

        self.response_generator = ResponseGenerator()


    def run(self, user_question):

        # ----------------------------
        # Conversation History
        # ----------------------------

        history = self.memory.get()

        # ----------------------------
        # Planning
        # ----------------------------

        print("\nAvailable Tools:")
        print(self.available_tools)
        # for tool in available_tools:
        #     print(tool)

        plan = self.planner.plan(
                user_question,
                history,
                self.available_tools
            )

        print("\nPlanner Output:")
        print(plan)

        # ----------------------------
        # Tool Execution
        # ----------------------------

        tool_result = self.tool_runner.execute(plan)

        print("\nTool Result:")
        print(tool_result)

        # ----------------------------
        # Project Reasoning
        # ----------------------------

        reasoning = self.reasoner.reason(
            user_question,
            tool_result
        )

        print("\nReasoning:")
        print(reasoning)

        # ----------------------------
        # Natural Language Response
        # ----------------------------

        answer = self.response_generator.generate(
            user_question,
            history,
            reasoning
        )

        # ----------------------------
        # Save Conversation
        # ----------------------------

        self.memory.add("user", user_question)

        self.memory.add("assistant", answer)

        return answer


    # def run(self, user_question):

    #     history = self.memory.get()
    #     planner_prompt = build_planner_prompt(
    #         user_question,
    #         history,
    #         self.available_tools
    #     )

    #     planner_response = self.llm.generate(planner_prompt)

    #     plan = json.loads(planner_response)

    #     print(" Planner Output:")
    #     print(plan)

    #     tool = TOOL_REGISTRY[plan["selected_tool"]]

    #     tool_result = tool.execute(**plan["parameters"])

    #     print(" Tool Result:")
    #     print(tool_result)
 
    #     responder_prompt = build_responder_prompt(
    #         user_question,
    #         history,
    #         tool_result
    #     )

    #     answer = self.llm.generate(responder_prompt)
    #     self.memory.add("user", user_question)
    #     self.memory.add("assistant", answer)        

    #     return answer

