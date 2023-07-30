import streamlit as st

st.set_page_config(
    page_title="Homepage",
)

st.write("# Welcome to the Boreal Forest Carbon Calculator")

st.sidebar.success("What would you like to do?")

st.markdown(
    """
    Single location or compare mulitple locations. 
"""
)
