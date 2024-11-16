import streamlit as st
import joblib
import pandas as pd
import numpy as np
import json

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="🏠 Property Price Prediction in Belgium",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# 2. Load Models and Metrics
# ==============================
@st.cache_resource
def load_models_and_metrics():
    """
    Load models and their performance metrics dynamically.
    """
    try:
        apartment_model = joblib.load("streamlit/apartments_xgb_model_log.joblib")
        house_model = joblib.load("streamlit/price_prediction_pipeline.joblib")

        apartment_metrics = {"R_squared": 0.7078, "MAE": 38692.80, "Median_AE": 25947.45}
        house_metrics = {"R_squared": 0.7352, "MAE": 45213.67, "Median_AE": 31548.32}

        return {
            "Apartment": (apartment_model, apartment_metrics),
            "House": (house_model, house_metrics),
        }
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()


models = load_models_and_metrics()

# ==============================
# 3. Load ZIP Code Reference Data
# ==============================
@st.cache_data
def load_zip_code_reference():
    """
    Load reference data containing latitude, longitude, and city names for each ZIP code from JSON.
    """
    try:
        with open("streamlit/zipcode-belgium.json", "r") as f:
            zip_code_data = json.load(f)
        return {entry["zip"]: {"city": entry["city"], "latitude": entry["lat"], "longitude": entry["lng"]} for entry in zip_code_data}
    except FileNotFoundError as e:
        st.error(f"ZIP code reference file not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading ZIP code reference data: {e}")
        st.stop()


zip_code_mapping = load_zip_code_reference()

def get_zip_code_details(zip_code):
    """
    Retrieve city name, latitude, and longitude for a given ZIP code.
    """
    zip_code = str(zip_code)
    if zip_code in zip_code_mapping:
        details = zip_code_mapping[zip_code]
        return details["city"], details["latitude"], details["longitude"]
    return "Unknown", 0, 0  # Default values for missing zip_code

def get_province_from_zip(zip_code):
    """
    Map ZIP code to the corresponding province.
    """
    # Add mapping logic based on your ZIP code to province data
    province_mapping = {
        "1000": "Brussels Capital Region",
        # Add more mappings as needed
    }
    return province_mapping.get(zip_code, "Unknown")


# ==============================
# 4. User Input Form
# ==============================
st.title("🏠 Property Price Prediction in Belgium")
property_type = st.selectbox("Choose Property Type", ["Apartment", "House"])

with st.form("prediction_form"):
    zip_code = st.text_input("📍 ZIP Code", "", placeholder="Enter a 4-digit ZIP code (e.g., 1000)")
    total_area_sqm = st.number_input("📐 Total Area (sqm)", min_value=10, max_value=1000, value=75, step=1)
    nbr_bedrooms = st.number_input("🛏️ Number of Bedrooms", min_value=0, max_value=10, value=2, step=1)
    construction_year = st.number_input("🏗️ Construction Year", min_value=1900, max_value=2024, value=2000, step=1)
    state_building = st.selectbox("🏢 State of Building", ["NEW", "GOOD", "JUST RENOVATED", "TO RENOVATE", "TO RESTORE", "OTHER"])
    heating_type = st.selectbox(
        "🔥 Heating Type",
        options=["GAS", "ELECTRIC", "WOOD", "SOLAR", "CENTRAL", "OTHER"],
        index=0,
        help="Select the type of heating available for the property."
    )

    # Dynamically adjust inputs based on property type
    if property_type == "Apartment":
        terrace_sqm = st.number_input("🏞️ Terrace Area (sqm)", min_value=0, max_value=100, value=0, step=1)
        fl_furnished = st.radio("🛋️ Furnished?", ["Yes", "No"], index=1)
        fl_double_glazing = st.radio("🌞 Double Glazing?", ["Yes", "No"], index=0)
    else:
        garden_sqm = st.number_input("🌳 Garden Area (sqm)", min_value=0, max_value=2000, value=0, step=1)

    submit_button = st.form_submit_button("🔍 Predict Price")

# ==============================
# 5. Process Submission
# ==============================
if submit_button:
    zip_code = zip_code.strip()
    city_name, latitude, longitude = get_zip_code_details(zip_code)
    province = get_province_from_zip(zip_code)

    if city_name == "Unknown":
        st.error("❌ Invalid ZIP Code. Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        # Prepare input data dynamically with city_name, latitude, and longitude
        input_data = {
            "total_area_sqm": total_area_sqm,
            "construction_year": construction_year,
            "nbr_bedrooms": nbr_bedrooms,
            "state_building": state_building.upper(),
            "zip_code": zip_code,
            "city_name": city_name,
            "latitude": latitude,
            "longitude": longitude,
            "heating_type": heating_type.upper(),
            "province": province,
            "fl_floodzone": 0,  # Default value
        }

        # Add terrace and garden-related features
        if property_type == "Apartment":
            fl_terrace = 1 if terrace_sqm > 0 else 0
            input_data.update({
                "terrace_sqm": terrace_sqm,
                "fl_furnished": 1 if fl_furnished == "Yes" else 0,
                "fl_double_glazing": 1 if fl_double_glazing == "Yes" else 0,
                "fl_terrace": fl_terrace,
            })
        else:
            fl_terrace = 0
            input_data.update({
                "garden_sqm": garden_sqm,
                "fl_terrace": fl_terrace,
            })

        model, metrics = models[property_type]
        input_df = pd.DataFrame([input_data])

        try:
            with st.spinner("Predicting price..."):
                pred_log = model.predict(input_df)
                predicted_price = np.expm1(pred_log)[0]

            st.success(f"🎉 Predicted Price: **€{predicted_price:,.2f}**")
            st.write(f"**Model Performance:** R² = {metrics['R_squared']:.4f}, MAE = €{metrics['MAE']:,.2f}")
            st.write(f"**City Name:** {city_name}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ==============================
# 6. Footer
# ==============================
# ==============================
# 8. Add Footer with Project Information
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>About this project:</strong> This app uses machine learning to predict property prices based on various features like area, location, and amenities. 
        It is intended to help users estimate the value of houses and appartments in Belgium. 
        This app was made in the course of one week within my AI & Data Science course at BeCode, Ghent. </p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://www.github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
