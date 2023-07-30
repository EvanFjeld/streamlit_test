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
        Page("pages/about_page.py", "About"),
    ]
)

st.write("# Welcome to the Boreal Forest Carbon Calculator")

st.markdown(
    """
    Single location or compare mulitple locations. 
"""
)
