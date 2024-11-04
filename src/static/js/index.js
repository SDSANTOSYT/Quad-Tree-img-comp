const subdivision = document.getElementById("subdivision");
const threshold = document.getElementById("threshold");
const input_img = document.getElementById("input_image");
let uploadComplete = false;

async function updateImage() {
    const file = input_img.files[0];
    if (!file) {
        console.log("No file selected");
        return;
    }

    // Deshabilitar controles durante la carga
    disableControls(true);

    try {
        // Crear y enviar el FormData
        const forumsito = new FormData();
        forumsito.append("image", file);

        // Esperar a que se complete la subida
        const response = await fetch("/upload", {
            method: "POST",
            body: forumsito,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Upload complete:", result);

        // Actualizar la imagen original
        const originalimg = document.getElementById("originalimg");
        originalimg.src = URL.createObjectURL(file);

        // Marcar la subida como completada
        uploadComplete = true;
    } catch (error) {
        console.error("Error during upload:", error);
        alert("Error al subir la imagen. Por favor, intente nuevamente.");
        uploadComplete = false;
    } finally {
        // Habilitar controles después de la carga
        disableControls(false);
    }
}

async function compression() {
    // Verificar si la imagen se subió correctamente
    if (!uploadComplete) {
        alert(
            "Por favor, espere a que la imagen se suba completamente antes de comprimir."
        );
        return;
    }

    const subdiv = subdivision.value;
    const th = threshold.value;
    const th_label = document.getElementById("threshold_label");
    th_label.innerText = `Threshold: ${th}`;

    // Deshabilitar controles durante la compresión
    disableControls(true);

    try {
        const response = await fetch(`/compression?subdiv=${subdiv}&th=${th}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.blob();
        const compressedimg = document.getElementById("compressed");
        compressedimg.src = URL.createObjectURL(data);
    } catch (error) {
        console.error("Error during compression:", error);
        alert("Error al comprimir la imagen. Por favor, intente nuevamente.");
    } finally {
        // Habilitar controles después de la compresión
        disableControls(false);
    }
}

function disableControls(disabled) {
    // Deshabilitar/habilitar los controles durante el procesamiento
    input_img.disabled = disabled;
    subdivision.disabled = disabled;
    threshold.disabled = disabled;
}
