from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="PakWheels Price Prediction API")

try:
    artifact = joblib.load("pakwheels_svm_model.pkl")
    model = artifact["model"]
    scaler = artifact["scaler"]
    encoders = artifact["encoders"]
    features_list = artifact["features"]
    print("✅ Model artifact loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

class CarInput(BaseModel):
    year: int
    engine: float
    mileage: int
    transmission: str
    fuel: str
    body: str
    city: str

@app.get("/")
def home():
    return {"message": "Welcome to the PakWheels Price Category Predictor API"}

# 4. Define the Prediction Endpoint
@app.post("/predict")
def predict(car: CarInput):
    try:
        # Convert input to a dictionary
        input_data = car.dict()
        
        # Create a DataFrame for processing (must match training feature order)
        df_input = pd.DataFrame([input_data])
        
        #Apply the saved LabelEncoders to categorical columns
        categorical_cols = ['transmission', 'fuel', 'body', 'city']
        for col in categorical_cols:
            le = encoders[col]
            # Use .get() or handle unseen categories to prevent crashes
            val = input_data[col]
            if val in le.classes_:
                df_input[col] = le.transform([val])
            else:
                df_input[col] = le.transform([le.classes_[0]])

        # Scale the numerical features using the saved Scaler
        X_scaled = scaler.transform(df_input[features_list])
        
        prediction = model.predict(X_scaled)
        
        # 1 = High Price, 0 = Low Price
        result = "High Price" if prediction[0] == 1 else "Low Price"
        
        probabilities = model.predict_proba(X_scaled)
        confidence = np.max(probabilities)

        return {
            "prediction": result,
            "confidence": f"{confidence:.2%}",
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)