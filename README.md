# 📚 AI Study Assistant

**Internship:** AI & ML Intern @ Codomax Digital Solutions
**Intern:** Saqlain Munawar
**Module 5 — Day 17–20:** AI Tools & Mini Project

## 📌 About This Project
An AI-powered study companion built with **Streamlit** and **Google Gemini (gemini-2.5-flash)**. Paste any notes or topic text, and the app will:

- 📝 **Summarize** it into clear, concise bullet points
- 🎓 **Explain** it in simple, beginner-friendly language
- ❓ **Generate quiz questions** (with answers) to test your understanding

This project was built to explore how AI tools like Gemini can genuinely assist with learning and productivity — a core theme of this module.

## 🧠 What I Learned in This Module
- Explored AI tools (ChatGPT, Gemini, Microsoft Copilot) and compared how they assist with coding, research, and productivity
- Learned how to integrate the **Gemini API** into a real Python application using the `google-genai` SDK
- Practiced prompt engineering — writing different prompts for summarization, explanation, and quiz generation
- Built and deployed a working AI-powered app end-to-end

## 🛠️ Tech Stack
- Python
- Streamlit (UI)
- Google Gemini API (`gemini-2.5-flash`) via the `google-genai` SDK

## ▶️ How to Run Locally
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gemini API key: create `.streamlit/secrets.toml` (see `.streamlit/secrets_template.toml`) with:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🚀 Deployment
Deployed on **Streamlit Community Cloud** with the API key stored securely in the app's Secrets.

## 🔗 Deliverables
- **GitHub Repository:** this repo
- **LinkedIn Post:** sharing the learning journey for this module
