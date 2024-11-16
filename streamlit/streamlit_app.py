import streamlit as st
import joblib
import pandas as pd
import numpy as np

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
def load_model_and_metrics(apartment_path, house_path):
    """
    Load the models for apartment and house price predictions.
    """
    try:
        apartment_model = joblib.load(apartment_path)
        house_model = joblib.load(house_path)
        apartment_metrics = {"R_squared": 0.7078, "MAE": 38692.80, "Median_AE": 25947.45}
        house_metrics = {"R_squared": 0.7352, "MAE": 45213.67, "Median_AE": 31548.32}
        return {
            "Apartment": (apartment_model, apartment_metrics),
            "House": (house_model, house_metrics)
        }
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()

models = load_model_and_metrics(
    apartment_path="streamlit/apartments_xgb_model_log.joblib",
    house_path="streamlit/houses_xgb_model.joblib"
)

# ==============================
# 3. Helper Function: ZIP Code to Province
# ==============================
def get_province_from_zip(zip_code):
    """
    Map ZIP code to the corresponding province and region.
    """
    try:
        zip_code = int(zip_code)
    except ValueError:
        return None, None

    if 1000 <= zip_code <= 1299:
        return "Brussels Capital Region", "Brussels"
    elif 1300 <= zip_code <= 1499:
        return "Walloon Brabant", "Wallonia"
    elif 1500 <= zip_code <= 1999 or 3000 <= zip_code <= 3499:
        return "Flemish Brabant", "Flanders"
    elif 2000 <= zip_code <= 2999:
        return "Antwerp", "Flanders"
    elif 3500 <= zip_code <= 3999:
        return "Limburg", "Flanders"
    elif 4000 <= zip_code <= 4999:
        return "Liège", "Wallonia"
    elif 5000 <= zip_code <= 5999:
        return "Namur", "Wallonia"
    elif 6000 <= zip_code <= 6599 or 7000 <= zip_code <= 7999:
        return "Hainaut", "Wallonia"
    elif 6600 <= zip_code <= 6999:
        return "Luxembourg", "Wallonia"
    elif 8000 <= zip_code <= 8999:
        return "West Flanders", "Flanders"
    elif 9000 <= zip_code <= 9992:
        return "East Flanders", "Flanders"
    else:
        return None, None

# ==============================
# 4. User Input Form
# ==============================
st.title("🏠 Property Price Prediction in Belgium")
property_type = st.selectbox("Choose Property Type", ["Apartment", "House"])

with st.form("prediction_form"):
    zip_code = st.text_input("📍 ZIP Code", "1000", help="Enter the 4-digit Belgian ZIP Code.")
    total_area_sqm = st.number_input("📐 Total Area (sqm)", min_value=10, max_value=1000, value=75, step=1)
    nbr_bedrooms = st.number_input("🛏️ Number of Bedrooms", min_value=0, max_value=10, value=2, step=1)
    construction_year = st.number_input("🏗️ Construction Year", min_value=1900, max_value=2024, value=2000, step=1)
    state_building = st.selectbox("🏢 State of Building", ["NEW", "GOOD", "JUST RENOVATED", "TO RENOVATE", "TO RESTORE", "OTHER"])

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
    province, region = get_province_from_zip(zip_code)

    if not province:
        st.error("❌ Invalid ZIP Code. Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        input_data = {
            "total_area_sqm": total_area_sqm,
            "construction_year": construction_year,
            "nbr_bedrooms": nbr_bedrooms,
            "state_building": state_building.upper(),
            "zip_code": zip_code,
            "province": province.upper(),
            "region": region.upper(),
        }

        if property_type == "Apartment":
            fl_furnished = 1 if fl_furnished == "Yes" else 0
            fl_double_glazing = 1 if fl_double_glazing == "Yes" else 0
            input_data.update({
                "terrace_sqm": terrace_sqm,
                "fl_furnished": fl_furnished,
                "fl_double_glazing": fl_double_glazing,
            })
        else:
            input_data["garden_sqm"] = garden_sqm

        model, metrics = models[property_type]
        input_df = pd.DataFrame([input_data])

        try:
            pred_log = model.predict(input_df)
            predicted_price = np.expm1(pred_log)[0]

            st.success(f"🎉 Predicted Price: **€{predicted_price:,.2f}**")
            st.write(f"**Model Performance:** R² = {metrics['R_squared']:.4f}, MAE = €{metrics['MAE']:,.2f}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
