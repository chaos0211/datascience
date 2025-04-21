import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib, os

DATA_DIR = "data"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
    test_df = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))
    return train_df, test_df


def train_model(train_df, test_df):
    X_train, y_train = train_df["text"], train_df["sentiment"]
    X_test, y_test = test_df["text"], test_df["sentiment"]

    # 向量化文本数据
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 模型训练
    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)

    # 预测与评估
    y_pred = clf.predict(X_test_vec)
    print("准确率：", accuracy_score(y_test, y_pred))
    print("分类报告：\n", classification_report(y_test, y_pred))

    # 保存模型和向量器
    joblib.dump(clf, os.path.join(MODEL_DIR, "naive_bayes_model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
    print("模型和向量器已保存。")

def evaluate_model(X_test, y_test):
    clf = joblib.load('models/sentiment_model.pkl')
    vectorizer = joblib.load('models/vectorizer.pkl')

    X_test_vec = vectorizer.transform(X_test)
    y_pred = clf.predict(X_test_vec)
    print(classification_report(y_test, y_pred))

def main():
    # train_df = load_data('data')
    train_df, test_df = load_data()

    train_model(train_df, test_df)

if __name__ == '__main__':
    main()