import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Any, Dict, Optional

class WeatherForecastTool:

    def __init__(self, api_key:str, timeout:float = 15.0, units: str = "metric", lang: str = "en"):
        self.api_key = api_key
        self.timeout = timeout
        self.units = units
        self.lang = lang
        self.base_url = "http://api.openweathermap.org/data/2.5"

        # The session allows a way to persist certain parameters across multiple http requests - (useful when interacting with web services which require state management like authentication or maintaining cookies)
        self.session = requests.Session()
        # backoff_factor = Controls the delay between retries using exponential backoff.

        retries = Retry(
            total=5, 
            backoff_factor=0.5,
            allowed_methods=["GET"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))


    def _get(self, path: str, params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        try:
            q = {"appid": self.api_key, "units": self.units, "lang": self.lang}
            q.update(params or {})
            response = self.session.get(f"{self.base_url}{path}", params=q, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error during API request: {e}")
            return None
        
    def get_current_weather(self, place: str) -> Dict[str, Any]:
        """Current weather by city name."""
        if not place:
            raise ValueError("place must be a non-empty string")
        # /weather is the path and q is the params dict[str,any] containing the place
        return self._get("/weather", {"q": place})

    def get_forecast_weather(self, place: str, *, cnt: Optional[int] = None) -> Dict[str, Any]:
        """5-day/3-hour forecast by city name. Optionally limit entries with cnt."""
        if not place:
            raise ValueError("place must be a non-empty string")
        params: Dict[str, Any] = {"q": place}
        if cnt:
            params["cnt"] = cnt
            # so the params dictionary will look like:
            # {"q": place, "cnt": cnt}
            # /forecast is the path , which will be appended to the base_url
        return self._get("/forecast", params)
