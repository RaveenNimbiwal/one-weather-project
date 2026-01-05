# One Weather

One Weather is a Python project that shows real-time weather information and 5-day forecasts.  
It can be used through the command line or an interactive Streamlit web app.


---

## Features

- Search by city or latitude/longitude  
- View current weather with detailed information  
- See a 5-day forecast  
- Two ways to use the app:  
  - Command Line (CLI)  
  - Streamlit dashboard  

---

## How it works

The application uses the OpenWeather API to fetch live weather data.  
All API logic is placed in a separate file so it can be reused by both interfaces.  
This keeps the code organized and easier to maintain or extend later.

---

## API Key
This project requires an API key from OpenWeather.

## Running the project

You can run:
- the CLI script from your terminal  
- or the Streamlit app in your browser  

Both use the same backend functions to fetch and process weather data.

## Project structure

- main_cmd.py - Command line interface
- weather_api.py - API calls and data processing
- weather_gui_0.py - Basic Streamlit version
- weather_gui_1.py - Advanced Streamlit UI

