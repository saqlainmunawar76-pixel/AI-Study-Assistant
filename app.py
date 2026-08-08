"""
app.py
AI Study Assistant — a Streamlit app powered by Google Gemini.

Paste any notes or text, and the AI will:
1. Summarize it in simple language
2. Explain key concepts
3. Generate quiz questions to test your understanding

Internship: AI & ML Intern @ Codomax Digital Solutions
Module 5 — Day 17-20: AI Tools & Mini Project
Author: Saqlain Munawar
"""

import streamlit as st
from google import genai
from google.genai.types import ThinkingConfig, GenerateContentConfig

# ---------- Page Config ----------
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="centered")

st.title("📚 AI Study Assistant")
st.caption("Paste your notes below and let AI summarize, explain, or quiz you — powered by Google Gemini.")

# ---------- API Key ----------
api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.warning("⚠️ No Gemini API key found. Add `GEMINI_API_KEY` in your Streamlit Secrets to use this app.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Options")
mode = st.sidebar.radio(
    "What do you want the AI to do?",
    ["Summarize", "Explain Like I'm New to This", "Generate Quiz Questions"]
)

# ---------- Input ----------
notes = st.text_area("✍️ Paste your notes or topic text here:", height=250,
                      placeholder="e.g. Paste a chapter summary, lecture notes, or any topic you're studying...")

run_button = st.button("🚀 Generate", type="primary")


def build_prompt(mode: str, notes: str) -> str:
    if mode == "Summarize":
        return (
            "Summarize the following study notes into clear, concise bullet points. "
            "Keep it beginner-friendly and highlight the most important ideas:\n\n" + notes
        )
    elif mode == "Explain Like I'm New to This":
        return (
            "Explain the following study notes in very simple language, as if teaching "
            "someone completely new to the topic. Use short sentences and simple examples:\n\n" + notes
        )
    else:  # Quiz
        return (
            "Based on the following study notes, generate 5 quiz questions to test understanding. "
            "Mix multiple-choice and short-answer questions. Provide the correct answers "
            "at the end under a separate 'Answers' section:\n\n" + notes
        )


if run_button:
    if not notes.strip():
        st.error("Please paste some notes or text first.")
    else:
        with st.spinner("Thinking..."):
            prompt = build_prompt(mode, notes)
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=GenerateContentConfig(
                    thinking_config=ThinkingConfig(thinking_budget=0)
                ),
            )
            st.markdown("### ✅ Result")
            st.markdown(response.text)

st.divider()
st.caption("Built as part of the AI & ML Internship at Codomax Digital Solutions — Module 5: AI Tools & Mini Project.")
