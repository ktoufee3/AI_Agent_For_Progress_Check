# llm/llm_client.py
from groq import Groq

import config


class LLMClient:


    def __init__(self):

        self.client = Groq(
            api_key=config.GROQ_API_KEY
        )


    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You analyze software projects."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )


        return response.choices[0].message.content