import os
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

load_dotenv()

class WeatherInfoTool:

    def __init__(self):
        # creating an instance if WeatherForecastTool Class and passing the api_key(As rest variables are declared and set in the init)
        self.weather_tool_object = WeatherForecastTool(api_key=os.getenv("OPENWEATHERMAP_API_KEY"))
        # Thus weather_tool_list would contain list of all weather related tools , as _setup_tools returns a 
        self.weather_tool_list = self._setup_tools()


    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city:str) -> str:
            data = self.weather_tool_object.get_current_weather(city)
            if data:
                units = getattr(self.weather_tool_object, "units", "metric")
                sym = "°C" if units == "metric" else ("°F" if units == "imperial" else "K")
                temp = data.get('main', {}).get('temp', 'N/A')
                desc = (data.get('weather') or [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}{sym}, {desc}"
            
            return f"Could not fetch weather for {city}"

        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            forecast_data = self.weather_tool_object.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            
            return f"Could not fetch forecast for {city}"

        return [get_current_weather, get_weather_forecast]

