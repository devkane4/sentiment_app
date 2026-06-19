import requests

request_text = "とても素晴らしい"

URL = "http://localhost:8000/predict"
PAYLOAD = {"text": request_text}

try:
    response = requests.post(URL, json=PAYLOAD)

    if response.status_code == 200:
        result = response.json()
        
        print(f"入力: {result.get("text")}")
        match result.get("sentiment"):
            case "positive":
                print(f"判定結果: {result.get("sentiment")}")
                print("ポジティブな内容です")
            case "negative":
                print(f"判定結果: {result.get("sentiment")}")
                print("ネガティブな内容です")
            case _:
                print("エラーが発生しました", result.get("sentiment"))

    else:
        print(f"エラーが発生しました（ステータスコード: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("APIサーバーが起動していません。uvicorn が動いているか確認してください。")