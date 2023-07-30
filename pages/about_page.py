import streamlit as st

st.set_page_config(
    page_title="About",
)

st.write("# About the Boreal Forest Carbon Forecaster")

st.markdown(
    """
    
The MODIS (Moderate Resolution Imaging Spectroradiometer) dataset is a product of NASA's Earth Observing System (EOS) program and is obtained from instruments aboard two 
satellites: Terra (launched in 1999) and Aqua (launched in 2002). This dataset plays a crucial role in monitoring various Earth processes and gathering data on the planet's 
surface and atmosphere. It offers a combination of high spatial detail and global coverage, providing data at spatial resolutions of 250 meters, 500 meters, and 1 kilometer. 
MODIS captures data in multiple spectral bands, including visible, infrared, and thermal wavelengths, allowing scientists to analyze various properties of land, ocean, 
and atmosphere. With a high temporal resolution, MODIS revisits the entire Earth's surface every 1 to 2 days, making it valuable for near real-time monitoring of dynamic
processes like vegetation health, land cover changes, and weather patterns. The dataset finds applications in numerous fields, such as vegetation monitoring, land and sea
surface temperature assessment, snow and ice cover observation, and studying atmospheric parameters. MODIS data is publicly accessible through NASA's Earthdata Search and
other data portals, distributed in Hierarchical Data Format (HDF) for ease of scientific use. However, it's important to consult the most up-to-date sources for the latest
information on the MODIS program and its advancements since my last knowledge update in September 2021.
"""
)
