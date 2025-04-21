import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from metrics_storage import save_metrics_to_mysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
    test_df = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))
    return train_df, test_df

def train_model(train_df, test_df):
    X_train, y_train = train_df["text"], train_df["sentiment"]
    X_test, y_test = test_df["text"], test_df["sentiment"]

    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    print("准确率：", accuracy_score(y_test, y_pred))
    print("分类报告：\n", classification_report(y_test, y_pred))

    # 提取并保存指标
    report = classification_report(y_test, y_pred, output_dict=True)
    macro_avg = report["macro avg"]
    metrics = {
        "Precision": round(macro_avg["precision"], 3),
        "Recall": round(macro_avg["recall"], 3),
        "F1-score": round(macro_avg["f1-score"], 3)
    }

    save_metrics_to_mysql("Logistic Regression", metrics)

    joblib.dump(clf, os.path.join(MODEL_DIR, "logistic_model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer_logistic.pkl"))
    print("逻辑回归模型和向量器已保存。")

if __name__ == "__main__":
    train_df, test_df = load_data()
    train_model(train_df, test_df)