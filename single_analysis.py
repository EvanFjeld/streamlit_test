import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def single_location_files():
    file_name = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/Locations.csv"
    return pd.read_csv(file_name)

# Helper function to read data from AWS S3
def read_data_from_aws(file_name):
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)
    return df

# Plot the graph based on the selected option
def plot_graph(selected_option, data):
    filtered_data = data[data['X'] <= selected_option]

    chart = alt.Chart(filtered_data).mark_line().encode(
        x='date',
        y='Gpp'
    ).properties(
        title=f'Graph for X <= {selected_option}'
    )

    st.altair_chart(chart, use_container_width=True)

def main():
    st.title('Graph Gpp Data from AWS S3')

    # Create a dropdown to select a file from AWS S3
    location_files = single_location_files()
    st.write(location_files)
    
    selected_location = st.selectbox('Select Location', location_files.Location)
  
    # # Filter the DataFrame based on the location
    # filtered_df = df.loc[df['Location'] == selected_location]
    
    # # Get the filename for the specific location
    # filename_for_location = filtered_df['filename'].values[0]

    # # Read data from AWS S3 based on the selected file
    # try:
    #     df = read_data_from_aws(filename_for_location)
    # except Exception as e:
    #     st.error(f"Error reading the file from AWS: {e}")

main()
