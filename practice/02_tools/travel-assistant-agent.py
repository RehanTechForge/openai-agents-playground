# 🌍 AI Travel Assistant using OpenAI Agents SDK with custom tools

import os
from agents import Agent, Runner, WebSearchTool, ImageGenerationTool, OpenAIResponsesModel, function_tool
from dotenv import load_dotenv
from openai.types.responses.tool_param import ImageGeneration
import asyncio
import base64
from openai import AsyncOpenAI
import requests

# Initialize async OpenAI client
client = AsyncOpenAI()

# 🔐 Load environment variables from .env file (API keys etc.)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

if openai_api_key or weather_api_key:
    raise ValueError("Please Provide a api key to use this service")

# ⚠️ NOTE: OpenAI's built-in ImageGenerationTool only works with gpt-image-1, a protected model
# So we are skipping it and using a custom FunctionTool instead

# ❌ Example (not used here):
# image_tool_config = ImageGeneration(
#     type="image_generation",
#     background="auto",
#     model="dall-e-3",  # ❌ Will raise error: only 'gpt-image-1' is supported
#     ...
# )
# tools = [WebSearchTool(), ImageGenerationTool(tool_config=image_tool_config)]

# ✅ Custom FunctionTool for generating an image of a tourist place
@function_tool
async def generate_image(place_name: str) -> str:
    """Generate an image of a tourist location using DALL·E-3.

    Args:
        place_name: The name of the location to visualize.

    Returns:
        Path to the saved image or an error message.
    """
    try:
        # Call DALL·E-3 API to generate image (you must have access to this model)
        img = await client.images.generate(
            model="dall-e-3",  # ⚠️ Protected model: ensure access
            prompt=f"A beautiful tourist view of {place_name}",
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        # ✅ Check if the response contains valid image data
        if img and img.data and len(img.data) > 0 and img.data[0].b64_json:
            image_bytes = base64.b64decode(img.data[0].b64_json)
            file_path = f"{place_name}_image.png"
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            return f"Image saved successfully: {file_path}"
        else:
            return "Image generation returned empty result."

    except Exception as e:
        # Return error string if image generation fails
        return f"Failed to generate image for {place_name}: {str(e)}"


# ✅ Custom FunctionTool to check current weather of a given city
@function_tool
async def check_weather(city: str) -> str:
    """Fetch current temperature of a city using OpenWeather API."""
    
    # Send request to OpenWeatherMap API
    response = requests.get(
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}"
    )

    weather = "dummy weather"

    # ✅ If API call successful, extract temperature and convert to Celsius
    if response.status_code == 200:
        data = response.json()
        print("Weather data:", data)
        kelvin_temp = data['main']['temp']
        celsius_temp = kelvin_temp - 273.15
        weather = f"Temperature in {city}: {celsius_temp:.2f}°C"
    else:
        # ❌ Handle case where API call fails
        print("Failed to fetch data:", response.status_code)

    return weather


# 🧠 Triage Agent setup — routes user query to appropriate tools
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a triage agent. Your responsibility is to handle travel-related queries 
    and route them to the correct tools. Your available tools are:
    1. WebSearchTool – for finding places
    2. generate_image – for generating images of places
    3. check_weather – for fetching weather info
    """,
    tools=[WebSearchTool(), generate_image, check_weather],
)


# 🚀 Main function to run the agent and test a sample user query
async def main():
    user_query = "Suggest me 1 good tourist places in karachi, show me pictures, and also tell the weather and currency conversion if I have 1000 PKR."
    # Alternate test:
    # user_query = "Generate an image of a beautiful tourist spot in Istanbul"

    # 🔁 Run the agent using the Runner
    result = await Runner.run(triage_agent, user_query)

    # 🖨 Print the final combined output (from all tools)
    print(result.final_output)

    # For testing single tool separately:
    # result = await check_weather("karachi")
    # print(result)


# 🏁 Entry point
asyncio.run(main())