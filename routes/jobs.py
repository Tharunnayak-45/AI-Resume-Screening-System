import csv

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from config.db_config import get_db_connection

from nlp.job_matcher import (
    calculate_similarity,
    find_skill_difference
)


jobs_bp = Blueprint("jobs", __name__)


def load_jobs():

    jobs = []

    with open(
        "dataset/jobs.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            jobs.append(row)

    return jobs


@jobs_bp.route("/jobs")
def jobs():

    # Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Connect to MySQL
    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # Get latest uploaded resume
    cursor.execute(
        """
        SELECT
            id,
            extracted_text,
            skills
        FROM resumes
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
        LIMIT 1
        """,
        (user_id,)
    )

    resume = cursor.fetchone()

    cursor.close()
    connection.close()

    # No resume found
    if not resume:

        return render_template(
            "jobs.html",
            jobs=[],
            message="Please upload a resume first."
        )

    resume_text = resume["extracted_text"]
    resume_skills = resume["skills"]

    # Load jobs
    all_jobs = load_jobs()

    recommended_jobs = []

    # Process every job
    for job in all_jobs:

        # Combine job information
        job_text = (
            job["title"]
            + " "
            + job["skills"]
            + " "
            + job["description"]
        )

        # Calculate AI similarity score
        score = calculate_similarity(
            resume_text,
            job_text
        )

        # Find matched and missing skills
        matched_skills, missing_skills = (
            find_skill_difference(
                resume_skills,
                job["skills"]
            )
        )

        # Add results to job
        job["match_score"] = score

        job["matched_skills"] = matched_skills

        job["missing_skills"] = missing_skills

        recommended_jobs.append(job)

    # Highest score first
    recommended_jobs.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return render_template(
        "jobs.html",
        jobs=recommended_jobs,
        resume_skills=resume_skills
    )