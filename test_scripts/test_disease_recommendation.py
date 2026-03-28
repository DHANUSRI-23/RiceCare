import requests

url = "http://127.0.0.1:5000/predict_disease"

image_path = r"C:\Crop Project\Combined modal\Leaves Images split\train\Leaf_Blast\Blast_46.jpg"

files = {"image": open(image_path, "rb")}

response = requests.post(url, files=files)
data = response.json()

print("\nDISEASE + RECOMMENDATION TEST")

print(f"\nDetected Disease: {data['detected_disease']}")

print("\nCause:")
print(data["cause"])

print("\nRecommended Actions:")
for rec in data["recommended_actions"]:
    print("-", rec)

print("\nPrevention:")
for rec in data["prevention"]:
    print("-", rec)
