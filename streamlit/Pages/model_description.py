import streamlit as st
import os
import pandas as pd

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="📊 Model Description",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# 2. Define File Path Helper
# ==============================
def get_file_path(file_name):
    """
    Get the absolute file path for a given file name.
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(current_dir, "Plots", file_name)

scatter_plot_file = get_file_path("scatter_plot_properties_belgium.png")

# ==============================
# 3. Page Header
# ==============================
st.title("📊 Model Description")
st.markdown(
    """
    This page provides insights into the development of prediction models for apartments and houses in Belgium.
    """
)

# ==============================
# 6. Model Overview
# ==============================
st.markdown("---")
st.markdown("### 🤖 How the Models Work")
st.markdown(
    """
    The prediction models for apartments and houses leverage advanced machine learning techniques, particularly:
    - **XGBoost Regression** for efficient and accurate predictions.
    - **Log Transformation** on apartment prices to handle skewness.
    - **Feature Engineering**:
        - **Numerical Features**: Total area, bedrooms, construction year, latitude, longitude.
        - **Categorical Features**: State of the building, heating type, and province.
        - **Binary Features**: Terrace presence, double glazing, and flood zone status.
    - **Geospatial Features**: ZIP code-based latitude and longitude to capture regional price trends.

    #### 🛠️ Preprocessing Pipeline:
    - **Imputation**: Missing numerical and categorical values were filled using median and mode strategies.
    - **Scaling**: StandardScaler normalizes numerical data.
    - **Encoding**: Rare categories grouped into "Other"; one-hot encoding applied to categorical features.

    The final data is processed through an **XGBoost Regression Model**, optimized for performance and accuracy.
    """
)

# ==============================
# 4. Prediction Comparison Table
# ==============================
st.markdown("---")
st.markdown("### 🔍 Prediction Results: Sample Comparison")

# Define the comparison data
comparison_data = {
    "Actual Price (€)": [265000.0, 200000.0, 334900.0, 172000.0, 449000.0, 274000.0, 297500.0, 199000.0, 252000.0, 300000.0],
    "Predicted Price (€)": [326813.91, 226631.97, 355548.50, 214333.75, 345326.91, 258050.78, 350320.75, 186682.30, 253952.44, 348446.19],
    "Absolute Error (€)": [61813.91, 26631.97, 20648.50, 42333.75, 103673.09, 15949.22, 52820.75, 12317.70, 1952.44, 48446.19],
    "Percentage Error (%)": [23.33, 13.32, 6.17, 24.61, 23.09, 5.82, 17.75, 6.19, 0.77, 16.15],
}

# Display the comparison table
comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True)



# ==============================
# 7. Model Metrics
# ==============================
st.markdown("---")
st.markdown("### 📊 Model Performance Metrics")
st.markdown(
    """
    #### **Apartment Model:**
    - **R² Score**: 0.7078
    - **Mean Absolute Error (MAE)**: €38,692.80
    - **Median Absolute Error**: €25,947.45

    #### **House Model:**
    - **R² Score**: 0.7352
    - **Mean Absolute Error (MAE)**: €45,213.67
    - **Median Absolute Error**: €31,548.32
    """
)

# ==============================
# 5. Visualization: Scatter Plot
# ==============================
st.markdown("---")
st.markdown("### 🌍 Geographical Distribution of Properties used within the model")
if os.path.exists(scatter_plot_file):
    st.image(
        scatter_plot_file,
        caption="Geographical Distribution of Properties in Belgium",
        use_container_width=True,
    )
else:
    st.error("❌ Scatter plot image not found. Please ensure the file is located in the `Plots` directory.")



# ==============================
# 8. Footer
# ==============================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.9em; color: gray;">
        <p><strong>About this project:</strong> This app uses machine learning to predict property prices based on features like area, location, and amenities. 
        It is intended to help users estimate the value of properties in Belgium. 
        This app was developed during a one-week AI & Data Science course at BeCode, Ghent.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
