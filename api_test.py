import requests

# Define the API URL
url = "http://127.0.0.1:8000/predict_fuel"

# Define the payload
payload = {
    "distance": 200,  # Distance in kilometers
    "consommation_100km": 13  # Fuel consumption per 100 km
}

# Send a POST request to the API
try:
    response = requests.post(url, json=payload)

    # Print the response
    if response.status_code == 200:
        print("API Response:")
        print(response.json())
    else:
        print(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
