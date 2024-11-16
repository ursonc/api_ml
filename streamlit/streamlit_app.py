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

    zip_to_province_region = {
        range(1000, 1300): ("Brussels Capital Region", "Brussels"),
        range(1300, 1500): ("Walloon Brabant", "Wallonia"),
        range(1500, 2000): ("Flemish Brabant", "Flanders"),
        range(2000, 3000): ("Antwerp", "Flanders"),
        range(3000, 3500): ("Flemish Brabant", "Flanders"),
        range(3500, 4000): ("Limburg", "Flanders"),
        range(4000, 5000): ("Liège", "Wallonia"),
        range(5000, 6000): ("Namur", "Wallonia"),
        range(6000, 6600): ("Hainaut", "Wallonia"),
        range(6600, 7000): ("Luxembourg", "Wallonia"),
        range(7000, 8000): ("Hainaut", "Wallonia"),
        range(8000, 9000): ("West Flanders", "Flanders"),
        range(9000, 9993): ("East Flanders", "Flanders"),
    }

    for zip_range, (province, region) in zip_to_province_region.items():
        if zip_code in zip_range:
            return province, region
    return None, None


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
            input_data.update({
                "terrace_sqm": terrace_sqm,
                "fl_furnished": 1 if fl_furnished == "Yes" else 0,
                "fl_double_glazing": 1 if fl_double_glazing == "Yes" else 0,
            })
        else:
            input_data["garden_sqm"] = garden_sqm

        model, metrics = models[property_type]
        input_df = pd.DataFrame([input_data])

        try:
            with st.spinner("Predicting price..."):
                pred_log = model.predict(input_df)
                predicted_price = np.expm1(pred_log)[0]

            st.success(f"🎉 Predicted Price: **€{predicted_price:,.2f}**")
            st.write(f"**Model Performance:** R² = {metrics['R_squared']:.4f}, MAE = €{metrics['MAE']:,.2f}")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ==============================
# 6. Footer
# ==============================
st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <p><strong>About this project:</strong> Predict property prices in Belgium using machine learning. Developed for educational purposes at <strong>BeCode</strong>.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a>.</p>
    </div>
""", unsafe_allow_html=True)
