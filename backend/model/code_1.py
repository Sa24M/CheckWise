# backend/model/code_1.py
import os
import nltk
import joblib
import numpy as np

# Ensure NLTK resources
NLTK_RESOURCES = [
    "punkt", "punkt_tab", "stopwords", "wordnet",
    "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"
]
for res in NLTK_RESOURCES:
    try:
        nltk.data.find(res)
    except LookupError:
        nltk.download(res)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOP_WORDS = set(stopwords.words("english"))
_LEMMA = WordNetLemmatizer()

# =====================
# Preprocessing
# =====================
def preprocess_text(text: str) -> str:
    """
    Cleans and lemmatizes text for the ML model.
    """
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in STOP_WORDS]
    tokens = [_LEMMA.lemmatize(t) for t in tokens]
    return " ".join(tokens)


# =====================
# Model Loading
# =====================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "trained_model.pkl")

def load_model():
    """
    Loads the trained ML model from disk.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    return model


# =====================
# Scoring
# =====================
def predict_score(reference: str, answer: str, max_marks: float = 10.0) -> float:
    """
    Given preprocessed reference and answer strings, predict similarity/marks.
    Your trained model should output a score between 0 and 1.
    """
    # Example: model expects [ref, ans] vectorized together
    # Replace this with your actual feature extraction logic
    from sklearn.feature_extraction.text import TfidfVectorizer

    vect = TfidfVectorizer()
    tfidf = vect.fit_transform([reference, answer])
    sim = float((tfidf[0] @ tfidf[1].T).toarray()[0][0])

    # If your model predicts based on features:
    # features = extract_features(reference, answer)
    # sim = model.predict(features)[0]

    marks = sim * max_marks
    return marks
