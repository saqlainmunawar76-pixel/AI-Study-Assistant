"""
utils/styles.py
Design system for the AI Study Assistant SaaS UI.
Injects a consistent CSS design system into the Streamlit app:
colors, typography, spacing, radius, shadows, cards, buttons,
inputs, toasts, loading/empty/error states, and dark/light themes.
"""

import streamlit as st

LIGHT_THEME = {
    "bg": "#F7F8FB",
    "bg_secondary": "#FFFFFF",
    "sidebar_bg": "#FFFFFF",
    "text": "#1A1D29",
    "text_muted": "#6B7280",
    "border": "#E5E7EB",
    "card_bg": "#FFFFFF",
    "primary": "#6C5CE7",
    "primary_hover": "#5A4BD4",
    "primary_soft": "#EEEBFD",
    "accent": "#00C2A8",
    "success": "#16A34A",
    "warning": "#D97706",
    "error": "#DC2626",
    "shadow": "0 1px 3px rgba(16, 24, 40, 0.06), 0 1px 2px rgba(16, 24, 40, 0.04)",
    "shadow_lg": "0 8px 24px rgba(16, 24, 40, 0.10)",
}

DARK_THEME = {
    "bg": "#12131A",
    "bg_secondary": "#191B25",
    "sidebar_bg": "#15161E",
    "text": "#F1F2F6",
    "text_muted": "#9CA0B0",
    "border": "#272A38",
    "card_bg": "#1C1E29",
    "primary": "#8B7CF6",
    "primary_hover": "#A091FF",
    "primary_soft": "#26243F",
    "accent": "#2DE0C4",
    "success": "#34D399",
    "warning": "#FBBF24",
    "error": "#F87171",
    "shadow": "0 1px 3px rgba(0, 0, 0, 0.4)",
    "shadow_lg": "0 8px 24px rgba(0, 0, 0, 0.5)",
}


def inject_css(theme_name: str = "light"):
    t = DARK_THEME if theme_name == "dark" else LIGHT_THEME

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        :root {{
            --bg: {t['bg']};
            --bg-secondary: {t['bg_secondary']};
            --text: {t['text']};
            --text-muted: {t['text_muted']};
            --border: {t['border']};
            --card-bg: {t['card_bg']};
            --primary: {t['primary']};
            --primary-hover: {t['primary_hover']};
            --primary-soft: {t['primary_soft']};
            --accent: {t['accent']};
            --success: {t['success']};
            --warning: {t['warning']};
            --error: {t['error']};
            --shadow: {t['shadow']};
            --shadow-lg: {t['shadow_lg']};
            --radius: 14px;
            --radius-sm: 8px;
        }}

        .stApp {{
            background: var(--bg);
            color: var(--text);
        }}

        section[data-testid="stSidebar"] {{
            background: {t['sidebar_bg']};
            border-right: 1px solid var(--border);
        }}

        /* ---- Typography ---- */
        h1, h2, h3, h4 {{
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: var(--text) !important;
        }}

        /* Force readable text color across every Streamlit widget wrapper —
           needed because Streamlit's own theme classes otherwise fight
           our custom dark/light palette and text can become invisible. */
        p, span, label, li, div, .stMarkdown,
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"],
        [data-testid="stWidgetLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"],
        [data-testid="stExpander"] summary,
        .stRadio label, .stCheckbox label,
        .stSelectbox label, .stTextInput label,
        .stTextArea label, .stSlider label,
        .streamlit-expanderHeader {{
            color: var(--text) !important;
        }}

        [data-testid="stCaptionContainer"] p {{
            color: var(--text-muted) !important;
        }}

        /* Card values (the big numbers/HTML we render ourselves) already
           set their own color inline via CSS vars, so they're unaffected. */

        /* ---- Cards ---- */
        .sa-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px 22px;
            box-shadow: var(--shadow);
            margin-bottom: 16px;
            transition: box-shadow 0.15s ease, transform 0.15s ease;
        }}
        .sa-card:hover {{ box-shadow: var(--shadow-lg); }}

        .sa-card-title {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }}
        .sa-card-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text);
        }}

        /* ---- Gradient hero ---- */
        .sa-hero {{
            background: linear-gradient(135deg, var(--primary) 0%, #A78BFA 55%, var(--accent) 100%);
            border-radius: var(--radius);
            padding: 28px 30px;
            color: white;
            box-shadow: var(--shadow-lg);
            margin-bottom: 22px;
        }}
        .sa-hero h1 {{ color: white !important; margin: 0 0 6px 0; font-size: 1.7rem; }}
        .sa-hero p {{ color: rgba(255,255,255,0.9); margin: 0; }}

        /* ---- Pills / badges ---- */
        .sa-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            background: var(--primary-soft);
            color: var(--primary);
        }}
        .sa-badge.success {{ background: rgba(22,163,74,0.12); color: var(--success); }}
        .sa-badge.warning {{ background: rgba(217,119,6,0.12); color: var(--warning); }}
        .sa-badge.error {{ background: rgba(220,38,38,0.12); color: var(--error); }}

        /* ---- Buttons ---- */
        .stButton > button {{
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            border: 1px solid var(--border) !important;
            transition: all 0.15s ease !important;
        }}
        .stButton > button[kind="primary"] {{
            background: var(--primary) !important;
            border: none !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: var(--primary-hover) !important;
            transform: translateY(-1px);
        }}

        /* ---- Inputs ---- */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
            border-radius: var(--radius-sm) !important;
            border: 1px solid var(--border) !important;
            background: var(--card-bg) !important;
            color: var(--text) !important;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: var(--text-muted) !important;
        }}

        /* ---- Empty state ---- */
        .sa-empty {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
        }}
        .sa-empty .icon {{ font-size: 2.4rem; margin-bottom: 8px; }}

        /* ---- Divider ---- */
        .sa-divider {{ border-top: 1px solid var(--border); margin: 18px 0; }}

        /* ---- Flashcard ---- */
        .sa-flashcard {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 30px;
            font-size: 1.15rem;
            font-weight: 600;
            box-shadow: var(--shadow-lg);
        }}

        /* ---- Sidebar nav radio as menu ---- */
        section[data-testid="stSidebar"] .stRadio > label {{ display: none; }}

        #MainMenu, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


def card(title: str, value: str, sub: str = "", badge: str = ""):
    badge_html = f'<span class="sa-badge">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="sa-card">
        <div class="sa-card-title">{title}</div>
        <div class="sa-card-value">{value}</div>
        <div style="color: var(--text-muted); font-size: 0.85rem; margin-top:4px;">{sub} {badge_html}</div>
    </div>
    """, unsafe_allow_html=True)


def empty_state(icon: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="sa-empty">
        <div class="icon">{icon}</div>
        <div style="font-weight:600; color: var(--text); font-size:1rem;">{title}</div>
        <div style="font-size:0.85rem; margin-top:4px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
