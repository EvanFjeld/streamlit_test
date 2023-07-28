#pip install git+https://github.com/streamlit/files-connection
#from st_files_connection import FilesConnection
import streamlit as st

def intro():
    st.write("# Boreal Forest Carbon Calculator")

    st.markdown(
        """
        Welcome to the Boreal Forest Carbon Calculator
    """
    )

def single_location_page():
    page_names_to_funcs = pag_names_functions("Locations")
    location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
    single_location_to_funcs[location_name][1](single_location_to_funcs[location_name][0], location_name)

def location_comparison_page():
    st.markdown('# This page is meant to compare multiple locations')
    st.write(
        """
        What to know when you compare locations.
    """
    )

def about_page():
    st.markdown('# About the Carbon Forecaster')
    st.write(
        """
        This is the final project for a masters in data science program at UC Berkeley.
    """
    )

def single_location_analysis(file, location):
    import time
    import numpy as np
    import pandas as pd

    st.markdown(f'# {location}')
    st.write(
        """
        Gpp over time
    """
    )

    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)
    
    # Create the Streamlit app
    st.title("Gpp Data Visualization")
    
    # Progress bar and status text in the sidebar
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    # Line chart with 'Date' as the x-axis and 'Gpp' as the y-axis
    chart = st.line_chart(data=df, x='date', y='Gpp')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='gpp_data.csv',
        mime='text/csv',
    )


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def single_location_functions(file):
    import pandas as pd
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    saved_options = pd.read_csv(AWS_BUCKET_URL + file_name)

    saved_options['AnalysisType'] = single_location_analysis
    saved_options= saved_options.set_index('Location')
    
    options = {}
    
    for index, row in saved_options.iterrows():
        row_as_list = row.tolist()
        options[index] =  row_as_list
    
    return options

# Define the pages dictionary
pages = {
    "Homepage": intro,
    "Single Location": single_location_page,
    "Location Comparison": location_comparison_page,
    "About": about_page
}

single_location_to_funcs = single_location_functions("Locations")

st.sidebar.button("Homepage", on_click=intro)
st.sidebar.button("Single Location", on_click=single_location_page)
st.sidebar.button("Location Comparison", on_click=location_comparison_page)
st.sidebar.button("About", on_click=about_page)
