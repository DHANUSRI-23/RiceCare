import requests

url = "http://127.0.0.1:5000/predict_nutrient"

image_path = r"C:\Crop Project\Combined modal\With Split\train\Phosphorus\IMG_3805.JPG"

files = {"image": open(image_path, "rb")}

response = requests.post(url, files=files)
data = response.json()

print("\nNUTRIENT + RECOMMENDATION TEST")

print(f"\nDetected Deficiency: {data['detected_deficiency']}")

print("\nCause:")
print(data["cause"])

print("\nRecommended Actions:")
for rec in data["recommended_actions"]:
    print("-", rec)

print("\nPrevention:")
for rec in data["prevention"]:
    print("-", rec)
