import streamlit as st
import pandas as pd
import single_analysis

def intro():
    st.write("# Boreal Forest Carbon Calculator")
    st.markdown("Welcome to the Boreal Forest Carbon Calculator")

def single_analysis_page():
    # Call the single_analysis.py script using subprocess
    single_analysis.single_analysis_page()

# Define the pages dictionary
pages = {
    "Homepage": intro,
    "Single Location": single_location_page,
    "Location Comparison": location_comparison_page,
    "Explore Lat/Long": single_lat_long,
    "About": about_page
}

# Check if the app is just starting (no state exists)
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True  # Set the flag to True after displaying the intro
    intro()  # Display the homepage by default

st.sidebar.button("Homepage", on_click=intro)
st.sidebar.button("Single Location", on_click=single_analysis_page)
st.sidebar.button("Location Comparison", on_click=location_comparison_page)
st.sidebar.button("Explore Lat/Long", on_click=single_lat_long)
st.sidebar.button("About", on_click=about_page)
