import streamlit as st
import time
import numpy as np
import pandas as pd
from datetime import datetime

def none_selected(file, num):
    st.write("Don't know the location name?")
    st.markdown("If you don't have a location name in mind, select a latitude and longitude to see the analysis for that location.")

    col1, col2 = st.columns(2)
    with col1:
        lat = st.selectbox("Select Latitude", page_names_to_funcs.keys())
    with col2:
        long = st.selectbox("Select Longitude", page_names_to_funcs.keys())
        

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

def pag_names_functions(file):
    import pandas as pd
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    saved_options = pd.read_csv(AWS_BUCKET_URL + file_name)

    saved_options['AnalysisType'] = single_location_analysis
    saved_options= saved_options.set_index('Location')
    
    options = {"-": ["", none_selected]}
    
    for index, row in saved_options.iterrows():
        row_as_list = row.tolist()
        options[index] =  row_as_list
    
    return options


page_names_to_funcs = pag_names_functions("Locations")

# page_names_to_funcs = {
#     "—": [intro, ""],
#     "Location 1": [single_location_analysis, "test"],
#     "Location 2": [single_location_analysis, "location2"],
# }

st.write("# Boreal Forest Carbon Caolculator")

st.markdown(
    """
    Welcome to the Boreal Forest Carbon Calculator. Select a location to view analysis and a forecast of GPP in that area. 
"""
)

# age = st.slider('How old are you?', 0, 130, 25)
# st.write("I'm ", age, 'years old')

#st.sidebar.button("About")
location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)
