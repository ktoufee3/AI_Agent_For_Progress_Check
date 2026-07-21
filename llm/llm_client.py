# llm/llm_client.py
from groq import Groq, RateLimitError

import config


class LLMClient:

    def __init__(self):

        self.clients = [
            Groq(api_key=config.GROQ_API_KEY),
            Groq(api_key=config.RETRY_GROQ_API_KEY),
        ]


    def generate(self, prompt):

        last_exception = None

        for client in self.clients:

            try:

                response = client.chat.completions.create(
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

            except RateLimitError as e:

                print("Rate limit reached. Trying next API key...")
                last_exception = e

            except Exception as e:

                last_exception = e

        raise last_exception