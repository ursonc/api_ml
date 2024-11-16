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
    Load reference data containing city names, latitude, and longitude for each ZIP code from JSON.
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

# ==============================
# 4. Apply Custom CSS Styling
# ==============================
st.markdown("""
    <style>
        .main {
            background-color: #f7f7f7;
        }
        header, .st-bx {
            background-color: #333333;
            color: white;
        }
        .stButton>button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 0.5em 1em;
            font-size: 1em;
            border-radius: 0.25em;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #218838;
        }
        .footer {
            background-color: #333333;
            color: white;
            text-align: center;
            padding: 1em 0;
            margin-top: 2em;
        }
        .footer a {
            color: #ffc107;
            text-decoration: none;
            font-weight: bold;
        }
        .footer a:hover {
            color: #ffca2c;
        }
        .block-container {
            padding-top: 1rem;
        }
        label {
            font-weight: bold;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# 5. Collect User Input via Streamlit Form
# ==============================
st.title("🏠 Property Price Prediction in Belgium")
st.write(
    "Welcome! Choose the property type and fill in the details below to get an estimate of your property's price."
)

property_type = st.selectbox("Choose Property Type", ["Apartment", "House"])

# Organize the layout into clear sections
with st.form(key='prediction_form'):
    st.markdown("### Property Information")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        zip_code = st.text_input(
            "📍 ZIP Code",
            "1000",
            help="Enter the 4-digit Belgian ZIP Code of the property."
        )
        total_area_sqm = st.number_input(
            "📐 Total Area (sqm)",
            min_value=10,
            max_value=1000,
            value=75,
            step=1
        )
        nbr_bedrooms = st.number_input(
            "🛏️ Number of Bedrooms",
            min_value=0,
            max_value=10,
            value=2,
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
        if property_type == "Apartment":
            terrace_sqm = st.number_input(
                "🏞️ Terrace Area (sqm)",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )
        else:
            garden_sqm = st.number_input(
                "🌳 Garden Area (sqm)",
                min_value=0,
                max_value=2000,
                value=0,
                step=1
            )

    with col3:
        heating_type = st.selectbox(
            "🔥 Heating Type",
            options=["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"]
        )
        if property_type == "Apartment":
            fl_furnished = st.radio("🛋️ Furnished?", ["Yes", "No"], index=1, horizontal=True)
            fl_double_glazing = st.radio("🌞 Double Glazing?", ["Yes", "No"], index=0, horizontal=True)

    st.markdown("---")

    submit_button = st.form_submit_button(label="🔍 Predict Price")

# ==============================
# 6. Process Submission and Make Predictions
# ==============================
if submit_button:
    zip_code = zip_code.strip()
    city_name, latitude, longitude = get_zip_code_details(zip_code)

    if city_name == "Unknown":
        st.error("❌ Invalid ZIP Code. Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        fl_terrace = 1 if property_type == "Apartment" and terrace_sqm > 0 else 0
        input_data = {
            "zip_code": zip_code,
            "total_area_sqm": total_area_sqm,
            "nbr_bedrooms": nbr_bedrooms,
            "construction_year": construction_year,
            "state_building": state_building.upper(),
            "heating_type": heating_type.upper(),
            "latitude": latitude,
            "longitude": longitude,
            "city_name": city_name,
            "terrace_sqm": terrace_sqm if property_type == "Apartment" else 0,
            "garden_sqm": garden_sqm if property_type == "House" else 0,
            "fl_furnished": 1 if property_type == "Apartment" and fl_furnished == "Yes" else 0,
            "fl_double_glazing": 1 if property_type == "Apartment" and fl_double_glazing == "Yes" else 0,
            "fl_terrace": fl_terrace
        }

        model, metrics = models[property_type]
        input_df = pd.DataFrame([input_data])

        try:
            pred_log = model.predict(input_df)
            predicted_price = np.expm1(pred_log)[0]
            st.success(f"🎉 Predicted Price: **€{predicted_price:,.2f}**")
            st.write(f"**City Name:** {city_name}")
            st.write(f"**Model Performance:** R² = {metrics['R_squared']:.4f}, MAE = €{metrics['MAE']:,.2f}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ==============================
# 7. Footer
# ==============================
st.markdown("""
    <div class="footer">
        <p><strong>About this project:</strong> Predict property prices in Belgium using machine learning. Developed at <strong>BeCode</strong>.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a>.</p>
    </div>
""", unsafe_allow_html=True)
