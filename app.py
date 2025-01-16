import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load dataset (for options)
data = pd.read_csv('bmw.csv')

# Check if model exists, if not train and save it
try:
    pipeline = joblib.load('car_price_model.pkl')
except FileNotFoundError:
    # Features and target
    X = data[['model', 'year', 'transmission', 'mileage', 'fuelType']]
    y = data['price']

    # Preprocessing for categorical data
    categorical_features = ['model', 'transmission', 'fuelType']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'  # Keep numerical features as is
    )

    # Define the model
    model = RandomForestRegressor(random_state=42, n_estimators=100)

    # Create pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])

    # Train the model
    pipeline.fit(X, y)

    # Save the trained model
    joblib.dump(pipeline, 'car_price_model.pkl')

# Streamlit App
def main():
    st.title("Car Price Prediction App")

    st.sidebar.header("Input Car Details")

    # User Inputs
    model_input = st.sidebar.selectbox('Model', options=data['model'].unique())
    year_input = st.sidebar.number_input('Year', min_value=1990, max_value=2023, step=1, value=2015)
    transmission_input = st.sidebar.selectbox('Transmission', options=data['transmission'].unique())
    mileage_input = st.sidebar.number_input('Mileage', min_value=0, step=1, value=50000)
    fuel_type_input = st.sidebar.selectbox('Fuel Type', options=data['fuelType'].unique())

    # Submit Button
    if st.sidebar.button('Submit'):
        # Prepare input for prediction
        input_data = pd.DataFrame({
            'model': [model_input],
            'year': [year_input],
            'transmission': [transmission_input],
            'mileage': [mileage_input],
            'fuelType': [fuel_type_input]
        })

        # Prediction
        prediction = pipeline.predict(input_data)
        st.write(f"### Predicted Price: £{prediction[0]:,.2f}")

if __name__ == "_main_":
    main()