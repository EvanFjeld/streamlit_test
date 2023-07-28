#pip install git+https://github.com/streamlit/files-connection
#from st_files_connection import FilesConnection
import streamlit as st
import time
import numpy as np
import pandas as pd

def intro():
    st.write("# Boreal Forest Carbon Calculator")

    st.markdown(
        """
        Welcome to the Boreal Forest Carbon Calculator
    """
    )

def single_location_page():
    location_name = st.selectbox("Choose a location", single_location_to_funcs.keys())

    if "selected_location" not in st.session_state:
        st.session_state.selected_location = None

    if st.session_state.selected_location != location_name:
        # Clear the previous selection and re-initialize the graph
        st.session_state.selected_location = location_name
        st.session_state.graph_initialized = False

    # Check if the graph needs to be initialized
    if not st.session_state.get("graph_initialized", False):
        # Initialize an empty placeholder for the graph
        graph_placeholder = st.empty()
        single_location_analysis(graph_placeholder, single_location_to_funcs[location_name][0], location_name)
        st.session_state.graph_initialized = True
    else:
        # If graph is already initialized, display the existing graph
        single_location_analysis(None, single_location_to_funcs[location_name][0], location_name)




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

def single_location_landing_page(file, location):
    st.markdown(f"# {location}")
    st.write("Gpp over time")
    st.write("Select a location from the dropdown.")


def single_location_analysis(placeholder, file, location):
    if placeholder is not None:
        # Display the placeholder if it exists
        placeholder.markdown(f"# {location}")
        placeholder.write("Gpp over time")
    
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

def single_lat_long():
    df = get_lat_long_options()
    
    lat_options = df.Lat
    long_options = df.Long
    
    # Create two columns for the layout
    col1, col2 = st.columns(2)
    
    # Display the latitude selectbox in the first column
    with col1:
        lat = st.selectbox("Choose a Latitude", lat_options)
    
    # Display the longitude selectbox in the second column
    with col2:
        long = st.selectbox("Choose a Longitude", long_options)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def get_lat_long_options():
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/location_files/" + Lat_Long_Locations + ".csv"
    return pd.read_csv(AWS_BUCKET_URL + file_name)
    

def single_location_functions(file):
    import pandas as pd
    
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    saved_options = pd.read_csv(AWS_BUCKET_URL + file_name)

    saved_options['AnalysisType'] = single_location_analysis
    saved_options= saved_options.set_index('Location')
    
    # options = {{"-": ["", ""]}}
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
    "Explore Lat/Long": single_lat_long,
    "About": about_page
}

single_location_to_funcs = single_location_functions("Locations")

# Check if the app is just starting (no state exists)
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True  # Set the flag to True after displaying the intro
    intro()  # Display the homepage by default

st.sidebar.button("Homepage", on_click=intro)
st.sidebar.button("Single Location", on_click=single_location_page)
st.sidebar.button("Location Comparison", on_click=location_comparison_page)
st.sidebar.button("Explore Lat/Long", on_click=single_lat_long)
st.sidebar.button("About", on_click=about_page)

