"""
app.py
AI Study Assistant — Premium SaaS-style study platform powered by Google Gemini.

Internship: AI & ML Intern @ Codomax Digital Solutions
Module 5 — Day 17-20: AI Tools & Mini Project
Author: Saqlain Munawar
"""

import streamlit as st
from datetime import datetime

from utils import storage, ai, documents
from utils.styles import inject_css, card, empty_state

# ---------------- Page Config ----------------
st.set_page_config(page_title="StudyForge AI", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

# ---------------- Session State Defaults ----------------
if "theme" not in st.session_state:
    st.session_state.theme = storage.get_settings().get("theme", "light")
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "active_material_text" not in st.session_state:
    st.session_state.active_material_text = ""
if "flashcard_index" not in st.session_state:
    st.session_state.flashcard_index = 0
if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = False
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

inject_css(st.session_state.theme)

client = ai.get_client()

NAV_ITEMS = [
    ("Dashboard", "🏠"),
    ("My Materials", "📁"),
    ("AI Study Tools", "🤖"),
    ("Quiz & Practice", "📝"),
    ("Flashcards", "🎴"),
    ("Study Progress", "📊"),
    ("Cloud Storage", "☁️"),
    ("History", "🕓"),
    ("Settings", "⚙️"),
]

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## ✨ StudyForge AI")
    st.caption("Your AI-powered study companion")
    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)

    for label, icon in NAV_ITEMS:
        active = st.session_state.page == label
        btn_type = "primary" if active else "secondary"
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True, type=btn_type):
            st.session_state.page = label
            st.rerun()

    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)
    theme_label = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        storage.update_settings(theme=st.session_state.theme)
        st.rerun()

    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)
    st.caption("Signed in as **Saqlain Munawar**")

if client is None:
    st.error("⚠️ Missing `GEMINI_API_KEY` in Streamlit Secrets. Add it to use AI features.")


# ==================================================
# DASHBOARD
# ==================================================
def render_dashboard():
    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"

    st.markdown(f"""
    <div class="sa-hero">
        <h1>{greeting}, Saqlain! ✨</h1>
        <p>What would you like to study today?</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick actions
    cols = st.columns(5)
    actions = [
        ("📝 Summarize", "AI Study Tools"),
        ("💡 Explain Topic", "AI Study Tools"),
        ("❓ Generate Quiz", "Quiz & Practice"),
        ("🎴 Flashcards", "Flashcards"),
        ("🤖 Ask AI", "AI Study Tools"),
    ]
    for col, (label, target) in zip(cols, actions):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = target
                st.rerun()

    st.write("")

    stats = storage.get_stats()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Topics Studied", str(stats["topics_studied"]))
    with c2:
        card("Quizzes Completed", str(stats["quizzes_completed"]))
    with c3:
        card("Avg Quiz Score", f"{stats['avg_quiz_score']}%")
    with c4:
        card("Flashcard Sets", str(stats["flashcard_sets"]))

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("#### 📁 Recent Materials")
        materials = storage.get_materials()[:5]
        if not materials:
            empty_state("📄", "No materials yet", "Upload your first document in My Materials.")
        else:
            for m in materials:
                st.markdown(f"""
                <div class="sa-card" style="padding:14px 18px;">
                    <b>{m['name']}</b> <span class="sa-badge">{m['type']}</span>
                    <div style="color:var(--text-muted); font-size:0.8rem; margin-top:4px;">
                        {m['uploaded_at']} · {m['size_kb']} KB
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with right:
        st.markdown("#### 🕓 Recent Activity")
        history = storage.get_history()[:5]
        if not history:
            empty_state("⚡", "No activity yet", "Your recent AI study actions will show here.")
        else:
            for h in history:
                st.markdown(f"""
                <div class="sa-card" style="padding:14px 18px;">
                    <span class="sa-badge">{h['type']}</span>
                    <div style="margin-top:6px; font-weight:600;">{h['title']}</div>
                    <div style="color:var(--text-muted); font-size:0.8rem;">{h['created_at']}</div>
                </div>
                """, unsafe_allow_html=True)


# ==================================================
# MY MATERIALS
# ==================================================
def render_materials():
    st.markdown("### 📁 My Materials")
    st.caption("Upload PDF, DOCX, or TXT files to use with AI Study Tools, Quizzes, and Flashcards.")

    uploaded = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    if uploaded is not None:
        if st.button("📤 Process & Save", type="primary"):
            with st.spinner("Processing document..."):
                try:
                    text = documents.extract_text(uploaded)
                    size = documents.file_size_kb(uploaded)
                    ext = uploaded.name.split(".")[-1].upper()
                    storage.add_material(uploaded.name, ext, text, size)
                    st.success(f"✅ {uploaded.name} processed and saved.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to process file: {e}")

    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)

    materials = storage.get_materials()
    search = st.text_input("🔍 Search materials", placeholder="Search by file name...")
    if search:
        materials = [m for m in materials if search.lower() in m["name"].lower()]

    if not materials:
        empty_state("📄", "No materials found", "Upload a document above to get started.")
        return

    for m in materials:
        with st.container():
            st.markdown(f"""
            <div class="sa-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <b>{m['name']}</b> &nbsp;<span class="sa-badge success">{m['status']}</span>
                        <div style="color:var(--text-muted); font-size:0.82rem; margin-top:4px;">
                            {m['type']} · {m['size_kb']} KB · Uploaded {m['uploaded_at']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            if c1.button("📝 Summarize", key=f"sum_{m['id']}"):
                st.session_state.active_material_text = m["content"]
                st.session_state.page = "AI Study Tools"
                st.session_state.pending_tool = "Summarize"
                st.rerun()
            if c2.button("💡 Explain", key=f"exp_{m['id']}"):
                st.session_state.active_material_text = m["content"]
                st.session_state.page = "AI Study Tools"
                st.session_state.pending_tool = "Explain Like I'm New"
                st.rerun()
            if c3.button("❓ Quiz", key=f"quiz_{m['id']}"):
                st.session_state.active_material_text = m["content"]
                st.session_state.page = "Quiz & Practice"
                st.rerun()
            if c4.button("🎴 Flashcards", key=f"fc_{m['id']}"):
                st.session_state.active_material_text = m["content"]
                st.session_state.page = "Flashcards"
                st.rerun()
            if c5.button("🗑️ Delete", key=f"del_{m['id']}"):
                storage.delete_material(m["id"])
                st.rerun()


# ==================================================
# AI STUDY TOOLS
# ==================================================
def render_ai_tools():
    st.markdown("### 🤖 AI Study Tools")
    st.caption("Paste text, or use a saved material, and let AI help you understand it.")

    materials = storage.get_materials()
    source = st.radio("Source", ["Paste text", "Use a saved material"], horizontal=True)

    text = ""
    if source == "Paste text":
        text = st.text_area("Paste your notes or topic text here:", height=200,
                             value=st.session_state.active_material_text if st.session_state.active_material_text else "")
    else:
        if not materials:
            st.info("No saved materials yet. Upload one in **My Materials** first.")
        else:
            names = {m["name"]: m for m in materials}
            choice = st.selectbox("Choose a material", list(names.keys()))
            text = names[choice]["content"]

    tools = ["Summarize", "Explain Like I'm New", "Extract Key Concepts", "Create Study Notes", "Ask a Question"]
    default_tool = st.session_state.get("pending_tool", "Summarize")
    tool = st.selectbox("What should the AI do?", tools, index=tools.index(default_tool) if default_tool in tools else 0)

    question = ""
    if tool == "Ask a Question":
        question = st.text_input("Your question about this material:")

    if st.button("🚀 Generate", type="primary"):
        if not text.strip():
            st.error("Please provide some text first.")
        elif client is None:
            st.error("AI is not configured — add GEMINI_API_KEY in secrets.")
        else:
            with st.spinner("AI is thinking..."):
                try:
                    if tool == "Summarize":
                        result = ai.summarize(text)
                    elif tool == "Explain Like I'm New":
                        result = ai.explain_simple(text)
                    elif tool == "Extract Key Concepts":
                        result = ai.extract_key_concepts(text)
                    elif tool == "Create Study Notes":
                        result = ai.create_study_notes(text)
                    else:
                        result = ai.ask_question(text, question)

                    storage.add_history(tool, text[:40] + "...", result, result)

                    st.markdown("#### ✅ Result")
                    st.markdown(f'<div class="sa-card">{result}</div>', unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    c1.download_button("⬇️ Download", result, file_name="ai_result.txt")
                    c2.button("🔄 Regenerate", key="regen_tool")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")


# ==================================================
# QUIZ & PRACTICE
# ==================================================
def render_quiz():
    st.markdown("### 📝 Quiz & Practice")

    if st.session_state.active_quiz is None:
        st.caption("Generate a quiz from your study material to test your understanding.")
        materials = storage.get_materials()
        source = st.radio("Source", ["Paste text", "Use a saved material"], horizontal=True, key="quiz_source")

        text = ""
        if source == "Paste text":
            text = st.text_area("Paste study material:", height=180,
                                 value=st.session_state.active_material_text if st.session_state.active_material_text else "")
        elif materials:
            names = {m["name"]: m for m in materials}
            choice = st.selectbox("Choose a material", list(names.keys()), key="quiz_material")
            text = names[choice]["content"]
        else:
            st.info("No saved materials yet. Paste text instead, or upload one in **My Materials**.")

        c1, c2, c3 = st.columns(3)
        num_q = c1.slider("Number of questions", 3, 10, 5)
        difficulty = c2.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        q_type = c3.selectbox("Question type", ["Multiple Choice", "True/False"])

        if st.button("🎯 Generate Quiz", type="primary"):
            if not text.strip():
                st.error("Please provide study material first.")
            elif client is None:
                st.error("AI is not configured — add GEMINI_API_KEY in secrets.")
            else:
                with st.spinner("Generating quiz questions..."):
                    try:
                        questions = ai.generate_quiz(text, num_q, difficulty, q_type)
                        quiz = storage.add_quiz(f"Quiz — {datetime.now().strftime('%b %d, %H:%M')}", questions)
                        st.session_state.active_quiz = quiz
                        st.session_state.quiz_answers = {}
                        st.rerun()
                    except Exception as e:
                        st.error(f"Couldn't generate quiz: {e}")
        return

    # ---- Taking the quiz ----
    quiz = st.session_state.active_quiz
    st.markdown(f"#### {quiz['title']}")

    submitted = st.session_state.get("quiz_submitted", False)

    for i, q in enumerate(quiz["questions"]):
        st.markdown(f"**{i+1}. {q['question']}**")
        answer = st.radio("Choose one:", q["options"], key=f"q_{i}", label_visibility="collapsed",
                           disabled=submitted, index=None)
        if answer:
            st.session_state.quiz_answers[i] = answer
        st.write("")

    if not submitted:
        if st.button("✅ Submit Quiz", type="primary"):
            st.session_state.quiz_submitted = True
            st.rerun()
    else:
        score = 0
        weak_topics = []
        for i, q in enumerate(quiz["questions"]):
            user_ans = st.session_state.quiz_answers.get(i)
            correct = user_ans == q["correct_answer"]
            if correct:
                score += 1
            else:
                weak_topics.append(q.get("topic", "General"))

        total = len(quiz["questions"])
        pct = round((score / total) * 100, 1) if total else 0
        storage.add_quiz_result(quiz["title"], score, total, weak_topics)

        st.markdown(f"""
        <div class="sa-hero">
            <h1>Score: {score}/{total} ({pct}%)</h1>
            <p>{"🎉 Great job!" if pct >= 70 else "📚 Keep practicing — review the topics below."}</p>
        </div>
        """, unsafe_allow_html=True)

        for i, q in enumerate(quiz["questions"]):
            user_ans = st.session_state.quiz_answers.get(i, "No answer")
            correct = user_ans == q["correct_answer"]
            badge = "success" if correct else "error"
            st.markdown(f"""
            <div class="sa-card">
                <b>{i+1}. {q['question']}</b><br/>
                Your answer: <span class="sa-badge {badge}">{user_ans}</span>
                {"" if correct else f' &nbsp; Correct answer: <span class="sa-badge success">{q["correct_answer"]}</span>'}
            </div>
            """, unsafe_allow_html=True)

        if weak_topics:
            st.markdown("#### 📌 Recommended Revision")
            for t in set(weak_topics):
                st.markdown(f"- {t}")

        if st.button("🔁 New Quiz"):
            st.session_state.active_quiz = None
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.rerun()


# ==================================================
# FLASHCARDS
# ==================================================
def render_flashcards():
    st.markdown("### 🎴 Flashcards")

    existing_sets = storage.get_flashcard_sets()

    tab1, tab2 = st.tabs(["Study Flashcards", "Generate New Set"])

    with tab2:
        materials = storage.get_materials()
        source = st.radio("Source", ["Paste text", "Use a saved material"], horizontal=True, key="fc_source")
        text = ""
        if source == "Paste text":
            text = st.text_area("Paste study material:", height=150,
                                 value=st.session_state.active_material_text if st.session_state.active_material_text else "",
                                 key="fc_text")
        elif materials:
            names = {m["name"]: m for m in materials}
            choice = st.selectbox("Choose a material", list(names.keys()), key="fc_material")
            text = names[choice]["content"]
        else:
            st.info("No saved materials yet.")

        num_cards = st.slider("Number of flashcards", 4, 15, 8)
        if st.button("🎴 Generate Flashcards", type="primary"):
            if not text.strip():
                st.error("Please provide study material first.")
            elif client is None:
                st.error("AI is not configured — add GEMINI_API_KEY in secrets.")
            else:
                with st.spinner("Creating flashcards..."):
                    try:
                        cards = ai.generate_flashcards(text, num_cards)
                        for c in cards:
                            c["status"] = "new"
                        storage.add_flashcard_set(f"Set — {datetime.now().strftime('%b %d, %H:%M')}", cards)
                        st.success("✅ Flashcards created! Switch to 'Study Flashcards' tab.")
                    except Exception as e:
                        st.error(f"Couldn't generate flashcards: {e}")

    with tab1:
        if not existing_sets:
            empty_state("🎴", "No flashcard sets yet", "Generate your first set in the tab above.")
            return

        set_names = {s["title"]: s for s in existing_sets}
        chosen_title = st.selectbox("Choose a flashcard set", list(set_names.keys()))
        fc_set = set_names[chosen_title]
        cards = fc_set["cards"]

        idx = st.session_state.flashcard_index % len(cards)
        current = cards[idx]

        known = sum(1 for c in cards if c.get("status") == "known")
        st.progress(known / len(cards) if cards else 0, text=f"{known}/{len(cards)} known")

        face_text = current["back"] if st.session_state.flashcard_flipped else current["front"]
        label = "ANSWER" if st.session_state.flashcard_flipped else "QUESTION"
        st.markdown(f"""
        <div class="sa-flashcard">
            <div>
                <div style="font-size:0.75rem; color:var(--text-muted); letter-spacing:0.08em; margin-bottom:10px;">{label} · CARD {idx+1}/{len(cards)}</div>
                {face_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("⬅️ Prev"):
            st.session_state.flashcard_index = (idx - 1) % len(cards)
            st.session_state.flashcard_flipped = False
            st.rerun()
        if c2.button("🔄 Flip"):
            st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
            st.rerun()
        if c3.button("➡️ Next"):
            st.session_state.flashcard_index = (idx + 1) % len(cards)
            st.session_state.flashcard_flipped = False
            st.rerun()
        if c4.button("✅ Known"):
            storage.update_flashcard_status(fc_set["id"], idx, "known")
            st.rerun()
        if c5.button("🔁 Review Again"):
            storage.update_flashcard_status(fc_set["id"], idx, "review")
            st.rerun()


# ==================================================
# STUDY PROGRESS
# ==================================================
def render_progress():
    st.markdown("### 📊 Study Progress")

    stats = storage.get_stats()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Materials Studied", str(stats["materials_count"]))
    with c2:
        card("Quizzes Completed", str(stats["quizzes_completed"]))
    with c3:
        card("Avg Quiz Score", f"{stats['avg_quiz_score']}%")
    with c4:
        card("Flashcard Sets", str(stats["flashcard_sets"]))

    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)

    results = storage.get_quiz_results()
    if not results:
        empty_state("📈", "No quiz history yet", "Complete a quiz to see your progress here.")
        return

    st.markdown("#### Quiz Performance Over Time")
    import pandas as pd
    df = pd.DataFrame(results[::-1])
    st.line_chart(df.set_index("date")["percentage"])

    st.markdown("#### Recent Results")
    for r in results[:8]:
        badge = "success" if r["percentage"] >= 70 else "warning"
        st.markdown(f"""
        <div class="sa-card" style="padding:14px 18px;">
            <b>{r['quiz_title']}</b> &nbsp; <span class="sa-badge {badge}">{r['percentage']}%</span>
            <div style="color:var(--text-muted); font-size:0.8rem;">{r['score']}/{r['total']} correct · {r['date']}</div>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# CLOUD STORAGE
# ==================================================
def render_cloud():
    st.markdown("### ☁️ Cloud Storage")
    st.caption("Import study material directly from your cloud storage.")

    st.markdown("""
    <div class="sa-card">
        <b>🔗 Google Drive</b> &nbsp;<span class="sa-badge warning">Not Connected</span>
        <div style="color:var(--text-muted); font-size:0.85rem; margin-top:6px;">
            Connect your Google Drive to browse and import documents directly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Configure Google Drive Connection"):
        st.markdown("""
        To enable Google Drive import, this app needs OAuth credentials configured
        in Streamlit Secrets:

        ```toml
        GOOGLE_CLIENT_ID = "your-client-id"
        GOOGLE_CLIENT_SECRET = "your-client-secret"
        GOOGLE_REDIRECT_URI = "your-redirect-uri"
        ```

        Once configured, this section will show:
        - A **Connect** button that starts the OAuth flow
        - Your connected Google account
        - A file browser for your Drive documents
        - Import / Sync / Remove actions per file

        This app does **not** simulate a fake connection — until real credentials
        are added, the Drive integration stays clearly marked as "Not Connected".
        """)

    st.markdown("<div class='sa-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### 📤 Local File Upload")
    st.caption("Until cloud sync is configured, you can still upload files directly.")
    if st.button("Go to My Materials →"):
        st.session_state.page = "My Materials"
        st.rerun()


# ==================================================
# HISTORY
# ==================================================
def render_history():
    st.markdown("### 🕓 History")
    st.caption("All your previous AI study sessions, in one place.")

    history = storage.get_history()
    search = st.text_input("🔍 Search history")
    if search:
        history = [h for h in history if search.lower() in h["title"].lower() or search.lower() in h["preview"].lower()]

    c1, c2 = st.columns([4, 1])
    with c2:
        if st.button("🗑️ Clear All", use_container_width=True):
            storage.clear_history()
            st.rerun()

    if not history:
        empty_state("🕓", "No history yet", "Your AI study sessions will appear here.")
        return

    for h in history:
        with st.expander(f"{h['type']} — {h['title']}  ·  {h['created_at']}"):
            st.markdown(h["content"] if h["content"] else h["preview"])


# ==================================================
# SETTINGS
# ==================================================
def render_settings():
    st.markdown("### ⚙️ Settings")

    tabs = st.tabs(["Account", "Appearance", "AI Preferences", "Cloud Connections", "Data & Privacy"])

    with tabs[0]:
        st.text_input("Name", value="Saqlain Munawar", disabled=True)
        st.text_input("Role", value="AI & ML Intern @ Codomax Digital Solutions", disabled=True)

    with tabs[1]:
        theme = st.radio("Theme", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1,
                          format_func=lambda x: "☀️ Light" if x == "light" else "🌙 Dark")
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            storage.update_settings(theme=theme)
            st.rerun()

    with tabs[2]:
        st.selectbox("Default explanation style", ["Simple", "Detailed", "Exam-focused"])
        st.selectbox("Default quiz difficulty", ["Easy", "Medium", "Hard"], index=1)
        st.caption("These preferences guide future AI generations (coming soon).")

    with tabs[3]:
        st.info("Google Drive is not connected. Configure it in the **Cloud Storage** page.")

    with tabs[4]:
        st.warning("Clearing history or materials cannot be undone.")
        c1, c2 = st.columns(2)
        if c1.button("🗑️ Clear Study History"):
            storage.clear_history()
            st.success("History cleared.")
        if c2.button("⬇️ Export My Data"):
            import json
            db_export = {
                "materials": storage.get_materials(),
                "history": storage.get_history(),
                "quiz_results": storage.get_quiz_results(),
                "flashcards": storage.get_flashcard_sets(),
            }
            st.download_button("Download JSON", json.dumps(db_export, indent=2),
                                file_name="studyforge_export.json")


# ==================================================
# ROUTER
# ==================================================
PAGES = {
    "Dashboard": render_dashboard,
    "My Materials": render_materials,
    "AI Study Tools": render_ai_tools,
    "Quiz & Practice": render_quiz,
    "Flashcards": render_flashcards,
    "Study Progress": render_progress,
    "Cloud Storage": render_cloud,
    "History": render_history,
    "Settings": render_settings,
}

PAGES[st.session_state.page]()
