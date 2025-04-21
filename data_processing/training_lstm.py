import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from metrics_storage import save_metrics_to_mysql


def train_model(texts, labels):
    max_words = 5000
    max_len = 100
    embedding_dim = 64

    tokenizer = Tokenizer(num_words=max_words, lower=True)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=max_len)

    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, labels, test_size=0.2, random_state=42
    )

    model = Sequential()
    model.add(Embedding(max_words, embedding_dim, input_length=max_len))
    model.add(SpatialDropout1D(0.2))
    model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=3, batch_size=64, validation_split=0.1, verbose=2)

    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)

    accuracy = accuracy_score(y_test, y_pred)
    print("准确率：", accuracy)
    report = classification_report(y_test, y_pred, output_dict=True)
    print("分类报告：\n", classification_report(y_test, y_pred))

    # 保存模型结构和权重
    model.save("data_processing/models/lstm_model.h5")
    # 保存 Tokenizer
    import pickle
    with open("data_processing/models/lstm_tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    # 提取宏平均指标并写入数据库
    macro_avg = report["macro avg"]
    metrics = {
        "Precision": round(macro_avg["precision"], 3),
        "Recall": round(macro_avg["recall"], 3),
        "F1-score": round(macro_avg["f1-score"], 3)
    }
    save_metrics_to_mysql("LSTM", metrics)


def main():
    df = pd.read_csv("data_processing/data/train.csv")
    df = df[df["sentiment"] != 2]  # 只保留二分类（0-负面，2-正面）
    df["sentiment"] = df["sentiment"].replace(2, 1)
    train_model(df["text"], df["sentiment"].astype(int))


if __name__ == "__main__":
    main()
