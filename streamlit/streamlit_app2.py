import streamlit as st
import joblib
import pandas as pd
import numpy as np

# ==============================
# 1. Set Page Configuration
# ==============================
st.set_page_config(
    page_title="🏠 Appartment Price Prediction in Belgium",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# 2. Load the Trained Model and Metrics with Caching
# ==============================
@st.cache_resource
def load_model_and_metrics(path):
    try:
        model_pipeline = joblib.load(path)
        # Model performance metrics
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
        st.error(f"An error occurred while loading the model: {e}")
        st.stop()

model_path = "streamlit/apartments_xgb_model_log.joblib"

# Load the model and metrics
model_pipeline, model_metrics = load_model_and_metrics(model_path)

# ==============================
# 3. Apply Custom CSS Styling
# ==============================
st.markdown("""
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
""", unsafe_allow_html=True)

# ==============================
# 4. App Title and Description
# ==============================
st.title("🏠 Appartment Price Prediction in Belgium")
st.write(
    "Welcome to the Appartment Price Prediction app! Fill in the details below to get an estimate of your appartments's price."
)

# Add a horizontal divider
st.markdown("---")

# ==============================
# 5. Define Helper Function to Map ZIP Code to Province
# ==============================
def get_province_from_zip_code(zip_code):
    try:
        zip_int = int(zip_code)
    except ValueError:
        return None  # Invalid ZIP code format

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
        return None  # ZIP code not recognized

# ==============================
# 6. Collect User Input via Streamlit Form
# ==============================
with st.form(key='prediction_form'):
    # Organize inputs in three columns for a compact layout
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        zip_code = st.text_input(
            "📍 ZIP Code",
            "1000",
            help="Enter the 4-digit Belgian ZIP Code of the appartment."
        )
        total_area_sqm = st.number_input(
            "📐 Total Area (sqm)",
            min_value=10,
            max_value=500,
            value=75,
            step=1,
            help="Enter the total area of the appartment in square meters."
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
            help="Enter the year the appartment was constructed."
        )
        state_building = st.selectbox(
            "🏢 State of Building",
            options=["NEW", "GOOD", "JUST RENOVATED", "TO RENOVATE", "TO RESTORE", "OTHER"],
            index=1,
            help="Select the current state of the building."
        )

    with col3:
        heating_type = st.selectbox(
            "🔥 Heating Type",
            options=["GAS", "ELECTRIC", "CENTRAL", "WOOD", "SOLAR", "OTHER"],
            index=0,
            help="Select the type of heating available."
        )
        fl_furnished_input = st.radio(
            "🛋️ Is the appartment furnished?",
            options=["Yes", "No"],
            index=1,
            horizontal=True,
            help="Indicate whether the appartment is furnished."
        )
        fl_double_glazing_input = st.radio(
            "🌞 Has Double Glazing?",
            options=["Yes", "No"],
            index=0,
            horizontal=True,
            help="Indicate whether the appartment has double glazing."
        )

    # Center the submit button using custom CSS
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label='🔍 Predict Price')
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 7. Process Form Submission and Make Predictions
# ==============================
if submit_button:
    # Validate ZIP code input
    zip_code = zip_code.strip()
    if not (zip_code.isdigit() and len(zip_code) == 4):
        st.error("❌ Please enter a valid 4-digit Belgian ZIP Code.")
    else:
        # Determine province based on ZIP code
        province = get_province_from_zip_code(zip_code)
        if province is None:
            st.error("❌ ZIP Code not recognized. Please enter a valid Belgian ZIP Code.")
        else:
            # Map "Yes"/"No" to 1/0 for binary features
            fl_furnished = 1 if fl_furnished_input == "Yes" else 0
            fl_double_glazing = 1 if fl_double_glazing_input == "Yes" else 0

            # Determine if there's a terrace based on terrace_sqm
            fl_terrace = 1 if terrace_sqm > 0 else 0

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
                # Make prediction using the loaded pipeline
                pred_log = model_pipeline.predict(input_df)
                predicted_price = np.expm1(pred_log)[0]  # Apply expm1 to get the original price

                # Display prediction with formatting
                st.success("🎉 **Prediction successful!**")
                st.subheader("💰 Predicted Price")
                st.write(f"The estimated price of the appartment is: **€{predicted_price:,.2f}**")

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
                st.error(f"❌ Prediction failed: {e}")
                st.write("Please check the input values and try again.")

# ==============================
# 8. Add Footer with Project Information
# ==============================
st.markdown(
    """
    <div class="footer">
        <p><strong>About this project:</strong> This app uses machine learning to predict appartment prices based on various features like area, location, and amenities. 
        It is intended to help users estimate the value of properties in Belgium. 
        This app was made in the course of one week within my AI & Data Science course at BeCode, Ghent. </p>
        <p>Developed by <a href="https://www.linkedin.com/in/ursoncallens" target="_blank">Urson Callens</a> | <a href="https://www.github.com/ursonc" target="_blank">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
