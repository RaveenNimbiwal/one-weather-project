from weather_api import *
import pandas as pd

print(r"""
             ,-----.  ,--.  ,--, ,------.      ,--.   .--. ,------.   ,----.  ,----------. ,--. ,--. ,------. ,-------.
            |  .-.  | |   \ |  | |  .---'      |  |   |  | |  .---'  /  __  \ '--.    .--' |  | |  | |  .---' |  .--.  |
            |  | |  | |    \|  | |  |          |  |   |  | |  |     |  .  .  |    |  |     |  |_|  | |  |     |  |__|  |
            |  | |  | |  .     | |  '--.       |  |.'.|  | |  '--.  |  |__|  |    |  |     |       | |  '--.  |  |   _.'
            |  | |  | |  |\    | |  .--'       |         | |  .--'  |   .-.  |    |  |     |  .-.  | |  .--'  |  |_  \
            |  '-'  | |  | \   | |  `---.      |   ,'.   | |  `---. |  |  |  |    |  |     |  | |  | |  `---. |  | \  \
             `-----'  `--'  `--' `------'      '--'   '--' `------' `--'  `--'    `--'     `--' `--' `------' `--'  '--'
                                                                                                Welcome to "One Weather"
""")


while True:
    input_1 = input("> Enter 'current' to see real_time_weather or 'forecast' to see 5 days forecast "
                    "(Enter 'q' to exit) : ")

    if input_1 == "current":
        location = input("> Enter City name OR type 'coord' for latitude & longitude : ").strip()
        if location.lower() == "coord":
            try:
                lon = float(input("> Enter longitude: "))
                lat = float(input("> Enter latitude: "))
                result = get_current_data(lon=lon, lat=lat)
            except ValueError:
                result = {"success": False, "error": "Error: Invalid latitude or longitude.", "data": None}
        else:
            result = get_current_data(city=location)

        if result["success"] :
            for key, value in result["data"].items():
                print(f"\t\t{key}: {value}")
        else:
            print(result["error"])

    elif input_1 == "forecast":
        location = input("> Enter City name OR type 'coord' for latitude & longitude : ").strip()
        if location.lower() == "coord":
            try:
                lon = float(input("> Enter longitude: "))
                lat = float(input("> Enter latitude: "))
                result = get_forecast_data(lon=lon, lat=lat)
            except ValueError:
                result = {"success": False, "error": "Error: Invalid latitude or longitude.", "data": None}
        else:
            result = get_forecast_data(city=location)

        if result["success"]:
            print(result["data"]["city"])

            pd.set_option("display.max_columns", None)
            df = pd.DataFrame(result["data"]["forecast"])
            print(df)

        else:
            print(result["error"])

    elif input_1 == "q":
        break

    else:
        print("Enter valid response. Try again")



