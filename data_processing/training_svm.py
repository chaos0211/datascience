import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib
from metrics_storage import save_metrics_to_mysql


def train_model(texts, labels):
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', LinearSVC())
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("准确率：", accuracy)

    report = classification_report(y_test, y_pred, output_dict=True)
    print("分类报告：\n", classification_report(y_test, y_pred))

    # 保存模型和向量器
    joblib.dump(pipeline, 'data_processing/models/svm_model.pkl')

    # 保存指标到 MySQL
    macro_avg = report["macro avg"]
    metrics = {
        "Precision": round(macro_avg["precision"], 3),
        "Recall": round(macro_avg["recall"], 3),
        "F1-score": round(macro_avg["f1-score"], 3)
    }
    save_metrics_to_mysql("SVM", metrics)


def main():
    df = pd.read_csv("data/train.csv")
    train_model(df["text"], df["sentiment"])


if __name__ == "__main__":
    main()
