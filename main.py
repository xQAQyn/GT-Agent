from dotenv import load_dotenv
load_dotenv()

from agents import ReActAgent

agent = ReActAgent()
print("Starting ReAct agent...")
response = agent.run("What is the result of 123 multiplied by 321?")