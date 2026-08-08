"""
utils/storage.py
Lightweight local persistence layer using a JSON file.

This plays the role of a database for now (materials, quizzes,
flashcards, history, settings). The data model here is intentionally
structured so it can be swapped for Supabase/Firebase later without
changing the rest of the app — every function below is the only
place that touches storage.
"""

import json
import os
import re
import uuid
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Current signed-in user (set once via set_user() after login).
# Each user gets their own JSON file so accounts stay separate.
_CURRENT_USER = "guest"


def set_user(user_id: str):
    """Switch the active user. Call this right after login."""
    global _CURRENT_USER
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", user_id.strip().lower()) or "guest"
    _CURRENT_USER = safe_id


def get_user():
    return _CURRENT_USER


def _db_path():
    return os.path.join(DATA_DIR, f"db_{_CURRENT_USER}.json")


DEFAULT_DB = {
    "materials": [],
    "quizzes": [],
    "flashcards": [],
    "quiz_results": [],
    "history": [],
    "settings": {"theme": "light"},
}


def _load():
    path = _db_path()
    if not os.path.exists(path):
        _save(DEFAULT_DB)
        return json.loads(json.dumps(DEFAULT_DB))  # deep copy
    with open(path, "r") as f:
        return json.load(f)


def _save(db):
    path = _db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(db, f, indent=2)


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ---------------- Materials ----------------
def add_material(name, file_type, content, size_kb):
    db = _load()
    material = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "type": file_type,
        "content": content,
        "size_kb": size_kb,
        "uploaded_at": _now(),
        "status": "Ready",
    }
    db["materials"].insert(0, material)
    _save(db)
    return material


def get_materials():
    return _load()["materials"]


def delete_material(material_id):
    db = _load()
    db["materials"] = [m for m in db["materials"] if m["id"] != material_id]
    _save(db)


# ---------------- History ----------------
def add_history(entry_type, title, content_preview, full_content=""):
    db = _load()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "type": entry_type,  # Summary / Explanation / Quiz / Flashcards / Key Concepts / Notes
        "title": title,
        "preview": content_preview[:160],
        "content": full_content,
        "created_at": _now(),
    }
    db["history"].insert(0, entry)
    _save(db)
    return entry


def get_history():
    return _load()["history"]


def clear_history():
    db = _load()
    db["history"] = []
    _save(db)


# ---------------- Quizzes & Results ----------------
def add_quiz(title, questions):
    db = _load()
    quiz = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "questions": questions,
        "created_at": _now(),
    }
    db["quizzes"].insert(0, quiz)
    _save(db)
    return quiz


def get_quizzes():
    return _load()["quizzes"]


def add_quiz_result(quiz_title, score, total, weak_topics):
    db = _load()
    result = {
        "id": str(uuid.uuid4())[:8],
        "quiz_title": quiz_title,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "weak_topics": weak_topics,
        "date": _now(),
    }
    db["quiz_results"].insert(0, result)
    _save(db)
    return result


def get_quiz_results():
    return _load()["quiz_results"]


# ---------------- Flashcards ----------------
def add_flashcard_set(title, cards):
    db = _load()
    fc_set = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "cards": cards,  # [{"front":..., "back":..., "status":"new"}]
        "created_at": _now(),
    }
    db["flashcards"].insert(0, fc_set)
    _save(db)
    return fc_set


def get_flashcard_sets():
    return _load()["flashcards"]


def update_flashcard_status(set_id, card_index, status):
    db = _load()
    for fc in db["flashcards"]:
        if fc["id"] == set_id:
            fc["cards"][card_index]["status"] = status
    _save(db)


# ---------------- Settings ----------------
def get_settings():
    return _load()["settings"]


def update_settings(**kwargs):
    db = _load()
    db["settings"].update(kwargs)
    _save(db)
    return db["settings"]


# ---------------- Stats ----------------
def get_stats():
    db = _load()
    results = db["quiz_results"]
    avg_score = round(sum(r["percentage"] for r in results) / len(results), 1) if results else 0
    return {
        "topics_studied": len(db["materials"]) + len(db["history"]),
        "quizzes_completed": len(results),
        "avg_quiz_score": avg_score,
        "materials_count": len(db["materials"]),
        "flashcard_sets": len(db["flashcards"]),
    }
