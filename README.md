🐞 Bug Reporting & Classification Tool

Describe a bug in plain English — get its category in milliseconds. An ML-powered triage assistant that classifies bug reports into UI, Backend, Database, Performance, or Security, paired with a secure FastAPI bug-tracking backend.

📖 Overview

In every engineering team, someone has to read each incoming bug report and decide who should look at it. This project automates that first step.

The repository contains two parts that work together:

Bug Classification AI – a Flask web app that uses a TF‑IDF + Logistic Regression model to predict a bug's category and confidence score from free-text descriptions.
Bug Tracker API – a FastAPI backend with JWT authentication, rate limiting, and a MySQL database to store and retrieve bug reports per user.
✨ Features
🤖 Classification Web App
Instant category prediction with a confidence percentage
Clean, responsive UI built with Tailwind CSS
🌗 Dark / light mode toggle
🕘 Prediction history (last 10 predictions)
Loading spinner, hover, and focus micro-animations
Trained on a balanced dataset across 5 categories
🔐 Bug Tracker API
User registration & login with bcrypt password hashing
JWT authentication (15-minute access tokens)
Rate limiting with SlowAPI (e.g. login: 5/min, create bug: 10/min)
Password complexity validation (min 8 chars, uppercase, digit)
Pagination (skip / limit, capped at 100)
Per-user data isolation — users only see their own bugs
Filter bugs by category
Connection pooling with SQLAlchemy
🧠 How the Model Works
Bug description  ──►  TF‑IDF Vectorizer  ──►  Logistic Regression  ──►  Category + Confidence
Item	Detail
Vectorizer	TfidfVectorizer
Classifier	LogisticRegression
Categories	UI, Backend, Database, Performance, Security
Training data	bug_data.csv — 125 samples (25 per class)
Evaluation set	eval_set.csv — 50 samples (10 per class)
Hard cases	borderline_samples.csv — 25 ambiguous, cross-category reports
Split	80 / 20 train-test, random_state=42

The borderline samples are deliberately tricky bugs, such as "Submit endpoint returns 200 but bug never shows in list", that sit between two categories. They make a great stress test for the model.

🗂️ Project Structure
Bug-Reporting-Classification-Tool/
├── bug_classifier.pkl        # Trained Logistic Regression model
├── vectorizer.pkl            # Fitted TF‑IDF vectorizer
├── bug_data.csv              # Training dataset
├── eval_set.csv              # Evaluation dataset
├── borderline_samples.csv    # Ambiguous edge-case samples
│
├── train_model.py            # Train & save the model
├── test_model.py             # Quick CLI sanity check
│
├── app.py                    # Flask app (classification UI)
├── templates/
│   └── index.html            # Jinja2 + Tailwind template
├── static/
│   ├── style.css             # Animations & custom styles
│   └── app.js                # Loading spinner logic
│
├── main.py                   # FastAPI app (Bug Tracker API)
├── auth.py                   # JWT creation & verification
├── database.py               # SQLAlchemy engine & session
├── models.py                 # User & Bug ORM models
├── schemas.py                # Pydantic request/response schemas
├── utils.py                  # Password hashing helpers
├── tables.py                 # Creates DB tables
└── requirements.txt

📌 index.html must live in a templates/ folder and style.css / app.js in a static/ folder — this is what Flask expects.

🚀 Getting Started
1. Clone the repository
bash
git clone https://github.com/puspitapuja19/Bug-Reporting-Classification-Tool.git
cd Bug-Reporting-Classification-Tool
2. Create a virtual environment
bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
pip install flask scikit-learn pandas joblib
4. (Optional) Retrain the model
bash
python train_model.py

This prints the test accuracy and regenerates bug_classifier.pkl and vectorizer.pkl.

5. Run the classification web app
bash
python app.py

Open http://127.0.0.1:5000 and describe a bug.

6. Quick model test from the terminal
bash
python test_model.py
🔌 Running the Bug Tracker API
Set up MySQL
sql
CREATE DATABASE bug_tracker;

Update DATABASE_URL in database.py with your own credentials, then create the tables:

bash
python tables.py
Start the server
bash
uvicorn main:app --reload

Interactive docs are available at http://127.0.0.1:8000/docs.

API Endpoints
Method	Endpoint	Auth	Rate limit	Description
GET	/	❌	—	Welcome message
POST	/register	❌	—	Create a new user
POST	/login	❌	5/min	Get a JWT access token
POST	/bugs	✅	10/min	Create a bug report
GET	/bugs	✅	30/min	List your bugs (paginated)
GET	/bugs/{category}	✅	30/min	List your bugs by category
Example
bash
# Register
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "puspita", "password": "StrongPass1"}'

# Login
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "puspita", "password": "StrongPass1"}'

# Create a bug (use the token from login)
curl -X POST http://127.0.0.1:8000/bugs \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Login fails", "description": "Login button does nothing on Chrome", "category": "UI"}'
🛡️ Security Notes

Before deploying or sharing this project publicly, please:

Move secrets to environment variables. SECRET_KEY (in auth.py) and DATABASE_URL (in database.py) are currently hardcoded. Store them in a .env file (already supported via python-dotenv) and add .env to .gitignore.
Never commit real database passwords to a public repository.
Disable debug=True in app.py for production.
Restrict CORS origins to your real frontend domains.
🗺️ Roadmap
 Connect the classifier to the API so bugs are auto-categorized on creation
 Expand the dataset with real-world bug reports
 Add evaluation metrics (precision, recall, F1, confusion matrix) using eval_set.csv
 Try alternative models (Linear SVM, Naive Bayes, transformer embeddings)
 Add severity / priority prediction
 Dockerize the whole stack
 Unit tests and CI with GitHub Actions
🤝 Contributing

Contributions, ideas, and bug reports are welcome!

Fork the repository
Create a feature branch: git checkout -b feature/amazing-idea
Commit your changes: git commit -m "Add amazing idea"
Push to the branch: git push origin feature/amazing-idea
Open a Pull Request
👩‍💻 Author

Puspita Nandi — @puspitapuja19

If you found this project useful, consider giving it a ⭐ — it really helps!
