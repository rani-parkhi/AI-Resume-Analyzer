def generate_explanation(
    final_score,
    skill_score,
    ml_score,
    ats_score,
    length_score
):

    explanation = []

    explanation.append(
        f"🎯 Final Resume Score: {final_score}%"
    )

    explanation.append("")

    explanation.append("Score Breakdown")

    explanation.append(
        f"• Skill Match (60%) : {round(skill_score * 0.60,2)}"
    )

    explanation.append(
        f"• NLP Similarity (10%) : {round(ml_score * 0.10,2)}"
    )

    explanation.append(
        f"• ATS Sections (20%) : {round(ats_score * 0.20,2)}"
    )

    explanation.append(
        f"• Resume Quality (10%) : {round(length_score * 0.10,2)}"
    )

    explanation.append("")

    if final_score >= 85:
        explanation.append(
            "Excellent alignment with the selected role."
        )

    elif final_score >= 70:
        explanation.append(
            "Good match. Improving missing skills can further increase your score."
        )

    elif final_score >= 50:
        explanation.append(
            "Average match. Add more role-specific skills and improve ATS optimization."
        )

    else:
        explanation.append(
            "Low match. Focus on strengthening both technical skills and resume quality."
        )

    return explanation