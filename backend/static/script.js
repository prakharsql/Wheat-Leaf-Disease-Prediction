const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const result = document.getElementById("result");
const treatment = document.getElementById("treatment");
const loader = document.getElementById("loader");

// Image preview
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];
    if (file) {
        previewImage.src = URL.createObjectURL(file);
        previewImage.style.display = "block";
        result.innerText = "";
        treatment.innerText = "";
    }
});

async function predict() {
    if (imageInput.files.length === 0) {
        alert("Please upload an image");
        return;
    }

    const formData = new FormData();
    formData.append("file", imageInput.files[0]);

    loader.style.display = "block";
    result.innerText = "Analyzing image...";
    treatment.innerText = "";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        result.innerText =
            `Disease: ${data.disease} | Confidence: ${data.confidence}%`;

        treatment.innerText =
            `Treatment: ${data.treatment}`;

    } catch (error) {
        result.innerText = "Prediction failed. Try another image.";
    } finally {
        loader.style.display = "none";
    }
}
