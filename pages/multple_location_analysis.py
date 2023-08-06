import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components
from datetime import datetime

# def none_selected(file, num):
#     st.write("Don't know the location name?")
#     st.markdown("If you don't have a location name in mind, select a latitude and longitude to see the analysis for that location.")

#     # Create 2 columns for latitude and longitude for comparison
#     ll_col1, ll_col2 = st.columns(2)
#     with ll_col1:
#         st.write("Location #1")
#         loc1_lat = st.selectbox("Location 1 Latitude", page_names_to_funcs.keys())
#         loc1_long = st.selectbox("Location 1 Longitude", page_names_to_funcs.keys())
#     with ll_col2:
#         st.write("Location #2")
#         loc2_lat = st.selectbox("Location 2 Latitude", page_names_to_funcs.keys())
#         loc2_long = st.selectbox("Location 2 Longitude", page_names_to_funcs.keys())
        

def multiple_location_analysis(file1, file2, location1, location2, model_name, model):
    if location1 == "-" or location2 == "-":
        st.markdown(f'# Select a Location')
        return ""
    
    st.markdown(f'# {location1} vs. {location2}')

    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    
    loc_1_file_name = "/streamlit_data/data/" + model + "/" + file1 + ".csv"
    st.write(loc_1_file_name)
    try:
        loc1_df = pd.read_csv(AWS_BUCKET_URL + loc_1_file_name)
    except HTTPError:
        st.title(f'{location1} not available with the {model_name.lower()}-term model')
        st.write(f'The {model_name.lower()}-term model is not avaialble for {location1}. Please select another location or model.')
        return ""

    loc_2_file_name = "/streamlit_data/data/" + model + "/" + file2 + ".csv"
    try:
        loc2_df = pd.read_csv(AWS_BUCKET_URL + loc_2_file_name)
    except HTTPError:
        st.title(f'{location2} not available with the {model_name.lower()}-term model')
        st.write(f'The {model_name.lower()}-term model is not avaialble for {location2}. Please select another location or model.')
        return ""
    

    loc1_df = loc1_df[['date', 'Gpp', 'isforecasted']]
    loc2_df = loc2_df[['date', 'Gpp']]
    
    # Convert the 'date' column to datetime type
    #df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
    loc1_df['date'] = pd.to_datetime(loc1_df.date)
    loc2_df['date'] = pd.to_datetime(loc2_df.date)

    df = loc1_df.merge(loc2_df, on='date', suffixes=('_loc1', '_loc2'))
    df['date'] = pd.to_datetime(df['date'])    

    min_date = df.date.min().to_pydatetime()
    max_date = df.date.max().to_pydatetime()
    start_month = min_date.strftime("%B")
    start_year = min_date.year
    end_month = max_date.strftime("%B")
    end_year = max_date.year

    loc1_gpp_avg = loc1_df.Gpp.mean()
    loc2_gpp_avg = loc2_df.Gpp.mean()
    
    st.write(f'This is a comparison between {location1} and {location2}. The Gpp for this site was tracked as far back as {start_month}, {start_year} and our forecast projects Gpp until {end_month}, {end_year}')
    st.write(f'{location1} will have an mean monthly Gpp of {round(loc1_gpp_avg)} while {location2} will have a mean monthly Gpp of {round(loc2_gpp_avg)}')

    # creation optional time priods:
    time_frame_options = ["Monthly", "Quarterly", "Yearly"]
    
    # Create the sliders
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_frame = st.selectbox("Time Interval", time_frame_options)
        st.write("Time Interval:", time_frame)
    
    with col2:
        start_date = st.slider("Start Date", 
                           min_value = min_date, 
                           max_value=max_date, 
                           value = min_date, 
                           format = "YYYY-MM-DD")
    
        st.write("Starting date:", start_date)
    
    with col3:
        end_date = st.slider("End Date", 
                         min_value = start_date, 
                         max_value=max_date, 
                         value = max_date, 
                         format = "YYYY-MM-DD")
        st.write("Ending date:", end_date)

    # group dataset for time period
    if time_frame == "Yearly":
        filtered_df = df.groupby(df['date'].dt.year).agg({
            'Gpp_loc1': 'mean',
            'Gpp_loc2': 'mean',
            'isforecasted': lambda x: any(x)  # Check if any value in 'isforecasted' is True
        }).reset_index()
        # Filter the DataFrame based on the selected date range
        filtered_df = filtered_df[(filtered_df.date >= start_date.year) & (filtered_df.date <= end_date.year)]
    elif time_frame == "Quarterly":
        filtered_df = df
        filtered_df.date = pd.PeriodIndex(filtered_df.date, freq='Q')
        filtered_df = filtered_df.groupby('date').agg({
            'Gpp_loc1': 'mean',
            'Gpp_loc2': 'mean',
            'isforecasted': lambda x: any(x)  # Check if any value in 'isforecasted' is True
        }).reset_index()
        # Filter the DataFrame based on the selected date range
        filtered_df = filtered_df[(filtered_df.date >= pd.Period(start_date, freq='Q')) & (filtered_df.date <= pd.Period(end_date, freq='Q'))]
        filtered_df['date'] = filtered_df['date'].dt.to_timestamp()
    else:
        filtered_df = df
        # Filter the DataFrame based on the selected date range
        filtered_df = filtered_df[(filtered_df.date >= start_date) & (filtered_df.date <= end_date)]

    # Filter the DataFrame based on the selected date range
    #filtered_df = filtered_df[(df.date >= start_date) & (df.date <= end_date)]

    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('black')  # Set black background
    ax.set_title('Gpp Forecasting', color='white', fontsize=16)  # Set white title
    
    # Plot the lines for 'Gpp_loc1' and 'Gpp_loc2' based on 'isforecasted' column
    for is_forecasted, group in filtered_df.groupby('isforecasted'):
        linestyle = '--' if is_forecasted == 1 else '-'
        label = "Forecast" if is_forecasted == 1 else "Actual"
        ax.plot(group['date'], group['Gpp_loc1'], linestyle=linestyle, label=f'{label} - {location1}')
        ax.plot(group['date'], group['Gpp_loc2'], linestyle=linestyle, label=f'{label} - {location2}')
    
    ax.legend(loc='best', facecolor='black', edgecolor='white', labelcolor='white')  # Set legend properties
    
    # Set the color of tick labels and title to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Set the color of the axis spines (lines representing the axes) to white
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    # Set the x-axis color to black
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Set the color of the axis spines (lines representing the axes) to white
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
        
    fig.patch.set_facecolor('black')

    # Set the y-axis to start at 0
    ax.set_ylim(bottom=0)
    
    # Plot!
    st.pyplot(fig)

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='gpp_comparison_data.csv',
        mime='text/csv',
    )

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.write("# Boreal Forecast GPP Forecast Comparison")

st.markdown(
    """
    Welcome to the Boreal Forest Carbon Calculator. Here you can compare two locations and their forecast. This is a great way to compare logging locations to understand the impact on Gpp over time 
"""
)

# creation optional time priods:
time_frame_options = ["Monthly", "Yearly"]
#models
#models = {"Short": "Model3", "Medium": "Model4", "Long": "Model5"}
models = {"Model": "Model6"}

# set model - comment this out and replace with options if necessary
model = "Model"

# Columns for 2 locations to compare
options_df = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/locations.csv")
location_options = options_df.dropna(subset=['Location'])

options = ["-"] + list(location_options.Location.unique())

location1_options = options
location_1_name = "-"
loc_1_filename = ""
location2_options = options
location_2_name = "-"
loc_2_filename = ""

loc_col1, loc_col2 = st.columns(2)
with loc_col1:
    if location_2_name != "-": location1_options = [x for x in location2_options if x != location_2_name]
    location_1_name = st.selectbox("Choose the first location", location1_options)
    if location_1_name != "-": loc_1_filename = options_df.loc[(options_df["Location"] == location_1_name), "filename"].values[0]
    else: loc_1_filename = 'average'
with loc_col2:
    if location_1_name != "-": location2_options = [x for x in location1_options if x != location_1_name]
    location_2_name = st.selectbox("Choose the second location", location2_options)
    if location_2_name != "-": loc_2_filename = options_df.loc[(options_df["Location"] == location_2_name), "filename"].values[0]
    else: loc_2_filename = 'average'

if location_1_name != "-" and location_2_name != "-":
    multiple_location_analysis(file1 = loc_1_filename, 
                           file2 = loc_2_filename, 
                           location1 = location_1_name, 
                           location2 = location_2_name,
                           model_name = model,
                           model = models[model])
