import streamlit as st
import time
import numpy as np
import pandas as pd
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
    st.markdown(f'# {location_name}')
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    loc_1_file_name = "/streamlit_data/" + file + ".csv"
    loc1_df = pd.read_csv(AWS_BUCKET_URL + loc_1_file_name)
    loc_2_file_name = "/streamlit_data/" + file2 + ".csv"
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

    # Line chart with 'Date' as the x-axis and 'Gpp' as the y-axis
    chart = st.line_chart(data=filtered_df, x='date', y='Gpp')

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

def pag_names_functions(file):
    import pandas as pd
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    saved_options = pd.read_csv(AWS_BUCKET_URL + file_name)

    saved_options['AnalysisType'] = multiple_location_analysis
    saved_options= saved_options.set_index('Location')
    
    options = {"-": ["", none_selected]}
    
    for index, row in saved_options.iterrows():
        row_as_list = row.tolist()
        options[index] =  row_as_list
    
    return options


page_names_to_funcs = pag_names_functions("Locations")

st.write("# Boreal Forecast GPP Forecast Comparison")

st.markdown(
    """
    Welcome to the Boreal Forest Carbon Calculator. Here you can compare two locations and their forecast. This is a great way to compare logging locations to understand the impact on Gpp over time 
"""
)

#st.sidebar.button("About")

# Columns for 2 locations to compare
options_df = saved_options = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/Locations_temp.csv")
locations_df = options_df[['Location', 'filename']].set_index('Location')

options = {"-": [""]}

for index, row in locations_df.iterrows():
    row_as_list = row.tolist()
    options[index] =  row_as_list

loc_col1, loc_col2 = st.columns(2)
with loc_col1:
  location1_options = options.keys()
  location_1_name = st.selectbox("Choose the first location", location1_options)
with loc_col2:
  location2_options = [x for x in location1_options if x != location_1_name]
  location_2_name = st.selectbox("Choose the second location", Location2_options)

multiple_location_analysis(options[location_1_name], options[location_2_name], location_1_name, location_2_name)
