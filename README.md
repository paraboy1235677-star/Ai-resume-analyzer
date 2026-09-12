# AI Resume Analyzer - ATS Checker

A beginner-friendly Python web app that analyzes how well a resume matches
a job description, the way real Applicant Tracking Systems (ATS) do.

## Features
- Upload a resume in PDF or DOCX format
- Paste in any job description
- Get a **match score (0-100%)** based on TF-IDF text similarity
- See **missing keywords** you could add to your resume
- Get simple **ATS formatting tips**

## Tech Stack
- **Python 3**
- **Streamlit** - for the web interface
- **PyPDF2 / python-docx** - to read resume files
- **scikit-learn** - for TF-IDF and cosine similarity (the "AI"/NLP part)

## How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Your browser will open automatically at `http://localhost:8501`

## Project Structure
```
ai-resume-analyzer/
├── app.py                  # Main Streamlit app (UI)
├── utils/
│   ├── resume_parser.py    # Extracts text from PDF/DOCX
│   └── ats_scorer.py       # Scoring + keyword matching logic
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works
1. The uploaded resume file is converted into plain text.
2. Both the resume text and job description are cleaned (lowercased,
   punctuation removed).
3. TF-IDF vectors are built for both texts, and cosine similarity between
   them produces the match score.
4. The most frequent meaningful words in the job description are compared
   against the resume's words to find what's missing.

## Future Improvements
- Support for scanned/image-based PDFs using OCR
- Section-wise scoring (skills, experience, education separately)
- Resume formatting/grammar suggestions using an LLM API
