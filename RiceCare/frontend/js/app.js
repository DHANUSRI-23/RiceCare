const BASE_URL = "http://127.0.0.1:5000";

// ---------------------- DISEASE ----------------------
async function predictDisease() {
    const fileInput = document.getElementById("disease-image");
    const file = fileInput.files[0];
    if (!file) { alert("Please upload an image!"); return; }

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch(`${BASE_URL}/predict_disease`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("disease-result").classList.remove("d-none");
    document.getElementById("disease-name").innerText = data.prediction || "N/A";
    document.getElementById("disease-cause").innerText = data.cause || "N/A";

    const actionsList = document.getElementById("disease-actions");
    actionsList.innerHTML = "";
    if (data.recommendations) {
        data.recommendations.forEach(rec => {
            const li = document.createElement("li");
            li.innerText = rec;
            actionsList.appendChild(li);
        });
    }
}

// ---------------------- NUTRIENT ----------------------
async function predictNutrient() {
    const fileInput = document.getElementById("nutrient-image");
    const file = fileInput.files[0];
    if (!file) { alert("Please upload an image!"); return; }

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch(`${BASE_URL}/predict_nutrient`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("nutrient-result").classList.remove("d-none");
    document.getElementById("nutrient-name").innerText = data.prediction || "N/A";

    const actionsList = document.getElementById("nutrient-actions");
    actionsList.innerHTML = "";
    if (data.recommendations) {
        data.recommendations.forEach(rec => {
            const li = document.createElement("li");
            li.innerText = rec;
            actionsList.appendChild(li);
        });
    }
}

// ---------------------- YIELD ----------------------
async function predictYield() {
    const district = document.getElementById("district").value;
    const season = document.getElementById("season").value;
    const area = document.getElementById("area").value;

    if (!district || !season || !area) {
        alert("Please fill all fields!");
        return;
    }

    const payload = { district, season, area: parseFloat(area) };

    const res = await fetch(`${BASE_URL}/predict_yield`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    document.getElementById("yield-result").classList.remove("d-none");
    document.getElementById("yield-value").innerText = data.predicted_yield || "N/A";

    const weatherSummary = `Avg Temp: ${data.weather.avg_temp || "N/A"} °C, 
Max Temp: ${data.weather.max_temp || "N/A"} °C, 
Min Temp: ${data.weather.min_temp || "N/A"} °C, 
Humidity: ${data.weather.humidity || "N/A"} %, 
Rainfall: ${data.weather.rainfall || "N/A"} mm, 
Solar Radiation: ${data.weather.solar_radiation || "N/A"}`;
    document.getElementById("weather-summary").innerText = weatherSummary;

    const actionsList = document.getElementById("yield-actions");
    actionsList.innerHTML = "";
    if (data.recommendations) {
        data.recommendations.forEach(rec => {
            const li = document.createElement("li");
            li.innerText = rec;
            actionsList.appendChild(li);
        });
    }
}
