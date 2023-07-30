import streamlit as st
import pandas as pd

st.title("Request a New Location")

current = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/locations.csv")

# Request location name
location_name_input = st.text_input("Enter Location Name:")

#text input
lat = st.number_input("Latitude (between 1 and 100)", min_value=49.8574, max_value=50.954, value=49.8574)
long = st.number_input("Longitude (between 1 and 100)", min_value=-92.5, max_value=-87.85, value=-92.5)

location_name = ''

if lat in current.Lat.values and long in current.Long.values:
    location_name = current.loc[(current["Lat"] == lat) & (current["Long"] == long), "Location"]
    if location_name.size != 0:
        st.write(f"This location is already an option. It is called {location_name}")
    elif location_name_input == "":
        st.write(f"This location exists but does not have a name, enter a location name if you would like to save it as a location.")
    else:
        st.write(f"Do you want to save a location with latitude {lat} and longitue {long} as {location_name_input}.")
        st.button("Save")
elif location_name in current.Location.values:
    st.write(f"{location_name_input} name is already in use. Please select a different name.")
elif location_name_input != "":
    st.button("Request New Location")
else: 
    st.write(f"You are requesting a new location called {location_name_input} with a latitude of {lat} and a longitude of {long}")
    st.write("Please enter a name, latitude, and longitude.")
