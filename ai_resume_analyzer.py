#AI Resume Analyzer (Enhanced with NLP + ML)
#Requirements:
#pip install streamlit PyPDF2 scikit-learn matplotlib

import streamlit as st 
import matplotlib.pyplot as plt 
from collections import Counter
import PyPDF2 
import re

#NLP / ML imports

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

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

common_skills = [

    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "php", "ruby", "go", "rust", "swift", "kotlin", "r", "matlab",

    # Web Development
    "html", "css", "bootstrap", "tailwind css",
    "react", "angular", "vue", "node.js", "nodejs",
    "express", "django", "flask", "fastapi", "streamlit",

    # Databases
    "sql", "mysql", "postgresql", "sqlite",
    "mongodb", "oracle", "redis",

    # Data Science
    "numpy", "pandas", "matplotlib",
    "seaborn", "plotly", "scikit-learn",
    "statistics", "data analysis", "data visualization",

    # AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "computer vision",
    "natural language processing",
    "nlp",
    "tensorflow",
    "keras",
    "pytorch",
    "opencv",

    # Cloud
    "aws",
    "azure",
    "google cloud",
    "gcp",

    # DevOps
    "git",
    "github",
    "docker",
    "kubernetes",
    "linux",

    # BI
    "power bi",
    "tableau",
    "excel",

     # Software Engineering
    "oop",
    "object oriented programming",
    "dsa",
    "data structures",
    "algorithms",
    "rest api",

    # Soft Skills
    "communication",
    "teamwork",
    "leadership",
    "problem solving",
    "critical thinking",
    "time management"
]

JOB_ROLE_SKILLS = {

    "AI Engineer": [
        "python","machine learning","deep learning",
        "tensorflow","pytorch","numpy","pandas",
        "scikit-learn","opencv","git","github"
    ],

    "Machine Learning Engineer": [
        "python","machine learning","deep learning",
        "tensorflow","pytorch","numpy","pandas",
        "scikit-learn","sql","git"
    ],

    "Data Scientist": [
        "python","sql","numpy","pandas",
        "matplotlib","seaborn",
        "machine learning","statistics",
        "scikit-learn"
    ],

    "Data Analyst": [
        "python","sql","excel",
        "power bi","tableau",
        "pandas","numpy"
    ],

     "Python Developer": [
        "python","sql","git",
        "github","flask",
        "fastapi","oop"
    ],

    "Frontend Developer": [
        "html","css","javascript",
        "react","bootstrap"
    ],

    "Backend Developer": [
        "python","sql","flask",
        "fastapi","mongodb",
        "mysql","git"
    ],

     "Full Stack Developer": [
        "html","css","javascript",
        "react","node.js",
        "python","sql",
        "git","github"
    ],

    "Software Engineer": [
        "python","java","c++",
        "sql","git","github",
        "oop","dsa"
    ],

    
    "Web Developer": [
        "html","css","javascript",
        "react","node.js",
        "sql","git"
    ]
}

JOB_ROLE_DESCRIPTION = {

    "AI Engineer":
    """
    AI Engineer skilled in Python, machine learning, deep learning,
    artificial intelligence, data science, TensorFlow, PyTorch,
    computer vision, NLP and developing AI applications.
    """,

    "Machine Learning Engineer":
    """
    Machine Learning Engineer skilled in Python, machine learning,
    deep learning, model development, data preprocessing,
    scikit-learn, TensorFlow, PyTorch and deployment.
    """,

    "Data Scientist":
    """
    Data Scientist skilled in Python, SQL, statistics,
    data analysis, machine learning, pandas, numpy,
    visualization and predictive modeling.
    """,

    "Web Developer":
    """
    Web Developer skilled in HTML, CSS, JavaScript,
    React, Node.js, databases, APIs and building websites.
    """
}

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

#---------------- HELPER FUNCTIONS ----------------

def extract_text_from_pdf(file): 
    reader = PyPDF2.PdfReader(file) 
    text = "" 
    for page in reader.pages:
         text += page.extract_text() or ""
    return text.lower()

def extract_text_from_txt(file): 
    return file.read().decode("utf-8").lower()

#Clean text for NLP

def clean_text(text):
     text = re.sub(r"[^a-zA-Z0-9 ]", " ", text) 
     text = re.sub(r"\s+", " ", text) 
     return text.strip().lower()

    

def extract_skills(text, skills_list):
    text = clean_text(text)
    found_skills = []

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))

#ML-based similarity using TF-IDF + Cosine Similarity

def compute_similarity(resume_text, jd_text): 
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text]) 
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)

#Keyword frequency

def keyword_frequency(text):
     words = text.split() 
     return Counter(words).most_common(10)

#Detailed scoring

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

    # Skill Match Score
    skill_score = (
        len(matched_skills) /
        max(len(jd_skills), 1)
    ) * 100

    # Keyword Score
    keyword_score = skill_score

    return (
        int(length_score),
        int(skill_score),
        int(keyword_score)
    )

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

    # ---------- Final Score ----------
    # Weight Distribution:
    # Skill Match = 60%
    # NLP Similarity = 10%
    # ATS Sections = 20%
    # Resume Quality = 10%
    
    final_score = (
    skill_score * 0.60 +
    ml_score * 0.10 +
    section_score * 0.20 +
    length_score * 0.10
    )

    return round(final_score, 2)

#Improvement tips

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

#Highlight keywords

def highlight_keywords(text, skills):
     for skill in skills: 
        text = text.replace(skill, f"{skill.upper()}")
     return text

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

        "Skills": len(extract_skills(text, common_skills)) >= 3,

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
            section_status = check_resume_sections(resume_text)
            required_skills = JOB_ROLE_SKILLS[job_role]
            job_text = JOB_ROLE_DESCRIPTION.get(
                job_role,
                " ".join(required_skills)
                )
            # NLP-based Similarity
            ml_score = compute_similarity(resume_text, job_text)
            # Skill extraction
            resume_skills = extract_skills(resume_text, common_skills)
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

    st.download_button(
            "📥 Download Report",
            report,
            "resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

#---------------- FOOTER ----------------

st.write("---")
st.markdown(" 2026 AI Resume Analyzer ")