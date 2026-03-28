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

# -------------------------------------------------------
# INITIALIZE APP
# -------------------------------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------------------------------
# LOAD MODELS
# -------------------------------------------------------
disease_model = tf.keras.models.load_model(
    r"C:\Crop Project\Combined modal\paddy_disease_mobilenet.h5"
)

nutrient_model = tf.keras.models.load_model(
    r"C:\Crop Project\Combined modal\paddy_nutrient_model.h5"
)

yield_model = pickle.load(open(r"C:\Crop Project\Combined modal\yield_model.pkl", "rb"))
district_encoder = pickle.load(open(r"C:\Crop Project\Combined modal\district_encoder.pkl", "rb"))
season_encoder = pickle.load(open(r"C:\Crop Project\Combined modal\season_encoder.pkl", "rb"))

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
disease_names = {

    "Bacterial_leaf_blight":{
        "en":"Bacterial Leaf Blight",
        "ta":"பாக்டீரியா இலை உலர்ச்சி"
    },

    "Brown_spot":{
        "en":"Brown Spot",
        "ta":"பழுப்பு தழும்பு"
    },

    "Leaf_Blast":{
        "en":"Leaf Blast",
        "ta":"இலை பிளாஸ்ட்"
    },

    "tungro":{
        "en":"Tungro Disease",
        "ta":"துங்க்ரோ நோய்"
    },

    "Healthy_leaf":{
        "en":"Healthy Leaf",
        "ta":"ஆரோக்கியமான இலை"
    }

}

nutrient_names = {

    "Nitrogen":{
        "en":"Nitrogen Deficiency",
        "ta":"நைட்ரஜன் குறைபாடு"
    },

    "Phosphorus":{
        "en":"Phosphorus Deficiency",
        "ta":"பாஸ்பரஸ் குறைபாடு"
    },

    "Potassium":{
        "en":"Potassium Deficiency",
        "ta":"பொட்டாசியம் குறைபாடு"
    },

    "Healthy":{
        "en":"Healthy Leaf",
        "ta":"ஆரோக்கியமான இலை"
    }

}


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
        season
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

    if disease_confidence >= 0.80 and disease != "Healthy_leaf":

        response = disease_recommendations(disease,lang)

        return jsonify({

            "type":"disease",
            "prediction":disease_names.get(disease,{}).get(lang,disease),
            "confidence":round(disease_confidence,3),
            "cause":response.get("cause",""),
            "recommendations":response.get("actions",[]),
            "prevention":response.get("prevention",[])

        })

    # -------------------------------------------------------
    # NUTRIENT MODEL
    # -------------------------------------------------------
    nutrient_img = preprocess_input(img_array*255.0)

    nutrient_pred = nutrient_model.predict(nutrient_img)

    nutrient_idx = int(np.argmax(nutrient_pred))
    nutrient = nutrient_classes[nutrient_idx]

    response = nutrient_recommendations(nutrient,lang)

    return jsonify({

        "type":"nutrient",
        "prediction":nutrient_names.get(nutrient,{}).get(lang,nutrient),
        "cause":response.get("cause",""),
        "recommendations":response.get("actions",[]),
        "prevention":response.get("prevention",[])

    })

# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)