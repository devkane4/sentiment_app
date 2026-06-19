# TF = 文書内でその単語が何回出るか
# IDF = 多くの文書に出る単語(の、が等)の重要性を下げる
from sklearn.feature_extraction.text import TfidfVectorizer
corpus = ["私は AI が 好き です", "AI プログラミング は 楽しい です"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names_out())
print(X.toarray())