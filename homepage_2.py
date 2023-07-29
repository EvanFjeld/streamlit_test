import streamlit as st
import pandas as pd

def intro():
    st.write("# Boreal Forest Carbon Calculator")
    st.markdown("Welcome to the Boreal Forest Carbon Calculator")

def single_location_nav(location_name):
    single_location_to_funcs[location_name][1](single_location_to_funcs[location_name][0], location_name)

def single_location_page():
    st.markdown('# Analysis of a Single Location')
    st.write("Great!")
    single_location_nav(single_location_to_funcs)

def location_comparison_page():
    st.markdown('# This page is meant to compare multiple locations')
    st.write("What to know when you compare locations.")

def single_location_page():
    st.markdown('# Analysis of a Single Location')
    st.write("Great!")
    single_location_to_funcs = single_location_names()
    location_name = st.selectbox("Choose a location", list(single_location_to_funcs.keys()))
    single_location_nav(location_name)

def single_location_landing_page(file, location):
    st.markdown(f"# {location}")
    st.write("Gpp over time")
    st.write("Select a location from the dropdown.")

def about_page():
    st.markdown('# About the Carbon Forecaster')
    st.write("This is the final project for a master's in data science program at UC Berkeley.")

def single_location_basic():
    st.markdown('# Analysis of a Single Location')
    st.write("Great!")

def single_location_analysis(placeholder, file, location):
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/" + file + ".csv"
    df = pd.read_csv(AWS_BUCKET_URL + file_name)

    if placeholder is not None:
        # Display the placeholder if it exists
        placeholder.markdown(f"# {location}")
        placeholder.write("Gpp over time")

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

    lat_options = df.Lat.unique()

    # Check if the selected latitude is in the session state, if not, initialize it to the first option
    if "selected_lat" not in st.session_state:
        st.session_state.selected_lat = lat_options[0]

    # Display the latitude selectbox
    lat = st.selectbox("Choose a Latitude", lat_options, index=lat_options.tolist().index(st.session_state.selected_lat))

    # Update the selected latitude in the session state
    st.session_state.selected_lat = lat

    # Filter the DataFrame to get the corresponding longitude options based on the selected latitude
    filtered_df = df.loc[df['Lat'] == lat]
    long_options = filtered_df.Long.unique()

    # Check if the selected longitude is in the session state, if not, initialize it to the first option
    if "selected_long" not in st.session_state:
        st.session_state.selected_long = long_options[0]

    # Display the longitude selectbox
    long = st.selectbox("Choose a Longitude", long_options, index=long_options.tolist().index(st.session_state.selected_long))

    # Update the selected longitude in the session state
    st.session_state.selected_long = long

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def get_lat_long_options():
    AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
    file_name = "/streamlit_data/location_files/Lat_Long_Locations.csv"
    return pd.read_csv("https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/location_files/Lat_Long_Locations.csv")

def single_location_names():
    file_name = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com/streamlit_data/Locations.csv"
    saved_options = pd.read_csv(file_name)

    options = {"-": single_location_basic}  # Initialize with the intro function

    for index, row in saved_options.iterrows():
        location_name = row["Location"]
        analysis_function = single_location_analysis  # Assuming you want to use single_location_analysis for all locations
        options[location_name] = analysis_function

    return options



# Define the pages dictionary
pages = {
    "Homepage": intro,
    "Single Location": single_location_page,
    "Location Comparison": location_comparison_page,
    "Explore Lat/Long": single_lat_long,
    "About": about_page
}

# Check if the app is just starting (no state exists)
if "initialized" not in st.session_state:
    st.session_state["initialized"] = True  # Set the flag to True after displaying the intro
    intro()  # Display the homepage by default

st.sidebar.button("Homepage", on_click=intro)
st.sidebar.button("Single Location", on_click=single_location_page)
st.sidebar.button("Location Comparison", on_click=location_comparison_page)
st.sidebar.button("Explore Lat/Long", on_click=single_lat_long)
st.sidebar.button("About", on_click=about_page)
