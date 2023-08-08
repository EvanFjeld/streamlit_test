import streamlit as st

st.set_page_config(
    page_title="About the Project",
)
donation_url = "https://donorbox.org/wl-ncp"
tft_url = "https://arxiv.org/pdf/1912.09363.pdf"

st.write('# About the Project')

st.markdown(
    """
This project was completed by Anshuman Awathi, Patricia Gallagher, and Evan Fjeld with support from the Wildlands League 
as the final project for the University of California at Berkeley's School of Information Master's in Data Science program. 
The final project was completed in the summer term of 2023.
""")

st.markdown(
    f"""
    The objective of this project was to develop a user-friendly app that offers the Wildlands League valuable insights 
    into the climate impact of Logging Scars. This innovative tool not only presents real GPP data spanning from 2002 to 
    2022 but also provides projections for GPP extending from 2023 to 2050. These projections were generated using a 
    [Temporal Fusion Transformer]({tft_url}).
""")

wildlandsleague_url = "https://wildlandsleague.org/"
report_url = "chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://loggingscars.ca/wp-content/uploads/2020/07/logging-scars-press-release-2020.pdf"

st.write(f'# [Motivation]({wildlandsleague_url})')

st.markdown(
    f"""
The Wildlands League released a [report]({report_url}) in 2019 showcasing 270 barren sites, labeled as logging scars, that have remained 
treeless for up to three decades due to road construction and heavy equipment use related to forest operations. Logging 
scars are areas in forests where the regrowth of trees is suppressed due to compacted soil resulting from machinery and 
the decay of tree "waste" piles that suffocate future growth. These scars exist outside of Ontario's forest management 
planning and make up an estimated 10.2% to 23.7% of reforested areas post-logging. The total deforested area across these 
scars amounts to approximately 650,000 hectares, creating a significant net deforestation impact that has been largely 
overlooked. These scars are not considered in forest area calculations by provincial and federal governments or in carbon 
storage estimations for Canada's boreal forest, used in international climate reporting. The deforestation issue has 
far-reaching implications for climate change, the preservation of threatened species like boreal caribou, and the 
sustainable timber supply. Despite this, the province aims to increase logging while reducing regulations, recently 
removing environmental safeguards for forest operations. This situation raises concerns about the potential negative 
impacts on environmental sustainability and biodiversity in Canada's untouched boreal forests.
""")

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

st.write('# Thank You!')

st.markdown(
    """
Thank you to Puya Vahabi and Alberto Todeschini for their support and mentorship, and to the Wildlands League for inspiring 
and guiding this project.
""")

st.markdown(f'[Donate to the Wildlands League]({donation_url})')

col1, col2 , col3, col4 = st.columns(4)

with col1:
    # Assuming you have the URL of the image
    wildlands_image_url = "https://wildlandsleague.org/wp-content/themes/wildlands-league/assets/img/wildlands-league.png"
    
    # Load and display the image from the URL
    st.image(wildlands_image_url, caption='Wildlands League', use_column_width=True)
    st.markdown(f'[Donate]({donation_url})')

with col4:
    berkeley_image_url = "https://ischoolonline.berkeley.edu/wp-content/uploads/sites/37/2021/10/UCB-CYB_Logo_282x56-1.png"
    # Load and display the image from the URL
    st.image(berkeley_image_url, caption='UC Berkeley MIDS', use_column_width=True)
