import os
from agents import Agent,Runner,OpenAIChatCompletionsModel,RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

gemini_api_key= os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
  raise ValueError("Gemini Api key not found")


external_client= AsyncOpenAI(
  api_key=gemini_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

external_model=OpenAIChatCompletionsModel(
  model="gemini-2.0-flash",
  openai_client=external_client,
  
)

config = RunConfig(
  model=external_model,
  model_provider=external_client,
  tracing_disabled=True
)


greeting_agent:Agent = Agent(
  name="Greeting Agent",
  instructions="You are a greeting agent and your task is simple send greeting message to user",
  
)

result:Runner = Runner.run_sync(starting_agent=greeting_agent,input="hey there",run_config=config)

print(result.final_output)