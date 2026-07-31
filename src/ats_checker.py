import re
from src.skill_extractor import extract_skills
from src.config import COMMON_SKILLS


def check_resume_sections(text):
    
    text = text.lower()

    sections = {

        "Contact Information": (
            "gmail" in text or
            "linkedin" in text or
            "github" in text or
            re.search(r"\b91\s?\d{10}\b", text) is not None or
            re.search(r"\b\d{10}\b", text) is not None
        ),

         "Education": any(word in text for word in [
            "b.tech",
            "btech",
            "be",
            "b.e",
            "bachelor",
            "diploma",
            "m.tech",
            "mtech",
            "college",
            "university"
        ]),

        "Skills": len(extract_skills(text, COMMON_SKILLS)) >= 3,

        "Projects": any(word in text for word in [
            "project",
            "expense tracker",
            "resume analyzer",
            "management system",
            "dashboard",
            "portfolio"
        ]),

        "Experience": any(word in text for word in [
            "experience",
            "intern",
            "internship",
            "worked",
            "training"
        ]),

        "Certifications": any(word in text for word in [
            "certificate",
            "certification",
            "certified",
            "coursera",
            "udemy",
            "sololearn",
            "nptel"
        ])
    }

    return sections