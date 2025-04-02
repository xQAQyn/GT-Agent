from dotenv import load_dotenv
load_dotenv()

from agents import ReActAgent

agent = ReActAgent()
print("Starting ReAct agent...")
response = agent.run(input=input("请输入问题："))

# Example usage: What is the result of (5 + 2 * (3^2 - 1))^2?