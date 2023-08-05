import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.error
from urllib.error import HTTPError

def none_selected(options_df):
    st.write("Don't know the location name?")
    st.markdown("If you don't have a location name in mind, select a latitude and longitude to see the analysis for that location.")

    #options_df = options_df[["Lat","Long","filename"]]
    lat = "-"
    long = "-"

    options_df = options_df.dropna(subset=['Lat','Long'])
    
    if long == "-": lat_options = [lat] + list(options_df.Lat.unique())
    else: lat_options = [lat] + list(options_df[(options_df.Long == long)].Lat.unique())
    
    if lat == "-": long_options = [long] + list(options_df.Long.unique())
    else: long_options = [long] + list(options_df[(options_df.Lat == lat)].Long.unique())

    col1, col2 = st.columns(2)
    with col1:
        if long != "-": lat_options = [lat] + list(options_df[(options_df.Lat == long)].Long.unique())
        lat = st.selectbox("Select Latitude", lat_options)
    with col2:
        if lat != "-": long_options = [long] + list(options_df[(options_df.Lat == lat)].Long.unique())
        long = st.selectbox("Select Longitude", long_options)

    if lat != "-" and long != "-": 
        file_name = options_df.loc[(options_df["Lat"] == lat) & (options_df["Long"] == long), "filename"].values[0]
        location_name = options_df.loc[(options_df["Lat"] == lat) & (options_df["Long"] == long), "Location"].values[0]
        st.write(location_name)
        single_location_analysis(file_name, location_name)

def single_location_analysis(file, location, model_name):
    if location == "-": return ""

    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/data/" + file + ".csv"
    try:
        df = pd.read_csv(AWS_BUCKET_URL + file_name)
        st.title(f'{location}')
    except HTTPError:
        st.title(f'{location} not available with the {model_name.lower()}-term model')
        st.write(f'The {model_name.lower()}-term model is not avaialble for {location}. Please select another location or model.')
        return ""

    # Convert the 'date' column to datetime type
    #df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
    df['date'] = pd.to_datetime(df.date)

    min_date = df.date.min().to_pydatetime()
    max_date = df.date.max().to_pydatetime()
    start_month = min_date.strftime("%B")
    start_year = min_date.year
    end_month = max_date.strftime("%B")
    end_year = max_date.year
    
    st.write(f'Here is the analysis and forecast for {location}. The Gpp for this site was tracked as far back as {start_month}, {start_year} and our forecast projects Gpp until {end_month}, {end_year}')
    
    col1a, col2a = st.columns(2)

    with col1a:
        start_date = st.slider("Start Date", 
                           min_value = min_date, 
                           max_value=max_date, 
                           value = min_date, 
                           format = "YYYY-MM-DD")
    
        st.write("Starting date:", start_date)
    
    with col2a:
        end_date = st.slider("End Date", 
                         min_value = start_date, 
                         max_value=max_date, 
                         value = max_date, 
                         format = "YYYY-MM-DD")
        st.write("Ending date:", end_date)

    # group dataset for time period
    if time_frame == "Yearly":
        filtered_df = df.groupby(df['date'].dt.year).agg({
            'Gpp': 'sum',
            'isforecasted': lambda x: any(x)  # Check if any value in 'isforecasted' is True
        }).reset_index()
        # Filter the DataFrame based on the selected date range
        filtered_df = filtered_df[(filtered_df.date >= start_date.year) & (filtered_df.date <= end_date.year)]
    else:
        filtered_df = df
        # Filter the DataFrame based on the selected date range
        filtered_df = filtered_df[(filtered_df.date >= start_date) & (filtered_df.date <= end_date)]
    
    

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('black')  # Set black background
    ax.set_title('Gpp Forecasting', color='white', fontsize=16)  # Set white title
    
    # Plot the lines based on 'isforecasted' column
    for is_forecasted, group in filtered_df.groupby('isforecasted'):
        linestyle = '--' if is_forecasted == 1 else '-'
        label = "Forecast" if is_forecasted == 1 else "Actual"
        ax.plot(group['date'], group['Gpp'], linestyle=linestyle, label=label)
    
    ax.legend(loc='best', facecolor='black', edgecolor='white', labelcolor='white')  # Set legend properties
    
    # Set the color of tick labels to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # sex axis background color to black
    fig.patch.set_facecolor('black')
    
    # Plot!
    st.pyplot(fig)

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='gpp_data.csv',
        mime='text/csv',
    )

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


options_df = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/locations.csv")

location_options = options_df.dropna(subset=['Location'])

options = ["-"] + list(location_options.Location.unique())

st.write("# Boreal Forecast GPP Forecast")

st.markdown(
    """
    Welcome to the Boreal Forest Carbon Calculator. Here you can analyze a single location of the Boreal Forest. 
"""
)

# age = st.slider('How old are you?', 0, 130, 25)
# st.write("I'm ", age, 'years old')

#st.sidebar.button("About")
location_name = st.selectbox("Choose a location", options)
location_filename = "-"
if location_name != "-": location_filename = options_df.loc[(options_df["Location"] == location_name), "filename"].values[0]

# Create the sliders
col1, col2, col3 = st.columns(3)

# creation optional time priods:
time_frame_options = ["Monthly", "Yearly"]
#models
models = {"Short": "Model3", "Medium": "Model4", "Long": "Model5"}

with col1:
    time_frame = st.selectbox("Time Interval", time_frame_options)
    model = st.selectbox("Model Projection", models.keys())

location_filename = location_filename + "_" + models[model]
#st.write(location_filename)

single_location_analysis(location_filename, location_name, model)

if location_name == "-":
    none_selected(options_df)
