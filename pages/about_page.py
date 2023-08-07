import streamlit as st

st.set_page_config(
    page_title="About",
)


AWS_BUCKET_URL = "https://carbon-forecaster-capstone-s3.s3.us-west-2.amazonaws.com"
image_name = "/streamlit_data/about/boreal_forest.jpeg"

st.write("# About the Boreal Forest Carbon Forecaster")

st.image(AWS_BUCKET_URL + image_name, caption='Boreal Forest', use_column_width=True)

st.write("# What is GPP?")

st.markdown(
    """
GPP stands for Gross Primary Productivity. It is a crucial concept in the study of Earth's ecosystems and the carbon cycle. GPP represents the total amount of energy that
primary producers, such as plants and algae, capture through photosynthesis in a given area and time period. Photosynthesis is the process by which plants, algae, and some
bacteria convert carbon dioxide (CO2) and sunlight into organic matter (usually in the form of glucose) and release oxygen (O2 as a byproduct). This organic matter serves 
as food for various organisms, and the process of photosynthesis is fundamental in sustaining life on Earth. GPP is a fundamental parameter in understanding the global carbon
cycle because it quantifies the rate at which carbon is captured from the atmosphere and converted into organic matter. It is a critical variable for assessing the carbon 
sequestration capacity of ecosystems and their role in mitigating climate change by acting as carbon sinks. Researchers and scientists use various methods, such as satellite
observations, eddy covariance measurements, and ecosystem models, to estimate GPP at different scales, from individual plants to entire ecosystems and the global level. 
Understanding GPP helps scientists assess the health and productivity of ecosystems, monitor changes in vegetation, and make predictions about how ecosystems might respond 
to climate change and human activities.
""")

st.write("# What is MODIS?")

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

st.write("# About the Project")

st.markdown(
    """
This project was completed by Anshuman Awathi, Patricia Gallagher, and Evan Fjeld with support from the Wildland's Leauge as the final project for the University
of California at Berkeley's School of Information Master's in Data Science program. The final project was complated in the summer term of 2023.
"""
)
col1, col2 , col3, col4 = st.columns(4)

with col1:
    # Assuming you have the URL of the image
    wildlands_image_url = "https://wildlandsleague.org/wp-content/themes/wildlands-league/assets/img/wildlands-league.png"
    
    # Load and display the image from the URL
    st.image(wildlands_image_url, caption='Wildlands League', use_column_width=True)
