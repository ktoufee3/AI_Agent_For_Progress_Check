# agent/response_generator.py

import json

from llm.llm_client import LLMClient


class ResponseGenerator:

    def __init__(self):
        self.llm = LLMClient()


    def generate(
        self,
        user_question,
        history,
        reasoning
    ):

        prompt = self.build_prompt(
            user_question,
            history,
            reasoning
        )

        return self.llm.generate(prompt)


    def build_prompt(
        self,
        user_question,
        history,
        reasoning
    ):

        return f"""
You are ProjectGPT.

You are a friendly AI software project assistant.

Conversation History:

{history}

User Question:

{user_question}

Project Reasoning:

{json.dumps(reasoning, indent=4)}

Instructions:

- Answer naturally.
- Be conversational.
- Use the reasoning provided.
- Do not mention JSON.
- Do not mention tool outputs.
- Do not invent facts.
- If the user asks for advice, use the recommendations.
- If the user asks for opinions, base them on project health and progress.
- If information is insufficient, clearly explain that.

Generate the best possible response.
"""
    
    # - Response should be precise, to the point, and upto 50 words. Not more than that.