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

# def get_aws_data(file_name):
#     s3_bucket = "s3://carbon-forecaster-capstone-s3/streamlit_data/"
#     conn = st.experimental_connection("s3", type=FilesConnection)
#     df = conn.read_csv(f"s3://{s3_bucket}/{file_key}")
#     st.dataframe(df)

def plotting_demo(file):
    import streamlit as st
    import time
    import numpy as np
    import pandas as pd

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
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

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


page_names_to_funcs = {
    "—": intro,
    "Location 1": plotting_demo("test.csv"),
}

st.sidebar.button("About")
demo_name = st.sidebar.selectbox("Choose a location", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
