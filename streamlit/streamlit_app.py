import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load the trained model pipeline
try:
    model_pipeline = joblib.load(r"C:\Users\Becode-son\Desktop\API-ML\streamlit\apartments_xgb_model_log.joblib")
except FileNotFoundError:
    st.error("Model file not found. Please ensure the model file is in the correct path.")
    st.stop()

# Function to determine province from zip code
def get_province_from_zip_code(zip_code):
    try:
        # Convert zip_code to integer for range comparison
        zip_int = int(zip_code)
    except ValueError:
        return None  # Invalid zip code format

    if 1000 <= zip_int <= 1299:
        return "Brussels Capital Region"
    elif 1300 <= zip_int <= 1499:
        return "Walloon Brabant"
    elif (1500 <= zip_int <= 1999) or (3000 <= zip_int <= 3499):
        return "Flemish Brabant"
    elif 2000 <= zip_int <= 2999:
        return "Antwerp"
    elif 3500 <= zip_int <= 3999:
        return "Limburg"
    elif 4000 <= zip_int <= 4999:
        return "Liège"
    elif 5000 <= zip_int <= 5999:
        return "Namur"
    elif (6000 <= zip_int <= 6599) or (7000 <= zip_int <= 7999):
        return "Hainaut"
    elif 6600 <= zip_int <= 6999:
        return "Luxembourg"
    elif 8000 <= zip_int <= 8999:
        return "West Flanders"
    elif 9000 <= zip_int <= 9999:
        return "East Flanders"
    else:
        return None  # Zip code not recognized

# Title and description
st.title("Apartment Price Prediction")
st.write("This application predicts apartment prices based on several input features.")

# Collect user input within a form
with st.form(key='prediction_form'):
    total_area_sqm = st.number_input(
        "Total Area (sqm)",
        min_value=10,
        max_value=500,
        value=75,
        step=1,
        format="%d"
    )
    construction_year = st.number_input(
        "Construction Year",
        min_value=1900,
        max_value=2024,
        value=2000,
        step=1,
        format="%d"
    )
    nbr_bedrooms = st.number_input(
        "Number of Bedrooms",
        min_value=0,
        max_value=10,
        value=2,
        step=1,
        format="%d"
    )
    terrace_sqm = st.number_input(
        "Terrace Area (sqm)",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        format="%d"
    )
    state_building = st.selectbox(
        "State of Building",
        options=["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO RESTORE", "OTHER"],
        index=1
    )
    # zip_code is collected as a string
    zip_code = st.text_input("ZIP Code", "1000")
    heating_type = st.selectbox(
        "Heating Type",
        options=["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"],
        index=0
    )
    # Use "Yes"/"No" options for boolean inputs
    fl_furnished_input = st.radio("Is Furnished?", options=["Yes", "No"], index=1)
    fl_double_glazing_input = st.radio("Has Double Glazing?", options=["Yes", "No"], index=0)

    # Submit button
    submit_button = st.form_submit_button(label='Predict')

if submit_button:
    # Input validation
    zip_code = zip_code.strip()
    if not zip_code.isdigit():
        st.error("Please enter a valid ZIP Code consisting of digits only.")
    else:
        province = get_province_from_zip_code(zip_code)
        if province is None:
            st.error("ZIP Code not recognized. Please enter a valid Belgian ZIP Code.")
        else:
            st.success(f"Province determined from ZIP Code: {province}")

            # Determine fl_terrace based on terrace_sqm
            fl_terrace = 1 if int(terrace_sqm) > 0 else 0

            # Map "Yes"/"No" to 1/0 for fl_furnished and fl_double_glazing
            fl_furnished = 1 if fl_furnished_input == "Yes" else 0
            fl_double_glazing = 1 if fl_double_glazing_input == "Yes" else 0

            # Prepare input data
            data = {
                "total_area_sqm": int(total_area_sqm),
                "construction_year": int(construction_year),
                "nbr_bedrooms": int(nbr_bedrooms),
                "terrace_sqm": int(terrace_sqm),
                "state_building": state_building.upper(),
                "zip_code": zip_code,  # Keep zip_code as a string
                "province": province.upper(),
                "heating_type": heating_type.upper(),
                "fl_furnished": fl_furnished,
                "fl_terrace": fl_terrace,
                "fl_double_glazing": fl_double_glazing
            }

            input_data = pd.DataFrame([data])

            try:
                # Make prediction using the loaded pipeline
                pred_log = model_pipeline.predict(input_data)
                predicted_price = np.expm1(pred_log)[0]  # Apply expm1 to get the original price

                # Display prediction
                st.success("Prediction successful!")
                st.subheader("Predicted Price")
                st.write(f"The predicted price of the apartment is: **€{predicted_price:,.2f}**")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                st.write("Please check the input values and try again.")
