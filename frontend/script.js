async function analyzeLeaf() {
    const fileInput = document.getElementById("leafImage");
    const resultBox = document.getElementById("resultBox");

    if (!fileInput.files.length) {
        alert("Please upload a leaf image");
        return;
    }

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    resultBox.style.display = "block";
    resultBox.innerHTML = "🔍 Analyzing leaf...";

    try {
        /* 1️⃣ Call Disease API */
        const diseaseRes = await fetch("http://127.0.0.1:5000/predict_disease", {
            method: "POST",
            body: formData
        });
        const diseaseData = await diseaseRes.json();

        /* 2️⃣ If disease is detected */
        if (diseaseData.prediction !== "Healthy_leaf") {
            resultBox.innerHTML = `
                <h3>🦠 Disease Detected</h3>
                <b>${diseaseData.prediction}</b><br><br>
                <b>Cause:</b> ${diseaseData.cause}<br><br>
                <b>Recommended Actions:</b>
                <ul>${diseaseData.recommendations.map(r => `<li>${r}</li>`).join("")}</ul>
            `;
            return;
        }

        /* 3️⃣ Call Nutrient API only if disease is healthy */
        const nutrientRes = await fetch("http://127.0.0.1:5000/predict_nutrient", {
            method: "POST",
            body: formData
        });
        const nutrientData = await nutrientRes.json();

        if (nutrientData.prediction !== "Healthy") {
            resultBox.innerHTML = `
                <h3>🌿 Nutrient Deficiency Detected</h3>
                <b>${nutrientData.prediction}</b><br><br>
                <b>Recommended Actions:</b>
                <ul>${nutrientData.recommendations.map(r => `<li>${r}</li>`).join("")}</ul>
            `;
            return;
        }

        /* 4️⃣ Healthy */
        resultBox.innerHTML = `
            <h3>✅ Crop is Healthy</h3>
            No disease or nutrient deficiency detected.
        `;

    } catch (error) {
        resultBox.innerHTML = "❌ Error analyzing leaf. Please try again.";
        console.error(error);
    }
}
