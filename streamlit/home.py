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

# ==============================
# 2. App Title and Description
# ==============================
st.title("🏠 Price Prediction for Houses and Appartments in Belgium")
st.markdown(
    """
    Welcome to the **Price Prediction App**!  
    This app uses advanced **Machine Learning Models** to predict property prices for:
    - **Appartments**
    - **Houses**

    ### 🔍 How to Use:
    - Use the **Sidebar** on the left to navigate to:
        - **Appartment Price Prediction**
        - **House Price Prediction**
        - **Model Description**
    """
)

# ==============================
# 3. Visual Highlights (Optional)
# ==============================
st.markdown("---")
st.markdown("### 📊 **Quick Insights**")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="🏢 Appartment Model Accuracy (R²)", value="70.78%", delta="Based on MAE: €38,692.80")
    st.metric(label="🏢 Median Absolute Error (Median AE)", value="€25,947.45")

with col2:
    st.metric(label="🏡 House Model Accuracy (R²)", value="73.52%", delta="Based on MAE: €45,213.67")
    st.metric(label="🏡 Median Absolute Error (Median AE)", value="€31,548.32")

# ==============================
# 4. Add a Footer
# ==============================
st.markdown("---")
st.markdown(
    """
    ---
    <div style="text-align: center;">
        <p><strong>About this project:</strong> Developed as part of the **AI & Data Science Course** at BeCode, Ghent.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)
