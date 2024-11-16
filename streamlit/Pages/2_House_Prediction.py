import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="🏠 House Price Prediction in Belgium",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# 2. Load the Trained Model and Metrics
# ==============================
@st.cache_resource
def load_model_and_metrics(path):
    if not os.path.exists(path):
        st.error(f"❌ Model file not found at: {path}")
        st.stop()
    try:
        model_pipeline = joblib.load(path)
        # Model performance metrics (hardcoded for now)
        model_metrics = {
            "R_squared": 0.7352,
            "MAE": 45213.67,
            "Median_AE": 31548.32,
        }
        return model_pipeline, model_metrics
    except Exception as e:
        st.error(f"❌ An error occurred while loading the model: {e}")
        st.stop()

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "Trained_Models", "price_prediction_pipeline.joblib")
model_pipeline, model_metrics = load_model_and_metrics(model_path)

# ==============================
# 3. Load ZIP Code Reference Data
# ==============================
@st.cache_data
def load_zip_code_reference():
    try:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        zip_file_path = os.path.join(current_dir, "Trained_Models", "zipcode-belgium.json")
        if not os.path.exists(zip_file_path):
            raise FileNotFoundError(f"ZIP code file not found at: {zip_file_path}")
        with open(zip_file_path, "r") as f:
            zip_code_data = json.load(f)
        return {entry["zip"]: entry for entry in zip_code_data}
    except Exception as e:
        st.error(f"❌ Error loading ZIP code reference data: {e}")
        st.stop()

zip_code_mapping = load_zip_code_reference()

def get_zip_code_details(zip_code):
    details = zip_code_mapping.get(zip_code, {"city": "Unknown", "lat": 0, "lng": 0})
    return details["city"], details["lat"], details["lng"]

def get_province_from_zip(zip_code):
    try:
        zip_int = int(zip_code)
    except ValueError:
        return "Unknown"
    if 1000 <= zip_int <= 1299:
        return "Brussels Capital Region"
    elif 1300 <= zip_int <= 1499:
        return "Walloon Brabant"
    elif 1500 <= zip_int <= 1999 or 3000 <= zip_int <= 3499:
        return "Flemish Brabant"
    elif 2000 <= zip_int <= 2999:
        return "Antwerp"
    elif 3500 <= zip_int <= 3999:
        return "Limburg"
    elif 4000 <= zip_int <= 4999:
        return "Liège"
    elif 5000 <= zip_int <= 5999:
        return "Namur"
    elif 6000 <= zip_int <= 6599 or 7000 <= zip_int <= 7999:
        return "Hainaut"
    elif 6600 <= zip_int <= 6999:
        return "Luxembourg"
    elif 8000 <= zip_int <= 8999:
        return "West Flanders"
    elif 9000 <= zip_int <= 9992:
        return "East Flanders"
    else:
        return "Unknown"

# ==============================
# 4. User Input Form
# ==============================
st.title("🏠 House Price Prediction in Belgium")
st.write(
    "Welcome to the House Price Prediction page! Fill in the details below to get an estimated price for your house."
)

with st.form(key="prediction_form"):
    st.markdown("### Property Information")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        zip_code = st.text_input(
            "📍 ZIP Code", 
            "1000", 
            help="Enter the 4-digit Belgian ZIP Code of the house."
        )
        total_area_sqm = st.number_input(
            "📐 Total Area (sqm)", 
            min_value=10, 
            max_value=1000, 
            value=150, 
            step=1
        )
        nbr_bedrooms = st.number_input(
            "🛏️ Number of Bedrooms", 
            min_value=0, 
            max_value=10, 
            value=3, 
            step=1
        )

    with col2:
        construction_year = st.number_input(
            "🏗️ Construction Year", 
            min_value=1900, 
            max_value=2024, 
            value=2000, 
            step=1
        )
        state_building = st.selectbox(
            "🏢 State of Building", 
            options=["NEW", "GOOD", "JUST RENOVATED", "TO RENOVATE", "TO RESTORE", "OTHER"]
        )
        garden_sqm = st.number_input(
            "🌳 Garden Area (sqm)", 
            min_value=0, 
            max_value=2000, 
            value=50, 
            step=1
        )

    with col3:
        heating_type = st.selectbox(
            "🔥 Heating Type", 
            options=["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"]
        )

    submit_button = st.form_submit_button(label="🔍 Predict Price")

# ==============================
# 5. Process Form Submission and Make Predictions
# ==============================
if submit_button:
    zip_code = zip_code.strip()
    city_name, latitude, longitude = get_zip_code_details(zip_code)
    province = get_province_from_zip(zip_code)

    if city_name == "Unknown":
        st.error("❌ Invalid ZIP Code. Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        input_data = {
            "zip_code": zip_code,
            "province": province,
            "total_area_sqm": total_area_sqm,
            "nbr_bedrooms": nbr_bedrooms,
            "construction_year": construction_year,
            "state_building": state_building.upper(),
            "latitude": latitude,
            "longitude": longitude,
            "garden_sqm": garden_sqm,
            "heating_type": heating_type.upper(),
            "terrace_sqm": 0,
            "fl_terrace": 0,
            "fl_floodzone": 0,
        }

        input_df = pd.DataFrame([input_data])

        try:
            pred_price = model_pipeline.predict(input_df)

            st.success("🎉 Prediction successful!")
            st.subheader("💰 Predicted Price")
            st.write(f"The estimated price is: **€{pred_price[0]:,.2f}**")

            st.markdown("### 🌍 Property Location")
            st.write(f"- **City:** {city_name}")
            st.write(f"- **Province:** {province}")

            st.markdown("### 📊 Model Metrics")
            st.write(f"- **R²:** {model_metrics['R_squared']:.4f}")
            st.write(f"- **Mean Absolute Error (MAE):** €{model_metrics['MAE']:,.2f}")
            st.write(f"- **Median Absolute Error (Median AE):** €{model_metrics['Median_AE']:,.2f}")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ==============================
# 6. Add Footer with Project Information
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>About this project:</strong> This app uses machine learning to predict house prices based on various features like area, location, and amenities. 
        It is intended to help users estimate the value of properties in Belgium. 
        This app was made in the course of one week within my AI & Data Science course at BeCode, Ghent. </p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://www.github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
