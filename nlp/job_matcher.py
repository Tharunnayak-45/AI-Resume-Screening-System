from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_text):

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    documents = [
        resume_text,
        job_text
    ]

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    score = similarity[0][0] * 100

    return round(score, 2)


def find_skill_difference(resume_skills, job_skills):

    # Convert resume skills into a set
    resume_skill_set = set(
        skill.strip().lower()
        for skill in resume_skills.split(",")
        if skill.strip()
    )

    # Convert job skills into a set
    job_skill_set = set(
        skill.strip().lower()
        for skill in job_skills.split(",")
        if skill.strip()
    )

    # Find common skills
    matched_skills = (
        resume_skill_set.intersection(
            job_skill_set
        )
    )

    # Find skills missing from resume
    missing_skills = (
        job_skill_set - resume_skill_set
    )

    return (
        sorted(matched_skills),
        sorted(missing_skills)
    )