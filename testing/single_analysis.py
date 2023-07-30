import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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

def single_location_analysis(file, location):
    if location == "-": return ""
    
    st.markdown(f'# {location}')
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)

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
    # st.write("Starting date:", min_date)
    # st.write("Max date:", max_date)
    
    # Create the Streamlit app
    st.title("Gpp Data Visualization")

    # Create the sliders
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.slider("Start Date", 
                           min_value = min_date, 
                           max_value=max_date, 
                           value = min_date, 
                           format = "YYYY-MM-DD")
    
        st.write("Starting date:", start_date)
    
    with col2:
        end_date = st.slider("End Date", 
                         min_value = start_date, 
                         max_value=max_date, 
                         value = max_date, 
                         format = "YYYY-MM-DD")
        st.write("Ending date:", end_date)

    # Filter the DataFrame based on the selected date range
    filtered_df = df[(df.date >= start_date) & (df.date <= end_date)]

    # Create the Streamlit app
    st.title("Gpp Data Visualization")

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('black')  # Set black background
    ax.set_title('Gpp Forecasting', color='white', fontsize=16)  # Set white title
    
    # Plot the lines based on 'isforecasted' column
    for is_forecasted, group in filtered_df.groupby('isforecasted'):
        linestyle = '-' if is_forecasted else '--'
        ax.plot(group['date'], group['Gpp'], linestyle=linestyle, label=f'Is Forecasted: {is_forecasted}')
    
    ax.legend(loc='best', facecolor='black', edgecolor='white')  # Set legend properties
    
    # Set the color of tick labels to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Display the plot
    plt.show()

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

single_location_analysis(location_filename, location_name)

if location_name == "-":
    none_selected(options_df)
