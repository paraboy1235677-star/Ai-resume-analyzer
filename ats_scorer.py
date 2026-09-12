"""
ats_scorer.py
-------------
This is the "brain" of the ATS checker.

How it works (in plain English):
1. Clean up both the resume text and the job description text.
2. Turn each into a list of important keywords/phrases (ignoring common
   words like "the", "and", "with").
3. Use TF-IDF (a standard NLP technique that scores how important a word
   is to a document) + cosine similarity to measure how closely the
   resume matches the job description. This gives a match score out of 100.
4. Find keywords that appear in the job description but NOT in the resume
   -> these are the "missing keywords" the student should add.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text: str) -> str:
    """Lowercase the text and strip out punctuation/extra whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_match_score(resume_text: str, job_description: str) -> float:
    """
    Returns a percentage (0-100) showing how well the resume matches
    the job description, using TF-IDF + cosine similarity.
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)
    return score


def extract_keywords(text: str, top_n: int = 25) -> set:
    """
    Pulls out the most meaningful single-word and two-word phrases
    from a piece of text, ignoring common stop words.
    """
    cleaned = clean_text(text)
    words = [w for w in cleaned.split() if w not in ENGLISH_STOP_WORDS and len(w) > 2]

    # Count frequency
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # Sort by frequency, take the top N
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_keywords = {w for w, _ in sorted_words[:top_n]}
    return top_keywords


def get_missing_keywords(resume_text: str, job_description: str, top_n: int = 25) -> list:
    """
    Returns keywords that show up in the job description but are
    missing from the resume - these are good candidates for the
    student to add so the resume passes ATS keyword filters.
    """
    jd_keywords = extract_keywords(job_description, top_n=top_n)
    resume_keywords = extract_keywords(resume_text, top_n=top_n * 3)  # check against a wider resume set

    missing = jd_keywords - resume_keywords
    return sorted(missing)


def get_ats_tips(resume_text: str) -> list:
    """
    A few simple, rule-based checks for common ATS-unfriendly resume
    mistakes. Real ATS checkers use dozens of rules; these are a
    beginner-friendly starting set.
    """
    tips = []
    text_lower = resume_text.lower()

    if "table" in text_lower or "\t\t\t" in resume_text:
        tips.append("Avoid complex tables/columns - some ATS software struggles to read them.")

    if len(resume_text.strip()) < 300:
        tips.append("Your resume text seems very short. Make sure your PDF isn't just an image (ATS can't read images).")

    if "@" not in resume_text:
        tips.append("No email address detected - make sure your contact info is in plain text, not inside an image.")

    if not re.search(r"(\+?\d[\d\-\s()]{7,}\d)", resume_text):
        tips.append("No phone number detected - double check your contact details are readable as plain text.")

    if not tips:
        tips.append("No major formatting red flags detected. Nice work!")

    return tips
