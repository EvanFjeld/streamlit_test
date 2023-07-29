import streamlit as st
import pandas as pd
import single_analysis

def intro():
    st.write("# Boreal Forest Carbon Calculator")
    st.markdown("Welcome to the Boreal Forest Carbon Calculator")

def single_analysis_page():
    st.markdown('# Here is an analysis of a single pre-defined location')
    st.write("What to know when you compare locations.")
    single_analysis

def location_comparison_page():
    st.markdown('# This page is meant to compare multiple locations')
    st.write("What to know when you compare locations.")

def single_lat_long():
    st.markdown('# Explore Lat/Long')
    st.write("Exploring Lat/Long.")

def about_page():
    st.markdown('# About the Carbon Forecaster')
    st.write("This is the final project for a master's in data science program at UC Berkeley.")

# Define the pages dictionary
pages = {
    "Homepage": intro,
    "Single Location": single_analysis_page,
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
