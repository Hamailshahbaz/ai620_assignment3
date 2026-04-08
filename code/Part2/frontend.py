import streamlit as st
import requests

st.set_page_config(page_title="PakWheels Price Predictor", page_icon="🚗")

st.title("PakWheels Price Category Predictor")
st.write("Enter the car details below to predict if it falls into a **High** or **Low** price category.")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Model Year", min_value=1980, max_value=2026, value=2018)
    engine = st.number_input("Engine Capacity (cc)", min_value=600, max_value=6000, step=100, value=1300)
    mileage = st.number_input("Mileage (km)", min_value=0, max_value=1000000, step=500, value=50000)

with col2:
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid"])
    body = st.selectbox("Body Type", ["Sedan", "Hatchback", "SUV", "Compact Sedan", "Van"])
    city = st.selectbox("City", ["Lahore", "Karachi", "Islamabad", "Rawalpindi", "Peshawar"])

if st.button("Predict Price Category"):
    payload = {
        "year": int(year),
        "engine": float(engine),
        "mileage": int(mileage),
        "transmission": transmission,
        "fuel": fuel,
        "body": body,
        "city": city
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            confidence = result.get("confidence", "N/A")

            # 3. Display the result
            st.divider()
            if prediction == "High Price":
                st.success(f"### Result: {prediction}")
            else:
                st.info(f"### Result: {prediction}")
            
            st.write(f"**Confidence Level:** {confidence}")
        else:
            st.error(f"Error: {response.json().get('detail', 'The API returned an error.')}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Connection Refused! Is your FastAPI server running at http://127.0.0.1:8000?")
