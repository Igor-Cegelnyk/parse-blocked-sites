document.addEventListener("DOMContentLoaded", () => {
    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");

    uploadBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Будь ласка, оберіть файл для завантаження");
            return;
        }

        uploadBtn.disabled = true;
        uploadBtn.textContent = "Завантаження...";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/filesearch/", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Помилка при завантаженні файлу");
            }

            alert("Функціонал в розробці");
            // const data = await response.json();
            // alert(data.message || "Файл успішно завантажено");
        } catch (err) {
            console.error(err);
            alert("Не вдалося завантажити файл");
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.textContent = "🔼 Завантажити";
            fileInput.value = "";
        }
    });
});