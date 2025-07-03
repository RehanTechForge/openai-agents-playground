from agents import Agent,RunConfig,Runner,OpenAIChatCompletionsModel
from openai import AsyncClient
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key=os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
  raise ValueError("Gemini api key not found")


external_client = AsyncClient(
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


dummy_weather_agent:Agent = Agent(
  name="Weather App",
  instructions="""
    You're a weather assistant. If the user asks about the weather of any city, you will respond with the weather information — but it will be dummy data because you don't have access to real-time information. However, you will still answer the user and also give a hint that the weather data is dummy. If the user talks about anything other than the weather, you will stop them and not continue the conversation."""
)

result = Runner.run_sync(
  starting_agent=dummy_weather_agent,
  input="what is weather of karachi",
  run_config=config
)

print(result.final_output)