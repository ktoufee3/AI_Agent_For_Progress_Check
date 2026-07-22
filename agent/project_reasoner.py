# agent/project_reasoner.py

import json

from llm.llm_client import LLMClient


class ProjectReasoner:

    def __init__(self):
        self.llm = LLMClient()


    def reason(self, user_question, tool_result):

        prompt = self.build_prompt(
            user_question,
            tool_result
        )

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            return {
                "summary": "Unable to analyze project.",
                "project_health": "Unknown",
                "recommendations": [],
                "risks": [],
                "insights": [],
                "raw_response": response
            }


    def build_prompt(self, user_question, tool_result):

        return f"""
You are a Senior Software Project Manager.

Your job is NOT to answer the user.

Your job is to analyze the project using the available data.

User Question:
{user_question}

Project Data:
{json.dumps(
    tool_result,
    indent=4,
    default=str
)}

Analyze the project.

Determine:

- Current project health
- Progress summary
- Important insights
- Risks
- Recommendations

Return JSON only.

Format:

{{
    "summary": "",
    "project_health": "",
    "insights": [
        ""
    ],
    "risks": [
        ""
    ],
    "recommendations": [
        ""
    ]
}}

Rules:

- Base every conclusion on the provided data.
- Do not invent missing information.
- If data is insufficient, mention that in the relevant field.
- Do not return markdown.
- Return valid JSON only.
"""