import os
import re

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


# =========================================================
# ATS ANALYSIS
# =========================================================

def analyze_ats(resume_text, skills):

    text = resume_text.lower()

    # -----------------------------------------------------
    # Skills Score / 20
    # -----------------------------------------------------

    skill_count = len(skills)

    if skill_count >= 10:
        skills_score = 20

    elif skill_count >= 8:
        skills_score = 17

    elif skill_count >= 5:
        skills_score = 14

    elif skill_count >= 3:
        skills_score = 10

    elif skill_count >= 1:
        skills_score = 5

    else:
        skills_score = 0


    # -----------------------------------------------------
    # Section Score / 22
    # -----------------------------------------------------

    sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certification",
        "certifications",
        "summary",
        "objective"
    ]

    section_count = 0

    for section in sections:

        if section in text:
            section_count += 1

    section_score = min(
        section_count * 3,
        22
    )


    # -----------------------------------------------------
    # Contact Score / 6
    # -----------------------------------------------------

    contact_score = 0

    email_pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    phone_pattern = (
        r"\b(?:\+91[-\s]?)?"
        r"[6-9]\d{9}\b"
    )

    if re.search(
        email_pattern,
        resume_text
    ):
        contact_score += 3

    if re.search(
        phone_pattern,
        resume_text
    ):
        contact_score += 3


    # -----------------------------------------------------
    # Resume Length / 10
    # -----------------------------------------------------

    character_count = len(resume_text)

    if character_count >= 3000:
        length_score = 10

    elif character_count >= 2000:
        length_score = 8

    elif character_count >= 1000:
        length_score = 5

    elif character_count >= 500:
        length_score = 3

    else:
        length_score = 0


    # -----------------------------------------------------
    # Action Verbs / 10
    # -----------------------------------------------------

    action_words = [
        "analyze",
        "analyzed",
        "build",
        "built",
        "create",
        "created",
        "debug",
        "debugged",
        "design",
        "designed",
        "develop",
        "developed",
        "implement",
        "implemented",
        "integrate",
        "integrated",
        "manage",
        "managed",
        "test",
        "tested"
    ]

    action_verbs = []

    for verb in action_words:

        if re.search(
            r"\b"
            + re.escape(verb)
            + r"\b",
            text
        ):

            action_verbs.append(
                verb
            )

    action_score = min(
        len(action_verbs) * 0.5,
        10
    )

    action_score = round(
        action_score,
        1
    )


    # -----------------------------------------------------
    # Quantified Results / 7
    # -----------------------------------------------------

    quantified_results = re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        resume_text
    )

    quantified_results = list(
        dict.fromkeys(
            quantified_results
        )
    )

    quantified_score = min(
        len(quantified_results),
        7
    )


    # -----------------------------------------------------
    # Suggestions
    # -----------------------------------------------------

    suggestions = []


    if skill_count < 5:

        suggestions.append(
            "Add more relevant technical skills "
            "that match your target job."
        )


    if "education" not in text:

        suggestions.append(
            "Add a clear Education section "
            "with your degree and institution."
        )


    if (
        "project" not in text
        and "projects" not in text
    ):

        suggestions.append(
            "Add a Projects section with "
            "technologies and measurable outcomes."
        )


    if len(action_verbs) < 5:

        suggestions.append(
            "Use strong action verbs such as "
            "developed, implemented, designed, "
            "tested and analyzed."
        )


    if len(quantified_results) < 3:

        suggestions.append(
            "Add accurate measurable results using "
            "numbers, percentages, modules or project metrics."
        )


    if not suggestions:

        suggestions.append(
            "Your resume contains the main ATS elements. "
            "Continue tailoring it to the target job description."
        )


    # -----------------------------------------------------
    # ATS DATA
    # -----------------------------------------------------

    ats_data = {

        "skills_score": skills_score,

        "section_score": section_score,

        "contact_score": contact_score,

        "length_score": length_score,

        "action_score": action_score,

        "quantified_score": quantified_score,

        "keyword_score": 0,

        "keyword_match_percentage": 0
    }


    return (
        ats_data,
        action_verbs,
        quantified_results,
        suggestions
    )


# =========================================================
# UPLOAD RESUME
# =========================================================

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

        # -------------------------------------------------
        # Check file
        # -------------------------------------------------

        if "resume" not in request.files:

            return "No file selected."


        file = request.files["resume"]


        if file.filename == "":

            return "No file selected."


        # -------------------------------------------------
        # Check file type
        # -------------------------------------------------

        if not allowed_file(
            file.filename
        ):

            return (
                "Only PDF and DOCX files are allowed."
            )


        # -------------------------------------------------
        # Secure filename
        # -------------------------------------------------

        filename = secure_filename(
            file.filename
        )


        # -------------------------------------------------
        # Create upload folder
        # -------------------------------------------------

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )


        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(
            file_path
        )


        # -------------------------------------------------
        # Extract text
        # -------------------------------------------------

        resume_text = extract_text(
            file_path
        )


        # -------------------------------------------------
        # Clean text
        # -------------------------------------------------

        resume_text = clean_text(
            resume_text
        )


        # -------------------------------------------------
        # Extract skills
        # -------------------------------------------------

        skills = extract_skills(
            resume_text
        )


        # -------------------------------------------------
        # Calculate resume score
        # -------------------------------------------------

        resume_score = calculate_resume_score(
            resume_text,
            skills
        )


        # -------------------------------------------------
        # Detailed ATS analysis
        # -------------------------------------------------

        (
            ats_data,
            action_verbs,
            quantified_results,
            suggestions
        ) = analyze_ats(
            resume_text,
            skills
        )


        # -------------------------------------------------
        # Skills text
        # -------------------------------------------------

        skills_text = ", ".join(
            skills
        )


        # -------------------------------------------------
        # Save into MySQL
        # -------------------------------------------------

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


        # Get inserted resume ID
        resume_id = cursor.lastrowid


        cursor.close()

        connection.close()


        # -------------------------------------------------
        # Show analysis page
        # -------------------------------------------------

        return render_template(
            "resume_analysis.html",

            resume_id=resume_id,

            filename=filename,

            resume_text=resume_text,

            skills=skills,

            skills_count=len(skills),

            resume_score=resume_score,

            text_length=len(resume_text),

            ats_data=ats_data,

            action_verbs=action_verbs,

            quantified_results=quantified_results,

            suggestions=suggestions,

            job_title=None,

            company=None,

            location=None,

            job_description=None,

            matched_keywords=[],

            missing_keywords=[]
        )


    return render_template(
        "upload_resume.html"
    )