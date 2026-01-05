import requests
import os
from datetime import datetime, timezone, timedelta
import pandas as pd

weather_icons = {
    "01d": {"description": "clear sky", "emoji": "☀️"},
    "01n": {"description": "clear sky", "emoji": "🌙"},
    "02d": {"description": "few clouds", "emoji": "🌤️"},
    "02n": {"description": "few clouds", "emoji": "☁️🌙"},
    "03d": {"description": "scattered clouds", "emoji": "☁️"},
    "03n": {"description": "scattered clouds", "emoji": "☁️🌙"},
    "04d": {"description": "broken clouds", "emoji": "☁️"},
    "04n": {"description": "broken clouds", "emoji": "☁️🌙"},
    "09d": {"description": "shower rain", "emoji": "🌧️"},
    "09n": {"description": "shower rain", "emoji": "🌧️"},
    "10d": {"description": "rain", "emoji": "🌦️"},
    "10n": {"description": "rain", "emoji": "🌧️"},
    "11d": {"description": "thunderstorm", "emoji": "⛈️"},
    "11n": {"description": "thunderstorm", "emoji": "⛈️"},
    "13d": {"description": "snow", "emoji": "❄️"},
    "13n": {"description": "snow", "emoji": "❄️"},
    "50d": {"description": "mist", "emoji": "🌫️"},
    "50n": {"description": "mist", "emoji": "🌫️"}
}

try:
    api_key = os.getenv("weather_api")
except KeyError:
    raise RuntimeError("Can't find api key")

base_url = "https://api.openweathermap.org/data/2.5"


def get_current_data(city=None, lat=None, lon=None):
    """ get current weather location of any location or city
    Args:
        1)city (str) : City name or
        2)lat (int): latitude
        3)lon (int) longitude
    **Either provide city name or lat and lon
    Returns:
        A python dictionary
    """

    if city is not None:
        params = {"q": city, "appid": api_key, "units": "metric"}
    elif lat is not None and lon is not None:
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    else:
        # print("Either provide a city name or latitude & longitude values.")
        return {"success": False, "error": "No location provided. Please enter a city or latitude & longitude.",
                "data": None}

    try:
        response = requests.get(f"{base_url}/weather", params=params, timeout=10)
        response.raise_for_status()
        return {"success": True, "data": _filter_current_data(response.json()), "error": None}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Error: Request timed out, Try again later.", "data": None}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Error: Network problem, Check your internet connection", "data": None}

    except requests.exceptions.HTTPError:
        return {"success": False, "error": "Error: Invalid city name or coordinates", "data": None}

    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}", "data": None}


def _filter_current_data(data):
    """
    Extracts only useful information from the raw JSON file and returns a well-formatted Python dictionary.
    Args:
        data (dict): current weather JSON response from API
    Returns:
        dict: dictionary with cleaned and safe weather information
    """

    tz = timezone(timedelta(seconds=data.get("timezone", 0)))
    def to_local_time(timestamp):
        if timestamp is None:
            return None
        try:
            return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(tz).strftime("%Y-%m-%d %I:%M %p")
        except Exception:
            return None

    id = str(data.get("weather", [{}])[0].get("icon", "-"))

    def get_weather_icon(i):
        return weather_icons.get(i, {}).get("emoji", "☁️")

    main = data.get("main", {})
    sys_data = data.get("sys", {})

    mydict = {
        "city": data.get("name", "-"),
        "date_time": to_local_time(data.get("dt")),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "weather_description": data.get("weather", [{}])[0].get("description", "-"),
        "weather_icon": get_weather_icon(id),
        # "weather_id_icon": data.get("weather",[{}])[0].get("icon", "-"),
        "pressure": main.get("pressure"),
        "humidity": main.get("humidity"),
        "visibility": data.get("visibility"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "sunrise": to_local_time(sys_data.get("sunrise")),
        "sunset": to_local_time(sys_data.get("sunset")),
        "long": data.get("coord", {}).get("lon"),
        "lat": data.get("coord", {}).get("lat"),
        "timezone": data.get("timezone", 0),
        "country": sys_data.get("country", "-"),
    }

    return mydict


def get_multiple_city(cities):
    """ Fetch weather data for multiple cities.
    Args:
        cities (list of str): List of city names.
    Returns:
        list of dict: Each dict contains processed weather info."""

    results = []
    for city in cities:
        res = get_current_data(city=city)

        results.append({
            "city": city,
            "success": res["success"],
            "data": res["data"],
            "error": res["error"]})

    return results


def get_multiple_location(coordinates):
    """
    Fetch weather data for multiple coordinates.
    Args:
        coordinates (list of tuples): List of (lat, lon) tuples.
    Returns:
        list of dict: Each dict contains processed weather info.
    """
    results = []
    for lat, lon in coordinates:
        res = get_current_data(lat=lat, lon=lon)

        results.append({
            "lat": lat,
            "lon": lon,
            "success": res["success"],
            "data": res["data"],
            "error": res["error"]})

    return results


def get_forecast_data(city=None, lat=None, lon=None):
    """ get forecast data of any location or city
    Args:
        1)city (str) : City name  or
        2)lat (int): latitude
        3)lon (int) longitude
    **Either provide city name or lat and lon
    Returns:
        A JSON file
    """

    if city:
        params = {"q": city, "appid": api_key, "units": "metric"}

    elif lat is not None and lon is not None:
        # url = f"{base_url}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    else:
        return {"success": False, "error": "No location provided. Please enter a city or latitude & longitude.",
                "data": None}

    try:
        response = requests.get(f"{base_url}/forecast", params=params, timeout=10)
        response.raise_for_status()
        return {"success": True, "data": filter_forecast_data(response.json()), "error": None}

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Unable to fetch weather data at the moment. Please try again later.",
                "data": None}

def filter_forecast_data(data):
    """ filter forecast data and return useful information
    Args:
        data(JSON): forecast data
    Returns:
        pyhton list:the python list contains two elements
                1) the metadata dictionary, which stores location into
                2) the weather list, which contains forecast data for the location
    """

    tz = timezone(timedelta(seconds=data.get("city", {}).get("timezone", 0)))

    def to_local_time(timestamp):
        if timestamp is None:
            return None
        try:
            return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(tz).strftime("%Y-%m-%d %I:%M %p")
        except Exception:
            return None



    # metadata
    city_info = {
        "city": data.get("city", {}).get("name", "-"),
        "latitude": data.get("city", {}).get("coord", {}).get("lat"),
        "longitude": data.get("city", {}).get("coord", {}).get("lon"),
        "country": data.get("city", {}).get("country", "-"),
        "timezone": data.get("city", {}).get("timezone", 0)
    }

    infolist = []
    forecast_list = data.get("list", [])

    for item in forecast_list:
        main = item.get("main", {})
        weather_list = item.get("weather", [{}])

        id = weather_list[0].get("icon", "-")

        def get_weather_icon(i):
            return weather_icons.get(i, {}).get("emoji", "☁️")

        mydict = {"date": to_local_time(item.get("dt")),
                  "temperature": main.get("temp"),
                  "feels_like": main.get("feels_like"),
                  "weather_description": weather_list[0].get("description", "-"),
                  "weather_icon": get_weather_icon(id),
                  "pressure": main.get("pressure"),
                  "humidity": main.get("humidity"),
                  "visibility": item.get("visibility"),
                  "wind_speed": item.get("wind", {}).get("speed"),
                  "sunrise": to_local_time(data.get("city", {}).get("sunrise", 0)),
                  "sunset": to_local_time(data.get("city", {}).get("sunset", 0))

                  }

        infolist.append(mydict)
    return {
        "city": city_info,
        "forecast": infolist
    }



