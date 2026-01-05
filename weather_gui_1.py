import streamlit as st
from weather_api import get_current_data, get_forecast_data
from datetime import datetime
import pandas as pd


# ******************  Helper functions  *************************
def display_datetime(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%d %I:%M %p")
    return dt.strftime("%A, %d %b %Y  %I:%M %p")

def display_suntime(dt_str):
    dt = datetime.strptime(dt_str,"%Y-%m-%d %I:%M %p" )
    return dt.strftime("%I:%M %p")


def mini_card(title, value):
    return f"""
    <div style="
        background:#2b2b40;
        border-radius:14px;
        padding:16px;
        margin: 14px 0px;
        text-align:center;
    ">
        <div style="font-size:18px; color:#aaa;">{title}</div>
        <div style="font-size:20px; font-weight:600;">{value}</div>
    </div>
    """

def other_card(x_title, x_value, y_title, y_value):
    return f"""
        <div style="
            background: #2b2b40;
            color: white;
            padding: 25px;
            border-radius:14px;
            margin-bottom: 30px;
            justify-content: space-between;
        ">
            <div style="text-align:center;">
            <div style="font-size:18px;">
            <span style="font-weight:bold;">{x_title}:</span> {x_value}
            </div>
            <div style="font-size:18px;">
            <span style="font-weight:bold;">{y_title}:</span> {y_value}
            </div>
            </div>
        </div>
    """

def tile(row):
    return f"""
    <div style="
        height:160px;
        width:200px;
        padding:10px;
        border-radius:15px;
        background:#ffa066;
        color: #0d3b66;
        text-align:center;
        display:flex;
        flex-direction:column;
        justify-content:center;
        margin-bottom:16px; ">
        <div style="font-size:18px;">  {row["date"].strftime('%A, %d-%m-%Y')} </div>    
        <div style="font-size:18px;">  {row["date"].strftime('%I:%M %p')} </div>
        <div style="font-size:24px;">{row["weather_icon"]} </div>
        <div class="subheading_1">{row["temperature"]:.0f}°C </div>
        <div style="font-size:14px;">{row["weather_description"]}</div>
    </div>
    """

def forecast_heading():
    columns = ["Date", "Temperature", "Description", "Humidity", "Pressure"]

    mystr = ""

    for col in columns:
        mystr += f'<div style="flex:1; text-align:center;">{col}</div>'

    return f"""
        <div style="
            display:flex;
            align-items:center;
            padding: 12px 16px;
            background:#1e293d ;
            border-bottom: 1px solid #334155;
            border-radius: 16px;
            font-weight:600;
            color:#cbd5e1;
        ">
            {mystr}
        </div>
        """

def forecast_row(row):
    return f"""
    <div style="
        background:#2b2b40;
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:16px 22px;
        border-radius:14px;
        margin-bottom:12px;
    ">
        <div class="forecast_row">
            <div style="font-size:16px; font-weight:600;"> {row['date'].strftime('%a %d %b')} </div>
            <div style="font-size:13px; color:#9ca3af;"> {row['date'].strftime('%I:%M %p')} </div>
        </div>
        <div class="forecast_row">
            <div style="font-size:18px; font-weight:600;"> {row['temperature']:.0f}°C </div>
            <div style="font-size:14px; color:#9ca3af;">Feels like: {row['feels_like']:.0f}°C </div>
        </div>            
        <div class="forecast_row"> {row['weather_description']}  {row['weather_icon']} </div>
        <div class="forecast_row"> 💧  {row['humidity']}%</div>
        <div class="forecast_row"> 🧭 {row['pressure']} hPa</div>
    </div>
    """

# ********************* CSS ****************************

st.markdown(
    """
    <style>
        .stApp {                                                         
            background: linear-gradient(180deg, #0f172a, #1e293b);         /* App background */
                                           
        .block-container {                              /* Remove default padding */
            padding-top: 2rem; 
            max-width: 1000px; }

        .main_box_1{
                background: #ffa066;
                color:black;
                height: 210px;
                border-radius:20px;
                padding-top:30px;
                text-align:center;  }
        
        .main_box_2{
                background: #63599d;
                color: white;
                height: 210px;
                border-radius: 20px;
                padding: 15px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                
        .subheading_1{font-size:20px;}       
        
        .forecast_row{
            flex: 1;
            text-align: center;
            font-size: 16px;
            color: #d1d5db;
            white-space: nowrap;
        }

        
    </style>
    """, unsafe_allow_html=True,)


# ********************* User Handling ****************************

st.set_page_config(
    page_title="One Weather",
    page_icon="🌤️",
    layout="wide" )


# ---------------------------- main heading
st.markdown("""
<div>
    <h1 style="font-size:62px;">🌦️ One Weather </h1>
    <p style="font-size:22px;color:#9ca3af;margin-top:-6px;">Weather, at a glance.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""<hr style='border:1px solid #6366f1; margin: 20px 0;'>""", unsafe_allow_html=True)

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = None


c1, c2 = st.columns([0.7, 0.3])
with c2:
    is_coord = st.toggle("Use Lon / Lat")

with c1:
    if is_coord:
        cl1, cl2 = st.columns(2)
        lat = cl1.number_input("Latitude", min_value=-90.0, max_value=90.0, value=28.6128)
        lon = cl2.number_input("Longitude", min_value=-180.0, max_value=180.0, value=77.2311)
        city = None

    else:
        city = st.text_input("City name")
        lat, lon = None, None

if st.button("Get Weather"):
    with st.spinner("Fetching weather..."):
        st.session_state.weather_data = get_current_data(city, lat, lon)
        st.session_state.forecast_data = None

st.markdown("""
<hr style='border:1px solid #6366f1; margin: 0px 0;'>
""", unsafe_allow_html=True)


# ************************** Current data *******************************************

if st.session_state.weather_data:
    info = st.session_state.weather_data

    if info["error"]:
        st.error(info["error"])
    else:
        st.title("🌤 Weather Details: ")
        data = info["data"]

        # main variables
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="main_box_1">
                <div style='font-size:42px;font-weight:bold;'>{data['city']}, {data['country']}</div>
                <div class="subheading_1">{display_datetime(data["date_time"])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='main_box_2'>
                <div style="text-align:center; flex: 1;">
                    <div style="font-size:52px; font-weight:bold;">{data['temperature']}°C</div>
                    <div class="subheading_1">Feels like: {data['feels_like']}°C</div>
                </div>            
                <div style="text-align:center; flex: 1;">
                    <div style="font-size:58px;">{data['weather_icon']}</div>
                    <div class="subheading_1">{data["weather_description"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        #  secondary variables
        c11, c12, c13 = st.columns(3)
        c11.markdown(mini_card("💨 Wind", f"{data['wind_speed']} m/s"), unsafe_allow_html=True)
        c12.markdown(mini_card("💧 Humidity", f"{data['humidity']} %"), unsafe_allow_html=True)
        c13.markdown(mini_card("🧭 Pressure", f"{data['pressure']} hPa"), unsafe_allow_html=True)

        # other variables
        sunrise = display_suntime(data["sunrise"])
        sunset = display_suntime(data["sunset"])

        cl21, cl22, cl23 = st.columns(3)
        cl21.markdown(other_card('Timezone offset', data['timezone'], '🌍 Country', data['country']), unsafe_allow_html=True)
        cl22.markdown(other_card('🌅 Sunrise', sunrise, '🌇Sunset', sunset), unsafe_allow_html=True)
        cl23.markdown(other_card('Latitude', data['lat'], 'Longitude', data['long']), unsafe_allow_html=True)


# ************************  Forecast *************************
forecast_btn = st.toggle("Show forecast: ")


if forecast_btn:
    st.markdown("""<hr style='border:1px solid #6366f1; margin: 10px 0;'>""", unsafe_allow_html=True)



    if st.session_state.forecast_data is None:
        with st.spinner("Fetching Forecast data..."):
            st.session_state.forecast_data = get_forecast_data(city=city, lat=lat, lon=lon)

    fc_info = st.session_state.forecast_data

    if fc_info["success"]:
        st.header("🌤 Forecast Data")
        st.subheader("24 Hour forecast Data: ")

        df = pd.DataFrame(fc_info["data"]["forecast"])
        df["date"] = pd.to_datetime(df["date"])


        # ---------------Tiles
        df_forecast = df.head(8)
        for i in range(0, 8, 4):
            cols = st.columns(4)

            for col, (_, row) in zip(cols, df_forecast.iloc[i:i + 4].iterrows()):
                with col:
                    st.markdown(tile(row), unsafe_allow_html=True)


# ------------------ other
        st.markdown("<hr style='border:1px solid #6366f1; margin: 10px 0;'>", unsafe_allow_html=True)

        st.subheader("🕒 5-Day Detailed Forecast")

        df_rows = ""
        for i, row in df.iterrows():
            df_rows += forecast_row(row)

        headers = forecast_heading()

        st.markdown(
            f"""
            <div style="
                max-height:600px;
                background: #1e293d;
                border: 3px solid #334155;
                border-radius: 16px;
            ">
                <div>{headers}</div>
                <div style="
                    max-height: 320px;
                    overflow-y: auto;
                    background: #1e293b;
                    padding: 16px;
                ">
                {df_rows}</div>
            </div>
            """,
            unsafe_allow_html=True)

    else:
        st.error(fc_info["error"])

