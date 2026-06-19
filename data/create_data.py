import csv

# 学習、テスト用の感情データ
positives = ["とても面白いです", "簡単でわかりやすい", "買ってよかったです"]
negatives = ["つまらないです", "難しくて挫折しました", "お金の無駄でした"]

# リスト内包表記とデータの結合
# 1 = positives, 0 = negatives
dataset = [(text, 1) for text in positives] + [(text, 0) for text in negatives]

# CSVファイルへの書き出し
with open("data/sentiment_dataset.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])    # ヘッダー
    writer.writerows(dataset)