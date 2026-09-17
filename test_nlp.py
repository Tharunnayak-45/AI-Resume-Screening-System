from nlp.text_processor import clean_text
from nlp.skill_extractor import extract_skills


resume_text = """
I am a Computer Science student.
I have knowledge of Java, Python, HTML, CSS,
JavaScript, MySQL and Machine Learning.
"""


cleaned_text = clean_text(resume_text)

skills = extract_skills(cleaned_text)


print("Cleaned Text:")
print(cleaned_text)

print("\nSkills Found:")
print(skills)