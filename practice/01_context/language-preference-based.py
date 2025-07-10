from typing import Literal
import os
import random
from dotenv import load_dotenv
from agents import Agent,RunContextWrapper,Runner
import asyncio
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


class LanguageContext:
  def __init__(self,language: Literal["en","ur","it"]) -> None:
    self.language = language


def custom_instructions(run_context: RunContextWrapper[LanguageContext],agent: Agent[LanguageContext]):
  lang = run_context.context.language
  if lang == "en":
        return "Respond in English."
  elif lang == "ur":
        return "Respond in Urdu."
  else:
        return "Respond in Italian,Roman English."
  

agent = Agent(
    name="Chat Bot",
    instructions=custom_instructions
)

async def main():
    choice:Literal["en","ur","it"] = random.choice(["en","ur","it"])
    context = LanguageContext(language=choice)

    print(f"Using style: {choice}\n")

    user_message = "How are You?"
    print(f"User: {user_message}")
    result = await Runner.run(agent,user_message,context=context)

    print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
    