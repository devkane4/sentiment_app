document.getElementById("analyzeButton").addEventListener("click", async () => {
    const text = document.getElementById("textInput").value;

    if (!text.trim()) {
        alert("文章を入力してください");
        return;
    }

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        if (!response.ok) {
            throw new Error(`サーバエラー: ${response.status}`)
        }

        const data = await response.json();

        document.getElementById("resultArea").textContent =
            `感情: ${data.sentiment}`;

    } catch (error) {
        console.error(error);

        document.getElementById("resultArea").textContent =
            "エラーが発生しました";
    }
});