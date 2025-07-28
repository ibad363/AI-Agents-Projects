import os
import requests
from typing import Optional
from dataclasses import dataclass
from agents import Agent, Runner, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from setup_config import config

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    
@app.get("/")
def read_root():
    return {"Hello World"}

@dataclass
class WeatherInfo:
   temperature: float
   feels_like: float
   humidity: int
   description: str
   wind_speed: float
   pressure: int
   location_name: str
   rain_1h: Optional[float] = None
   visibility: Optional[int] = None
   
@function_tool
def get_weather(lat: float,lon: float) -> str:
    """Get the current weather for a specified location using OpenWeatherMap API.

    Args:
       lat: Latitude of the location (-90 to 90)
       lon: Longitude of the location (-180 to 180)
    """
    WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response  = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        weather_info = WeatherInfo(
           temperature=data["main"]["temp"],
           feels_like=data["main"]["feels_like"],
           humidity=data["main"]["humidity"],
           description=data["weather"][0]["description"],
           wind_speed=data["wind"]["speed"],
           pressure=data["main"]["pressure"],
           location_name=data["name"],
           visibility=data.get("visibility"),
           rain_1h=data.get("rain", {}).get("1h"),
        )
        weather_report = f"""
        Weather in {weather_info.location_name}:
        - Temperature: {weather_info.temperature}°C (feels like {weather_info.feels_like}°C)
        - Conditions: {weather_info.description}
        - Humidity: {weather_info.humidity}%
        - Wind speed: {weather_info.wind_speed} m/s
        - Pressure: {weather_info.pressure} hPa
        """
        return weather_report
    except requests.exceptions.RequestException as e:
       return f"Error fetching weather data: {str(e)}"
   
# Create a weather assistant
weather_assistant = Agent(
   name="Weather Assistant",
   instructions="""You are a weather assistant that can provide current weather information.
  
   When asked about weather, use the get_weather tool to fetch accurate data.
   If the user doesn't specify a country code and there might be ambiguity,
   ask for clarification (e.g., Paris, France vs. Paris, Texas).
  
   Provide friendly commentary along with the weather data, such as clothing suggestions
   or activity recommendations based on the conditions.
   """,
   tools=[get_weather]
)

@app.post("/weather-stream")
async def stream_weather(req: ChatRequest):
    message = req.message

    async def event_generator():
            result = Runner.run_streamed(weather_assistant, message, run_config=config)

            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    yield event.data.delta
                
   # this method is for working with next js api route, this gives EventSourceResponse to nextjs api route 
    return EventSourceResponse(
        event_generator(),
        headers={
            "Cache-Control": "no-cache",
            "Content-Type": "text/event-stream",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )