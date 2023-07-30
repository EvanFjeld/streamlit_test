import streamlit as st
import time
import numpy as np
import pandas as pd
from datetime import datetime

def none_selected(options_df):
    st.write("Don't know the location name?")
    st.markdown("If you don't have a location name in mind, select a latitude and longitude to see the analysis for that location.")

    #options_df = options_df[["Lat","Long","filename"]]
    lat = "-"
    lat_options = [lat] + list(options_df.Lat.unique())
    long = "-"
    long_options = [long] + (options_df.Long.unique())

    col1, col2 = st.columns(2)
    with col1:
        if long != "-": lat_options = [x for x in long_options if x != long]
        lat = st.selectbox("Select Latitude", lat_options)
    with col2:
        if lat != "-": long_options = [x for x in lat_options if x != lat]
        long = st.selectbox("Select Longitude", long_options)

    file_name = options_df.loc[(options_df["Lat"] == lat) & (options_df["Long"] == long), "filename"].values[0]
    location_name = options_df.loc[(options_df["Lat"] == lat) & (options_df["Long"] == long), "Location"].values[0]

    single_location_analysis(file_name, location_name)
    
    return file_name

def single_location_analysis(file, location):
    st.markdown(f'# {location_name}')
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
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
    
    st.write(f'Here is the analysis and forecast for {location_name}. The Gpp for this site was tracked as far back as {start_month}, {start_year} and our forecast projects Gpp until {end_month}, {end_year}')
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
    # Plot the graph
    # plt.plot(df["date"], df["Gpp"])
    # plt.xlim([start_date, end_date])
    # plt.show()

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

# def pag_names_functions(file):
#     import pandas as pd
    
#     AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
#     file_name = "/streamlit_data/" + file + ".csv"
#     saved_options = pd.read_csv(AWS_BUCKET_URL + file_name)

#     saved_options['AnalysisType'] = single_location_analysis
#     saved_options= saved_options.set_index('Location')
    
#     options = {"-": ["", none_selected]}
    
#     for index, row in saved_options.iterrows():
#         row_as_list = row.tolist()
#         options[index] =  row_as_list
    
#     return options


#page_names_to_funcs = pag_names_functions("Locations")

options_df = saved_options = pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/Locations_temp.csv")

options = ["-"] + list(options_df.Location.unique())

st.write("# Boreal Forecast GPP Forecast")

st.markdown(
    """
    Welcome to the Boreal Forest Carbon Calculator. Here you can analyze a single location of the Boreal Forest. 
"""
)

# age = st.slider('How old are you?', 0, 130, 25)
# st.write("I'm ", age, 'years old')

#st.sidebar.button("About")
location_name = st.selectbox("Choose a location", options.keys())
location_filename = locations_df.loc[(options_df["Location"] == location_name), "filename"].values[0]
#page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)
single_location_analysis(location_filename, location_name)

if location_name == "-":
    lat, long = none_selected(options_df)
