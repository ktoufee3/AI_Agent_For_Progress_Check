#app.py
from agent.agent import Agent
import uvicorn
import config

def main():

    agent = Agent()

    print("SMS Project AI Agent")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            answer = agent.run(question)

            print("\nAssistant:")
            print(answer)
            print()

        except Exception as e:
            print(f"\nError: {e}\n")



if __name__ == "__main__":
    # main()

    uvicorn.run(
        "api.app:app",
        host=config.API_IP,
        port=config.API_PORT,
        reload=True
    )