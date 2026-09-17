def calculate_resume_score(resume_text, skills):

    score = 0

    text = resume_text.lower()

    # 1. Resume content
    if len(resume_text) >= 500:
        score += 20
    elif len(resume_text) >= 250:
        score += 10

    # 2. Skills
    skill_count = len(skills)

    if skill_count >= 8:
        score += 25
    elif skill_count >= 5:
        score += 20
    elif skill_count >= 3:
        score += 10

    # 3. Education
    education_keywords = [
        "education",
        "b.tech",
        "bachelor",
        "degree",
        "university",
        "college"
    ]

    if any(
        keyword in text
        for keyword in education_keywords
    ):
        score += 15

    # 4. Experience
    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "work experience"
    ]

    if any(
        keyword in text
        for keyword in experience_keywords
    ):
        score += 15

    # 5. Projects
    if "project" in text or "projects" in text:
        score += 10

    # 6. Certifications
    if (
        "certification" in text
        or "certifications" in text
    ):
        score += 5

    # Maximum score = 90
    return min(score, 100)