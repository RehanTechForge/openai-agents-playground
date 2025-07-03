import os
from agents import Agent,Runner,OpenAIChatCompletionsModel,RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
  raise ValueError("Gemini Api Key no Found")


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


math_agent:Agent = Agent(
  name="Math Agent",
  instructions="Your are a Math Agents you task is to answer a user/person math question"
  "only answer in math specific question use If the user asks anything else, then refuse to answer."
)

result:Runner = Runner.run_sync(starting_agent=math_agent,input="What is 25 + 33?",run_config=config)

print(result.final_output)