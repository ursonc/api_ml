import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

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
def load_models_and_metrics():
    """
    Load trained models and metrics for both apartments and houses.
    """
    try:
        model_pipeline = joblib.load(path)
        model_metrics = {
            "R_squared": 0.7352,  # R-squared
            "MAE": 45213.67,      # Mean Absolute Error
            "Median_AE": 31548.32 # Median Absolute Error
        }
        return model_pipeline, model_metrics
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model_path = "streamlit/price_prediction_pipeline.joblib"
model_pipeline, model_metrics = load_model_and_metrics(model_path)

# ==============================
# 3. Load ZIP Code Reference Data
# ==============================
@st.cache_data
def load_zip_code_reference():
    try:
        with open("streamlit/zipcode-belgium.json", "r") as f:
            zip_code_data = json.load(f)
        return {entry["zip"]: entry for entry in zip_code_data}
    except FileNotFoundError as e:
        st.error(f"ZIP code reference file not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading ZIP code reference data: {e}")
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
st.title("🏠 House Price Prediction")
st.write(
    "Welcome! Fill in the details below to get an estimate of your house's price."
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
            "total_area_sqm": total_area_sqm,
            "nbr_bedrooms": nbr_bedrooms,
            "construction_year": construction_year,
            "state_building": state_building.upper(),
            "latitude": latitude,
            "longitude": longitude,
            "garden_sqm": garden_sqm,
            "heating_type": heating_type.upper(),
            "province": province,
            "fl_floodzone": 0  # Default value
        }

        input_df = pd.DataFrame([input_data])
        try:
            # Load the appropriate model and its metadata
            model, metrics, is_log_transformed = models[property_type]

            # Make prediction
            pred_price = model.predict(input_df)

            # Apply inverse log transformation if needed
            if is_log_transformed:
                pred_price = np.expm1(pred_price[0])
            else:
                pred_price = pred_price[0]

            # Display results
            st.success(f"🎉 Predicted Price: **€{pred_price:,.2f}**")
            st.write(f"**City Name:** {city_name}")
            st.write(f"**Province:** {province}")
            st.write(f"**Model Performance:** R² = {model_metrics['R_squared']:.4f}, MAE = €{model_metrics['MAE']:,.2f}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ==============================
# 6. Add Footer
# ==============================
st.markdown("""
    <div class="footer">
        <p><strong>About this project:</strong> Predict property prices in Belgium using machine learning. This app helps estimate house values based on ZIP code, area, and amenities.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a>.</p>
    </div>
""", unsafe_allow_html=True)