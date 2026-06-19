document.getElementById("analyzeButton").addEventListener("click", async () => {
    const text = document.getElementById("textInput").value;

    if (!text.trim()) {
        alert("文章を入力してください");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        document.getElementById("resultArea").textContent =
            `感情: ${data.sentiment}`;

    } catch (error) {
        console.error(error);

        document.getElementById("resultArea").textContent =
            "エラーが発生しました";
    }
});