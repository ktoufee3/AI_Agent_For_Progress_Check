#app.py
from agent.agent import Agent

agent = Agent()

question = input("You: ")

answer = agent.run(question)

print("\nAgent:")
print(answer)