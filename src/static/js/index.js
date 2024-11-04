const subdivision = document.getElementById("subdivision");
const threshold = document.getElementById("threshold");
const input_img = document.getElementById("input_image");
let uploadComplete = false;

// Metodo que actualiza el label de los sliders============================================================================================
function UpdateLabel() {
    const th_label = document.getElementById("threshold_label");
    const subdiv_label = document.getElementById("subdivision_label");

    th_label.innerText = `Threshold: ${threshold.value}`;
    subdiv_label.innerText = `Subdivision: ${subdivision.value}`;
}

// Metodo que sube la imagen al servidor===================================================================================================
async function updateImage() {
    const file = input_img.files[0];
    if (!file) {
        console.log("No file selected");
        return;
    }

    // Se deshabilitan los controles durante la carga======================================================================================
    disableControls(true);

    try {
        // Se crea y envia el FormData=====================================================================================================
        const forumsito = new FormData();
        forumsito.append("image", file);

        // Se espera a que se complete la subida===========================================================================================
        const response = await fetch("/upload", {
            method: "POST",
            body: forumsito,
        });

        // Validacion de la respuesta======================================================================================================
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        console.log("Upload complete:", result);

        // Se actualiza el valor máximo de la subdivisión==================================================================================
        console.log(result['size']);
        subdivision.max = Math.log2(result['size']);

        // Se actualiza la imagen original=================================================================================================
        const originalimg = document.getElementById("originalimg");
        originalimg.src = URL.createObjectURL(file);

        // Se Marca la subida como completada==============================================================================================
        uploadComplete = true;

    } catch (error) {
        console.error("Error during upload:", error);
        alert("Error al subir la imagen. Por favor, intente nuevamente.");
        uploadComplete = false;

    } finally {
        // Se habilitan los controles después de la carga==================================================================================
        disableControls(false);
    }
}

// Metodo que comprime la imagen===========================================================================================================
async function compression() {
    // Se verifica si la imagen se subió correctamente=====================================================================================
    if (!uploadComplete) {
        alert(
            "Por favor, espere a que la imagen se suba completamente antes de comprimir."
        );
        return;
    }

    // Se obtienen los valores de los sliders==============================================================================================
    const subdiv = subdivision.value;
    const th = threshold.value;

    // Se deshabilitan controles durante la compresión=====================================================================================
    disableControls(true);

    try {
        // Se espera a que se complete la compresión=======================================================================================
        const response = await fetch(`/compression?subdiv=${subdiv}&th=${th}`);

        // Validación de la respuesta======================================================================================================
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Se actualiza la imagen comprimida===============================================================================================
        const data = await response.blob();
        const compressedimg = document.getElementById("compressed");
        compressedimg.src = URL.createObjectURL(data);

    } catch (error) {
        console.error("Error during compression:", error);
        alert("Error al comprimir la imagen. Por favor, intente nuevamente.");
    } finally {
        // Se habilitan los controles después de la compresión=============================================================================
        disableControls(false);
    }
}

// Metodo que deshabilita/ habilita los controles===========================================================================================
function disableControls(disabled) {
    input_img.disabled = disabled;
    subdivision.disabled = disabled;
    threshold.disabled = disabled;
}
