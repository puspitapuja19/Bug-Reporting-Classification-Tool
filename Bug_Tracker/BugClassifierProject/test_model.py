from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR.parent / "bug_classifier.pkl")
vectorizer = joblib.load(BASE_DIR.parent / "vectorizer.pkl")

test_input = ["the login page is broken"]
vec_input = vectorizer.transform(test_input)
prediction = model.predict(vec_input)

print(f"Predicted category: {prediction[0]}")