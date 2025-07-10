from agents import Agent,Runner,RunContextWrapper
import asyncio
import os
from dotenv import load_dotenv
from typing import Literal
import random

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class RoleContext:
  def __init__(self,role: Literal["student","developer","manager"]) -> None:
    self.role = role


def custom_instructions(run_context: RunContextWrapper[RoleContext],agent: Agent[RoleContext]) -> str:

  print(agent)

  role = run_context.context.role
  if role == "student":
          return "Explain things in a simple way, as if you're teaching a student."
  elif role == "developer":
          return "Use technical language and examples. Respond as if you're helping another developer."
  else:
          return "Use professional tone and give executive-level summaries."


agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
    
)


async def main():
    choice: Literal["student","developer","manager"] = random.choice(["student","developer","manager"])
    context = RoleContext(role=choice)
    print(f"Using style: {choice}\n")

    user_message = "Explain REST API"
    print(f"User: {user_message}")
    result = await Runner.run(agent, user_message, context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
