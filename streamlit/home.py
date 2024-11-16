import streamlit as st

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="🏠 Property Price Prediction in Belgium",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ==============================
# 2. Landing Page Content
# ==============================
# Add a title
st.title("🏠 Welcome to the Property Price Prediction App")

# Add an introductory paragraph
st.write(
    """
    Welcome to the **Property Price Prediction App**! This application leverages **machine learning models** to help you estimate the value of properties in Belgium.
    Whether you're buying, selling, or just curious, our app provides a reliable and user-friendly tool for predicting real estate prices.
    The data for this app was scraped from Immoweb. We have deployed two seperate models - one for houses and one for appartments.
    """
)

# Add a horizontal divider
st.markdown("---")

# Add navigation instructions
st.markdown("### What would you like to do?")
st.write(
    """
    - 🏢 **[Predict Apartment Prices](1_Appartment_Prediction)**  
      Estimate the value of an apartment based on its location and features.
      
    - 🏠 **[Predict House Prices](2_House_Prediction)**  
      Estimate the value of a house based on its size, amenities, and location.
      
    - 📊 **[Learn About the Model](3_Model_Description)**  
      Understand how our models work and their performance metrics.
    """
)

# Add an image (optional)
st.image("https://source.unsplash.com/800x400/?real-estate", use_column_width=True, caption="Accurate predictions powered by data science!")

# Add a footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p><strong>About this project:</strong> This app uses **machine learning models** to estimate property prices in Belgium.
        The predictions are based on key factors such as location, size, and amenities.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://www.github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
""", unsafe_allow_html=True)
