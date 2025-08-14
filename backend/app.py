from flask import Flask, request, jsonify, render_template
import os
from backend.model.grader import grade_answer

app = Flask(__name__, template_folder="templates")

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_zip", methods=["POST"])
def upload_zip():
    try:
        if "zip_file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        uploaded_file = request.files["zip_file"]
        max_marks = float(request.form.get("max_marks", 10.0))

        df, _ = grade_answer(uploaded_file.read(), max_marks, uploads_dir=UPLOADS_DIR)

        # If no results found, return empty array instead of None
        if df.empty:
            return jsonify([])

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
