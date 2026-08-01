import streamlit as st 
import matplotlib.pyplot as plt 
from collections import Counter
from src.quality_analyzer import analyze_resume_quality
from src.normalization import normalize_resume_text
from src.explainability import generate_explanation
from src.report_generator import generate_pdf

from src.config import (
    COMMON_SKILLS,
    JOB_ROLE_SKILLS,
    JOB_ROLE_DESCRIPTION
)

from src.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_txt,
    clean_text
)

from src.skill_extractor import extract_skills

from src.similarity import compute_similarity

from src.scoring import (
    calculate_final_score,
    detailed_scores
)

from src.ats_checker import check_resume_sections

from src.recommendations import advanced_tips

#---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

#---------------- CUSTOM UI ----------------

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Main Header */
.title {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    color: #1F2937;
    margin-bottom: 8px;
}

/* Subtitle */
.subtitle {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 18px;
    font-weight: 400;
    text-align: center;
    color: #6B7280;
    margin-bottom: 25px;
}

/* Cards */
.card {
    background-color: #FFFFFF;
    padding: 24px;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06);
    margin-bottom: 20px;
}
            
            /* Analyze Button */
.stButton > button {
    width: 100%;
    height: 48px;
    background-color: #2563EB;
    color: #FFFFFF;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 16px;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

#---------------- HEADER ----------------

st.markdown(
    '<div class="title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered resume analysis based on your target job role</div>',
    unsafe_allow_html=True
)

st.write("---")

#---------------- INPUT ----------------

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 24px;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 5px;
    ">
        📋 Resume Analysis
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 15px;
        color: #6B7280;
        margin-bottom: 20px;
    ">
        Upload your resume and select the job role you are targeting.
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf", "txt", "docx"],
    help="Upload your resume in PDF, TXT, or DOCX format."
)

job_role = st.selectbox(
    "🎯 Target Job Role",
    ["Select a Role"] + list(JOB_ROLE_SKILLS.keys())
)

st.markdown('</div>', unsafe_allow_html=True)

# Analyze Button

analyze = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)

#Keyword frequency

def keyword_frequency(text):
     words = text.split() 
     return Counter(words).most_common(10)

#Highlight keywords

def highlight_keywords(text, skills):
     for skill in skills: 
        text = text.replace(skill, f"{skill.upper()}")
     return text

#---------------- ANALYSIS ----------------

if analyze:
    if uploaded_file is None:
        st.warning("Please upload a resume.")

    elif job_role == "Select a Role":
        st.warning("Please select a target job role.")

    else:
        with st.spinner("Analyzing resume... 🔍"):
            # Read file
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_txt(uploaded_file)
            resume_text = clean_text(resume_text)
            resume_text = normalize_resume_text(resume_text)
            quality = analyze_resume_quality(resume_text)
            section_status = check_resume_sections(resume_text)
            required_skills = JOB_ROLE_SKILLS[job_role]
            job_text = JOB_ROLE_DESCRIPTION.get(
                job_role,
                " ".join(required_skills)
                )
            # NLP-based Similarity
            ml_score = compute_similarity(resume_text, job_text)
            # Skill extraction
            resume_skills = extract_skills(resume_text, COMMON_SKILLS)
            jd_skills = required_skills
            matched_skills = [
                skill
                for skill in jd_skills
                if skill in resume_skills
                ]
            missing_skills = [
                skill
                for skill in jd_skills
                if skill not in resume_skills
                ]
            
            final_score = calculate_final_score(
                ml_score,
                matched_skills,
                jd_skills,
                section_status,
                resume_text
                )
            
        st.success("Analysis Completed ✅")

        # ---------------- MAIN SCORE ----------------
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 10px;
            ">
            🎯 Resume Match Score
            </div>
            """,
            unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 42px;
            font-weight: 700;
            color: #2563EB;
            margin-bottom: 5px;
            ">
            {final_score}%
            </div>
            """,
            unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
            color: #6B7280;
            margin-bottom: 15px;
            ">
            Target Role: <strong>{job_role}</strong>
            </div>
            """,
            unsafe_allow_html=True
            )
        
        st.progress(min(int(final_score), 100))
        
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- ANALYSIS METRICS ----------------
        
        skill_match_display = round(
            (len(matched_skills) / max(len(jd_skills), 1)) * 100,
            2
            )
        
        ats_section_display = round(
            (sum(section_status.values()) / len(section_status)) * 100,
            2
            )
        
        resume_words_display = len(resume_text.split())
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 20px;
            ">
        🤖 Resume Analysis Metrics
        </div>
        """,
        unsafe_allow_html=True
        )
        
        metric1, metric2, metric3, metric4 = st.columns(4)
        with metric1:
            st.metric(
                "🤖 NLP Similarity",
                f"{ml_score}%"
                )
            
            with metric2:
                st.metric(
                    "🛠 Skill Match",
                    f"{skill_match_display}%"
                    )
                
                with metric3:
                    st.metric(
                        "📑 ATS Sections",
                        f"{ats_section_display}%"
                        )
                
                with metric4:
                    st.metric(
                        "📄 Resume Words",
                        f"{resume_words_display}"
                        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- ATS BREAKDOWN ----------------
        
        length_score, skill_score, keyword_score = detailed_scores(
            resume_text,
            jd_skills,
            matched_skills
            )
        
        explanation = generate_explanation(
            final_score,
            skill_match_display,
            ml_score,
            ats_section_display,
            length_score
            )
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 20px;
            ">
            📊 ATS Score Breakdown
            </div>
            """,
            unsafe_allow_html=True
            )
        
        ats1, ats2, ats3 = st.columns(3)
        
        with ats1:
            st.metric(
                "📄 Resume Length",
                f"{length_score}%"
                )
            
            with ats2:
                st.metric(
                    "🛠 Skill Match",
                    f"{skill_score}%"
                    )
                
            with ats3:
                st.metric(
                    "🔑 Keyword Optimization",
                    f"{keyword_score}%"
                    )
                st.markdown(
                    """
                    <div style="
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 13px;
                    color: #6B7280;
                    margin-top: 15px;
                    ">
                    ATS scores are based on resume structure, relevant skills,
                    and keyword alignment with the selected role.
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("## 📝 Resume Quality Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Quality Score", f"{quality['score']}%")
        col2.metric("Action Verbs", quality["action_verbs"])
        col3.metric("Achievements", quality["numbers"])
        col4.metric("Weak Phrases", quality["weak_phrases"])
        
        if quality["feedback"]:
            st.subheader("Suggestions")
        for item in quality["feedback"]:
            st.warning(item)
        else:
            st.success("Excellent resume writing quality!")
    
        # ---------------- ATS RESUME SECTIONS ----------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                📑 ATS Resume Sections
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 20px;
            ">
                Checks whether important resume sections are detected.
            </div>
            """,
            unsafe_allow_html=True
        )

        section_col1, section_col2 = st.columns(2)

        section_items = list(section_status.items())

        with section_col1:
            for section, found in section_items[:3]:
                if found:
                    st.success(f"✅ {section}")
                else:
                    st.error(f"❌ {section}")

        with section_col2:
            for section, found in section_items[3:]:
                if found:
                    st.success(f"✅ {section}")
                else:
                    st.error(f"❌ {section}")

        st.markdown('</div>', unsafe_allow_html=True)

        
        # ---------------- SKILLS ----------------

        skill_col1, skill_col2 = st.columns(2)

        # Resume Skills
        with skill_col1:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                """
                <div style="
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 20px;
                    font-weight: 600;
                    color: #1F2937;
                    margin-bottom: 8px;
                ">
                    ✅ Resume Skills
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
                    color: #6B7280;
                    margin-bottom: 15px;
                ">
                    Skills detected from your resume
                </div>
                """,
                unsafe_allow_html=True
            )

            if resume_skills:
                st.write(", ".join(resume_skills))
            else:
                st.info("No relevant skills detected.")

            st.markdown('</div>', unsafe_allow_html=True)

        # Job Skills
        with skill_col2:

            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                """
                <div style="
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 20px;
                    font-weight: 600;
                    color: #1F2937;
                    margin-bottom: 8px;
                ">
                    🎯 Required Skills
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
                    color: #6B7280;
                    margin-bottom: 15px;
                ">
                    Skills expected for the selected role
                </div>
                """,
                unsafe_allow_html=True
            )

            if jd_skills:
                st.write(", ".join(jd_skills))
            else:
                st.info("No required skills available.")

            st.markdown('</div>', unsafe_allow_html=True)

        
        # ---------------- MISSING SKILLS ----------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                ❌ Missing Skills
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 15px;
            ">
                Skills required for the selected role that were not detected in your resume.
            </div>
            """,
            unsafe_allow_html=True
        )

        if missing_skills:
            st.warning(
                "Missing: " + ", ".join(missing_skills)
            )
        else:
            st.success(
                "🎉 Excellent! All required role skills were detected in your resume."
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- SKILL ANALYSIS ----------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                📊 Skill Analysis
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 20px;
            ">
                Comparison between skills detected in your resume and skills required for the selected role.
            </div>
            """,
            unsafe_allow_html=True
        )

        matched_count = len(matched_skills)
        missing_count = len(missing_skills)

        if matched_count == 0 and missing_count == 0:

            st.info("No relevant skills found to display.")

        else:

            chart_col1, chart_col2 = st.columns([2, 1])

            with chart_col1:

                fig, ax = plt.subplots(figsize=(5, 4))

                ax.pie(
                    [matched_count, missing_count],
                    labels=["Matched", "Missing"],
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.set_title(
                    "Required Skill Coverage",
                    fontsize=14,
                    fontweight="bold"
                )

                st.pyplot(fig)

            with chart_col2:

                st.metric(
                    "✅ Matched Skills",
                    matched_count
                )

                st.metric(
                    "❌ Missing Skills",
                    missing_count
                )

                total_required = matched_count + missing_count

                if total_required > 0:
                    coverage = round(
                        (matched_count / total_required) * 100,
                        2
                    )
                else:
                    coverage = 0

                st.metric(
                    "🎯 Skill Coverage",
                    f"{coverage}%"
                )

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- IMPROVEMENT TIPS ----------------

        tips = advanced_tips(final_score, missing_skills)

        generate_pdf(
            "resume_report.pdf",
            job_role,
            final_score,
            ml_score,
            skill_match_display,
            ats_section_display,
            matched_skills,
            missing_skills,
            tips
            )

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                🚀 Improvement Tips
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 18px;
            ">
                Personalized recommendations based on your resume analysis.
            </div>
            """,
            unsafe_allow_html=True
        )

        for tip in tips:

            st.markdown(
                f"""
                <div style="
                    background-color: #F8FAFC;
                    border: 1px solid #E5E7EB;
                    border-radius: 10px;
                    padding: 14px 16px;
                    margin-bottom: 10px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 15px;
                    color: #374151;
                ">
                    💡 {tip}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("## 🧠 Explainable AI")
        
        for line in explanation:
            st.write(line)

        # ---------------- KEYWORD HIGHLIGHT ----------------

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                🔍 Keyword Highlight
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 15px;
            ">
                Relevant keywords detected in your resume for the selected role.
            </div>
            """,
            unsafe_allow_html=True
        )

        highlighted_text = highlight_keywords(
            resume_text[:1000],
            jd_skills
        )

        st.text_area(
            "Resume Keyword Preview",
            highlighted_text,
            height=220,
            label_visibility="collapsed"
        )

        st.markdown('</div>', unsafe_allow_html=True)
        
    # ---------------- DOWNLOAD REPORT ----------------

    tips = advanced_tips(final_score, missing_skills)

    report = f"""
    AI RESUME ANALYZER REPORT

    =========================

    Target Role: {job_role}
    
    Final Match Score: {final_score}%
    
    NLP + ML Similarity Score: {ml_score}%
    
    Skill Match Score: {round((len(matched_skills) / max(len(jd_skills), 1)) * 100, 2)}%
    
    ATS Section Score: {round((sum(section_status.values()) / len(section_status)) * 100, 2)}%
    
    Resume Words: {len(resume_text.split())}
    
    Matched Skills:
    {', '.join(matched_skills) if matched_skills else 'None'}
    
    Missing Skills:
    {', '.join(missing_skills) if missing_skills else 'None'}
    
    Improvement Tips:
    {chr(10).join('- ' + tip for tip in tips)}
    
    =========================
    
    Generated by AI Resume Analyzer
    """

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #1F2937;
                margin-bottom: 8px;
            ">
                📥 Download Analysis Report
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
            """
            <div style="
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #6B7280;
                margin-bottom: 18px;
            ">
                Download your resume analysis results as a text report.
            </div>
            """,
            unsafe_allow_html=True
        )

    with open("resume_report.pdf", "rb") as pdf_file:
        st.download_button(
            "📥 Download PDF Report",
            pdf_file,
            file_name="Resume_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

#---------------- FOOTER ----------------

st.write("---")
st.markdown(" 2026 AI Resume Analyzer ")