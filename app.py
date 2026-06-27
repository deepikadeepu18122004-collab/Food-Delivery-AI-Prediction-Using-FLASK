from flask import Flask, render_template, request
import numpy as np
import joblib
import sqlite3
import os

app = Flask(__name__)

# ----------------------------
# INIT DATABASE
# ----------------------------
def init_db():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        ratings REAL,
        distance REAL,
        weather TEXT,
        traffic TEXT,
        vehicle TEXT,
        preparation_time INTEGER,
        prediction REAL
    )
    """)

    conn.commit()
    conn.close()


init_db()

# ----------------------------
# LOAD MODELS
# ----------------------------
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

weather_encoder = joblib.load("weather_encoder.pkl")
traffic_encoder = joblib.load("traffic_encoder.pkl")
vehicle_encoder = joblib.load("vehicle_encoder.pkl")


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# PREDICTION ROUTE
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

    # encode categorical values
    weather = weather_encoder.transform([weather])[0]
    traffic = traffic_encoder.transform([traffic])[0]
    vehicle = vehicle_encoder.transform([vehicle])[0]

    # prepare input
    data = np.array([[
        age,
        ratings,
        distance,
        weather,
        traffic,
        vehicle,
        preparation_time
    ]])

    # scale input
    data = scaler.transform(data)

    # prediction
    prediction = model.predict(data)[0]
    prediction = round(prediction, 1)

    # ----------------------------
    # SAVE TO DATABASE
    # ----------------------------
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (
        age, ratings, distance, weather, traffic, vehicle, preparation_time, prediction
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        age,
        ratings,
        distance,
        str(weather),
        str(traffic),
        str(vehicle),
        preparation_time,
        prediction
    ))

    conn.commit()
    conn.close()

    return render_template("result.html", prediction=prediction)


# ----------------------------
# HISTORY PAGE
# ----------------------------
@app.route("/history")
def history():

    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template("history.html", data=data)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)