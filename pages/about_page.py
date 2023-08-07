import streamlit as st

st.set_page_config(
    page_title="About the Project",
)

st.write('# About the Project')

st.markdown(
    """
This project was completed by Anshuman Awathi, Patricia Gallagher, and Evan Fjeld with support from the Wildlands League 
as the final project for the University of California at Berkeley's School of Information Master's in Data Science program. 
The final project was completed in the summer term of 2023.
""")

st.markdown(
    """
    The objective of this project was to develop a user-friendly app that offers the Wildlands League valuable insights 
    into the climate impact of Logging Scars. This innovative tool not only presents real GPP data spanning from 2002 to 
    2022 but also provides projections for GPP extending from 2023 to 2048. These projections were generated using a Temporal 
    Fusion Transfer Model.
""")

st.write('# Motivation')

st.markdown(
    """
The Wildlands League released a report in 2019 showcasing 270 barren sites, labeled as logging scars, that have remained 
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

st.write('# Thank You!')

st.markdown(
    """
Thank you to Puya Vahabi and Alberto Todeschini for their support and mentorship, and to the Wildlands League for inspiring 
and guiding this project.
""")

col1, col2 , col3, col4 = st.columns(4)

with col1:
    # Assuming you have the URL of the image
    wildlands_image_url = "https://wildlandsleague.org/wp-content/themes/wildlands-league/assets/img/wildlands-league.png"
    
    # Load and display the image from the URL
    st.image(wildlands_image_url, caption='Wildlands League', use_column_width=True)

with col4:
    berkeley_image_url = "https://ischoolonline.berkeley.edu/wp-content/uploads/sites/37/2021/10/UCB-CYB_Logo_282x56-1.png"
    # Load and display the image from the URL
    st.image(berkeley_image_url, caption='UC Berkeley MIDS', use_column_width=True)
