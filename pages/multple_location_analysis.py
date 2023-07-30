import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components
from datetime import datetime

def none_selected(file, num):
    st.write("Don't know the location name?")
    st.markdown("If you don't have a location name in mind, select a latitude and longitude to see the analysis for that location.")

    # Create 2 columns for latitude and longitude for comparison
    ll_col1, ll_col2 = st.columns(2)
    with ll_col1:
        st.write("Location #1")
        loc1_lat = st.selectbox("Location 1 Latitude", page_names_to_funcs.keys())
        loc1_long = st.selectbox("Location 1 Longitude", page_names_to_funcs.keys())
    with ll_col2:
        st.write("Location #2")
        loc2_lat = st.selectbox("Location 2 Latitude", page_names_to_funcs.keys())
        loc2_long = st.selectbox("Location 2 Longitude", page_names_to_funcs.keys())
        

def multiple_location_analysis(file1, file2, location1, location2):
    if location1 == "-" or location2 == "-":
        st.markdown(f'# Select a Location')
        return ""
    
    st.markdown(f'# {location1} & {location2}')
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    loc_1_file_name = "/streamlit_data/data/" + file1 + ".csv"
    loc1_df = pd.read_csv(AWS_BUCKET_URL + loc_1_file_name)
    loc_2_file_name = "/streamlit_data/data/" + file2 + ".csv"
    loc2_df = pd.read_csv(AWS_BUCKET_URL + loc_2_file_name)

    loc1_df = loc1_df[['date', 'Gpp']]
    loc2_df = loc2_df[['date', 'Gpp']]
    
    # Convert the 'date' column to datetime type
    #df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
    loc1_df['date'] = pd.to_datetime(loc1_df.date)
    loc2_df['date'] = pd.to_datetime(loc2_df.date)

    df = loc1_df.merge(loc2_df, on='date', suffixes=('_loc1', '_loc2'))

    min_date = df.date.min().to_pydatetime()
    max_date = df.date.max().to_pydatetime()
    start_month = min_date.strftime("%B")
    start_year = min_date.year
    end_month = max_date.strftime("%B")
    end_year = max_date.year
    
    st.write(f'This is a comparison between {location1} and {location2}. The Gpp for this site was tracked as far back as {start_month}, {start_year} and our forecast projects Gpp until {end_month}, {end_year}')
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

    fig, ax = plt.subplots()

    # Plot the first line for 'Gpp_loc1'
    ax.plot(filtered_df['date'], filtered_df['Gpp_loc1'], label='Gpp_loc1', color='blue')

    ## Plot the second line for 'Gpp_loc2'
    ax.plot(filtered_df['date'], filtered_df['Gpp_loc2'], label='Gpp_loc2', color='green')

    # CODE TO ADD
    # Define some CSS to control our custom labels
    css = """
    table
    {
      border-collapse: collapse;
    }
    th
    {
      color: #ffffff;
      background-color: #000000;
    }
    td
    {
      background-color: #cccccc;
    }
    table, th, td
    {
      font-family:Arial, Helvetica, sans-serif;
      border: 1px solid black;
      text-align: right;
    }
    """
    for axes in fig.axes:
        for line in axes.get_lines():
            # get the x and y coords
            xy_data = line.get_xydata()
            labels = []
            for x, y in xy_data:
                # Create a label for each point with the x and y coords
                html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                labels.append(html_label)
            # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
            tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
            # Since this is a separate plugin, you have to connect it
            plugins.connect(fig, tooltip)
    
    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Gpp')
    ax.set_title('Gpp Data Visualization')

    ax.legend()
    # Display the plot using st.pyplot()
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600)

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

# Columns for 2 locations to compare
options_df = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/locations.csv")
location_options = options_df.dropna(subset=['Location'])

options = ["-"] + list(location_options.Location.unique())

location1_options = options
location_1_name = "-"
location2_options = options
location_2_name = "-"

loc_col1, loc_col2 = st.columns(2)
with loc_col1:
    if location_2_name != "-": location1_options = [x for x in location2_options if x != location_2_name]
    location_1_name = st.selectbox("Choose the first location", location1_options)
    if location_1_name != "-": loc_1_filename = options_df.loc[(options_df["Location"] == location_1_name), "filename"].values[0]
with loc_col2:
    if location_1_name != "-": location2_options = [x for x in location1_options if x != location_1_name]
    location_2_name = st.selectbox("Choose the second location", location2_options)
    if location_1_name != "-": loc_2_filename = options_df.loc[(options_df["Location"] == location_1_name), "filename"].values[0]

multiple_location_analysis(loc_1_filenamek, loc_2_filename, location_1_name, location_2_name)
