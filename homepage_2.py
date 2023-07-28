#pip install git+https://github.com/streamlit/files-connection
#from st_files_connection import FilesConnection
import streamlit as st

def intro(file, num):
    import streamlit as st

    st.write("# Boreal Forest Carbon Caolculator")

    st.markdown(
        """
        Welcome to the Boreal Forest Carbon Calculator
    """
    )

def single_location_page():
    location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
    page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)

def single_location_analysis(file, location):
    import streamlit as st
    import time
    import numpy as np
    import pandas as pd

    st.markdown(f'# {location_name}')
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


@st.cache
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
    
    options = {"-": ["", intro]}
    
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

st.sidebar.button("Single Location", single_location_page())
st.sidebar.button("Location Comparison")
st.sidebar.button("About")
# location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)
