# api/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from predict import predict

app = FastAPI()

# Function to determine province from zip code
def get_province_from_zip_code(zip_code):
    try:
        zip_int = int(zip_code)
    except ValueError:
        return None  # Invalid zip code format

    if 1000 <= zip_int <= 1299:
        return "Brussels"
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
    elif 6000 <= zip_int <= 6599 or 7000 <= zip_int <= 7999:
        return "Hainaut"
    elif 6600 <= zip_int <= 6999:
        return "Luxembourg"
    elif 8000 <= zip_int <= 8999:
        return "West Flanders"
    elif 9000 <= zip_int <= 9999:
        return "East Flanders"
    else:
        return None

# Define the input data model
class PropertyData(BaseModel):
    total_area_sqm: float = Field(..., example=75.0)
    construction_year: int = Field(..., example=2000)
    nbr_bedrooms: int = Field(..., example=2)
    terrace_sqm: float = Field(..., example=10.0)
    state_building: str = Field(..., example="Good")
    zip_code: str = Field(..., example="1000")
    heating_type: str = Field(..., example="Gas")
    fl_furnished: int = Field(..., example=0)
    fl_terrace: int = Field(..., example=1)
    fl_double_glazing: int = Field(..., example=1)

@app.get("/")
def read_root():
    return {"message": "API is alive"}

@app.post("/predict/")
def make_prediction(data: PropertyData):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # Map zip_code to province
        province = get_province_from_zip_code(data.zip_code)
        if province is None:
            raise HTTPException(status_code=400, detail="Invalid zip code provided.")
        input_df['province'] = province

        # Preprocess input data if necessary
        input_df = preprocess_input_data(input_df)

        # Make prediction
        predicted_price = predict(input_df)

        return {"prediction": predicted_price}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Preprocessing function (if necessary)
def preprocess_input_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert categorical variables to match training
    df['state_building'] = df['state_building'].str.upper()
    df['heating_type'] = df['heating_type'].str.upper()
    df['province'] = df['province'].str.upper()

    # Handle any other preprocessing steps required
    # ...

    return df
