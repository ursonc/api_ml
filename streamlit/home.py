import streamlit as st

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="🏠 Property Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from pages import appartment_prediction, house_prediction, model_description

# ==============================
# 2. Sidebar Navigation
# ==============================
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio(
    "Go to",
    ["Home", "Apartment Prediction", "House Prediction", "Model Description"]
)

# ==============================
# 3. Page Content Logic
# ==============================
if selected_page == "Home":
    st.title("🏠 Welcome to Property Price Prediction")
    st.markdown(
        """
        Welcome to the **Property Price Prediction App**!  
        This app uses advanced **Machine Learning Models** to predict property prices for:
        - **Apartments**
        - **Houses**

        ### 🔍 How to Use:
        - Use the **Sidebar** on the left to navigate to:
            - **Apartment Price Prediction**
            - **House Price Prediction**
            - **Model Description**
        """
    )

elif selected_page == "Apartment Prediction":
    # Run the apartment prediction page
    appartment_prediction.run()

elif selected_page == "House Prediction":
    house_prediction.run()

elif selected_page == "Model Description":
    model_description.run()

# ==============================
# 4. Footer
# ==============================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p><strong>About this project:</strong> Developed as part of the **AI & Data Science Course** at BeCode, Ghent.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)
