import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load the trained model pipeline
try:
    model_pipeline = joblib.load("apartments_xgb_model_log.joblib")
except FileNotFoundError:
    st.error("Model file not found. Please ensure the model file is in the correct path.")
    st.stop()
=======
<<<<<<< HEAD
# Set page configuration
st.set_page_config(
    page_title="Apartment Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)
=======
# Define the model path
model_path = "streamlit/appartments_xgb_model_log.joblib"
>>>>>>> c86494f54c5d83b90b5b3011b7e11d64799ae109

# Load the model with caching
@st.cache_resource  # Cache the model loading to avoid reloading on each rerun
def load_model(path):
    try:
        model = joblib.load(path)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {path}. Please ensure the model file is in the correct path.")
        st.stop()

# Use the model
model = load_model(model_path)


# CSS to make the form more compact
st.markdown("""
    <style>
        .css-1aumxhk { padding-top: 1rem; }
        .css-1lsmgbg { padding-top: 1rem; padding-bottom: 1rem; }
        .css-17lntkn {
            font-size: 0.85rem;
            padding: 5px 10px;
        }
        .css-1dq8tca, .css-12oz5g7 {
            font-size: 0.85rem;
            padding: 5px;
        }
        .css-1djdy6k {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)
>>>>>>> de17b805c9995f4548974f7d1e9446034825f690

# Load the trained model pipeline and metrics
@st.cache_data
def load_model_and_metrics():
    try:
<<<<<<< HEAD
        model_pipeline = joblib.load("apartments_xgb_model_log.joblib")
        # Updated model performance metrics with your provided values
        model_metrics = {
            "R_squared": 0.7078,   # R-squared 
            "MAE": 38692.80,       # Mean Absolute Error 
            "Median_AE": 25947.45, # Median Absolute Error 
       
        }
        return model_pipeline, model_metrics
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

# Load the model and metrics
model_pipeline, model_metrics = load_model_and_metrics()

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Main layout */
    .main {
        background-color: #f7f7f7;
    }
    /* Header */
    header, .st-bx {
        background-color: #333333;
        color: white;
    }
    /* Button styling */
    .stButton>button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 0.5em 1em;
        font-size: 1em;
        border-radius: 0.25em;
        cursor: pointer;
    }
    /* Button hover effect */
    .stButton>button:hover {
        background-color: #218838;
    }
    /* Footer styling */
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
    /* Remove whitespace at the top */
    .block-container {
        padding-top: 1rem;
    }
    /* Input labels */
    label {
        font-weight: bold;
    }
    /* Center content */
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🏠 Apartment Price Prediction")
st.write(
    "Welcome to the Apartment Price Prediction app! Fill in the details below to get an estimate of your apartment's price."
)

# Add a divider
st.markdown("---")
=======
        zip_int = int(zip_code)
    except ValueError:
        return None

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
        return None

# Title and description
st.title("🏠 Apartment Price Prediction in Belgium")
st.write("Predict the price of an apartment based on its features.")
>>>>>>> de17b805c9995f4548974f7d1e9446034825f690

# Collect user input in a compact two-column layout
with st.form(key='prediction_form'):
<<<<<<< HEAD
    # Organize inputs in columns
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        zip_code = st.text_input(
            "📍 ZIP Code",
            "1000",
            help="Enter the ZIP Code of the apartment."
        )
        total_area_sqm = st.number_input(
            "📐 Total Area (sqm)",
            min_value=10,
            max_value=500,
            value=75,
            step=1,
            help="Enter the total area of the apartment in square meters."
        )
        nbr_bedrooms = st.number_input(
            "🛏️ Number of Bedrooms",
            min_value=0,
            max_value=10,
            value=2,
            step=1,
            help="Enter the number of bedrooms."
        )

    with col2:
        terrace_sqm = st.number_input(
            "🏞️ Terrace Area (sqm)",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
            help="Enter the terrace area in square meters (if any)."
        )
        construction_year = st.number_input(
            "🏗️ Construction Year",
            min_value=1900,
            max_value=2024,
            value=2000,
            step=1,
            help="Enter the year the apartment was constructed."
        )
        state_building = st.selectbox(
            "🏢 State of Building",
            options=["NEW", "GOOD", "JUST RENOVATED", "TO RENOVATE", "TO RESTORE", "OTHER"],
            index=1
        )

    with col3:
        heating_type = st.selectbox(
            "🔥 Heating Type",
            options=["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"],
            index=0
        )
        fl_furnished_input = st.radio(
            "🛋️ Is the apartment furnished?",
            options=["Yes", "No"],
            index=1,
            horizontal=True
        )
        fl_double_glazing_input = st.radio(
            "🌞 Has Double Glazing?",
            options=["Yes", "No"],
            index=0,
            horizontal=True
        )

    # Center the submit button
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label='🔍 Predict Price')
    st.markdown("</div>", unsafe_allow_html=True)
=======
    col1, col2 = st.columns(2)

    with col1:
        total_area_sqm = st.number_input("**Total Area (sqm)**", min_value=10, max_value=500, value=75, step=1)
        construction_year = st.number_input("**Construction Year**", min_value=1900, max_value=2024, value=2000, step=1)
        nbr_bedrooms = st.number_input("**Number of Bedrooms**", min_value=0, max_value=6, value=2, step=1)
        terrace_sqm = st.number_input("**Terrace Area (sqm)**", min_value=0, max_value=100, value=0, step=1)
>>>>>>> de17b805c9995f4548974f7d1e9446034825f690

    with col2:
        state_building = st.selectbox("**State of the Building**", ["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO RESTORE", "OTHER"], index=1)
        zip_code = st.text_input("**ZIP Code**", "9000")
        heating_type = st.selectbox("**Heating Type**", ["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"], index=0)
        fl_furnished_input = st.radio("**Is Furnished?**", ["Yes", "No"], index=1, horizontal=True)
        fl_double_glazing_input = st.radio("**Double Glazing?**", ["Yes", "No"], index=0, horizontal=True)

    submit_button = st.form_submit_button(label='🚀 Predict')

# Process submission
if submit_button:
    # Validate ZIP code input
    zip_code = zip_code.strip()
    if not (zip_code.isdigit() and len(zip_code) == 4):
        st.error("Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        # Function to determine province from zip code
        def get_province_from_zip_code(zip_code):
            try:
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

        province = get_province_from_zip_code(zip_code)
        if province is None:
            st.error("ZIP Code not recognized. Please enter a valid Belgian ZIP Code.")
        else:
<<<<<<< HEAD
            # Determine fl_terrace based on terrace_sqm
            fl_terrace = 1 if terrace_sqm > 0 else 0

            # Map "Yes"/"No" to 1/0 for fl_furnished and fl_double_glazing
=======
            st.success(f"**Province determined from ZIP Code**: {province}")

            # Prepare binary flags and input data for prediction
            fl_terrace = 1 if int(terrace_sqm) > 0 else 0
>>>>>>> de17b805c9995f4548974f7d1e9446034825f690
            fl_furnished = 1 if fl_furnished_input == "Yes" else 0
            fl_double_glazing = 1 if fl_double_glazing_input == "Yes" else 0

            # Prepare the input data dictionary
            data = {
                "total_area_sqm": total_area_sqm,
                "construction_year": construction_year,
                "nbr_bedrooms": nbr_bedrooms,
                "terrace_sqm": terrace_sqm,
                "state_building": state_building.upper(),
                "zip_code": zip_code,
                "province": province.upper(),
                "heating_type": heating_type.upper(),
                "fl_furnished": fl_furnished,
                "fl_terrace": fl_terrace,
                "fl_double_glazing": fl_double_glazing
            }

            # Convert data to DataFrame for prediction
            input_df = pd.DataFrame([data])

            # Make prediction and convert back from log scale to EUR
            try:
<<<<<<< HEAD
                # Make prediction using the loaded pipeline
                pred_log = model_pipeline.predict(input_data)
                predicted_price = np.expm1(pred_log)[0]  # Apply expm1 to get the original price

                # Display prediction with formatting
                st.success("🎉 **Prediction successful!**")
                st.subheader("💰 Predicted Price")
                st.write(f"The estimated price of the apartment is: **€{predicted_price:,.2f}**")

                # Add model performance metrics
                st.markdown("### 📊 Model Performance Metrics")
                st.write(f"- **R² Score:** {model_metrics['R_squared']:.4f}")
                st.write(f"- **Mean Absolute Error (MAE):** €{model_metrics['MAE']:,.2f}")
                st.write(f"- **Median Absolute Error:** €{model_metrics['Median_AE']:,.2f}")

                # Add model explanation
                st.markdown("### 🤖 About the Model")
                st.write("""
                    This prediction is made using an **XGBoost** regression model. During the model selection process, 
                    multiple algorithms were evaluated, including Linear Regression, Random Forest, and XGBoost. The 
                    **XGBoost model delivered the best results**, achieving higher accuracy and better performance metrics 
                    compared to the others. XGBoost (Extreme Gradient Boosting) is an advanced implementation of gradient 
                    boosting that is optimized for speed and performance, making it a popular choice for machine learning 
                    tasks involving structured data.
                """)
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                st.write("Please check the input values and try again.")

# Footer
st.markdown(
    """
    <div class="footer">
        <p><strong>About this project:</strong> This app uses machine learning to predict apartment prices based on various features like area, location, and amenities. It is intended to help users estimate the value of properties in Belgium.</p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="www.github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
=======
                log_prediction = model_pipeline.predict(input_df)  # Prediction in log scale
                prediction = np.exp(log_prediction)  # Convert back to EUR scale
                st.success(f"💸 **Predicted Apartment Price**: €{prediction[0]:,.2f}")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
