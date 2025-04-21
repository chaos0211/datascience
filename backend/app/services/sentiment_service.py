import joblib
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

MODEL_PATH = os.path.join(BASE_DIR, 'data_processing', 'data_processing', 'models', 'lstm_model.h5')
TOKENIZER_PATH = os.path.join(BASE_DIR, 'data_processing', 'data_processing', 'models', 'lstm_tokenizer.pkl')

model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as f:
    tokenizer = pickle.load(f)

def analyze_sentiment(text):
    if not text.strip():
        return {"error": "Empty input"}

    sequences = tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(sequences, maxlen=100)
    pred_prob = model.predict(padded_seq)
    pred = np.argmax(pred_prob, axis=1)[0]

    print("输出Predicted probs:", pred_prob, pred)
    # 输出Predicted probs: [[1.4727230e-01 8.5272771e-01 1.1006053e-10]]  代表85%的概率是 1 符合预期

    label_map = {0: "negative", 1: "positive" }
    return {
        "text": text,
        "sentiment": label_map.get(pred, "unknown"),
        "code": int(pred),
        "probabilities": {
            "negative": round(float(pred_prob[0][0]) * 100, 2),
            "positive": round(float(pred_prob[0][1]) * 100, 2)
        }
    }