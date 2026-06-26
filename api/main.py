from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from janome.tokenizer import Tokenizer
import joblib, os, sys, urllib.request, traceback, types

# --------------------------------------------------
# Janomeで mecab_tokenizer を再定義
# --------------------------------------------------
_janome = Tokenizer()

def mecab_tokenizer(text):
    return [token.surface for token in _janome.tokenize(text)]


# 【修正】上部にあった古い sys.modules['__main__'] の偽装記述はすべて削除しました


app = FastAPI()

origins = [
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/predict",
    "http://127.0.0.1:8000/docs",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str

TMP_DIR = "/tmp"
MODEL_PATH = os.path.join(TMP_DIR, "final_sentiment_model_v2.joblib")
VECTORIZER_PATH = os.path.join(TMP_DIR, "latest_vectorizer_v2.joblib")

SUPABASE_MODEL_URL = "https://mmsgymltwmcyfydwuzde.supabase.co/storage/v1/object/public/models/final_sentiment_model_v3.joblib"
SUPABASE_VECTORIZER_URL = "https://mmsgymltwmcyfydwuzde.supabase.co/storage/v1/object/public/models/latest_vectorizer_v3.joblib"

if not os.path.exists(MODEL_PATH):
    urllib.request.urlretrieve(SUPABASE_MODEL_URL, MODEL_PATH)

if not os.path.exists(VECTORIZER_PATH):
    urllib.request.urlretrieve(SUPABASE_VECTORIZER_URL, VECTORIZER_PATH)

# --------------------------------------------------
# モデル・ベクトル化器読込（一瞬だけ騙して即座に戻す安全領域）
# --------------------------------------------------
try:
    # 1. Vercelオリジナルの起動用 __main__ を安全な変数に避難させる
    original_main = sys.modules.get('__main__')

    # 2. joblibの逆シリアル化（デパイク）を騙すための専用ダミー空間を用意
    mock_main = types.ModuleType('__main__')
    mock_main.mecab_tokenizer = mecab_tokenizer
    
    # 3. この一瞬だけシステム上のメイン空間をダミーにすり替える
    sys.modules['__main__'] = mock_main
    sys.modules['tokenizer'] = mock_main

    # 4. ダミー空間がある状態で、joblibに新モデルファイルを読み込ませる
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    
    # 5. 【最重要】読み込みが成功したら、即座に退避させていたVercelのメイン空間に復元する
    if original_main:
        sys.modules['__main__'] = original_main

    print("✅ モデル読込成功")

except Exception as e:
    # 万が一エラーで落ちた場合も、後続のシステムを壊さないようにオリジナルの空間に戻す
    if 'original_main' in locals() and original_main:
        sys.modules['__main__'] = original_main
    print(f"❌ モデル読込失敗: {e}")
    traceback.print_exc()
    raise


@app.post("/predict", response_model=SentimentResponse)
def predict(request: TextRequest):
    # text_vector = vectorizer.transform([request.text])
    # prediction = model.predict(text_vector)[0]
    prediction = model.predict([request.text])[0]
    return {
        "text": request.text,
        "sentiment": "positive" if int(prediction) == 1 else "negative"
    }
