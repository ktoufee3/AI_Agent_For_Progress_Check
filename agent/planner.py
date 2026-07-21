#agent/planner.py
import json

from llm.llm_client import LLMClient
from prompts.planner_prompt import build_planner_prompt


class Planner:

    def __init__(self):
        self.llm = LLMClient()

    def plan(
        self,
        user_question,
        history,
        available_tools
    ):

        prompt = build_planner_prompt(
            user_question,
            history,
            available_tools
        )

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            return {
                "intent": "unknown",
                "selected_tool": None,
                "parameters": {},
                "reason": "Planner returned invalid JSON."
            }