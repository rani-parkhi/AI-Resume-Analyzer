def calculate_final_score(
    ml_score,
    matched_skills,
    jd_skills,
    section_status,
    resume_text
):

# ---------- Skill Score ----------
    if len(jd_skills) == 0:
        skill_score = 0
    else:
        skill_score = (
            len(matched_skills) /
            len(jd_skills)
        ) * 100

# ---------- Resume Length ----------
    words = len(resume_text.split())

    if words < 150:
        length_score = 40
    elif words < 250:
        length_score = 70
    elif words <= 700:
        length_score = 100
    else:
        length_score = 80

# ---------- ATS Section Score ----------
    section_score = (
        sum(section_status.values())
        / len(section_status)
    ) * 100

    final_score = (
        skill_score * 0.60 +
        ml_score * 0.10 +
        section_score * 0.20 +
        length_score * 0.10
        )
    
    return round(final_score, 2)

def detailed_scores(resume_text, jd_skills, matched_skills):
    
    # Resume Length Score
    word_count = len(resume_text.split())

    if word_count < 150:
        length_score = 40
    elif word_count < 250:
        length_score = 70
    elif word_count <= 700:
        length_score = 100
    else:
        length_score = 80

    skill_score = (
        len(matched_skills) /
        max(len(jd_skills), 1)
    ) * 100

    keyword_score = skill_score

    return (
        int(length_score),
        int(skill_score),
        int(keyword_score)
    ) 
