const analyzeButton = document.getElementById("analyzeButton");
// ボタンの中にある「テキスト」と「スピナー」をそれぞれ特定する
const buttonText = analyzeButton.querySelector(".button-text");
const spinner = analyzeButton.querySelector(".spinner");

analyzeButton.addEventListener("click", async () => {
    const text = document.getElementById("textInput").value;

    if (!text.trim()) {
        alert("文章を入力してください");
        return;
    }

    // 1. ローディング状態にする
    analyzeButton.disabled = true;
    buttonText.textContent = "分析中...";
    spinner.classList.remove("hidden"); // スピナーを表示

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`サーバエラー: ${response.status}`)
        }

        const data = await response.json();
        document.getElementById("resultArea").textContent = `感情: ${data.sentiment}`;

    } catch (error) {
        console.error(error);
        document.getElementById("resultArea").textContent = "エラーが発生しました";
    } finally {
        // 2. 終わったら元の状態に戻す
        analyzeButton.disabled = false;
        buttonText.textContent = "分析";
        spinner.classList.add("hidden"); // スピナーを隠す
    }
});