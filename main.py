from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    pdf_file = request.files.get("pdf")

    if not pdf_file:
        return "No PDF uploaded", 400

    difficulty = request.form.get("difficulty")
    question_types = request.form.getlist("type")

    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages[:5]:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    text = text[:4000]

    # TEMP placeholders (no AI yet)
    analysis = text[:1000] + "..."
    study_plan = f"""
1. Read concepts carefully (Difficulty: {difficulty})
2. Practice {', '.join(question_types) if question_types else 'all'} questions
3. Revise formulas daily
4. Attempt mock tests every 3 days
"""
    exam = f"""
Q1. Explain the key concepts from the uploaded material.
Q2. Solve a numerical based on formulas found in the text.
Q3. Write short notes from the chapter.
"""

    return render_template(
        "index.html",
        success=True,
        difficulty=difficulty,
        question_types=question_types,
        analysis=analysis,
        study_plan=study_plan,
        exam=exam
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

