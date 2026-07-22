import json


def build_responder_prompt(user_question, history, tool_result):
    return f"""
You are an AI Assistant.

Answer the user's question using ONLY the tool output below.

Tool Output:
{json.dumps(
    tool_result,
    indent=4,
    default=str
)}

User Question:
{user_question}

If the answer is not present in the tool output, say so.
"""