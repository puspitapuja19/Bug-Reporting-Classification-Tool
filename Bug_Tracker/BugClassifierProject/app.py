from pathlib import Path
from collections import deque
from flask import Flask, request, render_template
import joblib

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "bug_classifier.pkl"
VECTORIZER_PATH = BASE_DIR.parent / "vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Simple in-memory history (last 10)
history = deque(maxlen=10)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None
    text = ""

    if request.method == "POST":
        text = request.form.get("bug_text", "")
        if text.strip():
            vec = vectorizer.transform([text])
            proba = model.predict_proba(vec)[0]
            pred_idx = proba.argmax()
            prediction = model.classes_[pred_idx]
            confidence = round(proba[pred_idx] * 100, 2)

            history.appendleft({
                "text": text,
                "prediction": prediction,
                "confidence": confidence
            })

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        text=text,
        history=list(history)
    )

if __name__ == "__main__":
    app.run(debug=True)