"""
app.py
------
Main Streamlit app - polished UI version.
Run it with:  streamlit run app.py
"""

import streamlit as st
from resume_parser import extract_text
from ats_scorer import get_match_score, get_missing_keywords, get_ats_tips

# ---------- Page setup ----------
st.set_page_config(page_title="AI Resume Analyzer | ATS Checker", page_icon="📄", layout="centered")

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top, #1B1F3B 0%, #0E1117 55%, #0A0C12 100%);
    }

    .main {
        padding-top: 1.5rem;
    }

    .hero {
        text-align: center;
        padding: 2rem 1rem 2.5rem 1rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #A29BFE, #6C63FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #B0B3C1;
        font-size: 1.05rem;
    }

    .score-card {
        background: linear-gradient(135deg, #6C63FF 0%, #4834D4 100%);
        border-radius: 18px;
        padding: 1.8rem;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(108, 99, 255, 0.35);
    }
    .score-card h2 {
        font-size: 3.2rem;
        margin: 0;
        font-weight: 700;
    }
    .score-card p {
        margin: 0;
        opacity: 0.9;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }

    .section-card {
        background-color: #161A2B;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        border: 1px solid #262B40;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }

    .keyword-pill {
        display: inline-block;
        background-color: #262B40;
        color: #D6D8E4;
        padding: 5px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 0.85rem;
        border: 1px solid #3A4060;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #1B2A4A !important;
        border: 2px dashed #6C63FF !important;
        border-radius: 14px !important;
    }

    [data-testid="stTextArea"] textarea {
        background-color: #1B1730 !important;
        border: 2px solid #6C63FF !important;
        border-radius: 14px !important;
        color: #FAFAFA !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #6C63FF, #4834D4) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 0 !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(108, 99, 255, 0.45) !important;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
# ---------- Hero header ----------
st.markdown(
    """
    <div class="hero">
        <h1>📄 AI Resume Analyzer</h1>
        <p>See exactly how an ATS reads your resume — and what's missing.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Inputs ----------
col1, col2 = st.columns(2)
with col1:
    uploaded_resume = st.file_uploader("📎 Upload your resume", type=["pdf", "docx"])
with col2:
    job_description = st.text_area("💼 Paste the job description", height=150)

analyze_clicked = st.button("✨ Analyze Resume", use_container_width=True)

# ---------- Logic ----------
if analyze_clicked:
    if not uploaded_resume:
        st.warning("Please upload a resume first.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text(uploaded_resume)

            if not resume_text.strip():
                st.error("Couldn't read any text from that file. Is it a scanned image PDF?")
            else:
                score = get_match_score(resume_text, job_description)
                missing_keywords = get_missing_keywords(resume_text, job_description)
                tips = get_ats_tips(resume_text)

                if score >= 75:
                    verdict = "Great match! 🎉"
                elif score >= 50:
                    verdict = "Decent match — tailor it a bit more."
                else:
                    verdict = "Low match — add more relevant keywords."

                # ---------- Score card ----------
                st.markdown(
                    f"""
                    <div class="score-card">
                        <p>ATS MATCH SCORE</p>
                        <h2>{score}%</h2>
                        <p>{verdict}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ---------- Missing keywords ----------
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 🔑 Keywords Missing From Your Resume")
                if missing_keywords:
                    pills = "".join(f'<span class="keyword-pill">{kw}</span>' for kw in missing_keywords)
                    st.markdown(pills, unsafe_allow_html=True)
                else:
                    st.write("No major missing keywords detected. Nice job!")
                st.markdown("</div>", unsafe_allow_html=True)

                # ---------- Tips ----------
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 📝 ATS Formatting Tips")
                for tip in tips:
                    st.write(f"- {tip}")
                st.markdown("</div>", unsafe_allow_html=True)

                with st.expander("View extracted resume text (what the ATS actually 'sees')"):
                    st.text(resume_text)