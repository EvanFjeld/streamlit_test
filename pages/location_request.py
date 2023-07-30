import streamlit as st
import pandas as pd

st.title("Request a New Location")

current = saved_options = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/Locations_temp.csv")

# Request location name
location_name = st.text_input("Enter Location Name:")

# Request latitude value between 1 and 100
# lat = st.slider("Enter Latitude (between 1 and 100):", min_value=1.0, max_value=100.0, value=50.0, step=0.1)
# long = st.slider("Enter Longitude (between 1 and 100):", min_value=1.0, max_value=100.0, value=50.0, step=0.1)

#text input
lat = st.number_input("Latitude (between 1 and 100)", min_value=1.1, max_value=100.0, value=1.0)
long = st.number_input("Longitude (between 1 and 100)", min_value=1.0, max_value=100.0, value=1.0)

# Display the submitted information
st.write("You entered the following information:")
st.write(f"Location Name: {location_name}")
st.write(f"Latitude: {lat}")
st.write(f"Longitude: {long}")

if lat in current.Lat.values and long in current.Long.values:
    location_name = current.loc[(current["Lat"] == lat) & (current["Long"] == long), "Location"].values[0]
    st.write(f"This location is already an option. It is called {location_name}")
else:
    st.button("Request")
