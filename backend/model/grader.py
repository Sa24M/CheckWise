# backend/model/grader.py
import os
import pandas as pd
import zipfile
import tempfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def grade_answer(zip_bytes, max_marks=10.0, uploads_dir=None):
    if uploads_dir is None:
        uploads_dir = tempfile.mkdtemp()
    else:
        os.makedirs(uploads_dir, exist_ok=True)

    # Save uploaded zip
    temp_zip_path = os.path.join(uploads_dir, "uploaded.zip")
    with open(temp_zip_path, "wb") as f:
        f.write(zip_bytes)

    # Extract zip
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(uploads_dir)

    # Locate answers folder
    answers_dir = None
    for root, dirs, _ in os.walk(uploads_dir):
        if "answers" in dirs:
            answers_dir = os.path.join(root, "answers")
            break

    if not answers_dir:
        raise FileNotFoundError("'answers' folder not found in uploaded zip")

    rows = []

    # Loop through question folders
    for q_folder in sorted(os.listdir(answers_dir)):
        q_path = os.path.join(answers_dir, q_folder)
        if not os.path.isdir(q_path):
            continue

        files_in_q = os.listdir(q_path)

        # Identify reference file
        reference_file = None
        for f in files_in_q:
            if "ref" in f.lower():
                reference_file = os.path.join(q_path, f)
                break

        if not reference_file:
            continue

        with open(reference_file, "r", encoding="utf-8") as rf:
            reference_text = rf.read().strip()

        # Compare all other files to reference using TF-IDF
        for f in files_in_q:
            file_path = os.path.join(q_path, f)
            if file_path == reference_file or not os.path.isfile(file_path):
                continue

            with open(file_path, "r", encoding="utf-8") as af:
                answer_text = af.read().strip()

            # TF-IDF similarity
            vectorizer = TfidfVectorizer().fit([reference_text, answer_text])
            tfidf_matrix = vectorizer.transform([reference_text, answer_text])
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

            marks = round(similarity_score * max_marks, 2)

            rows.append({
                "question": q_folder,
                "answer_file": f,
                "reference_file": os.path.basename(reference_file),
                "marks": marks
            })

    df = pd.DataFrame(rows)
    return df, uploads_dir
