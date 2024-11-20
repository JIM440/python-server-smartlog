from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import random
import pickle
import json
import datetime

app = FastAPI()

# Define the input schema
class FuelRequest(BaseModel):
    distance: float
    consommation_100km: float

# Function from your code
def fuel_consumption(distance, consommation_100km):
    alert = ""

    # Random fuel level in the tank
    a = 0
    b = 60
    valeur_flot = round(random.uniform(a, b), 2)

    # Load the prediction model
    try:
        with open('carburant.pickle', 'rb') as fichier:
            loaded_model = pickle.load(fichier)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error: 'carburant.pickle' file not found!")
    except pickle.UnpicklingError:
        raise HTTPException(status_code=500, detail="Error: Unable to load the model file!")

    # Predict fuel consumption
    données = np.array([[distance, consommation_100km]])
    try:
        prediction = loaded_model.predict(données)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

    # Generate alert
    if prediction[0] < valeur_flot:
        alert = f"Les {valeur_flot} Litres présents dans le reservoir sont suffisants pour parcourir cette distance!"
    else:
        alert = f"!!!URGENT!!! \nBien vouloir ajouter {round(prediction[0] - valeur_flot, 2)} Litres aux {valeur_flot} Litres Actuellement présents dans le reservoir!!!"

    # Collect data
    Data_récupérées = {
        "Quantité_reservoir": valeur_flot,
        "carburant_a_consommer": round(prediction[0], 2),
        "carburant_mission": round((prediction[0] * 2) * 1.3, 2),
        "message": alert,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Save to JSON
    try:
        with open("Data.json", "w") as f:
            json.dump(Data_récupérées, f, indent=4)
    except IOError:
        raise HTTPException(status_code=500, detail="Error: Unable to write to 'Data.json'!")

    return Data_récupérées

# FastAPI endpoint
@app.post("/predict_fuel")
def predict_fuel(data: FuelRequest):
    """
    Predict fuel consumption based on the distance and fuel consumption rate.
    """
    result = fuel_consumption(data.distance, data.consommation_100km)
    return result
