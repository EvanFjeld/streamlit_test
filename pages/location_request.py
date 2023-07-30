import streamlit as st

st.title("Request a New Location")

# Request location name
location_name = st.text_input("Enter Location Name:")

# Request latitude value between 1 and 100
lat = st.slider("Enter Latitude (between 1 and 100):", min_value=1.0, max_value=100.0, value=50.0, step=0.1)

# Request longitude value between 1 and 100
long = st.slider("Enter Longitude (between 1 and 100):", min_value=1.0, max_value=100.0, value=50.0, step=0.1)

# Display the submitted information
st.write("You entered the following information:")
st.write(f"Location Name: {location_name}")
st.write(f"Latitude: {lat}")
st.write(f"Longitude: {long}")
