import re
from .resume_parser import clean_text

def extract_skills(text, skills_list):
    text = clean_text(text)
    found_skills = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))
