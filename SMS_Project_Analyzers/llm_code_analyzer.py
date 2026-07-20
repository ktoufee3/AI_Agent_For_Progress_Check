#SMS_Project_Analyzers/llm_code_analyzer.py
# SMS_Project_Analyzers/llm_code_analyzer.py

from llm.llm_client import LLMClient


class LLMCodeAnalyzer:


    def analyze(self, files, project_context):

        prompt = self.build_prompt(
            files,
            project_context
        )

        import json

        response = LLMClient().generate(prompt)

        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        try:
            analysis = json.loads(response)

            return analysis

        except json.JSONDecodeError:

            return {
                "success": False,
                "error": "Invalid JSON returned by LLM",
                "raw_response": response
            }



    def build_prompt(self, files, project_context):

        code_context = ''

        for file in files:

            code_context += f"""

========================
FILE: {file['path']}
========================

{file['content']}

"""


        prompt = f"""
You are a software project analyzer.

Project modules:

{project_context}


Analyze the following code changes.

Rules:

- Only use module names from the provided list.
- Do not create new modules.
- Map code changes to the closest existing module.
- Return ONLY valid JSON.
- Do not wrap JSON inside markdown code blocks.

Expected format:

{{
    "modules": [
        {{
            "module_name": "",
            "changes": [],
            "status": "",
            "progress": 0
        }}
    ]
}}


CODE:

{code_context}

"""

        return prompt