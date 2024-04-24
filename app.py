import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from flask import Flask, request, jsonify

# Load and preprocess the initial data from CSV
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['TimeOfAccess'] = pd.to_datetime(data['TimeOfAccess'], format='%d-%m-%Y %H:%M')

    categorical_features = ['UserID', 'DeviceID', 'TypeOfAccess']
    label_encoders = {}
    for feature in categorical_features:
        label_encoders[feature] = LabelEncoder()
        data[feature] = label_encoders[feature].fit_transform(data[feature])

    data['TimeOfDay'] = data['TimeOfAccess'].dt.hour
    data['DayOfWeek'] = data['TimeOfAccess'].dt.dayofweek

    return data, label_encoders

# Train the Isolation Forest model
def train_model(data):
    X = data[['UserID', 'DeviceID', 'TypeOfAccess', 'UserAuthorityLevel', 'DeviceAuthorityLevel', 'TimeOfDay', 'DayOfWeek']]
    model = IsolationForest(contamination=0.1)
    model.fit(X)
    return model

# Preprocess new entries and predict anomalies
def predict_anomalies(new_data, label_encoders, model):
    new_data['TimeOfAccess'] = pd.to_datetime(new_data['TimeOfAccess'], format='%d-%m-%Y %H:%M')

    categorical_features = ['UserID', 'DeviceID', 'TypeOfAccess']
    for feature in categorical_features:
        new_data[feature] = label_encoders[feature].transform(new_data[feature])

    new_data['TimeOfDay'] = new_data['TimeOfAccess'].dt.hour
    new_data['DayOfWeek'] = new_data['TimeOfAccess'].dt.dayofweek

    X = new_data[['UserID', 'DeviceID', 'TypeOfAccess', 'UserAuthorityLevel', 'DeviceAuthorityLevel', 'TimeOfDay', 'DayOfWeek']]
    anomaly_scores = model.decision_function(X)
    new_data['AnomalyScore'] = anomaly_scores
    new_data['Anomaly'] = (anomaly_scores < -0.1).astype(int)  # Adjust the threshold as needed

    return new_data[['UserID', 'DeviceID', 'TypeOfAccess', 'TimeOfAccess', 'UserAuthorityLevel', 'DeviceAuthorityLevel', 'AnomalyScore', 'Anomaly']]

# Flask app
app = Flask(__name__)

# Load data and train model
data, label_encoders = load_data('access_control_data.csv')
model = train_model(data)

# API endpoint to predict anomalies
@app.route('/predict_anomalies', methods=['POST'])
def predict_anomalies_endpoint():
    new_data = pd.DataFrame(request.get_json())
    result = predict_anomalies(new_data, label_encoders, model)
    return result.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)