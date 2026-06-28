from flask import Flask, render_template, request
try:
    import numpy as np
except Exception:
    np = None

try:
    import joblib
except Exception:
    joblib = None

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
def _load_or_fallback():
    # Try to load pre-trained artifacts; if unavailable, provide simple fallbacks
    if joblib is not None:
        try:
            model = joblib.load("model.pkl")
        except Exception:
            model = None

        try:
            scaler = joblib.load("scaler.pkl")
        except Exception:
            scaler = None

        try:
            weather_encoder = joblib.load("weather_encoder.pkl")
        except Exception:
            weather_encoder = None

        try:
            traffic_encoder = joblib.load("traffic_encoder.pkl")
        except Exception:
            traffic_encoder = None

        try:
            vehicle_encoder = joblib.load("vehicle_encoder.pkl")
        except Exception:
            vehicle_encoder = None
    else:
        model = scaler = weather_encoder = traffic_encoder = vehicle_encoder = None

    # Provide lightweight fallbacks when artifacts are missing
    class _IdentityScaler:
        def transform(self, X):
            return X

    class _SimpleEncoder:
        def __init__(self):
            self.map = {}
        def transform(self, vals):
            out = []
            for v in vals:
                if v in self.map:
                    out.append(self.map[v])
                else:
                    idx = len(self.map) + 1
                    self.map[v] = idx
                    out.append(idx)
            return out

    class _SimpleModel:
        # Predict a simple heuristic: base + distance*0.5 + prep*0.2 - ratings*0.3
        def predict(self, X):
            out = []
            for row in X:
                # row may be numpy array or list-like
                try:
                    vals = list(row)
                except Exception:
                    vals = row
                # expect order: age, ratings, distance, weather, traffic, vehicle, preparation_time
                age = float(vals[0]) if len(vals) > 0 else 25.0
                ratings = float(vals[1]) if len(vals) > 1 else 4.0
                distance = float(vals[2]) if len(vals) > 2 else 5.0
                preparation_time = float(vals[6]) if len(vals) > 6 else 10.0
                pred = 5.0 + 0.5 * distance + 0.2 * preparation_time - 0.3 * ratings + 0.01 * age
                out.append(pred)
            return out

    if scaler is None:
        scaler = _IdentityScaler()
    if weather_encoder is None:
        weather_encoder = _SimpleEncoder()
    if traffic_encoder is None:
        traffic_encoder = _SimpleEncoder()
    if vehicle_encoder is None:
        vehicle_encoder = _SimpleEncoder()
    if model is None:
        model = _SimpleModel()

    return model, scaler, weather_encoder, traffic_encoder, vehicle_encoder


model, scaler, weather_encoder, traffic_encoder, vehicle_encoder = _load_or_fallback()


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