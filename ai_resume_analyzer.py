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
.main { background-color: #f5f7fa; }
.title { font-size: 40px; font-weight: bold; text-align: center; color: #2c3e50; }
.subtitle { text-align: center; color: #7f8c8d; font-size: 18px; }
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
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


#---------------- HEADER ----------------

st.markdown('<div class="title">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze your Resume within seconds...</div>', unsafe_allow_html=True) 
st.write("---")

#---------------- INPUT ----------------

st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf", "txt" , "docx"]) 
job_role = st.selectbox(
    "🎯 Select Your Target Job Role",
    ["Select a Role"] + list(JOB_ROLE_SKILLS.keys())
)
st.markdown('</div>', unsafe_allow_html=True)
analyze = st.button("🔍 Analyze Resume", use_container_width=True)

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
            job_text = " ".join(required_skills)
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
            # Basic scoring
            basic_score = 0
            if len(jd_skills) > 0:
                basic_score = round((len(matched_skills) / len(jd_skills)) * 100)

            # ----- Weighted Final Score -----
            similarity_weight = 30
            skill_weight = 50
            resume_weight = 20

            # Resume quality based on length
            word_count = len(resume_text.split())

            if word_count < 150:
                resume_quality = 40
            elif word_count < 300:
                resume_quality = 70
            elif word_count <= 700:
                resume_quality = 100
            else:
                resume_quality = 80

            final_score = round(
                (ml_score * similarity_weight / 100)
                + (basic_score * skill_weight / 100)
                + (resume_quality * resume_weight / 100),
                2
                )

        st.success("Analysis Completed ✅")

        # ---------------- MAIN SCORE ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Final Match Score")
        st.progress(min(int(final_score), 100))
        st.write(f"### {final_score}% Match")
        st.markdown('</div>', unsafe_allow_html=True)
        # ---------------- ML SCORE ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🤖 NLP + ML Similarity Score")
        st.write(f"Similarity Score: {ml_score}%")
        st.markdown('</div>', unsafe_allow_html=True)
        # ---------------- ATS BREAKDOWN ----------------
        length_score, skill_score, keyword_score = detailed_scores(
            resume_text,
            jd_skills,
            matched_skills
            )

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 ATS Score Breakdown")
        st.write(f"📄 Resume Length: {length_score}%")
        st.write(f"🛠 Skill Match: {skill_score}%")
        st.write(f"🔑 Keyword Optimization: {keyword_score}%")
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- ATS RESUME SECTIONS ----------------
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📑 ATS Resume Sections")
        for section, found in section_status.items():
            if found:
                st.success(f"✅ {section}")
            else:
                st.error(f"❌ {section}")
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- SKILLS ----------------
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("✅ Resume Skills")
            st.write(", ".join(resume_skills) if resume_skills else "No skills found")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎯 Job Skills")
            st.write(", ".join(jd_skills) if jd_skills else "No skills found")
            st.markdown('</div>', unsafe_allow_html=True)

         # ---------------- MISSING SKILLS ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("❌ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "No missing skills 🎉")
        st.markdown('</div>', unsafe_allow_html=True)

       # ---------------- CHART ----------------
       # ---------------- CHART ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Skill Analysis")

        matched_count = len(matched_skills)
        missing_count = len(missing_skills)

        # ✅ FIX: prevent crash
        if matched_count == 0 and missing_count == 0:
            st.warning("No skills found to display chart.")
        else:
            fig, ax = plt.subplots()
            ax.pie(
            [matched_count, missing_count],
            labels=["Matched", "Missing"],
            autopct="%1.1f%%"
        )
            st.pyplot(fig)

        st.markdown('</div>', unsafe_allow_html=True)
        # ---------------- TIPS ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚀 Improvement Tips")
        for tip in advanced_tips(final_score, missing_skills):
            st.write("👉", tip)
            st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- KEYWORD HIGHLIGHT ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔍 Keyword Highlight")
        st.write(highlight_keywords(resume_text[:1000], jd_skills))
        st.markdown('</div>', unsafe_allow_html=True)
        
         # ---------------- DOWNLOAD ----------------
    tips = advanced_tips(final_score, missing_skills)

    report = f"""
    Resume Score: {final_score}%

    Matched Skills:
    {', '.join(matched_skills)}

    Missing Skills:
    {', '.join(missing_skills)}

    Improvement Tips:
    {chr(10).join(tips)}
    """
    st.download_button("📥 Download Report", report, "resume_report.txt")

#---------------- FOOTER ----------------

st.write("---")
st.markdown(" 2026 AI Resume Analyzer ")