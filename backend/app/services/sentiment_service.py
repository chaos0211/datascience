import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "data_processing", "models", "naive_bayes_model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "data_processing", "models", "tfidf_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

def analyze_sentiment(text):
    if not text.strip():
        return {"error": "Empty input"}

    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]

    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    return {
        "text": text,
        "sentiment": label_map.get(pred, "unknown"),
        "code": int(pred)
    }