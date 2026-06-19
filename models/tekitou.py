import joblib
from janome.tokenizer import Tokenizer

# 1. 保存時と同じカスタムトークナイザーを定義
t = Tokenizer()
def tokenize(text):
    return [token.surface for token in t.tokenize(text)]

def run_inference(texts):
    # 2. モデルとベクトル化器の読み込み
    # 同じディレクトリに .joblib ファイルがある前提です
    try:
        vectorizer = joblib.load('./models/vectorizer.joblib')
        model = joblib.load('./models/model.joblib')
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # 3. 予測の実行
    vecs = vectorizer.transform(texts)
    preds = model.predict(vecs)

    # 4. 結果の出力
    for text, pred in zip(texts, preds):
        label = "ポジティブ" if pred == 1 else "ネガティブ"
        print(f"[{label}] {text}")

if __name__ == "__main__":
    with open("./models/test.txt") as f:
        inputs = f.readlines()
    sample_inputs = []
    for inputs in inputs:
        sample_inputs.append(inputs.replace("\n", ""))
    run_inference(sample_inputs)