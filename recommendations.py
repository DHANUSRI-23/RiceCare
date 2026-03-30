# recommendations.py

# ---------------------------------------------------
# PRODUCT DATABASE
# ---------------------------------------------------

PRODUCT_DATABASE = {
    "Tricyclazole": {
        "name": "Tricyclazole",
        "image": "tricyclazole.png",
        "price_en": "₹289 / 100g",
        "price_ta": "₹289 / 100 கிராம்"
    },
    "Copper_Oxychloride": {
        "name": "Copper Oxychloride",
        "image": "copper_oxychloride.png",
        "price_en": "₹550 / 500g",
        "price_ta": "₹550 / 500 கிராம்"
    },
    "Mancozeb": {
        "name": "Mancozeb",
        "image": "mancozeb.png",
        "price_en": "₹300 / 500g",
        "price_ta": "₹300 / 500 கிராம்"
    },
    "Urea": {
        "name": "Urea",
        "image": "urea.png",
        "price_en": "₹270 / 45kg bag",
        "price_ta": "₹270 / 45 கிலோ பை"
    },
    "DAP": {
        "name": "Di-Ammonium Phosphate (DAP)",
        "image": "dap.png",
        "price_en": "₹1350 / 50kg bag",
        "price_ta": "₹1350 / 50 கிலோ"
    },
    "MOP": {
        "name": "Muriate of Potash (MOP)",
        "image": "mop.png",
        "price_en": "₹1700 / 50kg bag",
        "price_ta": "₹1700 / 50 கிலோ"
    },
    "Imidacloprid": {
        "name": "Imidacloprid",
        "image": "imidacloprid.png",
        "price_en": "₹500 / 250ml",
        "price_ta": "₹500 / 250 மில்லி"
    },
    "Thiamethoxam": {
        "name": "Thiamethoxam",
        "image": "thiamethoxam.png",
        "price_en": "₹450 / 250ml",
        "price_ta": "₹450 / 250 மில்லி"
    },
    "Fipronil": {
        "name": "Fipronil",
        "image": "fipronil.png",
        "price_en": "₹600 / 250ml",
        "price_ta": "₹600 / 250 மில்லி"
    }
}

# ---------------------------------------------------
# YIELD-BASED RECOMMENDATIONS
# ---------------------------------------------------

def yield_recommendations(pred_yield, weather, season, lang="en"):

    rec_en = []
    rec_ta = []

    if pred_yield < 2.5:

        rec_en.extend([
            "Increase irrigation frequency to avoid dry soil",
            "Apply balanced fertilizers based on soil condition",
            "Use good quality high-yield rice seeds"
        ])

        rec_ta.extend([
            "மண் உலராமல் இருக்க பாசனத்தை அதிகரிக்கவும்",
            "மண் நிலைக்கு ஏற்ப சமநிலை உரங்களை பயன்படுத்தவும்",
            "நல்ல தரமான அதிக விளைச்சல் தரும் விதைகளை பயன்படுத்தவும்"
        ])

        if weather["rainfall_mm"] < 20:
            rec_en.append("Provide additional irrigation since rainfall is low")
            rec_ta.append("மழை குறைவாக இருப்பதால் கூடுதல் பாசனம் வழங்கவும்")

        if weather["avg_temperature"] > 32:
            rec_en.append("Maintain water level in field to reduce heat stress")
            rec_ta.append("அதிக வெப்பம் இருப்பதால் வயலில் நீர் அளவை பராமரிக்கவும்")

    elif 2.5 <= pred_yield < 4.0:

        rec_en.extend([
            "Provide irrigation regularly during crop growth",
            "Apply nitrogen fertilizer (urea) during plant growth stage",
            "Check the field weekly for pests or leaf color changes"
        ])

        rec_ta.extend([
            "பயிர் வளர்ச்சி காலத்தில் பாசனத்தை முறையாக வழங்கவும்",
            "செடி வளர்ச்சி காலத்தில் யூரியா உரத்தை பயன்படுத்தவும்",
            "வாரம் ஒருமுறை வயலை பூச்சி அல்லது இலை நிற மாற்றத்திற்காக பரிசோதிக்கவும்"
        ])

    else:

        rec_en.extend([
            "Current crop growth is good, continue present farming practices",
            "Continue regular irrigation and monitoring"
        ])

        rec_ta.extend([
            "பயிர் வளர்ச்சி நல்ல நிலையில் உள்ளது, தற்போதைய முறைகளை தொடரவும்",
            "பாசனம் மற்றும் கண்காணிப்பை தொடர்ந்து செய்யவும்"
        ])

    # Season based advice
    if season == "Kharif":
        rec_en.append("Maintain proper drainage after heavy rains")
        rec_ta.append("அதிக மழைக்கு பிறகு நீர் தேங்காமல் வயலில் நீரேற்றத்தை சரி செய்யவும்")

    elif season == "Winter":
        rec_en.append("Ensure the crop receives enough sunlight")
        rec_ta.append("பயிருக்கு போதுமான சூரிய ஒளி கிடைப்பதை உறுதி செய்யவும்")

    return rec_ta if lang == "ta" else rec_en


# ---------------------------------------------------
# DISEASE RECOMMENDATIONS
# ---------------------------------------------------

DISEASE_RECOMMENDATIONS = {

    "Leaf_Blast": {
        "cause_en": "Fungal infection caused by Magnaporthe oryzae.",
        "cause_ta": "பூஞ்சை காரணமாக ஏற்படும் இலை பிளாஸ்ட் நோய்.",
        "actions_en": [
            "Spray Tricyclazole 0.6 g per liter of water",
            "Avoid excessive nitrogen fertilizer application",
            "Maintain proper spacing between plants for airflow"
        ],
        "actions_ta": [
            "ஒரு லிட்டர் நீருக்கு 0.6 கிராம் Tricyclazole தெளிக்கவும்",
            "அதிக நைட்ரஜன் உரத்தை தவிர்க்கவும்",
            "தாவரங்களுக்கு சரியான இடைவெளி வைக்கவும்"
        ],
        "prevention_en": [
            "Use blast-resistant rice varieties",
            "Avoid dense planting",
            "Monitor crop especially during humid weather"
        ],
        "prevention_ta": [
            "நோய் எதிர்ப்பு நெல் வகைகளை பயன்படுத்தவும்",
            "அதிக நெருக்கமாக நடவு செய்ய வேண்டாம்",
            "ஈரப்பதம் அதிகமாக இருக்கும் போது வயலை கண்காணிக்கவும்"
        ]
    },

    "Bacterial_leaf_blight": {
        "cause_en": "Bacterial infection caused by Xanthomonas oryzae.",
        "cause_ta": "பாக்டீரியா காரணமாக ஏற்படும் இலை நோய்.",
        "actions_en": [
            "Spray Copper oxychloride 2.5 g per liter of water",
            "Remove severely infected leaves from the field",
            "Reduce excess fertilizer application"
        ],
        "actions_ta": [
            "ஒரு லிட்டர் நீருக்கு 2.5 கிராம் Copper oxychloride தெளிக்கவும்",
            "அதிக பாதிக்கப்பட்ட இலைகளை அகற்றவும்",
            "அதிக உரத்தை தவிர்க்கவும்"
        ],
        "prevention_en": [
            "Use disease-free certified seeds",
            "Avoid overhead irrigation",
            "Maintain clean field conditions"
        ],
        "prevention_ta": [
            "நோய் இல்லாத விதைகளை பயன்படுத்தவும்",
            "மேலிருந்து பாசனம் செய்ய வேண்டாம்",
            "வயலை சுத்தமாக வைத்திருக்கவும்"
        ]
    },

    "Brown_spot": {
        "cause_en": "Fungal infection due to Bipolaris oryzae.",
        "cause_ta": "பூஞ்சை காரணமாக ஏற்படும் பழுப்பு புள்ளி நோய்.",
        "actions_en": [
            "Spray Mancozeb 2 g per liter of water",
            "Apply balanced NPK fertilizers",
            "Improve soil fertility using organic manure"
        ],
        "actions_ta": [
            "ஒரு லிட்டர் நீருக்கு 2 கிராம் Mancozeb தெளிக்கவும்",
            "NPK சமநிலை உரங்களை பயன்படுத்தவும்",
            "மண் வளத்தை உயர்த்த உயிர்சத்து உரம் பயன்படுத்தவும்"
        ],
        "prevention_en": [
            "Use certified seeds",
            "Avoid nutrient deficiency",
            "Maintain soil health"
        ],
        "prevention_ta": [
            "சான்றளிக்கப்பட்ட விதைகளை பயன்படுத்தவும்",
            "ஊட்டச்சத்து குறைபாடு வராமல் பார்த்துக்கொள்ளவும்",
            "மண் ஆரோக்கியத்தை பராமரிக்கவும்"
        ]
    },

    "tungro": {
        "cause_en": "Viral disease transmitted by green leafhopper.",
        "cause_ta": "பூச்சி மூலம் பரவும் வைரஸ் நோய்.",
        "actions_en": [
            "Spray Imidacloprid 0.3–0.5 g per liter of water",
            "Spray Thiamethoxam 0.3–0.5 g per liter of water",
            "Spray Fipronil 0.2–0.4 g per liter of water",
            "Remove infected plants immediately",
            "Keep field free from weeds"
        ],
        "actions_ta": [
            "ஒரு லிட்டர் நீருக்கு 0.3–0.5 கிராம் Imidacloprid தெளிக்கவும்",
            "ஒரு லிட்டர் நீருக்கு 0.3–0.5 கிராம் Thiamethoxam தெளிக்கவும்",
            "ஒரு லிட்டர் நீருக்கு 0.2–0.4 கிராம் Fipronil தெளிக்கவும்",
            "பாதிக்கப்பட்ட தாவரங்களை உடனே அகற்றவும்",
            "வயலில் கொடிகளை அகற்றவும்"
        ],
        "prevention_en": [
            "Use resistant varieties",
            "Monitor insect population regularly",
            "Avoid late planting"
        ],
        "prevention_ta": [
            "நோய் எதிர்ப்பு வகைகளை பயன்படுத்தவும்",
            "பூச்சி எண்ணிக்கையை கண்காணிக்கவும்",
            "தாமதமாக நடவு செய்ய வேண்டாம்"
        ]
    },

    "Healthy_leaf": {
        "cause_en": "No disease detected.",
        "cause_ta": "எந்த நோயும் இல்லை.",
        "actions_en": ["No treatment required"],
        "actions_ta": ["சிகிச்சை தேவையில்லை"],
        "prevention_en": ["Continue regular crop monitoring"],
        "prevention_ta": ["வயலை தொடர்ந்து கண்காணிக்கவும்"]
    }
}

def disease_recommendations(disease_name, lang="en"):

    data = DISEASE_RECOMMENDATIONS.get(disease_name)

    if not data:
        return {
            "cause": "Unknown disease",
            "actions": [],
            "prevention": [],
            "product": None
        }

    product = None

    if disease_name == "Leaf_Blast":
        product = PRODUCT_DATABASE["Tricyclazole"]
    elif disease_name == "Bacterial_leaf_blight":
        product = PRODUCT_DATABASE["Copper_Oxychloride"]
    elif disease_name == "Brown_spot":
        product = PRODUCT_DATABASE["Mancozeb"]
    elif disease_name == "tungro":
        # default product for display
        product = PRODUCT_DATABASE["Imidacloprid"]

    if lang == "ta":
        return {
            "cause": data["cause_ta"],
            "actions": data["actions_ta"],
            "prevention": data["prevention_ta"],
            "product": product
        }

    return {
        "cause": data["cause_en"],
        "actions": data["actions_en"],
        "prevention": data["prevention_en"],
        "product": product
    }

# ---------------------------------------------------
# NUTRIENT DEFICIENCY RECOMMENDATIONS
# ---------------------------------------------------

NUTRIENT_RECOMMENDATIONS = {
    "Nitrogen": {
        "cause_en": "Nitrogen deficiency in soil.",
        "cause_ta": "மண்ணில் நைட்ரஜன் குறைபாடு.",
        "actions_en": [
            "Apply Urea 45–50 kg per acre",
            "Apply fertilizer in two stages during crop growth"
        ],
        "actions_ta": [
            "ஒரு ஏக்கருக்கு 45–50 கிலோ யூரியா வழங்கவும்",
            "உரத்தை இரண்டு கட்டமாக வழங்கவும்"
        ],
        "prevention_en": [
            "Conduct soil testing before fertilizer application",
            "Maintain proper irrigation to avoid nitrogen loss"
        ],
        "prevention_ta": [
            "உரமிடுவதற்கு முன் மண் பரிசோதனை செய்யவும்",
            "நைட்ரஜன் இழப்பை தவிர்க்க சரியான பாசனம் செய்யவும்"
        ]
    },

    "Phosphorus": {
        "cause_en": "Low phosphorus content in soil affecting plant growth.",
        "cause_ta": "மண்ணில் பாஸ்பரஸ் குறைபாடு.",
        "actions_en": [
            "Apply 20 kg DAP per acre during early crop stage",
            "Top dress 10 kg per acre at tillering stage",
            "Mix 15 kg DAP per acre with irrigation water at early vegetative stage"
        ],
        "actions_ta": [
            "பயிர் ஆரம்ப நிலையில் ஒரு ஏக்கருக்கு 20 கிலோ DAP பயன்படுத்தவும்",
            "தளிர்ச்சி கட்டத்தில் ஒரு ஏக்கருக்கு 10 கிலோ மேல்சுற்றும் உரம் வழங்கவும்",
            "முன்னணி வளர்ச்சி கட்டத்தில் ஒரு ஏக்கருக்கு 15 கிலோ DAP நீருடன் கலந்து வழங்கவும்"
        ],
        "prevention_en": [
            "Maintain proper soil nutrition",
            "Perform regular soil testing",
            "Ensure balanced fertilizer application"
        ],
        "prevention_ta": [
            "மண் ஊட்டச்சத்தை பராமரிக்கவும்",
            "மண் பரிசோதனையை முறையாக செய்யவும்",
            "சமநிலை உரங்களை பயன்படுத்தவும்"
        ]
    },

    "Potassium": {
        "cause_en": "Potassium deficiency affecting plant strength.",
        "cause_ta": "பொட்டாசியம் குறைபாடு.",
        "actions_en": [
            "Apply 30 kg MOP per acre at planting",
            "Top dress 20 kg MOP per acre at tillering stage",
            "Use 10 kg MOP per acre during panicle initiation for better grain quality"
        ],
        "actions_ta": [
            "நட்சத்திரத்தில் ஒரு ஏக்கருக்கு 30 கிலோ MOP உரம் பயன்படுத்தவும்",
            "தளிர்ச்சி கட்டத்தில் ஒரு ஏக்கருக்கு 20 கிலோ மேல்சுற்றும் MOP வழங்கவும்",
            "மலர் தொடக்க கட்டத்தில் ஒரு ஏக்கருக்கு 10 கிலோ MOP பயன்படுத்தவும்"
        ],
        "prevention_en": [
            "Maintain balanced fertilizers",
            "Perform regular soil testing",
            "Avoid overuse of single nutrient"
        ],
        "prevention_ta": [
            "சமநிலை உரங்களை பயன்படுத்தவும்",
            "மண் பரிசோதனையை முறையாக செய்யவும்",
            "ஒற்றை ஊட்டச்சத்தைக் கூடுதலாக பயன்படுத்த வேண்டாம்"
        ]
    },

    "Healthy_leaf": {
        "cause_en": "No disease detected.",
        "cause_ta": "எந்த நோயும் இல்லை.",
        "actions_en": ["No treatment required"],
        "actions_ta": ["சிகிச்சை தேவையில்லை"],
        "prevention_en": ["Continue regular crop monitoring"],
        "prevention_ta": ["வயலை தொடர்ந்து கண்காணிக்கவும்"]
    }
}

def nutrient_recommendations(nutrient, lang="en"):

    data = NUTRIENT_RECOMMENDATIONS.get(nutrient)

    if not data:
        return {
            "cause": "Unknown nutrient issue",
            "actions": [],
            "prevention": [],
            "product": None
        }

    product = None

    if nutrient == "Nitrogen":
        product = PRODUCT_DATABASE["Urea"]
    elif nutrient == "Phosphorus":
        product = PRODUCT_DATABASE["DAP"]
    elif nutrient == "Potassium":
        product = PRODUCT_DATABASE["MOP"]

    if lang == "ta":
        return {
            "cause": data["cause_ta"],
            "actions": data["actions_ta"],
            "prevention": data["prevention_ta"],
            "product": product
        }

    return {
        "cause": data["cause_en"],
        "actions": data["actions_en"],
        "prevention": data["prevention_en"],
        "product": product
    }