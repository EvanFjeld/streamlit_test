#pip install git+https://github.com/streamlit/files-connection
#from st_files_connection import FilesConnection
import streamlit as st

def intro():
    import streamlit as st

    st.write("# Boreal Forest Carbon Caolculator")

    st.markdown(
        """
        Welcome to the Boreal Forest Carbon Calculator
    """
    )

# def location_1():
#     plotting_demo("test", 1)

# def location_2():
#     plotting_demo("location2", 2)

def single_location_analysis(file, num):
    import streamlit as st
    import time
    import numpy as np
    import pandas as pd

    st.markdown(f'# {list(page_names_to_funcs.keys())[num]}')
    st.write(
        """
        Gpp over time
"""
    )

    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)
    
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = df.Gpp
    chart = st.line_chart(last_rows)

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
    df = pd.read_csv(AWS_BUCKET_URL + file_name)

    df['AnalysisType'] = "single_location_analysis"
    
    return df.set_index('Location').to_dict(orient='index')


page_names_to_funcs = pag_names_functions("Locations")

# page_names_to_funcs = {
#     "—": intro,
#     "Location 1": single_location_analysis, "test",
#     "Location 2": single_location_analysis, "location2",
# }

st.sidebar.button("About")
demo_name = st.sidebar.selectbox("Choose a location", page_names_to_funcs.keys())
st.markdown(str(demo_name))
page_names_to_funcs[demo_name[1]](page_names_to_funcs[demo_name[0]])
