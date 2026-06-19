# /Documents/sentiment_app/apiをカレントディレクトリにして、
# uv run uvicorn main:app --reload を実行
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api import tokenizer
import joblib
import os
import sys

app = FastAPI()

sys.modules['tokenizer'] = tokenizer

# --------------------
# 許可したいオリジンのリスト
# --------------------
origins = [
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/predict",
    "http://127.0.0.1:8000/docs",
]

# --------------------
# ミドルウェアの追加
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,    #許可するオリジンのリスト
    allow_methods = ["*"],    # 許可するHTTPメソッド(GET, POSTなど)
    allow_headers = ["*"],    # 許可するHTTPヘッダー
)

# --------------------
# リクエストデータ定義
# --------------------
class TextRequest(BaseModel):
    text: str


# --------------------
# レスポンスの型定義（新しく追加）
# --------------------
class SentimentResponse(BaseModel):
    text: str
    sentiment: str


# --------------------
# モデル・ベクトル化器読込
# --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))    # api/main.pyがあるディレクトリの絶対パスを取得
MODEL_DIR = os.path.join(BASE_DIR, "..", "models", "model.joblib")   # api/ から見て、ひとつ上の階層のmodels/model.joblib
VECTORIZER_DIR = os.path.join(BASE_DIR, "..", "models", "vectorizer.joblib") 

model = joblib.load(MODEL_DIR)
vectorizer = joblib.load(VECTORIZER_DIR)


# --------------------
# 感情分析エンドポイント
# --------------------
@app.post("/predict", response_model=SentimentResponse)
def predict(request: TextRequest):
    # テキストを特徴量に変換
    text_vector = vectorizer.transform([request.text])

    # 予測
    prediction = model.predict(text_vector)[0]

    # 結果返却
    return {
        "text": request.text,
        "sentiment": "positive" if int(prediction) == 1 else "negative"
    }