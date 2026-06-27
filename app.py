from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# ----------------------------
# Load Model and Objects
# ----------------------------

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

weather_encoder = joblib.load("weather_encoder.pkl")
traffic_encoder = joblib.load("traffic_encoder.pkl")
vehicle_encoder = joblib.load("vehicle_encoder.pkl")


# ----------------------------
# Home Page
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Prediction
# ----------------------------

@app.route("/predict", methods=["POST"])
def predict():

    age = int(request.form["age"])
    ratings = float(request.form["ratings"])
    distance = float(request.form["distance"])
    preparation_time = int(request.form["preparation_time"])

    weather = request.form["weather"]
    traffic = request.form["traffic"]
    vehicle = request.form["vehicle"]

    weather = weather_encoder.transform([weather])[0]
    traffic = traffic_encoder.transform([traffic])[0]
    vehicle = vehicle_encoder.transform([vehicle])[0]

    data = np.array([[
        age,
        ratings,
        distance,
        weather,
        traffic,
        vehicle,
        preparation_time
    ]])

    data = scaler.transform(data)

    prediction = model.predict(data)[0]

    prediction = round(prediction, 1)

    return render_template(
        "result.html",
        prediction=prediction
    )


# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
