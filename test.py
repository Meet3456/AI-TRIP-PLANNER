import os
import sys
from dotenv import load_dotenv

load_dotenv()  # expects OPENWEATHERMAP_API_KEY in .env

from tools.weather_info_tool import WeatherInfoTool

def _call_tool(tool, arg: str) -> str:
    # Works for both LangChain BaseTool API styles
    try:
        return tool.invoke(arg)
    except Exception:
        return tool.run(arg)

def main():
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("Set OPENWEATHERMAP_API_KEY in your .env")
        sys.exit(1)

    city = sys.argv[1] if len(sys.argv) > 1 else "Mumbai"

    weather = WeatherInfoTool()
    current_tool, forecast_tool = weather.weather_tool_list

    print(f"Testing current weather for: {city}")
    print(_call_tool(current_tool, city))
    print("\n---\n")
    print(f"Testing forecast for: {city}")
    print(_call_tool(forecast_tool, city))

if __name__ == "__main__":
    main()