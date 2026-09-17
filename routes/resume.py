import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.utils import secure_filename

from config.db_config import get_db_connection

from nlp.resume_parser import extract_text
from nlp.text_processor import clean_text
from nlp.skill_extractor import extract_skills
from nlp.resume_scorer import calculate_resume_score


resume_bp = Blueprint(
    "resume",
    __name__
)


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


@resume_bp.route(
    "/upload-resume",
    methods=["GET", "POST"]
)
def upload_resume():

    # Check login
    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    if request.method == "POST":

        # Check file
        if "resume" not in request.files:
            return "No file selected."

        file = request.files["resume"]

        if file.filename == "":
            return "No file selected."

        # Check file type
        if not allowed_file(file.filename):
            return "Only PDF and DOCX files are allowed."

        # Secure filename
        filename = secure_filename(
            file.filename
        )

        # Save file
        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(file_path)

        # Extract text
        resume_text = extract_text(
            file_path
        )

        # Clean text
        resume_text = clean_text(
            resume_text
        )

        # Extract skills
        skills = extract_skills(
            resume_text
        )

        # Calculate resume score
        resume_score = calculate_resume_score(
            resume_text,
            skills
        )

        skills_text = ", ".join(
            skills
        )

        # Save into MySQL
        connection = get_db_connection()

        cursor = connection.cursor()

        sql = """
        INSERT INTO resumes
        (
            user_id,
            filename,
            extracted_text,
            skills
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            session["user_id"],
            filename,
            resume_text,
            skills_text
        )

        cursor.execute(
            sql,
            values
        )

        connection.commit()

        cursor.close()
        connection.close()

        # Show analysis page
        return render_template(
            "resume_analysis.html",
            filename=filename,
            skills=skills,
            resume_score=resume_score,
            text_length=len(resume_text)
        )

    return render_template(
        "upload_resume.html"
    )