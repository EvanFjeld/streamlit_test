import streamlit as st
import pandas as pd
import numpy as np



# Add a number input form
lat = st.number_input("Latitude", min_value=0, max_value=150, value=30, step=1)
long = st.number_input("Latitude", min_value=0, max_value=150, value=30, step=1)

st.title('Boreal Forecast Carbon Forecaster')
st.write("Latitude / Longitude: ", lat, " / ", long)