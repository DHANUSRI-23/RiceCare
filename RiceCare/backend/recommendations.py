# recommendations.py

# ---------------------------------------------------
# YIELD-BASED RECOMMENDATIONS
# ---------------------------------------------------

def yield_recommendations(pred_yield, weather, season, lang="en"):

    rec_en = []
    rec_ta = []

    if pred_yield < 2.5:

        rec_en.extend([
            "Increase irrigation frequency to avoid moisture stress",
            "Apply balanced NPK fertilizers based on soil test",
            "Use certified high-yield rice varieties"
        ])

        rec_ta.extend([
            "மண் ஈரப்பதம் குறையாமல் இருக்க பாசனத்தை அதிகரிக்கவும்",
            "மண் பரிசோதனை அடிப்படையில் சமநிலை NPK உரங்களை பயன்படுத்தவும்",
            "உயர் விளைச்சல் தரும் சான்றளிக்கப்பட்ட நெல் வகைகளை பயன்படுத்தவும்"
        ])

        if weather["rainfall_mm"] < 20:
            rec_en.append("Supplement rainfall with controlled irrigation")
            rec_ta.append("மழை குறைந்தால் கட்டுப்படுத்தப்பட்ட பாசனத்தை வழங்கவும்")

        if weather["avg_temperature"] > 32:
            rec_en.append("Use mulching to reduce heat stress")
            rec_ta.append("வெப்ப அழுத்தத்தை குறைக்க மண்ணை மூடும் முறையை பயன்படுத்தவும்")

    elif 2.5 <= pred_yield < 4.0:

        rec_en.extend([
            "Maintain proper irrigation and nutrient schedule",
            "Monitor crop regularly for early detection"
        ])

        rec_ta.extend([
            "சரியான பாசன மற்றும் ஊட்டச்சத்து அட்டவணையை பராமரிக்கவும்",
            "நோய்களை முன்கூட்டியே கண்டறிய வயலை அடிக்கடி கண்காணிக்கவும்"
        ])

    else:

        rec_en.extend([
            "Continue current crop management practices",
            "Maintain regular field monitoring"
        ])

        rec_ta.extend([
            "தற்போதைய பயிர் மேலாண்மை முறைகளை தொடரவும்",
            "வயலை வழக்கமாக கண்காணிக்கவும்"
        ])

    if season == "Kharif":
        rec_en.append("Ensure proper drainage to prevent waterlogging")
        rec_ta.append("நீர் தேக்கம் ஏற்படாமல் சரியான நீரேற்றத்தை உறுதி செய்யவும்")

    elif season == "Winter":
        rec_en.append("Ensure adequate sunlight exposure")
        rec_ta.append("போதுமான சூரிய ஒளி கிடைப்பதை உறுதி செய்யவும்")

    return rec_ta if lang == "ta" else rec_en


# ---------------------------------------------------
# DISEASE RECOMMENDATIONS
# ---------------------------------------------------

DISEASE_RECOMMENDATIONS = {

    "Leaf_Blast": {

        "cause_en": "Fungal infection caused by Magnaporthe oryzae.",
        "cause_ta": "மக்னாபோர்தே ஓரிசே என்ற பூஞ்சை காரணமாக ஏற்படும் நோய்.",

        "actions_en": [
            "Apply Tricyclazole or Isoprothiolane fungicide",
            "Avoid excess nitrogen fertilizer",
            "Ensure proper drainage"
        ],

        "actions_ta": [
            "டிரைசைக்ளசோல் அல்லது ஐசோப்ரோத்தியோலேன் பூஞ்சைநாசினி பயன்படுத்தவும்",
            "அதிக நைட்ரஜன் உரத்தை தவிர்க்கவும்",
            "சரியான நீரேற்றத்தை உறுதி செய்யவும்"
        ],

        "prevention_en": [
            "Use resistant rice varieties",
            "Maintain proper plant spacing",
            "Conduct regular field monitoring"
        ],

        "prevention_ta": [
            "நோய் எதிர்ப்பு நெல் வகைகளை பயன்படுத்தவும்",
            "தாவர இடைவெளியை சரியாக பராமரிக்கவும்",
            "வயலை அடிக்கடி கண்காணிக்கவும்"
        ]
    },

    "Bacterial_leaf_blight": {

        "cause_en": "Bacterial infection caused by Xanthomonas oryzae.",
        "cause_ta": "ஜாந்தோமோனாஸ் ஓரிசே என்ற பாக்டீரியா காரணமாக ஏற்படும் நோய்.",

        "actions_en": [
            "Apply copper based bactericides",
            "Avoid excessive nitrogen fertilizer"
        ],

        "actions_ta": [
            "காப்பர் அடிப்படையிலான பாக்டீரியா நாசினி பயன்படுத்தவும்",
            "அதிக நைட்ரஜன் உரத்தை தவிர்க்கவும்"
        ],

        "prevention_en": [
            "Use resistant rice varieties",
            "Avoid overhead irrigation",
            "Maintain field sanitation"
        ],

        "prevention_ta": [
            "நோய் எதிர்ப்பு நெல் வகைகளை பயன்படுத்தவும்",
            "மேலிருந்து நீர் பாய்ச்சுவதை தவிர்க்கவும்",
            "வயல் சுத்தமாக வைத்திருக்கவும்"
        ]
    },

    "Brown_spot": {

        "cause_en": "Fungal infection due to Bipolaris oryzae.",
        "cause_ta": "பிபோலாரிஸ் ஓரிசே பூஞ்சை காரணமாக ஏற்படும் நோய்.",

        "actions_en": [
            "Apply Mancozeb or Carbendazim fungicide",
            "Apply balanced fertilizers"
        ],

        "actions_ta": [
            "மாங்கோசெப் அல்லது கார்பெண்டாசிம் பூஞ்சைநாசினி பயன்படுத்தவும்",
            "சமநிலை உரங்களை பயன்படுத்தவும்"
        ],

        "prevention_en": [
            "Improve soil fertility",
            "Use certified seeds"
        ],

        "prevention_ta": [
            "மண் வளத்தை மேம்படுத்தவும்",
            "சான்றளிக்கப்பட்ட விதைகளை பயன்படுத்தவும்"
        ]
    },

    "tungro": {

        "cause_en": "Viral disease transmitted by green leafhopper.",
        "cause_ta": "பச்சை இலை தாவர பூச்சி மூலம் பரவும் வைரஸ் நோய்.",

        "actions_en": [
            "Control green leafhopper population",
            "Remove infected plants"
        ],

        "actions_ta": [
            "பச்சை இலை பூச்சி எண்ணிக்கையை கட்டுப்படுத்தவும்",
            "பாதிக்கப்பட்ட தாவரங்களை அகற்றவும்"
        ],

        "prevention_en": [
            "Use resistant varieties",
            "Avoid staggered planting"
        ],

        "prevention_ta": [
            "நோய் எதிர்ப்பு வகைகளை பயன்படுத்தவும்",
            "தொடர்ச்சியான விதைப்பு முறையை தவிர்க்கவும்"
        ]
    },

    "Healthy_leaf": {

        "cause_en": "No disease detected.",
        "cause_ta": "எந்த நோயும் கண்டறியப்படவில்லை.",

        "actions_en": ["No action required"],
        "actions_ta": ["எந்த நடவடிக்கையும் தேவையில்லை"],

        "prevention_en": ["Continue regular monitoring"],
        "prevention_ta": ["வயலை வழக்கமாக கண்காணிக்கவும்"]
    }
}


def disease_recommendations(disease_name, lang="en"):

    data = DISEASE_RECOMMENDATIONS.get(disease_name)

    if not data:
        return {
            "cause": "Unknown disease",
            "actions": ["Monitor crop condition"],
            "prevention": ["Follow general crop management"]
        }

    if lang == "ta":
        return {
            "cause": data["cause_ta"],
            "actions": data["actions_ta"],
            "prevention": data["prevention_ta"]
        }

    return {
        "cause": data["cause_en"],
        "actions": data["actions_en"],
        "prevention": data["prevention_en"]
    }


# ---------------------------------------------------
# NUTRIENT DEFICIENCY RECOMMENDATIONS
# ---------------------------------------------------

NUTRIENT_RECOMMENDATIONS = {

    "Nitrogen": {

        "cause_en": "Nitrogen deficiency in soil.",
        "cause_ta": "மண்ணில் நைட்ரஜன் குறைபாடு.",

        "actions_en": [
            "Apply urea fertilizer",
            "Split nitrogen application"
        ],

        "actions_ta": [
            "யூரியா உரத்தை பயன்படுத்தவும்",
            "நைட்ரஜன் உரத்தை இரண்டு கட்டமாக வழங்கவும்"
        ],

        "prevention_en": [
            "Conduct soil testing",
            "Avoid nitrogen loss"
        ],

        "prevention_ta": [
            "மண் பரிசோதனை செய்யவும்",
            "நைட்ரஜன் இழப்பை தவிர்க்கவும்"
        ]
    },

    "Phosphorus": {

        "cause_en": "Low phosphorus content in soil.",
        "cause_ta": "மண்ணில் பாஸ்பரஸ் குறைபாடு.",

        "actions_en": [
            "Apply DAP or SSP fertilizer"
        ],

        "actions_ta": [
            "DAP அல்லது SSP உரத்தை பயன்படுத்தவும்"
        ],

        "prevention_en": [
            "Improve soil organic matter"
        ],

        "prevention_ta": [
            "மண் உயிர்ச்சத்து அதிகரிக்கவும்"
        ]
    },

    "Potassium": {

        "cause_en": "Potassium deficiency in soil.",
        "cause_ta": "மண்ணில் பொட்டாசியம் குறைபாடு.",

        "actions_en": [
            "Apply Muriate of Potash"
        ],

        "actions_ta": [
            "ம்யூரியேட் ஆஃப் பொட்டாஷ் உரத்தை பயன்படுத்தவும்"
        ],

        "prevention_en": [
            "Maintain balanced fertilization"
        ],

        "prevention_ta": [
            "சமநிலை உரங்களை பயன்படுத்தவும்"
        ]
    },

    "Healthy": {

        "cause_en": "No nutrient deficiency detected.",
        "cause_ta": "ஊட்டச்சத்து குறைபாடு இல்லை.",

        "actions_en": ["No correction required"],
        "actions_ta": ["எந்த திருத்தமும் தேவையில்லை"],

        "prevention_en": ["Maintain fertilizer schedule"],
        "prevention_ta": ["உர அட்டவணையை தொடரவும்"]
    }
}


def nutrient_recommendations(nutrient, lang="en"):

    data = NUTRIENT_RECOMMENDATIONS.get(nutrient)

    if not data:
        return {
            "cause": "Unknown nutrient issue",
            "actions": ["Consult expert"],
            "prevention": ["Conduct soil test"]
        }

    if lang == "ta":
        return {
            "cause": data["cause_ta"],
            "actions": data["actions_ta"],
            "prevention": data["prevention_ta"]
        }

    return {
        "cause": data["cause_en"],
        "actions": data["actions_en"],
        "prevention": data["prevention_en"]
    }

