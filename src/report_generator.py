from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    job_role,
    final_score,
    ml_score,
    skill_score,
    ats_score,
    matched_skills,
    missing_skills,
    tips
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph("<b>AI Resume Analyzer Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"Target Role : {job_role}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Final Match Score : {final_score}%", styles["BodyText"])
    )

    story.append(
        Paragraph(f"NLP Similarity : {ml_score}%", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Skill Match : {skill_score}%", styles["BodyText"])
    )

    story.append(
        Paragraph(f"ATS Score : {ats_score}%", styles["BodyText"])
    )

    story.append(
        Paragraph("<br/><b>Matched Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(", ".join(matched_skills), styles["BodyText"])
    )

    story.append(
        Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(", ".join(missing_skills), styles["BodyText"])
    )

    story.append(
        Paragraph("<br/><b>Recommendations</b>", styles["Heading2"])
    )

    for tip in tips:
        story.append(
            Paragraph("• " + tip, styles["BodyText"])
        )

    pdf.build(story)