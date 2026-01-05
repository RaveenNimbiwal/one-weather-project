import streamlit as st
from weather_api import *
import pandas as pd

st.title("One Weather")
st.divider()

with st.form(key="hello"):
    cl1, cl2 = st.columns([70, 30])

    with cl2:
        is_coord = st.toggle("Use Lon/Lat")

    with cl1:
        if is_coord:
            c1, c2 = st.columns(2)
            lat = c1.text_input("Enter latitude: ")
            lon = c2.text_input("Enter longitude: ")
            city = None

        else:
            city = st.text_input("Enter city name: ")
            lat, lon = None, None

    info = get_current_data(city, lat, lon)

    main_btn = st.form_submit_button()

st.subheader("Weather Details: ")


if main_btn:
    if info["error"]:
        st.write(info["error"])
    else:
        data = info["data"]
        # st.write(info["data"])


        # main variables
        cl01, cl02, cl03 = st.columns(3)

        with cl01:
            st.header(f'{data["city"]}, {data["country"]}')
            st.write(data["date_time"])

        with cl02:
            st.write("")
            st.subheader(f"{data['temperature']} °C")
            st.write(f"Feels like: {data['feels_like']} °C")

        with cl03:
            st.write("")
            st.write("")
            st.write("***Feels like:***")
            st.write(f"{data['feels_like']} °C")

        # main variables
        # cl11, cl12, cl13 = st.columns(3)
        # with cl11:
        #     st.metric(label="***Temperature***", value=f"{data['temperature']} °C")
        #     # st.write(f"{data['weather_description']}")
        #     # st.write(f"Feels like: {data['feels_like']} °C")
        #
        # with cl12:
        #     st.metric(label="***Feels like***", value=f"{data['feels_like']} °C")
        #     # st.metric(label="", value="10.5°C")
        #
        # with cl13:
        #     st.metric(label="***Description***", value=data["weather_description"])

        cl21, cl22, cl23 = st.columns(3)

        with cl21:
            st.metric(label="***Wind Speed:***", value=f"{data['wind_speed']} m/s")

        with cl22:
            st.metric(label="***Humidity:***", value=f"{data['humidity']}%")

        with cl23:
            st.metric(label="***Pressure:***", value=f"{data['pressure']} hPa")

        # other important variables
        cl41, cl42, cl43 = st.columns(3)
        with cl41:
            st.write(f"***Time Offset***: {data['timezone']}")
            st.write(f"***Country***: {data['country']}")

        with cl42:
            st.write(f"***Sunrise***: {data['sunrise'][-8:]}")
            st.write(f"***Sunset***: {data['sunset'][-8:]}")

        with cl43:
            st.write(f"***Latitude***: {data['lat']}")
            st.write(f"***Longitude***: {data['long']}")

else:
    st.write("Enter City name or Coordinate fo see current weather data.")



