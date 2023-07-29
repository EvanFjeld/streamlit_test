import streamlit as st
import time
import numpy as np
import pandas as pd

def intro(x, y):
    st.write("Select a location")

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
    
    # Create the Streamlit app
    st.title("Gpp Data Visualization")
    
    # Line chart with 'Date' as the x-axis and 'Gpp' as the y-axis
    chart = st.line_chart(data=df, x='date', y='Gpp')

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
    
    options = {"-": ["", intro]}
    
    for index, row in saved_options.iterrows():
        row_as_list = row.tolist()
        options[index] =  row_as_list
    
    return options


page_names_to_funcs = pag_names_functions("Locations")

location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)

def main():
    page_names_to_funcs = pag_names_functions("Locations")

    location_name = st.selectbox("Choose a location", page_names_to_funcs.keys())
    page_names_to_funcs[location_name][1](page_names_to_funcs[location_name][0], location_name)

if __name__ == '__main__':
    main()
