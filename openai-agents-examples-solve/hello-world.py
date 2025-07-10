import asyncio
from agents import Agent,Runner
import os 
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
  raise ValueError("OPENAI key is not defined")




async def main():

  hello_agent: Agent = Agent(
    name="Hello Agent",
    instructions="You only respond in haikus."
  )

  result = await Runner.run(hello_agent, "Tell me about recursion in programming.")
  print(result.final_output)

  # print("SImple Hello")



asyncio.run(main())