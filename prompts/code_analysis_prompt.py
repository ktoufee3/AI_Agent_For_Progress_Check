#prompts/code_analysis_prompt.py
def build_code_analysis_prompt(files):

    return f"""
You are a senior Django software architect.

You are given modified files from a Django project.

Your tasks are:

1. Determine what functionality was added or modified.
2. Identify which module(s) these files belong to.
3. For each module, determine whether it is:
   - Completed
   - In Progress
   - Not Started
4. Give a concise summary.

Return ONLY valid JSON.

Do NOT wrap the JSON in markdown.

Return this format exactly:

{{
    "modules": [
        {{
            "module": "",
            "status": "",
            "reason": ""
        }}
    ],
    "summary": ""
}}

Modified Files:

{files}
"""