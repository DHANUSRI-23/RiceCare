import requests

url = "http://127.0.0.1:5000/predict_yield"

payload = {
    "district": "Chennai",
    "season": "Winter",
    "area": 120
}

response = requests.post(url, json=payload)
data = response.json()

print("\nYIELD + RECOMMENDATION TEST")

print(f"\nPredicted Yield (tons/hectare): {data.get('predicted_yield', 'N/A')}")

print("\nWeather Summary:")
print(f"Average Temperature: {data['weather']['avg_temperature']} °C")
print(f"Maximum Temperature: {data['weather']['max_temperature']} °C")
print(f"Minimum Temperature: {data['weather']['min_temperature']} °C")
print(f"Humidity: {data['weather']['humidity']} %")
print(f"Rainfall: {data['weather']['rainfall']} mm")
print(f"Solar Radiation Index: {data['weather']['solar_radiation']}")

print("\nRecommendations:")
for rec in data["recommendations"]:
    print("-", rec)


