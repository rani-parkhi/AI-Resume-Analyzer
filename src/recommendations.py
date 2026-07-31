def advanced_tips(score, missing_skills):
    
    tips = []

    if score >= 90:
        tips.append("Excellent resume. Your profile is highly suitable for this role.")

    elif score >= 75:
        tips.append("Very good resume. Add a few missing skills to become a stronger candidate.")

    elif score >= 60:
        tips.append("Good foundation. Improve your resume by adding more relevant skills and projects.")

    elif score >= 40:
        tips.append("Your resume needs improvement. Add technical projects and strengthen your skills.")

    else:
        tips.append("Your resume currently doesn't match the selected role. Focus on building the required skills first.")

    if missing_skills:
         tips.append("Missing Skills: " + ", ".join(missing_skills))

    if len(missing_skills) >= 5:
        tips.append("Consider completing one project using these missing technologies.")

    return tips