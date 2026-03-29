import os
import io
import numpy as np
import pandas as pd
import pickle
import requests
from datetime import datetime
from PIL import Image

from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

from recommendations import (
    yield_recommendations,
    disease_recommendations,
    nutrient_recommendations
)

from translations import disease_names, nutrient_names

# -------------------------------------------------------
# INITIALIZE APP
# -------------------------------------------------------
app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# -------------------------------------------------------
# LOAD MODELS
# -------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

disease_model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "Models", "paddy_disease_mobilenet.h5")
)

nutrient_model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "Models", "paddy_nutrient_model.h5")
)

yield_model = pickle.load(
    open(os.path.join(BASE_DIR, "Models", "yield_model.pkl"), "rb")
)

district_encoder = pickle.load(
    open(os.path.join(BASE_DIR, "Models", "district_encoder.pkl"), "rb")
)

season_encoder = pickle.load(
    open(os.path.join(BASE_DIR, "Models", "season_encoder.pkl"), "rb")
)

# -------------------------------------------------------
# CLASSES
# -------------------------------------------------------
disease_classes = [
    "Bacterial_leaf_blight",
    "Brown_spot",
    "Healthy_leaf",
    "Leaf_Blast",
    "others",
    "tungro"
]

nutrient_classes = [
    "Healthy",
    "Nitrogen",
    "Phosphorus",
    "Potassium"
]

API_KEY = "e78ee0e517b617b3f082bb1ddddd6d31"


# -------------------------------------------------------
# HOME
# -------------------------------------------------------
@app.route("/")
def home():
    return "Backend is Running"


# -------------------------------------------------------
# DISEASE PREDICTION
# -------------------------------------------------------
@app.route("/predict_disease", methods=["POST"])
def predict_disease():

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = disease_model.predict(img_array)
    disease = disease_classes[int(np.argmax(pred))]

    response = disease_recommendations(disease)

    return jsonify({
        "prediction": disease,
        "recommendations": response.get("actions", []),
        "prevention": response.get("prevention", [])
    })


# -------------------------------------------------------
# NUTRIENT PREDICTION
# -------------------------------------------------------
@app.route("/predict_nutrient", methods=["POST"])
def predict_nutrient():

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    pred = nutrient_model.predict(img_array)

    nutrient = nutrient_classes[int(np.argmax(pred))]

    response = nutrient_recommendations(nutrient)

    return jsonify({
        "prediction": nutrient,
        "recommendations": response.get("actions", [])
    })


# -------------------------------------------------------
# YIELD PREDICTION
# -------------------------------------------------------
@app.route("/predict_yield", methods=["POST"])
def predict_yield():

    data = request.json

    district = data.get("district", "").strip()
    season = data.get("season", "").strip()
    area = float(data.get("area", 0))

    lang = data.get("lang", "en")

    if not district or not season or area <= 0:
        return jsonify({"error": "district, season and area required"}), 400


    # -------------------------------------------------------
    # GET GEO LOCATION
    # -------------------------------------------------------
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={district},IN&limit=1&appid={API_KEY}"

    geo = requests.get(geo_url).json()

    if not geo:
        return jsonify({"error": f"Invalid district: {district}"}), 400

    lat = geo[0]["lat"]
    lon = geo[0]["lon"]


    # -------------------------------------------------------
    # WEATHER FORECAST
    # -------------------------------------------------------
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    forecast = requests.get(forecast_url).json().get("list", [])

    if not forecast:
        return jsonify({"error": "Weather data unavailable"}), 400


    temp_avg = float(np.mean([d["main"]["temp"] for d in forecast]))
    temp_max = float(np.max([d["main"]["temp_max"] for d in forecast]))
    temp_min = float(np.min([d["main"]["temp_min"] for d in forecast]))
    humidity = float(np.mean([d["main"]["humidity"] for d in forecast]))
    rainfall = float(np.sum([d.get("rain", {}).get("3h", 0) for d in forecast]))
    solar = float(np.mean([100 - d["clouds"]["all"] for d in forecast]))


    # -------------------------------------------------------
    # MODEL INPUT
    # -------------------------------------------------------
    df = pd.DataFrame([{

        "District": district,
        "Year": datetime.now().year,
        "Season": season,
        "Area": area,
        "Production": 0,

        "T2M": temp_avg,
        "T2M_MAX": temp_max,
        "T2M_MIN": temp_min,
        "RH2M": humidity,
        "Rainfall": rainfall,
        "Solar_Radiation": solar,

        "N": 90,
        "P": 45,
        "K": 120,
        "pH": 6.8
    }])


    # -------------------------------------------------------
    # ENCODE VALUES
    # -------------------------------------------------------
    try:
        df["District"] = district_encoder.transform(df["District"])
        df["Season"] = season_encoder.transform(df["Season"])
    except Exception as e:
        return jsonify({"error": "District or season not supported by model"}), 400


    # -------------------------------------------------------
    # PREDICT
    # -------------------------------------------------------
    predicted_yield = float(yield_model.predict(df)[0])


    # -------------------------------------------------------
    # RECOMMENDATIONS
    # -------------------------------------------------------
    recommendations = yield_recommendations(
    predicted_yield,
    {
        "avg_temperature": temp_avg,
        "rainfall_mm": rainfall
    },
    season,
    lang
)


    # -------------------------------------------------------
    # RESPONSE
    # -------------------------------------------------------
    return jsonify({

        "predicted_yield": round(predicted_yield, 2),

        "weather": {
            "avg_temperature": round(temp_avg, 2),
            "max_temperature": round(temp_max, 2),
            "min_temperature": round(temp_min, 2),
            "humidity": round(humidity, 2),
            "rainfall": round(rainfall, 2),
            "solar_radiation": round(solar, 2)
        },

        "recommendations": recommendations
    })



# -------------------------------------------------------
# ANALYZE LEAF (AUTO DETECT DISEASE / NUTRIENT)
# -------------------------------------------------------
@app.route("/analyze_leaf", methods=["POST"])
def analyze_leaf():
    file = request.files.get("image")
    lang = request.form.get("lang","en")

    if not file:
        return jsonify({"error":"No image uploaded"}),400

    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    img = img.resize((224,224))

    img_array = np.array(img)/255.0
    img_array = np.expand_dims(img_array,axis=0)

    # -------------------------------------------------------
    # DISEASE MODEL
    # -------------------------------------------------------
    disease_pred = disease_model.predict(img_array)

    disease_confidence = float(np.max(disease_pred))
    disease_idx = int(np.argmax(disease_pred))
    disease = disease_classes[disease_idx]

    response = None  # <-- initialize response

    if disease_confidence >= 0.60 and disease != "Healthy_leaf":
        response = disease_recommendations(disease, lang)

        product = response.get("product", None)
        if product:
            if not product["image"].startswith("http"):
                product["image"] = f"http://127.0.0.1:5000/static/products/{product['image']}"


        return jsonify({
            "type":"disease",
            "prediction":disease_names.get(disease,{}).get(lang,disease),
            "confidence":round(disease_confidence,3),
            "cause":response.get("cause",""),
            "actions":response.get("actions",[]),
            "prevention":response.get("prevention",[]),
            "product":product
        })

    # -------------------------------------------------------
    # NUTRIENT MODEL (if disease not detected)
    # -------------------------------------------------------
    nutrient_img = preprocess_input(img_array*255.0)
    nutrient_pred = nutrient_model.predict(nutrient_img)
    nutrient_idx = int(np.argmax(nutrient_pred))
    nutrient = nutrient_classes[nutrient_idx]

    response = nutrient_recommendations(nutrient, lang)
    product = response.get("product", None)
    if product:
        if not product["image"].startswith("http"):
            product["image"] = f"http://127.0.0.1:5000/static/products/{product['image']}"

    return jsonify({
        "type":"nutrient",
        "prediction":nutrient_names.get(nutrient,{}).get(lang,nutrient),
        "cause":response.get("cause",""),
        "actions":response.get("actions",[]),
        "prevention":response.get("prevention",[]),
        "product":product
    })

# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))