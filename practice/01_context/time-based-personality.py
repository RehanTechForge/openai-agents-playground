from typing import Literal
import os
import random
from dotenv import load_dotenv
from agents import Agent,RunContextWrapper,Runner
import asyncio
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


class TimeBasedPersonality:
  def __init__(self,time: Literal["morning","afternoon","night"]) -> None:
    self.time = time

def custom_instructions(run_context: RunContextWrapper[TimeBasedPersonality],agent: Agent[TimeBasedPersonality]):
  t = run_context.context.time
  if t == "morning":
        return "Start the conversation with a 'Good Morning' and be energetic."
  elif t == "afternoon":
        return "Greet with 'Good Afternoon' and keep it calm."
  else:
        return "Say 'Good Night' and keep the tone relaxed and cozy."
  

agent = Agent(
    name="Chat Assistant",
    instructions=custom_instructions
)

async def main():
    choice: Literal["morning","afternoon","night"] = random.choice(["morning","afternoon","night"])
    context=TimeBasedPersonality(time=choice)
    print(f"Using style: {choice}\n")

    user_message = "Any updates?"
    print(f"User: {user_message}")
    result = await Runner.run(agent,user_message,context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
    