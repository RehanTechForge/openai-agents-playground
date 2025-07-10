from agents import Agent,RunConfig,Runner,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os 
import asyncio
from dotenv import load_dotenv

load_dotenv()


gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

if not gemini_api_key:
  raise ValueError("GEMINI KEY not found")



external_client = AsyncOpenAI(
  api_key=gemini_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


external_model = OpenAIChatCompletionsModel(
  model="gemini-2.0-flash",
  openai_client=external_client
)

config = RunConfig(
  model=external_model,
  model_provider=external_client,
  tracing_disabled=True
)



async def main():
  
  agent = Agent(name="Tutor Agent",instructions="You are a tutor agent your task to answer user question related to education")

  result = await Runner.run(starting_agent=agent,input="hey there about math subject",run_config=config)

  print(result.final_output)


asyncio.run(main())




