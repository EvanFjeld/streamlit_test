import streamlit as st
import pandas as pd
import numpy as np

st.title('Boreal Forecast Carbon Forecaster')

# Function to create the navigation bar
def create_navbar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "Reports", "About"))

    if page == "Home":
        st.header("Welcome to the Home Page")
        # Add content for the Home page here

    elif page == "Reports":
        st.header("Welcome to the Reports Page")
        # Add content for the Reports page here

    elif page == "About":
        st.header("Welcome to the About Page")
        # Add content for the About page here

# Call the function to create the navigation bar
create_navbar()

# Add a number input form
lat = st.number_input("Latitude", min_value=0, max_value=150, value=30, step=1)
st.write("Latitude: ", lat)

long = st.number_input("Longitude", min_value=0, max_value=150, value=30, step=1)
st.write("Longitude: ", long)
