"""
utils/ai.py
All Gemini-powered AI functions for the Study Assistant, in one place.
Preserves the original app's model choice and thinking-budget settings.
"""

import json
import re
import streamlit as st
from google import genai
from google.genai.types import ThinkingConfig, GenerateContentConfig

MODEL = "gemini-2.5-flash"


@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def _generate(prompt: str) -> str:
    client = get_client()
    if client is None:
        raise RuntimeError("Missing GEMINI_API_KEY in Streamlit secrets.")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=GenerateContentConfig(
            thinking_config=ThinkingConfig(thinking_budget=0)
        ),
    )
    return response.text


def _extract_json(text: str):
    """Pulls the first JSON array/object out of a model response,
    even if wrapped in markdown code fences."""
    cleaned = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
    if not match:
        raise ValueError("Could not parse AI response as JSON.")
    return json.loads(match.group(1))


# ---------------- Core study tools ----------------

def summarize(text: str) -> str:
    prompt = (
        "Summarize the following study material into clear, concise bullet points. "
        "Keep it beginner-friendly and highlight the most important ideas:\n\n" + text
    )
    return _generate(prompt)


def explain_simple(text: str) -> str:
    prompt = (
        "Explain the following study material in very simple language, as if teaching "
        "someone completely new to the topic. Use short sentences and simple examples:\n\n" + text
    )
    return _generate(prompt)


def ask_question(text: str, question: str) -> str:
    prompt = (
        f"Based on the following study material, answer this question clearly and accurately.\n\n"
        f"Study Material:\n{text}\n\nQuestion: {question}"
    )
    return _generate(prompt)


def extract_key_concepts(text: str) -> str:
    prompt = (
        "Extract the key concepts and terms from the following study material. "
        "For each concept, give a one-line definition. Format as a bullet list:\n\n" + text
    )
    return _generate(prompt)


def create_study_notes(text: str) -> str:
    prompt = (
        "Turn the following material into well-organized study notes with clear headings, "
        "sub-points, and short definitions where useful. Use Markdown formatting:\n\n" + text
    )
    return _generate(prompt)


def generate_quiz(text: str, num_questions: int = 5, difficulty: str = "Medium",
                   q_type: str = "Multiple Choice") -> list:
    prompt = f"""Based on the following study material, generate exactly {num_questions} quiz questions.
Difficulty: {difficulty}
Question type: {q_type}

Return ONLY a valid JSON array, no other text, in this exact format:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "topic": "short topic label"
  }}
]
For True/False questions, use options ["True", "False"].

Study Material:
{text}
"""
    raw = _generate(prompt)
    return _extract_json(raw)


def generate_flashcards(text: str, num_cards: int = 8) -> list:
    prompt = f"""Based on the following study material, generate exactly {num_cards} flashcards.

Return ONLY a valid JSON array, no other text, in this exact format:
[
  {{"front": "question or term", "back": "answer or definition"}}
]

Study Material:
{text}
"""
    raw = _generate(prompt)
    return _extract_json(raw)
