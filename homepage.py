import streamlit as st
import time
import numpy as np
import pandas as pd

def none_selected(file, num):
    import streamlit as st

    st.write("## Select a location")

    st.markdown(
        """
        Welcome to the Boreal Forest Carbon Calculator. Select a location to view analysis and a forecast of GPP in that area. 
    """
    )

def single_location_analysis(file, location):


    st.markdown(f'# {location_name}')
    st.write(
        """
        Gpp over time
    """
    )

    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)

    # Convert the 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
    
    # Create the Streamlit app
    st.title("Gpp Data Visualization")
    
    # Get the min and max date values from the DataFrame
    min_date = df['date'].min()
    max_date = df['date'].max()

    # Add a slider to select the date range
    start_date = st.slider("Select start date", min_date, max_date, min_date)
    end_date = st.slider("Select end date", min_date, max_date, max_date)

    # Filter the DataFrame based on the selected date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

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

#st.sidebar.button("About")
location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)
