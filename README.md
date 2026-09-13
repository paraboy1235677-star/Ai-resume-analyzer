📄 AI Resume Analyzer — ATS Checker
An AI-powered resume analysis tool that shows job seekers exactly how an Applicant Tracking System (ATS) reads their resume — and what's missing before they apply.
🔗 Live Demo: [https://ai-resume-analyzer-h8vlzpuqoxmk2r....streamlit.app]
💻 Built by: Yuvraj Mishra
✨ Features
📎 Upload a resume (PDF or DOCX)
💼 Paste any job description
🎯 Get an ATS Match Score (0–100%) using TF-IDF + cosine similarity
🔑 See keywords missing from your resume that the job description expects
📝 Get quick ATS formatting tips (contact info visibility, tables, image-based text, etc.)
🛠️ Tech Stack
Layer
Tool
Language
Python
Web UI
Streamlit
NLP / Scoring
scikit-learn (TF-IDF, cosine similarity)
File Parsing
PyPDF2, python-docx
Deployment
Streamlit Community Cloud
🚀 Run It Locally
Bash
🧠 How It Works
The uploaded resume is converted into plain text.
Both the resume and job description are cleaned and vectorized using TF-IDF — a standard NLP technique that scores how important each word is to a document.
Cosine similarity between the two vectors produces the match score.
The most frequent meaningful terms in the job description are compared against the resume to surface missing keywords.
📌 Project Context
Built as a final-year college project to explore practical NLP applications in the hiring space.
🔮 Future Improvements
OCR support for scanned/image-based resumes
Section-wise scoring (skills, experience, education)
LLM-based resume rewriting suggestions