import requests
import json

# New data entries
new_data = [
    {
        "UserID": "U1007",
        "DeviceID": "D201",
        "TypeOfAccess": "Entry",
        "TimeOfAccess": "01-02-2024 08:57",
        "UserAuthorityLevel": 2,
        "DeviceAuthorityLevel": 1
    },
    {
        "UserID": "U1001",
        "DeviceID": "D202",
        "TypeOfAccess": "Exit",
        "TimeOfAccess": "01-02-2024 16:55",
        "UserAuthorityLevel": 2,
        "DeviceAuthorityLevel": 2
    }
]

# Send POST request to the API endpoint
url = "http://localhost:5000/predict_anomalies"
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(new_data), headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    predictions = response.json()
    print("Predictions:")
    for entry in predictions:
        print(f"UserID: {entry['UserID']}, DeviceID: {entry['DeviceID']}, TypeOfAccess: {entry['TypeOfAccess']}, TimeOfAccess: {entry['TimeOfAccess']}, Anomaly: {bool(entry['Anomaly'])}")
else:
    print(f"Error: {response.status_code} - {response.text}")