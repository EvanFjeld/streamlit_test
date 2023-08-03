import streamlit as st
from st_pages import Page, show_pages, add_page_title

st.set_page_config(
    page_title="Homepage",
)

# Optional -- adds the title and icon to the current page
#add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("homepage.py", "Homepage"),
        Page("pages/single_location_analysis.py", "Single Location Analysis"),
        Page("pages/multple_location_analysis.py", "Compare Multiple Locations"),
        Page("pages/location_request.py", "Request a New Location"),
        Page("pages/about_page.py", "About"),
    ]
)

st.write("# Welcome to the Boreal Forest Carbon Calculator")

# Display the image
AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
image_name = "/streamlit_data/about/boreal_forest.jpeg"
st.image(AWS_BUCKET_URL + image_name, caption='Boreal Forest', use_column_width=True)

# Text
st.markdown(
    """
    This app is meant to facilitate the exploration of Gross Primary Productivity (GPP) of Canada's Boreal Foreast. Using the MODIS dataset and a techniqule called Temporally-Fused
    Transformers (TFT) time-series modeling, we are able to look at GPP values in the Boreal Forest over the past 20 years to predict the next 30. 
"""
)
