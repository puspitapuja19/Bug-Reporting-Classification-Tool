from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset (always from same folder as this file)
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "bug_data.csv")

X = df["description"]
y = df["category"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Check accuracy
preds = model.predict(X_test_vec)
print(f"Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%")

# Save model
joblib.dump(model, "bug_classifier.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model saved!")