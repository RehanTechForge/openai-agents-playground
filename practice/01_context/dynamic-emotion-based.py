from typing import Literal
import os
import random
from dotenv import load_dotenv
from agents import Agent,RunContextWrapper,Runner
import asyncio
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

class EmotionBased:
  def __init__(self,mood:Literal["sad","happy","angry"]) -> None:
    self.mood = mood

def custom_instructions(run_context: RunContextWrapper[EmotionBased],agent: Agent[EmotionBased]):
  mood = run_context.context.mood
  if mood == "happy":
        return "Be cheerful and celebrate with the user!"
  elif mood == "sad":
        return "Be soft and encouraging, show empathy."
  else:
        return "Be calm and help the user relax, avoid triggering language."
  

agent = Agent(
    name="Chat Agent",
    instructions=custom_instructions
)

async def main():
    choice:Literal["sad","happy","angry"] = random.choice(["sad","happy","angry"])
    context = EmotionBased(mood=choice)

    print(f"Using style: {choice}\n")

    user_message = "I lost my job."
    print(f"User: {user_message}")
    result = await  Runner.run(agent,user_message,context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

