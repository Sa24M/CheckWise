# 📘 CheckWise -- Automated Answer Evaluation System

CheckWise is a web-based application that automatically evaluates
student answers by comparing them with reference answers using **TF-IDF
similarity**.\
It provides an interactive frontend for uploading answer ZIP files and
generates a marks report for each student response.


------------------------------------------------------------------------

## 🚀 Features

-   Upload a **ZIP file** containing student answers.
-   Extracts and compares answers with the provided **reference
    answer**.
-   Uses **TF-IDF + Cosine Similarity** to calculate marks.
-   Generates a **downloadable CSV report** of marks.
-   Interactive, responsive frontend with file upload and results table.
-   Deployable on **Render / Heroku** for cloud hosting.

  ------------------------------------------------------------------------
  
<img width="1729" height="887" alt="Screenshot (112)" src="https://github.com/user-attachments/assets/010dc8f2-abc4-4bd5-965f-630c1aa30a8f" />

------------------------------------------------------------------------

## 📂 Project Structure

    answer_evaluator/
    │── backend/
    │   │── app.py              # Flask backend entry point
    │   │── model/
    │   │   ├── grader.py       # Core grading logic (TF-IDF similarity)
    │   │── templates/
    │   │   └── index.html      # Frontend HTML
    │   │── static/
    │   │   ├── css/            # Stylesheets
    │   │   └── js/             # JavaScript files
    │   │── uploads/            # Uploaded ZIP files (temporary storage)
    │── results/                # Generated evaluation reports
    │── requirements.txt        # Python dependencies
    │── README.md               # Project documentation

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone https://github.com/<your-username>/CheckWise.git
cd CheckWise
```

### 2. Create a virtual environment

``` bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scriptsctivate      # On Windows
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Running Locally

``` bash
cd backend
python app.py
```

Now open <http://127.0.0.1:5000> in your browser.

------------------------------------------------------------------------

## ☁️ Deployment on Render

1.  Push code to GitHub.
2.  On [Render](https://render.com), create a **Web Service**:
    -   Runtime: Python

    -   Start Command:

            gunicorn backend.app:app
3.  Make sure `gunicorn` is listed in `requirements.txt`.
4.  Deploy 🎉

------------------------------------------------------------------------

## 📊 Example Output

-   Upload a ZIP with structure:

```{=html}
<!-- -->
```
    answers/
       Q1/
          ref.txt
          student1.txt
          student2.txt
       Q2/
          ref.txt
          student1.txt

-   Generated report (CSV):

```{=html}
<!-- -->
```
    question,answer_file,reference_file,marks
    Q1,student1.txt,ref.txt,8.7
    Q1,student2.txt,ref.txt,6.3
    Q2,student1.txt,ref.txt,9.1

------------------------------------------------------------------------

## 🔮 Future Enhancements

-   Use **BERT embeddings** for semantic similarity.
-   Support **PDF/DOCX uploads** instead of plain text.
-   Role-based dashboards (teacher & student views).
-   Graphical analytics of performance.

------------------------------------------------------------------------

## 👩‍💻 Author

**Sakshi Mishra**\
Project for automated answer evaluation using NLP & Web deployment.
