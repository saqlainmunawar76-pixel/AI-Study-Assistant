# ✨ StudyForge AI — AI-Powered Study Platform

**Internship:** AI & ML Intern @ Codomax Digital Solutions
**Intern:** Saqlain Munawar
**Module 5 — Day 17–20:** AI Tools & Mini Project

## 📌 About
StudyForge AI is a premium, SaaS-style study platform built with **Streamlit** and **Google Gemini (`gemini-2.5-flash`)**. It upgrades a simple single-purpose AI notes tool into a full study companion with document management, quizzes, flashcards, progress tracking, and a polished design system — while preserving the original working Gemini integration.

## ✨ Features

| Page | What it does |
|---|---|
| 🏠 **Dashboard** | Greeting, quick actions, stats, recent materials & activity |
| 📁 **My Materials** | Upload PDF / DOCX / TXT, search, and act on saved documents |
| 🤖 **AI Study Tools** | Summarize, Explain Simply, Extract Key Concepts, Create Study Notes, Ask a Question |
| 📝 **Quiz & Practice** | AI-generated quizzes (custom length/difficulty/type), scoring, weak-topic recommendations |
| 🎴 **Flashcards** | AI-generated flashcards with flip, next/prev, mark known/review, progress bar |
| 📊 **Study Progress** | Stats, quiz performance chart, recent results |
| ☁️ **Cloud Storage** | Google Drive import architecture (clearly marked "Not Connected" until credentials are added — no fake success states) |
| 🕓 **History** | Every AI session saved and searchable, reopen any past result |
| ⚙️ **Settings** | Account, Appearance (dark/light), AI Preferences, Cloud Connections, Data & Privacy (export/clear) |

## 🎨 Design System
A custom CSS design system (`utils/styles.py`) provides consistent colors, typography (Inter font), spacing, rounded cards, soft shadows, gradient hero banners, badges, and full **dark/light mode** — built to feel like a real AI SaaS product rather than a basic student project.

## 🏗️ Architecture
```
AI-Study-Assistant/
├── app.py                     # Main app: sidebar nav, routing, all page renders
├── utils/
│   ├── ai.py                  # All Gemini calls (summarize, explain, quiz, flashcards, etc.)
│   ├── storage.py             # Local JSON persistence — materials, quizzes, history, settings
│   ├── documents.py           # PDF / DOCX / TXT text extraction
│   └── styles.py              # Design system CSS + reusable UI components
├── data/                      # Local data store (db.json, git-ignored)
├── requirements.txt
└── .streamlit/secrets_template.toml
```

**Data layer:** currently a local JSON file acting as a lightweight database. The storage functions are isolated in `utils/storage.py` so it can be swapped for Supabase/Firebase later without touching the UI code.

**Cloud Storage:** the Google Drive UI and integration points are fully built, but intentionally show a "Not Connected" state with setup instructions rather than faking a successful connection — real OAuth credentials would need to be added to Secrets to activate it.

## 🛠️ Tech Stack
- Python, Streamlit
- Google Gemini API (`gemini-2.5-flash`) via `google-genai`
- Pandas (progress charts)
- pypdf, python-docx (document parsing)

## ▶️ Run Locally
```bash
pip install -r requirements.txt
```
Create `.streamlit/secrets.toml` (see `.streamlit/secrets_template.toml`):
```toml
GEMINI_API_KEY = "your-api-key-here"
```
Then run:
```bash
streamlit run app.py
```

## 🚀 Deployment
Deploy on **Streamlit Community Cloud** with `GEMINI_API_KEY` set in the app's Secrets (never in code).

## 🔗 Deliverables
- **GitHub Repository:** this repo
- **LinkedIn Post:** sharing the AI tools exploration and this project
