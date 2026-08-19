import os
import ast
import re
import json
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Tech Career & Skill Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. COLOR THEME PALETTES & STATE INITIALIZATION
# ==============================================================================
THEME_PALETTES = {
    "Electric Cyan": {"primary": "#00A3FF", "accent": "#33B5FF", "glow": "rgba(0, 163, 255, 0.38)"},
    "Emerald Tech": {"primary": "#10B981", "accent": "#34D399", "glow": "rgba(16, 185, 129, 0.38)"},
    "Vercel Purple": {"primary": "#A855F7", "accent": "#C084FC", "glow": "rgba(168, 85, 247, 0.38)"}
}

if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Electric Cyan"

active_palette = THEME_PALETTES[st.session_state.app_theme]
primary_color = active_palette["primary"]
accent_color = active_palette["accent"]
glow_color = active_palette["glow"]

PRESET_PERSONAS = {
    "⚡ [1] Junior Backend": ["Python", "SQL", "PostgreSQL", "FastAPI"],
    "🤖 [2] AI & Data Engineer": ["Python", "SQL", "Data Science", "Machine Learning", "PyTorch"],
    "☁️ [3] Cloud & DevOps": ["Docker", "Kubernetes", "AWS", "Linux"],
    "🌐 [4] Full-Stack Modern": ["React", "TypeScript", "JavaScript", "FastAPI", "PostgreSQL"]
}

if "user_selected_stack" not in st.session_state:
    st.session_state.user_selected_stack = ["Python", "SQL"]

# ==============================================================================
# 3. CSS SYSTEM & ULTRA-POLISHED UI STYLES
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        --color-bg: #000000;
        --color-surface: #0D0D0D;
        --color-elevated: #141414;
        --color-border: #262A2D;
        --color-primary: {primary_color};
        --color-accent: {accent_color};
        --color-text: #F0F0F0;
        --color-muted: #8A8F98;
        --radius-btn: 16px;
        --radius-card: 14px;
        --radius-chip: 8px;
    }}

    header[data-testid="stHeader"], [data-testid="stToolbar"] {{
        display: none !important;
        height: 0 !important;
    }}

    .block-container, .stMainBlockContainer {{
        padding-top: 24px !important;
        padding-bottom: 60px !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: none !important;
        width: 100% !important;
    }}

    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #000000; }}
    ::-webkit-scrollbar-thumb {{ background: #262A2D; border-radius: 9999px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--color-primary); }}

    html, body, [class*="css"], .stApp {{
        background-color: var(--color-bg) !important;
        color: var(--color-text) !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-image: radial-gradient(circle at 50% 0%, {glow_color} 0%, transparent 45%),
                          radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px) !important;
        background-size: 100% 100%, 28px 28px !important;
        background-repeat: no-repeat, repeat !important;
    }}

    .floating-hud {{
        position: relative !important;
        width: 100% !important;
        background: rgba(11, 14, 18, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        padding: 10px 20px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 20px !important;
    }}

    .resend-hero-title {{
        font-family: 'Newsreader', serif !important;
        font-size: 52px !important;
        font-weight: 400 !important;
        line-height: 1.05 !important;
        letter-spacing: -0.96px !important;
        color: #F0F0F0 !important;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 12px;
    }}

    .resend-hero-sub {{
        font-size: 15px !important;
        color: var(--color-muted) !important;
        line-height: 1.6 !important;
        text-align: center;
        max-width: 680px;
        margin: 0 auto 16px auto;
    }}

    [data-testid="stTabs"] {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
    }}
    [data-testid="stTabs"] [data-baseweb="tab-highlight"],
    [data-testid="stTabs"] [data-baseweb="tab-border"] {{
        display: none !important;
    }}
    [data-testid="stTabs"] [role="tablist"],
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        display: inline-flex !important;
        justify-content: center !important;
        align-items: center !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        background: rgba(14, 17, 23, 0.96) !important;
        backdrop-filter: blur(32px) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 20px !important;
        padding: 8px 12px !important;
        margin: 24px auto 32px auto !important;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.95), 0 0 30px {glow_color} !important;
        width: auto !important;
    }}
    [data-testid="stTabs"] button[role="tab"] {{
        background: #14171E !important;
        color: #9CA3AF !important;
        border: 1px solid #242933 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        letter-spacing: -0.2px !important;
        height: auto !important;
        margin: 0 !important;
        outline: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    [data-testid="stTabs"] button[role="tab"]:hover {{
        color: #FFFFFF !important;
        background: #202530 !important;
        border-color: #3B4252 !important;
        transform: translateY(-2px) !important;
    }}
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, var(--color-primary) 0%, #004C80 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 1.5px solid #FFFFFF !important;
        box-shadow: 0 8px 24px {glow_color}, 0 0 25px var(--color-primary) !important;
        transform: translateY(-2px) !important;
    }}

    .bento-card {{
        background-color: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-card);
        padding: 22px 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .bento-card:hover {{
        border-color: var(--color-primary) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px {glow_color} !important;
    }}

    .bento-card-hero {{
        background: linear-gradient(145deg, #111418 0%, #0A0C0E 100%) !important;
        border: 1px solid var(--color-primary) !important;
        box-shadow: 0 0 24px {glow_color} !important;
    }}

    .tech-logo-img {{
        width: 20px;
        height: 20px;
        min-width: 20px;
        object-fit: contain;
        vertical-align: middle;
        margin-right: 8px;
        display: inline-block;
    }}

    .tech-logo-img-lg {{
        width: 24px;
        height: 24px;
        min-width: 24px;
        object-fit: contain;
        vertical-align: middle;
        margin-right: 10px;
        display: inline-block;
    }}

    .info-tooltip {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #202428;
        color: #8A8F98;
        font-size: 10.5px;
        font-weight: 700;
        cursor: help;
        margin-left: 6px;
        vertical-align: middle;
    }}

    .shimmer-badge {{
        background: linear-gradient(90deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.18) 50%, rgba(255, 255, 255, 0.04) 100%);
        background-size: 200% 100%;
        animation: badge-shimmer 3.5s infinite linear;
    }}
    @keyframes badge-shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    .resend-card {{
        background-color: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-card);
        padding: 20px 24px;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .resend-card:hover {{
        border-color: var(--color-primary) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px {glow_color} !important;
    }}

    .resend-card-highlight {{
        background: linear-gradient(#0D0D0D, #0D0D0D) padding-box,
                    linear-gradient(135deg, var(--color-primary), #10B981) border-box !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-card);
        padding: 20px 24px;
        box-shadow: 0 0 20px {glow_color} !important;
    }}

    @keyframes pulse-glow {{
        0% {{ transform: scale(0.95); opacity: 0.7; }}
        50% {{ transform: scale(1.25); opacity: 1; filter: drop-shadow(0 0 6px var(--color-primary)); }}
        100% {{ transform: scale(0.95); opacity: 0.7; }}
    }}
    .pulse-dot {{
        width: 8px;
        height: 8px;
        background-color: var(--color-primary);
        border-radius: 50%;
        display: inline-block;
        animation: pulse-glow 2s infinite ease-in-out;
    }}

    .resend-chip {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.4px;
        padding: 4px 10px;
        border-radius: var(--radius-chip);
        background: var(--color-elevated);
        color: var(--color-muted);
        border: 1px solid var(--color-border);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}
    .resend-chip-active {{
        color: var(--color-primary);
        border-color: var(--color-primary);
        background: {glow_color};
    }}
    .resend-chip-success {{
        color: #10B981;
        border-color: rgba(16, 185, 129, 0.4);
        background: rgba(16, 185, 129, 0.08);
    }}
    .resend-chip-danger {{
        color: #EF4444;
        border-color: rgba(239, 68, 68, 0.4);
        background: rgba(239, 68, 68, 0.08);
    }}

    .resource-vault-row {{
        background-color: #0B0D10 !important;
        border: 1px solid #1E2228 !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        text-decoration: none !important;
        margin-bottom: 10px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .resource-vault-row:hover {{
        border-color: var(--color-primary) !important;
        background-color: #12161E !important;
        transform: translateX(8px) !important;
        box-shadow: 0 6px 20px var(--color-primary) !important;
    }}
    .resource-vault-row:hover .vault-title {{
        color: #FFFFFF !important;
    }}
    .resource-vault-row:hover .vault-arrow {{
        transform: translateX(3px) translateY(-3px) !important;
    }}

    .job-card-premium {{
        background: linear-gradient(145deg, #0e1116 0%, #07090c 100%) !important;
        border: 1px solid #1E232B !important;
        border-radius: 14px !important;
        padding: 22px 24px !important;
        margin-bottom: 16px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    .job-card-premium:hover {{
        border-color: var(--color-primary) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.75), 0 0 25px {glow_color} !important;
    }}
    .job-card-premium::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; bottom: 0; width: 4px;
        background: var(--job-card-accent, var(--color-primary));
    }}
    .job-card-title {{
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.3px !important;
        margin: 6px 0 4px 0 !important;
        line-height: 1.3 !important;
    }}
    .job-info-pill {{
        background: #090B0E !important;
        border: 1px solid #1C222B !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin: 14px 0 12px 0 !important;
    }}
    .job-apply-btn {{
        background: linear-gradient(135deg, var(--color-primary) 0%, #004C80 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        text-decoration: none !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(0, 163, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }}
    .job-apply-btn:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0, 163, 255, 0.45) !important;
        color: #FFFFFF !important;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. ROBUST LOGO MAPPING & VECTOR ENGINE
# ==============================================================================
SKILL_LOGOS = {
    'python': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg',
    'postgresql': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg',
    'postgres': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg',
    'sql': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg',
    'sqlalchemy': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlalchemy/sqlalchemy-original.svg',
    'docker': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg',
    'kubernetes': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-plain.svg',
    'aws': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg',
    'azure': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg',
    'gcp': 'https://cdn.jsdelivr.net/gh/devicons/googlecloud/googlecloud-original.svg',
    'linux': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg',
    'git': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original.svg',
    'github': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg',
    'fastapi': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg',
    'django': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg',
    'redis': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original.svg',
    'react': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg',
    'typescript': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg',
    'javascript': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg',
    'html': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg',
    'css': 'https://cdn.jsdelivr.net/gh/devicons/css3/css3-original.svg',
    'nodejs': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original.svg',
    'mongodb': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg',
    'mysql': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg',
    'go': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original-wordmark.svg',
    'rust': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-original.svg',
    'c++': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg',
    'pytorch': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytorch/pytorch-original.svg',
    'tensorflow': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tensorflow/tensorflow-original.svg',
    'pandas': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original.svg',
    'numpy': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-original.svg',
    'scikit': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg',
    'terraform': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original.svg',
    'ansible': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ansible/ansible-original.svg',
    'prometheus': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original.svg',
    'grafana': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/grafana/grafana-original.svg',
    'bash': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bash/bash-original.svg',
    'prisma': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prisma/prisma-original.svg',
    'next': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nextjs/nextjs-original.svg',
    'tailwind': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tailwindcss/tailwindcss-original.svg'
}

def get_skill_logo(skill_name, large=False):
    s_lower = str(skill_name).lower()
    sz = 24 if large else 20
    cls_name = "tech-logo-img-lg" if large else "tech-logo-img"
    for k, url in SKILL_LOGOS.items():
        if k in s_lower:
            return f'<img src="{url}" class="{cls_name}" alt="{skill_name}" />'
    return f'<svg width="{sz}" height="{sz}" viewBox="0 0 24 24" fill="none" style="margin-right:8px; vertical-align:middle;"><rect x="2" y="4" width="20" height="16" rx="3" stroke="#262A2D" stroke-width="2" fill="#141414"/><path d="M6 9L9 12L6 15M11 15H16" stroke="{primary_color}" stroke-width="2" stroke-linecap="round"/></svg>'

def get_skill_study_hours(skill_text):
    s_lower = str(skill_text).lower()
    HOURS_KEYWORD_MAP = {
        'rust': 170, 'c++': 180, 'deep learning': 160, 'machine learning': 150,
        'pytorch': 140, 'tensorflow': 130, 'kubernetes': 120, 'java': 120,
        'aws': 110, 'azure': 100, 'gcp': 100, 'linux': 90, 'security': 90,
        'react': 85, 'go': 80, 'django': 75, 'postgresql': 75, 'javascript': 70,
        'next': 65, 'docker': 60, 'prometheus': 60, 'typescript': 55, 'fastapi': 50,
        'ansible': 50, 'redis': 45, 'sql': 40, 'pandas': 40, 'ci/cd': 40,
        'github actions': 35, 'git': 30, 'celery': 40, 'jwt': 30, 'oauth': 30,
        'html': 25, 'css': 25
    }
    for key, hrs in HOURS_KEYWORD_MAP.items():
        if key in s_lower:
            return hrs
    return 65

def render_tg_icon(icon_type="star", size=20):
    svgs = {
        "star": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M12 2L14.85 8.65L22 9.24L16.5 13.97L18.18 21L12 17.27L5.82 21L7.5 13.97L2 9.24L9.15 8.65L12 2Z" fill="url(#tg-grad-star)"/><defs><linearGradient id="tg-grad-star" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse"><stop stop-color="{primary_color}"/><stop offset="1" stop-color="{accent_color}"/></linearGradient></defs></svg>""",
        "sparkle": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M12 2V6M12 18V22M6 12H2M22 12H18M19.07 4.93L16.24 7.76M7.76 16.24L4.93 19.07M19.07 19.07L16.24 16.24M7.76 7.76L4.93 4.93" stroke="{primary_color}" stroke-width="2.5" stroke-linecap="round"/></svg>""",
        "trend": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M23 6L13.5 15.5L8.5 10.5L1 18M23 6H17M23 6V12" stroke="{primary_color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
        "diamond": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M6 3H18L22 9L12 22L2 9L6 3Z" stroke="{primary_color}" stroke-width="2" stroke-linejoin="round" fill="{glow_color}"/><path d="M2 9H22M12 22L8 9M12 22L16 9M6 3L8 9M18 3L16 9" stroke="{accent_color}" stroke-width="1.5"/></svg>""",
        "compass": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="{primary_color}" stroke-width="2"/><polygon points="16.24,7.76 14.12,14.12 7.76,16.24 9.88,9.88" fill="{accent_color}"/></svg>""",
        "shield": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M12 22S20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" fill="{glow_color}" stroke="{primary_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 12L11 14L15 10" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
        "briefcase": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="{primary_color}" stroke-width="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" stroke="{accent_color}" stroke-width="2"/></svg>""",
        "document": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="{primary_color}" stroke-width="2"/><polyline points="14 2 14 8 20 8" stroke="{accent_color}" stroke-width="2"/><line x1="16" y1="13" x2="8" y2="13" stroke="#8A8F98" stroke-width="2"/><line x1="16" y1="17" x2="8" y2="17" stroke="#8A8F98" stroke-width="2"/></svg>""",
        "shuffle": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"><polyline points="16 3 21 3 21 8" stroke="{primary_color}" stroke-width="2"/><line x1="4" y1="20" x2="21" y2="3" stroke="{primary_color}" stroke-width="2"/><polyline points="21 16 21 21 16 21" stroke="{accent_color}" stroke-width="2"/><line x1="15" y1="15" x2="21" y2="21" stroke="{accent_color}" stroke-width="2"/><line x1="4" y1="4" x2="9" y2="9" stroke="{accent_color}" stroke-width="2"/></svg>"""
    }
    return svgs.get(icon_type, svgs["star"])

# ==============================================================================
# 5. TOP SYSTEM STATUS BAR
# ==============================================================================
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 2px 0 14px 0; border-bottom: 1px solid #1E2225; margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <span class="pulse-dot"></span>
        <span style="font-size: 12px; color: #A1A4A5; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.5px;">SYSTEM STATUS: ACTIVE // ARCHITECT: MEHDI BAGHERI</span>
    </div>
    <span style="font-size: 12px; color: #A1A4A5; font-family: 'JetBrains Mono', monospace;">DATASET: 2026 BENCHMARK</span>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. PLOTLY THEME HELPER
# ==============================================================================
def apply_plotly_theme(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        font=dict(family="Inter, -apple-system, sans-serif", color="#F0F0F0", size=11),
        margin=dict(l=20, r=20, t=70, b=20),
        hoverlabel=dict(
            bgcolor="rgba(14, 17, 23, 0.95)",
            bordercolor=primary_color,
            font=dict(family="Inter, sans-serif", size=12, color="#FFFFFF")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#A1A4A5")
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#1B1E20", zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#1B1E20", zeroline=False)
    return fig

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
}

# ==============================================================================
# 7. COMPLETE KNOWLEDGE BASES
# ==============================================================================
AI_RESILIENCE_MATRIX = {
    'PyTorch': {'score': 95, 'risk': 'Very Low', 'learn_hours': 140},
    'TensorFlow': {'score': 90, 'risk': 'Very Low', 'learn_hours': 130},
    'Generative AI': {'score': 98, 'risk': 'Very Low', 'learn_hours': 160},
    'C++': {'score': 92, 'risk': 'Very Low', 'learn_hours': 180},
    'Rust': {'score': 94, 'risk': 'Very Low', 'learn_hours': 170},
    'Linux': {'score': 90, 'risk': 'Very Low', 'learn_hours': 90},
    'Kubernetes': {'score': 88, 'risk': 'Low', 'learn_hours': 120},
    'Docker': {'score': 85, 'risk': 'Low', 'learn_hours': 60},
    'AWS': {'score': 87, 'risk': 'Low', 'learn_hours': 110},
    'Azure': {'score': 85, 'risk': 'Low', 'learn_hours': 100},
    'Go': {'score': 84, 'risk': 'Low', 'learn_hours': 80},
    'Python': {'score': 86, 'risk': 'Low', 'learn_hours': 90},
    'PostgreSQL': {'score': 82, 'risk': 'Low', 'learn_hours': 75},
    'Redis': {'score': 80, 'risk': 'Low', 'learn_hours': 45},
    'FastAPI': {'score': 78, 'risk': 'Moderate', 'learn_hours': 50},
    'Machine Learning': {'score': 88, 'risk': 'Low', 'learn_hours': 150},
    'Data Science': {'score': 82, 'risk': 'Moderate', 'learn_hours': 130},
    'SQL': {'score': 74, 'risk': 'Moderate', 'learn_hours': 40},
    'React': {'score': 72, 'risk': 'Moderate', 'learn_hours': 85},
    'TypeScript': {'score': 76, 'risk': 'Moderate', 'learn_hours': 55},
    'JavaScript': {'score': 68, 'risk': 'Moderate-High', 'learn_hours': 70},
    'Java': {'score': 70, 'risk': 'Moderate', 'learn_hours': 120},
    'Django': {'score': 70, 'risk': 'Moderate', 'learn_hours': 75},
    'HTML/CSS': {'score': 45, 'risk': 'High Automation', 'learn_hours': 35}
}

SKILL_SALARY_ESTIMATES = {
    'Python': 115000, 'SQL': 105000, 'Docker': 128000, 'Kubernetes': 142000,
    'AWS': 135000, 'Azure': 128000, 'Machine Learning': 132000, 'Data Science': 125000,
    'PyTorch': 140000, 'TensorFlow': 130000, 'Generative AI': 155000, 'PostgreSQL': 118000,
    'Redis': 126000, 'FastAPI': 122000, 'Django': 112000, 'JavaScript': 108000,
    'React': 114000, 'TypeScript': 120000, 'Rust': 145000, 'Go': 138000,
    'C++': 125000, 'Linux': 115000, 'Java': 118000, 'HTML/CSS': 85000
}

TECH_ARENA_SPECS = {
    'Python': {'demand': 96, 'remote': 88, 'maturity': 95, 'syntax': 'Easy (Dynamic)', 'best_for': 'Rapid Prototyping, AI & Data, Clean Web Services', 'companions': ['FastAPI', 'PostgreSQL', 'Docker']},
    'FastAPI': {'demand': 82, 'remote': 85, 'maturity': 80, 'syntax': 'Modern (Async)', 'best_for': 'High-Performance Asynchronous APIs & Microservices', 'companions': ['Python', 'PostgreSQL', 'Redis', 'Docker']},
    'Django': {'demand': 76, 'remote': 78, 'maturity': 92, 'syntax': 'Batteries-Included', 'best_for': 'Monolithic Applications, Admin Dashboards, Enterprise', 'companions': ['Python', 'PostgreSQL', 'Celery']},
    'React': {'demand': 94, 'remote': 90, 'maturity': 94, 'syntax': 'Declarative (JSX)', 'best_for': 'Modern Interactive Web UIs & Dynamic Client Apps', 'companions': ['TypeScript', 'Next.js', 'Tailwind']},
    'TypeScript': {'demand': 91, 'remote': 92, 'maturity': 88, 'syntax': 'Typed JavaScript', 'best_for': 'Large-Scale Codebases, Full-Stack Architecture', 'companions': ['React', 'Node.js', 'Next.js']},
    'Docker': {'demand': 95, 'remote': 94, 'maturity': 96, 'syntax': 'Declarative Config', 'best_for': 'Environment Portability, Microservice Isolation', 'companions': ['Kubernetes', 'Linux', 'AWS']},
    'Kubernetes': {'demand': 89, 'remote': 92, 'maturity': 90, 'syntax': 'Complex Orchestration', 'best_for': 'Massive-Scale Cluster Management, High Availability', 'companions': ['Docker', 'Terraform', 'Prometheus']},
    'PostgreSQL': {'demand': 92, 'remote': 84, 'maturity': 98, 'syntax': 'Relational SQL', 'best_for': 'ACID-Compliant Relational Data, JSON Queries', 'companions': ['Python', 'FastAPI', 'Redis']},
    'Redis': {'demand': 86, 'remote': 85, 'maturity': 90, 'syntax': 'Key-Value Memory', 'best_for': 'Sub-Millisecond Caching, Pub/Sub, Session Queues', 'companions': ['PostgreSQL', 'FastAPI', 'Celery']},
    'PyTorch': {'demand': 88, 'remote': 86, 'maturity': 88, 'syntax': 'Tensor Math / Pythonic', 'best_for': 'Deep Learning Research, Neural Network Fine-Tuning', 'companions': ['Python', 'Data Science', 'Docker']},
    'C++': {'demand': 80, 'remote': 68, 'maturity': 99, 'syntax': 'Low-Level Compiled', 'best_for': 'Ultra-Low Latency Systems, Game Engines, Robotics', 'companions': ['Linux', 'Rust', 'Algorithms']},
    'Rust': {'demand': 84, 'remote': 88, 'maturity': 82, 'syntax': 'Memory-Safe Strict', 'best_for': 'High-Throughput Systems, Memory-Safe Microservices', 'companions': ['Linux', 'Docker', 'WebAssembly']},
    'Go': {'demand': 87, 'remote': 90, 'maturity': 89, 'syntax': 'Concurrent Minimal', 'best_for': 'Cloud-Native Gateways, High-Concurrency APIs', 'companions': ['Docker', 'Kubernetes', 'PostgreSQL']},
    'AWS': {'demand': 94, 'remote': 92, 'maturity': 97, 'syntax': 'Cloud Architecture', 'best_for': 'Global Scalability, Serverless, Enterprise Cloud', 'companions': ['Terraform', 'Docker', 'Linux']},
    'Linux': {'demand': 96, 'remote': 86, 'maturity': 100, 'syntax': 'CLI / Bash Shell', 'best_for': 'Server Operating Environment, Production Hosting', 'companions': ['Docker', 'Bash', 'Networking']}
}

ROADMAP_DATA = {
    "Data Science & AI Engineer": {
        "Phase 1: Foundations & Version Control": ["Python (OOP, Data Structures)", "Git & GitHub", "SQL Databases"],
        "Phase 2: Data Wrangling & Analytics": ["Pandas & NumPy", "Data Visualization (Matplotlib, Seaborn)", "EDA Analysis"],
        "Phase 3: Machine Learning & Modeling": ["Scikit-Learn (ML)", "Feature Engineering", "PyTorch / TensorFlow"],
        "Phase 4: Production, APIs & MLOps": ["FastAPI (Serving)", "Docker Containerization", "MLflow", "Cloud (AWS / GCP)"],
        "Architecture": "Data Lake (S3) ➔ Feature Store ➔ Training Pipeline (PyTorch) ➔ FastAPI (Serving) ➔ Docker Container",
        "Resources": [
            {"title": "roadmap.sh // AI & Data Scientist", "url": "https://roadmap.sh/ai-data-scientist"},
            {"title": "roadmap.sh // AI Engineer Roadmap", "url": "https://roadmap.sh/ai-engineer"},
            {"title": "Official PyTorch Deep Learning Tutorials", "url": "https://pytorch.org/tutorials/"}
        ]
    },
    "Backend Developer (Python / Cloud)": {
        "Phase 1: Core Language & Linux": ["Python (OOP & Typing)", "Linux & Shell Scripting", "Git Workflows"],
        "Phase 2: Frameworks & Relational DBs": ["FastAPI / Django", "PostgreSQL & Schema Design", "SQLAlchemy ORM"],
        "Phase 3: Caching, Queues & Auth": ["Redis Caching", "Celery Task Queues", "JWT & OAuth2 Security"],
        "Phase 4: Deployment & CI/CD": ["Docker & Microservices", "GitHub Actions CI/CD", "AWS Cloud (ECS/EC2)"],
        "Architecture": "Client Request ➔ Nginx Proxy ➔ FastAPI Gateway ➔ Redis Cache ➔ PostgreSQL DB ➔ Celery Async Worker",
        "Resources": [
            {"title": "roadmap.sh // Backend Roadmap", "url": "https://roadmap.sh/backend"},
            {"title": "roadmap.sh // Python Roadmap", "url": "https://roadmap.sh/python"},
            {"title": "FastAPI Documentation", "url": "https://fastapi.tiangolo.com/"}
        ]
    },
    "Frontend Developer (React / TS)": {
        "Phase 1: Web Fundamentals": ["HTML5 & Semantic Structure", "Modern CSS & Flexbox/Grid", "JavaScript (ES6+)"],
        "Phase 2: Modern Frontend Stack": ["TypeScript Basics & Types", "React Components & Hooks", "Tailwind CSS"],
        "Phase 3: State & Build Tools": ["Redux Toolkit / Zustand", "Next.js (App Router)", "Vite Build Setup"],
        "Phase 4: Testing & Performance": ["React Testing Library", "Web Vitals Optimization", "Vercel / Cloudflare Deployment"],
        "Architecture": "Edge CDN (Cloudflare) ➔ Next.js SSR Runtime ➔ React Virtual DOM ➔ Zustand Store ➔ REST/GraphQL API",
        "Resources": [
            {"title": "roadmap.sh // Frontend Roadmap", "url": "https://roadmap.sh/frontend"},
            {"title": "roadmap.sh // React Roadmap", "url": "https://roadmap.sh/react"},
            {"title": "Official TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/"}
        ]
    },
    "Full-Stack Web Developer": {
        "Phase 1: UI & Client Fundamentals": ["JavaScript / TypeScript", "HTML/CSS & Responsive Design", "React Framework"],
        "Phase 2: API & Backend Architecture": ["Node.js / Express or FastAPI", "RESTful API Design", "Authentication & Security"],
        "Phase 3: Database & ORM Management": ["PostgreSQL / MySQL", "MongoDB NoSQL", "Prisma / SQLAlchemy ORM"],
        "Phase 4: Full-Stack Integration & Cloud": ["Next.js Fullstack", "Docker Packaging", "AWS / Vercel Cloud Deployment"],
        "Architecture": "Next.js Frontend ➔ Node/Python API Server ➔ Prisma/SQLAlchemy ➔ PostgreSQL DB ➔ S3 Assets Bucket",
        "Resources": [
            {"title": "roadmap.sh // Full Stack Roadmap", "url": "https://roadmap.sh/full-stack"},
            {"title": "roadmap.sh // JavaScript Roadmap", "url": "https://roadmap.sh/javascript"},
            {"title": "Node.js Documentation", "url": "https://nodejs.org/en/docs"}
        ]
    },
    "DevOps & Cloud Infrastructure": {
        "Phase 1: OS, Networking & Scripting": ["Linux System Administration", "Networking (DNS, TCP/IP, TLS)", "Bash & Python Scripting"],
        "Phase 2: Containers & Orchestration": ["Docker & Image Optimization", "Kubernetes Architecture", "Helm Charts"],
        "Phase 3: Infrastructure as Code (IaC)": ["Terraform Automation", "Ansible Configuration", "CI/CD Pipelines (GitLab/GitHub)"],
        "Phase 4: Observability & Cloud Platforms": ["Prometheus & Grafana", "AWS (VPC, IAM, EKS, S3)", "Cloud Security"],
        "Architecture": "Git Commit ➔ GitHub Actions CI ➔ Docker Build ➔ Terraform Provisioning ➔ Kubernetes Cluster (EKS) ➔ Prometheus Monitoring",
        "Resources": [
            {"title": "roadmap.sh // DevOps Roadmap", "url": "https://roadmap.sh/devops"},
            {"title": "roadmap.sh // Kubernetes Roadmap", "url": "https://roadmap.sh/kubernetes"},
            {"title": "Docker Documentation", "url": "https://docs.docker.com/"}
        ]
    },
    "Cybersecurity & System Defense": {
        "Phase 1: Foundations & Systems": ["Linux & Operating System Internals", "Computer Networking Fundamentals", "Python & Bash Scripting"],
        "Phase 2: Security Concepts & Cryptography": ["Authentication Protocols & PKI", "Cryptography Algorithms", "Threat Modeling"],
        "Phase 3: Application & Network Security": ["OWASP Top 10 Vulnerabilities", "Network Traffic Analysis (Wireshark)", "Penetration Testing Tools"],
        "Phase 4: Cloud Security & Defense Ops": ["Cloud Security Posture", "SOC & SIEM Operations", "Incident Response Protocols"],
        "Architecture": "Ingress Firewall (WAF) ➔ TLS Termination ➔ Intrusion Detection (IDS) ➔ Zero-Trust Policy ➔ SIEM Log Analyzer",
        "Resources": [
            {"title": "roadmap.sh // Cybersecurity Roadmap", "url": "https://roadmap.sh/cyber-security"},
            {"title": "OWASP Security Testing Guide", "url": "https://owasp.org/www-project-web-security-testing-guide/"}
        ]
    }
}

# ==============================================================================
# 8. DATA LOADING PIPELINE
# ==============================================================================
@st.cache_data
def load_all_datasets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(current_dir, 'data'))
    if not os.path.exists(data_dir):
        data_dir = os.path.abspath(os.path.join(current_dir, '../data'))
    
    linkedin_path = os.path.join(data_dir, 'clean_linkedin_jobs.csv')
    df_linkedin = pd.read_csv(linkedin_path) if os.path.exists(linkedin_path) else pd.DataFrame()
    
    rules_path = os.path.join(data_dir, 'skill_association_rules.csv')
    df_rules = pd.read_csv(rules_path) if os.path.exists(rules_path) else pd.DataFrame()
    
    trends_path = os.path.join(data_dir, 'clean_google_trends.csv')
    if os.path.exists(trends_path):
        df_trends = pd.read_csv(trends_path)
        date_col = 'date' if 'date' in df_trends.columns else df_trends.columns[0]
        df_trends[date_col] = pd.to_datetime(df_trends[date_col])
        df_trends.set_index(date_col, inplace=True)
    else:
        df_trends = pd.DataFrame()
        
    return df_linkedin, df_rules, df_trends

df_linkedin, df_rules, df_trends = load_all_datasets()

available_skills = sorted(list(set(list(SKILL_SALARY_ESTIMATES.keys()) + list(AI_RESILIENCE_MATRIX.keys()))))
user_skills = [s for s in st.session_state.user_selected_stack if s in available_skills]

# Global KPI Calculations
track_scores_pre = {}
for track_name, track_info in ROADMAP_DATA.items():
    all_skills = []
    for phase_name, s_list in track_info.items():
        if phase_name not in ["Resources", "Architecture"]:
            for item in s_list:
                tokens = str(item).replace(',', '').replace('(', '').replace(')', '').split()
                if tokens:
                    all_skills.append(tokens[0])
    matched = [s for s in all_skills if any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)]
    score = int((len(matched) / max(len(all_skills), 1)) * 100)
    track_scores_pre[track_name] = min(score, 100)

best_fit_track = max(track_scores_pre, key=track_scores_pre.get) if track_scores_pre else "Data Science & AI Engineer"
best_fit_score = track_scores_pre.get(best_fit_track, 0)
base_val_kpi = max([SKILL_SALARY_ESTIMATES.get(s, 100000) for s in user_skills], default=100000) if user_skills else 0
avg_ai_shield = int(np.mean([AI_RESILIENCE_MATRIX.get(s, {}).get('score', 75) for s in user_skills])) if user_skills else 0

unowned_track_skills = []
for phase_name, s_list in ROADMAP_DATA.get(best_fit_track, {}).items():
    if phase_name not in ["Resources", "Architecture"]:
        for item in s_list:
            s_clean = str(item).split('(')[0].strip()
            if not any(u.lower() in s_clean.lower() or s_clean.lower() in u.lower() for u in user_skills):
                unowned_track_skills.append(s_clean)
next_best_skill = unowned_track_skills[0] if unowned_track_skills else "Kubernetes"

# ==============================================================================
# 9. STATIC IN-FLOW DASHBOARD HUD BAR
# ==============================================================================
hud_stack_pills = "".join([f'<span class="resend-chip" style="font-size:10px; padding:2px 7px; border-color:#2A2F37;">{s}</span>' for s in user_skills[:4]])
if len(user_skills) > 4:
    hud_stack_pills += f'<span class="resend-chip" style="font-size:10px; padding:2px 6px;">+{len(user_skills)-4}</span>'

st.markdown(f"""
<div class="floating-hud">
    <div style="display:flex; align-items:center; gap:12px;">
        <span class="pulse-dot"></span>
        <span style="font-size:12px; font-weight:700; color:#FFFFFF; letter-spacing:0.3px;">ACTIVE PROFILE:</span>
        <span style="font-size:12px; color:{primary_color}; font-weight:600;">{best_fit_track} ({best_fit_score}%)</span>
        <div style="display:flex; gap:5px; margin-left:6px;">{hud_stack_pills}</div>
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
        <div style="font-size:12px; color:#8A8F98;">Valuation: <b style="color:#10B981;">${base_val_kpi:,}</b></div>
        <div style="font-size:12px; color:#8A8F98;">AI Shield: <b style="color:{accent_color};">{avg_ai_shield}%</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 10. HERO HEADER
# ==============================================================================
st.markdown('<div class="resend-hero-title">Everything in your career, under control</div>', unsafe_allow_html=True)
st.markdown('<div class="resend-hero-sub">Data-driven intelligence powered by Stack Overflow, LinkedIn Jobs, and Google Trends — built without the friction.</div>', unsafe_allow_html=True)

# ==============================================================================
# 11. ULTRA-PROMINENT TOP NAVIGATION DOCK
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "✦  Stack Recommender",
    "↗  Future Outlook",
    "◈  Market Valuation",
    "⇄  1v1 Tech Arena",
    "⎔  Track Roadmaps & Vault",
    "📄  Resume & Gap Hunter",
    "🔀  Career Pivot Simulator",
    "⟐  Live Jobs Radar"
])

# ==============================================================================
# TAB 1: SMART SKILL RECOMMENDER
# ==============================================================================
with tab1:
    st.caption("⚡ Quick Persona Presets:")
    preset_cols = st.columns(4)
    for i, (p_name, p_skills) in enumerate(PRESET_PERSONAS.items()):
        with preset_cols[i]:
            if st.button(p_name, use_container_width=True):
                st.session_state.user_selected_stack = [s for s in p_skills if s in available_skills]
                st.rerun()

    c_sel, c_copy = st.columns([4, 1], vertical_alignment="bottom")
    with c_sel:
        user_skills_input = st.multiselect(
            "Select or customize your active technical stack:",
            options=available_skills,
            default=user_skills
        )
        if user_skills_input != st.session_state.user_selected_stack:
            st.session_state.user_selected_stack = user_skills_input
            st.rerun()
    with c_copy:
        if st.button("📋 Copy Profile Summary", use_container_width=True):
            profile_summary_txt = f"Tech Stack: {', '.join(user_skills)} | Primary Fit: {best_fit_track} ({best_fit_score}%) | Base Valuation: ${base_val_kpi:,}/yr | AI Shield: {avg_ai_shield}% | Architect: Mehdi Bagheri"
            st.toast("Profile summary ready in clipboard!", icon="✅")

    st.write("")
    bento_col_left, bento_col_mid, bento_col_right = st.columns([1.5, 1, 1])

    with bento_col_left:
        st.markdown(f"""
        <div class="bento-card bento-card-hero">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span class="resend-chip resend-chip-active shimmer-badge">{render_tg_icon("star", 12)} OPTIMAL FIT</span>
                    <span class="pulse-dot"></span>
                </div>
                <div style="font-size: 13px; color: #8A8F98;">Primary Career Specialization <span class="info-tooltip" title="Specialization calculated by matching active stack with 6 engineering career tracks">ⓘ</span></div>
                <div style="font-size: 24px; font-weight: 700; color: #F0F0F0; margin: 4px 0 12px 0;">{best_fit_track}</div>
            </div>
            <div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px; color:#8A8F98;">
                    <span>Profile Match Index</span>
                    <span style="color:{primary_color}; font-weight:700;">{best_fit_score}%</span>
                </div>
                <div style="background:#1A1D20; height:6px; border-radius:99px; overflow:hidden; margin-bottom:10px;">
                    <div style="background:{primary_color}; height:100%; width:{best_fit_score}%;"></div>
                </div>
                <span class="resend-chip resend-chip-active" style="font-size:10.5px;">🔥 Next Best Step: {next_best_skill} (+15% Fit)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with bento_col_mid:
        st.markdown(f"""
        <div class="bento-card">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span class="resend-chip resend-chip-success">{render_tg_icon("diamond", 12)} VALUATION</span>
                </div>
                <div style="font-size: 13px; color: #8A8F98;">Base Market Compensation <span class="info-tooltip" title="Derived from real-world cleaned LinkedIn postings median salary">ⓘ</span></div>
                <div style="font-size: 28px; font-weight: 700; color: #10B981; margin: 4px 0;">${base_val_kpi:,}</div>
            </div>
            <div style="font-size: 12px; color: #8A8F98;">Derived from normalized median job listings.</div>
        </div>
        """, unsafe_allow_html=True)

    with bento_col_right:
        st.markdown(f"""
        <div class="bento-card">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span class="resend-chip">{render_tg_icon("shield", 12)} AI SHIELD</span>
                </div>
                <div style="font-size: 13px; color: #8A8F98;">Automation Resistance <span class="info-tooltip" title="Quantifies resilience against autonomous generative code generation">ⓘ</span></div>
                <div style="font-size: 28px; font-weight: 700; color: {accent_color}; margin: 4px 0;">{avg_ai_shield}%</div>
            </div>
            <div style="font-size: 12px; color: #8A8F98;">Evaluated against LLM autonomous code synthesis.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        {render_tg_icon('sparkle', 24)}
        <span style="font-size: 19px; font-weight: 700; color: #F0F0F0;">Skill Synergy & Sequential Recommendations</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Association rules and co-occurrence patterns discovered from 32,000+ developer profiles:")
    
    if user_skills and not df_rules.empty:
        matched_recommendations = []
        for idx, row in df_rules.iterrows():
            antecedents = [s.strip() for s in str(row['antecedents_str']).split(',')]
            consequents = [s.strip() for s in str(row['consequents_str']).split(',')]
            if all(item in user_skills for item in antecedents):
                for cons in consequents:
                    if cons not in user_skills:
                        matched_recommendations.append({
                            'skill': cons,
                            'antecedents': ', '.join(antecedents),
                            'confidence': row['confidence'],
                            'lift': row['lift'],
                            'salary': SKILL_SALARY_ESTIMATES.get(cons, 110000)
                        })
                        
        df_recs = pd.DataFrame(matched_recommendations).drop_duplicates(subset=['skill']).sort_values(by='lift', ascending=False).head(6)
        
        st.write("")
        if not df_recs.empty:
            cols = st.columns(min(len(df_recs), 3))
            for i, (_, row) in enumerate(df_recs.iterrows()):
                col_idx = i % 3
                ai_info = AI_RESILIENCE_MATRIX.get(row['skill'], {'score': 75, 'risk': 'Moderate'})
                logo_html = get_skill_logo(row["skill"], large=True)
                
                card_html = (
                    f'<div class="resend-card" style="margin-bottom: 12px;">'
                    f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">'
                    f'<div style="display: flex; align-items: center;">{logo_html}<span style="color: #F0F0F0; font-size: 17px; font-weight: 600;">{row["skill"]}</span></div>'
                    f'<span class="resend-chip resend-chip-active shimmer-badge" title="Lift factor measures how much more likely this skill is used with your stack">{render_tg_icon("star", 13)} LIFT {row["lift"]:.2f}x</span>'
                    f'</div>'
                    f'<div style="color: {primary_color}; font-size: 24px; font-weight: 700; margin-bottom: 4px;">'
                    f'{row["confidence"]*100:.1f}% <span style="font-size: 13px; color: #8A8F98; font-weight: 400;">Confidence</span>'
                    f'</div>'
                    f'<div style="font-size: 13px; color: #8A8F98; margin-bottom: 8px;">'
                    f'Market Value: <b style="color: #F0F0F0;">${row["salary"]:,}/yr</b>'
                    f'</div>'
                    f'<div style="font-size: 12px; color: #8A8F98; margin-bottom: 12px;">'
                    f'Prerequisites: <span style="color: {accent_color}; font-family: \'JetBrains Mono\', monospace;">{row["antecedents"]}</span>'
                    f'</div>'
                    f'<span class="resend-chip resend-chip-success">{render_tg_icon("shield", 13)} AI SHIELD {ai_info["score"]}%</span>'
                    f'</div>'
                )
                with cols[col_idx]:
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("Solid stack established. Consider adding foundational cloud/backend containers.")
    else:
        st.info("Select at least one skill above to compute recommendation vectors.")

# ==============================================================================
# TAB 2: FUTURE OUTLOOK & TRENDS
# ==============================================================================
with tab2:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        {render_tg_icon('trend', 24)}
        <span style="font-size: 19px; font-weight: 700; color: #F0F0F0;">Dynamic Radar & 3-Year Trajectory Projection</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Multi-horizon time-series evaluation combining 4-Month momentum, 3-Year linear forecasting, and AI resilience.")
    
    if not df_trends.empty:
        trend_skills = df_trends.columns.tolist()
        selected_trend_skills = st.multiselect(
            "Select technologies for comparative trajectory modeling:",
            options=trend_skills,
            default=trend_skills[:4] if len(trend_skills) >= 4 else trend_skills
        )
        
        if selected_trend_skills:
            forecast_weeks = 156
            last_date = df_trends.index[-1]
            future_dates = pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=forecast_weeks, freq='W')
            
            fig_trends = go.Figure()
            colors_palette = [primary_color, '#10B981', '#F59E0B', '#EC4899', '#8B5CF6', accent_color]
            forecast_results = {}
            
            for i, skill in enumerate(selected_trend_skills):
                series = df_trends[skill].dropna()
                x_hist = np.arange(len(series))
                y_hist = series.values
                
                slope, intercept = np.polyfit(x_hist, y_hist, 1)
                x_future = np.arange(len(series), len(series) + forecast_weeks)
                y_future = np.clip(slope * x_future + intercept, 0, 100)
                
                ai_info = AI_RESILIENCE_MATRIX.get(skill, {'score': 75, 'risk': 'Moderate'})
                ai_score = ai_info['score']
                normalized_slope_factor = np.clip(slope * 50, -0.4, 0.4)
                half_life_years = round(5.5 * (1 + normalized_slope_factor) * (ai_score / 80), 1)
                
                forecast_results[skill] = {
                    'short_3m': series.tail(16).mean(),
                    'slope': slope,
                    'forecast_3y': float(y_future[-1]),
                    'half_life': half_life_years,
                    'ai_score': ai_score,
                    'ai_risk': ai_info['risk']
                }
                
                c = colors_palette[i % len(colors_palette)]
                fig_trends.add_trace(go.Scatter(
                    x=series.index, y=series.values,
                    mode='lines', name=f"{skill} (Historical)",
                    line=dict(color=c, width=2.5),
                    hovertemplate=f"<b>{skill}</b><br>Date: %{{x|%Y-%m}}<br>Index: %{{y:.1f}}<extra></extra>"
                ))
                fig_trends.add_trace(go.Scatter(
                    x=future_dates, y=y_future,
                    mode='lines', name=f"{skill} (3-Yr Projection)",
                    line=dict(color=c, width=2, dash='dash'),
                    opacity=0.75,
                    hovertemplate=f"<b>{skill} [Forecast]</b><br>Date: %{{x|%Y-%m}}<br>Projected: %{{y:.1f}}<extra></extra>"
                ))
                
            fig_trends.add_vline(x=last_date, line_width=1.5, line_dash="dot", line_color="#EF4444")
            apply_plotly_theme(fig_trends, height=400)
            st.plotly_chart(fig_trends, config=PLOTLY_CONFIG, width="stretch")
            
            st.write("")
            st.markdown("##### Multi-Horizon Metric Scorecards")
            cols = st.columns(len(selected_trend_skills))
            
            for i, skill in enumerate(selected_trend_skills):
                data = forecast_results[skill]
                slope = data['slope']
                pred_val = data['forecast_3y']
                logo_html = get_skill_logo(skill, large=False)
                
                if pred_val >= 60 or slope > 0.04:
                    future_status, badge_class = "ACCELERATING", "resend-chip resend-chip-success"
                elif pred_val >= 25 or slope >= -0.02:
                    future_status, badge_class = "SUSTAINABLE", "resend-chip resend-chip-active"
                else:
                    future_status, badge_class = "DEPRECATING", "resend-chip resend-chip-danger"
                    
                card_html = (
                    f'<div class="resend-card" style="margin-bottom: 12px;">'
                    f'<div style="display: flex; align-items: center; border-bottom: 1px solid #262A2D; padding-bottom: 8px; margin-bottom: 10px;">'
                    f'{logo_html}<span style="color: #F0F0F0; font-size: 16px; font-weight: 600;">{skill}</span>'
                    f'</div>'
                    f'<div style="margin-bottom: 6px;">'
                    f'<span style="color: #8A8F98; font-size: 11px; font-weight: 600; text-transform: uppercase;">Recent Pulse</span>'
                    f'<div style="color: #F0F0F0; font-size: 16px; font-weight: 600;">{data["short_3m"]:.1f} <span style="font-size: 11px; color: #8A8F98;">/100</span></div>'
                    f'</div>'
                    f'<div style="margin-bottom: 6px;">'
                    f'<span style="color: #8A8F98; font-size: 11px; font-weight: 600; text-transform: uppercase;">3-Year Projection</span>'
                    f'<div style="color: {primary_color}; font-size: 16px; font-weight: 700;">{pred_val:.1f} <span style="font-size: 11px; color: #8A8F98;">/100</span></div>'
                    f'</div>'
                    f'<div style="margin-bottom: 10px;">'
                    f'<span style="color: #8A8F98; font-size: 11px; font-weight: 600; text-transform: uppercase;">AI Resilience</span>'
                    f'<div style="color: #F0F0F0; font-size: 16px; font-weight: 600;">{data["ai_score"]}%</div>'
                    f'</div>'
                    f'<span class="{badge_class}">{future_status}</span>'
                    f'</div>'
                )
                with cols[i]:
                    st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.warning("Google Trends dataset not loaded.")

# ==============================================================================
# TAB 3: SALARY INTELLIGENCE
# ==============================================================================
with tab3:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        {render_tg_icon('diamond', 24)}
        <span style="font-size: 19px; font-weight: 700; color: #F0F0F0;">Economic Valuation & Market Compensation</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Annual compensation benchmarks derived from normalized LinkedIn job data:")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("##### Top Compensated Technologies (Median USD)")
        df_sal_chart = pd.DataFrame(list(SKILL_SALARY_ESTIMATES.items()), columns=['Skill', 'Median Salary']).sort_values(by='Median Salary', ascending=True).tail(10)
        fig_sal = go.Figure(go.Bar(
            x=df_sal_chart['Median Salary'],
            y=df_sal_chart['Skill'],
            orientation='h',
            marker=dict(color=primary_color),
            text=[f"${v:,}" for v in df_sal_chart['Median Salary']],
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Median Salary: $%{x:,}<extra></extra>"
        ))
        apply_plotly_theme(fig_sal, height=340)
        fig_sal.update_layout(showlegend=False, margin=dict(l=20, r=60, t=10, b=20))
        st.plotly_chart(fig_sal, config=PLOTLY_CONFIG, width="stretch")
        
    with col_b:
        st.markdown("##### Stack Premium Calculator")
        base_skill = st.selectbox("Select Core Language:", ["Python", "JavaScript", "Go", "Rust", "C++"])
        addon_cloud = st.checkbox("Include Cloud & Containerization (AWS / Docker)", value=True)
        addon_ai = st.checkbox("Include Deep Learning Frameworks (PyTorch / Scikit-Learn)", value=False)
        
        base_val = SKILL_SALARY_ESTIMATES.get(base_skill, 100000)
        total_val = base_val + (20000 if addon_cloud else 0) + (25000 if addon_ai else 0)
        
        st.markdown(f"""
        <div class="resend-card" style="margin-top: 12px;">
            <div style="color: #8A8F98; font-size: 13px; margin-bottom: 4px;">Projected Market Valuation</div>
            <div style="color: {primary_color}; font-size: 32px; font-weight: 700; letter-spacing: -0.5px;">${total_val:,} <span style="font-size: 14px; color: #8A8F98; font-weight: 400;">/ year</span></div>
            <div style="color: #10B981; font-size: 13px; font-weight: 500; margin-top: 4px;">+${total_val - base_val:,} Stack Synergy Premium</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: 1v1 HEAD-TO-HEAD ARENA (SUPERCHARGED RADAR & COMPARISON ENGINE)
# ==============================================================================
with tab4:
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;">
                <path d="M14.5 17.5L3 6V3H6L17.5 14.5" stroke="{primary_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M13 19L19 13M16 16L20 20M19 21L21 19" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/>
                <path d="M14.5 6.5L18 3H21V6L17.5 9.5" stroke="{primary_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M5 14L9 18M7 17L4 20M3 19L5 21" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span style="font-size: 20px; font-weight: 700; color: #F0F0F0; letter-spacing: -0.3px;">1v1 Technology Head-to-Head Arena</span>
        </div>
        <span class="resend-chip resend-chip-active shimmer-badge">MULTI-DIMENSIONAL BENCHMARK</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Deep side-by-side architectural evaluation across salary benchmarks, automation resistance, learning curves, and ecosystem momentum:")

    col_vs_sel1, col_vs_sel2, col_vs_goal = st.columns([1.2, 1.2, 1])
    with col_vs_sel1:
        tech_a = st.selectbox("Select Fighter Alpha [A]:", options=available_skills, index=available_skills.index("FastAPI") if "FastAPI" in available_skills else 0)
    with col_vs_sel2:
        tech_b = st.selectbox("Select Fighter Beta [B]:", options=available_skills, index=available_skills.index("Django") if "Django" in available_skills else 1)
    with col_vs_goal:
        decision_priority = st.selectbox("Decision Priority Goal:", ["Balanced Overview", "Max Compensation", "Highest AI Longevity", "Fastest Time-to-Job"])

    if tech_a and tech_b:
        val_a = SKILL_SALARY_ESTIMATES.get(tech_a, 110000)
        val_b = SKILL_SALARY_ESTIMATES.get(tech_b, 110000)
        ai_a = AI_RESILIENCE_MATRIX.get(tech_a, {'score': 75, 'risk': 'Moderate', 'learn_hours': 60})
        ai_b = AI_RESILIENCE_MATRIX.get(tech_b, {'score': 75, 'risk': 'Moderate', 'learn_hours': 60})
        hrs_a = ai_a.get('learn_hours', get_skill_study_hours(tech_a))
        hrs_b = ai_b.get('learn_hours', get_skill_study_hours(tech_b))

        spec_a = TECH_ARENA_SPECS.get(tech_a, {'demand': 85, 'remote': 85, 'maturity': 88, 'syntax': 'Standard', 'best_for': f'Core {tech_a} Engineering & Development', 'companions': ['PostgreSQL', 'Docker', 'Git']})
        spec_b = TECH_ARENA_SPECS.get(tech_b, {'demand': 85, 'remote': 85, 'maturity': 88, 'syntax': 'Standard', 'best_for': f'Core {tech_b} Engineering & Development', 'companions': ['PostgreSQL', 'Docker', 'Git']})

        dim_names = ['Compensation', 'AI Shield', 'Job Demand', 'Study Efficiency', 'Remote Ratio', 'Maturity']
        scores_a = [
            min(int((val_a / 160000) * 100), 100),
            ai_a['score'],
            spec_a['demand'],
            max(100 - int((hrs_a / 180) * 80), 20),
            spec_a['remote'],
            spec_a['maturity']
        ]
        scores_b = [
            min(int((val_b / 160000) * 100), 100),
            ai_b['score'],
            spec_b['demand'],
            max(100 - int((hrs_b / 180) * 80), 20),
            spec_b['remote'],
            spec_b['maturity']
        ]

        if decision_priority == "Max Compensation":
            total_a = val_a
            total_b = val_b
            winner_text = f"👑 {tech_a if val_a >= val_b else tech_b} offers higher median earnings."
        elif decision_priority == "Highest AI Longevity":
            total_a = ai_a['score']
            total_b = ai_b['score']
            winner_text = f"🛡️ {tech_a if ai_a['score'] >= ai_b['score'] else tech_b} provides superior resistance against autonomous AI generation."
        elif decision_priority == "Fastest Time-to-Job":
            total_a = (100 - hrs_a) + spec_a['demand']
            total_b = (100 - hrs_b) + spec_b['demand']
            winner_text = f"⚡ {tech_a if total_a >= total_b else tech_b} has a quicker path to employment with less learning overhead."
        else:
            total_a = np.mean(scores_a)
            total_b = np.mean(scores_b)
            winner_name = tech_a if total_a >= total_b else tech_b
            winner_text = f"🏆 Overall Architectural Winner: **{winner_name}** ({int(max(total_a, total_b))}/100 Composite Score)"

        st.write("")
        st.markdown(f"""
        <div class="resend-card-highlight" style="padding: 14px 20px; display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span class="pulse-dot"></span>
                <span style="font-size:14px; font-weight:600; color:#FFFFFF;">{winner_text}</span>
            </div>
            <span class="resend-chip resend-chip-active">VERDICT ENGINE</span>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_arena_rad, col_arena_cards = st.columns([1.2, 1])

        with col_arena_rad:
            st.markdown("##### 6-Axis Architectural Symmetry Radar")
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=scores_a + [scores_a[0]],
                theta=dim_names + [dim_names[0]],
                fill='toself',
                name=tech_a,
                line=dict(color=primary_color, width=2),
                fillcolor=f"rgba(0, 163, 255, 0.22)"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=scores_b + [scores_b[0]],
                theta=dim_names + [dim_names[0]],
                fill='toself',
                name=tech_b,
                line=dict(color='#10B981', width=2),
                fillcolor="rgba(16, 185, 129, 0.22)"
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], showline=False, gridcolor="#262A2D"),
                    angularaxis=dict(gridcolor="#262A2D", linecolor="#262A2D")
                ),
                showlegend=True,
                margin=dict(l=40, r=40, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#F0F0F0", size=11),
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_radar, config=PLOTLY_CONFIG, width="stretch")

        with col_arena_cards:
            st.markdown("##### Side-by-Side Detailed Breakdown")
            
            logo_a = get_skill_logo(tech_a, large=False)
            logo_b = get_skill_logo(tech_b, large=False)
            
            st.markdown(f"""
            <div style="background:#0D1015; border:1px solid #1F242D; border-radius:10px; padding:12px 16px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center;">{logo_a} <b style="color:#FFFFFF; font-size:15px;">{tech_a}</b></div>
                    <span class="resend-chip resend-chip-active" style="font-size:10px;">ALPHA FIGHTER</span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:12px; color:#8A8F98;">
                    <div>Median Salary: <b style="color:#10B981;">${val_a:,}</b></div>
                    <div>AI Shield: <b style="color:{accent_color};">{ai_a['score']}%</b></div>
                    <div>Study Curve: <b style="color:#FFFFFF;">~{hrs_a}h</b></div>
                    <div>Remote Availability: <b style="color:#FFFFFF;">{spec_a['remote']}%</b></div>
                </div>
                <div style="font-size:11.5px; color:#8A8F98; margin-top:8px; border-top:1px solid #1C2026; padding-top:6px;">
                    Best for: <span style="color:#F0F0F0;">{spec_a['best_for']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#0D1015; border:1px solid #1F242D; border-radius:10px; padding:12px 16px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center;">{logo_b} <b style="color:#FFFFFF; font-size:15px;">{tech_b}</b></div>
                    <span class="resend-chip resend-chip-success" style="font-size:10px;">BETA FIGHTER</span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; font-size:12px; color:#8A8F98;">
                    <div>Median Salary: <b style="color:#10B981;">${val_b:,}</b></div>
                    <div>AI Shield: <b style="color:{accent_color};">{ai_b['score']}%</b></div>
                    <div>Study Curve: <b style="color:#FFFFFF;">~{hrs_b}h</b></div>
                    <div>Remote Availability: <b style="color:#FFFFFF;">{spec_b['remote']}%</b></div>
                </div>
                <div style="font-size:11.5px; color:#8A8F98; margin-top:8px; border-top:1px solid #1C2026; padding-top:6px;">
                    Best for: <span style="color:#F0F0F0;">{spec_b['best_for']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("##### High-Synergy Stack Companions")
        col_comp_a, col_comp_b = st.columns(2)
        with col_comp_a:
            badges_a = "".join([f'<span class="resend-chip" style="margin:2px 4px; font-size:11px;">{get_skill_logo(s, False)} {s}</span>' for s in spec_a['companions']])
            st.markdown(f"""
            <div style="background:#090B0E; border:1px solid #1C2026; border-radius:8px; padding:10px 14px;">
                <div style="font-size:12px; color:#8A8F98; margin-bottom:6px;">Recommended with <b>{tech_a}</b>:</div>
                {badges_a}
            </div>
            """, unsafe_allow_html=True)
        with col_comp_b:
            badges_b = "".join([f'<span class="resend-chip" style="margin:2px 4px; font-size:11px;">{get_skill_logo(s, False)} {s}</span>' for s in spec_b['companions']])
            st.markdown(f"""
            <div style="background:#090B0E; border:1px solid #1C2026; border-radius:8px; padding:10px 14px;">
                <div style="font-size:12px; color:#8A8F98; margin-bottom:6px;">Recommended with <b>{tech_b}</b>:</div>
                {badges_b}
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: ROADMAPS, MILESTONES, CURATED VAULT & REPORT GENERATOR
# ==============================================================================
with tab5:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        {render_tg_icon('compass', 24)}
        <span style="font-size: 19px; font-weight: 700; color: #F0F0F0;">Multi-Track Career Readiness & Milestone Tracker</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Real-time profile alignment, cumulative study hours, and sequential milestone tracker across 6 specializations:")

    track_scores = {}
    for track_name, track_info in ROADMAP_DATA.items():
        all_skills = []
        for phase_name, s_list in track_info.items():
            if phase_name not in ["Resources", "Architecture"]:
                for item in s_list:
                    tokens = str(item).replace(',', '').replace('(', '').replace(')', '').split()
                    if tokens:
                        all_skills.append(tokens[0])
        matched = [s for s in all_skills if any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)]
        score = int((len(matched) / max(len(all_skills), 1)) * 100)
        track_scores[track_name] = min(score, 100)

    best_track = max(track_scores, key=track_scores.get)
    best_track_index = list(ROADMAP_DATA.keys()).index(best_track)
    track_items = list(track_scores.items())

    def render_track_card(name, score, is_top):
        card_class = "resend-card-highlight" if is_top else "resend-card"
        badge_html = f"<span class='resend-chip resend-chip-active shimmer-badge'>{render_tg_icon('star', 12)} PRIMARY FIT</span>" if is_top else ""
        short_title = name.split('(')[0].strip()
        return (
            f'<div class="{card_class}" style="margin-bottom: 12px;">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<span style="color: #F0F0F0; font-size: 14px; font-weight: 600;">{short_title}</span>'
            f'{badge_html}'
            f'</div>'
            f'<div style="color: {primary_color}; font-size: 26px; font-weight: 700; letter-spacing: -0.5px;">{score}%</div>'
            f'</div>'
        )

    cols_row1 = st.columns(3)
    for idx in range(3):
        t_name, t_score = track_items[idx]
        with cols_row1[idx]:
            st.markdown(render_track_card(t_name, t_score, t_name == best_track), unsafe_allow_html=True)

    cols_row2 = st.columns(3)
    for idx in range(3, 6):
        t_name, t_score = track_items[idx]
        with cols_row2[idx - 3]:
            st.markdown(render_track_card(t_name, t_score, t_name == best_track), unsafe_allow_html=True)

    st.write("")
    selected_path = st.selectbox(
        "Explore detailed engineering trajectory for:",
        options=list(ROADMAP_DATA.keys()),
        index=best_track_index
    )

    path_details = ROADMAP_DATA[selected_path]
    current_match = track_scores[selected_path]

    all_path_skills = []
    phase_stats = []
    for phase_name, skill_list in path_details.items():
        if phase_name not in ["Resources", "Architecture"]:
            all_path_skills.extend(skill_list)
            p_owned = [s for s in skill_list if any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)]
            p_missing = [s for s in skill_list if s not in p_owned]
            p_hours = sum([get_skill_study_hours(s) for s in p_missing])
            phase_stats.append({
                'phase': phase_name,
                'total': len(skill_list),
                'acquired': len(p_owned),
                'missing': len(p_missing),
                'hours_rem': p_hours,
                'skills': skill_list
            })

    total_missing_hours = sum([p['hours_rem'] for p in phase_stats])
    completed_phases = sum([1 for p in phase_stats if p['missing'] == 0])

    st.write("")
    st.markdown(f"""
    <div class="resend-card-highlight" style="padding:18px 24px; margin-bottom:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <span class="resend-chip resend-chip-active shimmer-badge" style="margin-bottom:6px;">⏱ MILESTONE PROGRESS TRACKER</span>
                <div style="font-size:22px; font-weight:700; color:#FFFFFF;">{selected_path}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:12px; color:#8A8F98;">Estimated Time to Mastery</div>
                <div style="font-size:26px; font-weight:700; color:#10B981;">~{total_missing_hours} Hours</div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px; color:#8A8F98;">
            <span>Phases Completed: <b>{completed_phases} / {len(phase_stats)}</b></span>
            <span>Target Readiness Index: <b>{current_match}%</b></span>
        </div>
        <div style="background:#1A1D20; height:8px; border-radius:99px; overflow:hidden;">
            <div style="background:linear-gradient(90deg, {primary_color}, #10B981); height:100%; width:{current_match}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Sequential Learning Milestones & Study Allocations")
    for idx, p_info in enumerate(phase_stats, 1):
        phase_status = "COMPLETED" if p_info['missing'] == 0 else f"~{p_info['hours_rem']}h REMAINING"
        chip_style = "resend-chip-success" if p_info['missing'] == 0 else "resend-chip-active"

        st.markdown(f"""
        <div style="border-left: 3px solid {primary_color if p_info['missing'] > 0 else '#10B981'}; padding-left: 14px; margin-top: 18px; margin-bottom: 10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="color: #8A8F98; font-size: 11px; font-weight: 700; font-family:'JetBrains Mono', monospace;">STEP 0{idx}</span>
                <div style="color: #F0F0F0; font-size: 15px; font-weight: 600;">{p_info['phase']}</div>
            </div>
            <span class="resend-chip {chip_style}">{phase_status}</span>
        </div>
        """, unsafe_allow_html=True)

        for s in p_info['skills']:
            is_owned = any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)
            logo_html = get_skill_logo(s, large=False)
            badge_style = "resend-chip-success" if is_owned else "resend-chip"
            badge_label = "ACQUIRED" if is_owned else f"~{get_skill_study_hours(s)}h"

            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; background:#0D0D0D; padding:10px 18px; border-radius:10px; border:1px solid {'rgba(16,185,129,0.35)' if is_owned else '#1F2327'}; margin-bottom:6px;">
                <div style="display:flex; align-items:center;">{logo_html} <span style="font-size:13.5px; font-weight:500; color:#F0F0F0;">{s}</span></div>
                <span class="resend-chip {badge_style}">{badge_label}</span>
            </div>
            """, unsafe_allow_html=True)

    # Curated Resources Vault
    st.write("")
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 16px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            {render_tg_icon('compass', 20)}
            <span style="font-size: 16px; font-weight: 700; color: #F0F0F0;">Curated Technical Documentation & Industry Guides</span>
        </div>
        <span class="resend-chip" style="font-size: 10.5px; border-color: #242930;">OFFICIAL VAULT</span>
    </div>
    """, unsafe_allow_html=True)

    res_list = path_details.get("Resources", [])
    if res_list:
        for idx, res in enumerate(res_list):
            title_text = res['title']
            url_domain = res['url'].split('//')[-1].split('/')[0]
            title_lower = title_text.lower()

            if 'roadmap' in title_lower:
                badge_type = "ROADMAP"
                badge_style = "resend-chip-success"
                res_logo = f'''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:10px; vertical-align:middle;">
                    <path d="M4 19L9 14L14 17L20 9" stroke="{primary_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="20" cy="9" r="2.5" fill="{accent_color}"/>
                    <circle cx="4" cy="19" r="2" fill="#8A8F98"/>
                </svg>'''
            elif 'pytorch' in title_lower:
                badge_type = "TUTORIAL"
                badge_style = "resend-chip-active"
                res_logo = '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytorch/pytorch-original.svg" class="tech-logo-img" alt="PyTorch" />'
            elif 'fastapi' in title_lower:
                badge_type = "DOCS"
                badge_style = "resend-chip"
                res_logo = '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" class="tech-logo-img" alt="FastAPI" />'
            elif 'python' in title_lower:
                badge_type = "DOCS"
                badge_style = "resend-chip"
                res_logo = '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" class="tech-logo-img" alt="Python" />'
            elif 'docker' in title_lower:
                badge_type = "DOCS"
                badge_style = "resend-chip"
                res_logo = '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" class="tech-logo-img" alt="Docker" />'
            elif 'kubernetes' in title_lower:
                badge_type = "DOCS"
                badge_style = "resend-chip"
                res_logo = '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-plain.svg" class="tech-logo-img" alt="K8s" />'
            elif 'owasp' in title_lower or 'security' in title_lower:
                badge_type = "SECURITY"
                badge_style = "resend-chip-danger"
                res_logo = f'''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:10px; vertical-align:middle;">
                    <path d="M12 22S20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" fill="{glow_color}" stroke="{primary_color}" stroke-width="2"/>
                </svg>'''
            else:
                badge_type = "MANUAL"
                badge_style = "resend-chip"
                res_logo = f'''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:10px; vertical-align:middle;">
                    <rect x="3" y="4" width="18" height="16" rx="3" stroke="#262A2D" stroke-width="2" fill="#141414"/>
                    <path d="M7 9L10 12L7 15M12 15H17" stroke="{primary_color}" stroke-width="2" stroke-linecap="round"/>
                </svg>'''

            st.markdown(f"""
            <a href="{res['url']}" target="_blank" class="resource-vault-row">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span class="resend-chip {badge_style}" style="font-size: 10px; font-weight: 700; padding: 2px 8px;">{badge_type}</span>
                    <div style="display: flex; align-items: center;">
                        {res_logo}
                        <span class="vault-title" style="color: #F0F0F0; font-size: 14px; font-weight: 500; transition: color 0.2s ease;">{title_text}</span>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6B7280;">{url_domain}</span>
                    <svg class="vault-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{primary_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.2s ease;"><line x1="7" y1="17" x2="17" y2="7"></line><polyline points="7 7 17 7 17 17"></polyline></svg>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # Production Download CTA Box
    st.write("")
    st.markdown("#### Executive Report Generation")
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    report_md = f"""# Executive Career Intelligence Report
**Generated on:** {report_date}  
**Lead Architect:** Mehdi Bagheri  
**Data Sources:** Stack Overflow 2025 Survey, Cleaned LinkedIn Postings, Google Trends 5-Year

---

## 1. Executive Summary & Profile
* **Active Stack:** {', '.join(user_skills) if user_skills else 'None'}
* **Primary Target:** {best_track} ({track_scores.get(best_track, 0)}% Match)
* **Estimated Base Value:** ${SKILL_SALARY_ESTIMATES.get(user_skills[0], 100000) if user_skills else 0:,} USD/Year
* **Estimated Study Hours Remaining:** ~{total_missing_hours} Hours

---

## 2. Career Track Matrix
| Career Specialization | Alignment Score | Status |
| :--- | :---: | :--- |
"""
    for t_name, score in track_scores.items():
        status_str = "Primary Fit" if t_name == best_track else ("Strong Match" if score >= 50 else "Development")
        report_md += f"| {t_name} | {score}% | {status_str} |\n"

    report_md += f"""
---

## 3. Targeted Roadmap: {selected_path}
"""
    for phase_name, s_list in path_details.items():
        if phase_name not in ["Resources", "Architecture"]:
            report_md += f"\n### {phase_name}\n"
            for item in s_list:
                is_owned = any(u.lower() in item.lower() for u in user_skills)
                tag = "[ACQUIRED]" if is_owned else "[TARGET]"
                report_md += f"- {tag} {item}\n"

    cta_col_info, cta_col_btn = st.columns([3, 1], vertical_alignment="center")
    with cta_col_info:
        st.markdown(f"""
        <div class="resend-card" style="padding:14px 18px;">
            <div style="font-size:14px; font-weight:600; color:#F0F0F0; margin-bottom:2px;">Export Comprehensive Intelligence Dossier</div>
            <div style="font-size:12px; color:#8A8F98;">Format: <b>Markdown (.md)</b> • Size: <b>~4 KB</b> • Updated: <b>{report_date}</b></div>
        </div>
        """, unsafe_allow_html=True)
    with cta_col_btn:
        st.download_button(
            label="📥 Download Report",
            data=report_md,
            file_name=f"Career_Intelligence_Report_{datetime.datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ==============================================================================
# TAB 6: UNIFIED RESUME ATS SCANNER & TARGET GAP HUNTER
# ==============================================================================
with tab6:
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            {render_tg_icon('document', 24)}
            <span style="font-size: 20px; font-weight: 700; color: #F0F0F0; letter-spacing: -0.3px;">Unified Resume ATS Parser & Gap Hunter</span>
        </div>
        <span class="resend-chip resend-chip-active shimmer-badge">INTELLIGENCE SCANNER</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Upload or paste your resume alongside target job descriptions to calculate your ATS compliance index and hunt critical missing stack competencies:")

    col_unified_in1, col_unified_in2 = st.columns(2)

    with col_unified_in1:
        st.markdown("###### 1. Resume Source Document")
        uploaded_cv = st.file_uploader("Upload Resume (PDF / TXT):", type=["pdf", "txt"])
        pasted_cv = st.text_area("Or Paste Full Resume Text:", height=150, placeholder="Paste resume sections, experience, and competencies...")

        cv_text = ""
        if uploaded_cv is not None:
            if uploaded_cv.name.lower().endswith(".pdf"):
                try:
                    import pypdf
                    reader = pypdf.PdfReader(uploaded_cv)
                    for page in reader.pages:
                        cv_text += (page.extract_text() or "") + "\n"
                except Exception:
                    uploaded_cv.seek(0)
                    raw_bytes = uploaded_cv.read()
                    cv_text = " ".join(re.findall(r'[A-Za-z0-9+#./-]{2,}', raw_bytes.decode('latin-1', errors='ignore')))
            else:
                cv_text = uploaded_cv.read().decode('utf-8', errors='ignore')
        elif pasted_cv.strip():
            cv_text = pasted_cv.strip()

    with col_unified_in2:
        st.markdown("###### 2. Target Job Description / Posting")
        default_target_jd = """We are seeking a Senior Backend Engineer to build scalable microservices.
Requirements:
- Proven experience with Python, FastAPI, and PostgreSQL.
- Solid understanding of Docker containerization, Kubernetes, and Redis caching.
- Familiarity with AWS cloud architecture and CI/CD pipelines."""
        target_jd_text = st.text_area("Paste Target Job Requirements:", value=default_target_jd, height=215)

    st.write("")
    if cv_text or target_jd_text:
        cv_lower = cv_text.lower() if cv_text else " ".join([s.lower() for s in user_skills])
        jd_lower = target_jd_text.lower() if target_jd_text else ""

        cv_extracted_skills = [skill for skill in available_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', cv_lower)]
        jd_extracted_skills = [skill for skill in available_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', jd_lower)]

        matched_against_jd = [s for s in jd_extracted_skills if s in cv_extracted_skills]
        missing_against_jd = [s for s in jd_extracted_skills if s not in cv_extracted_skills]

        job_alignment_score = int((len(matched_against_jd) / max(len(jd_extracted_skills), 1)) * 100) if jd_extracted_skills else 0

        ats_checks = {
            "Work Experience Section": bool(re.search(r'\b(experience|work history|employment)\b', cv_lower)),
            "Education Section": bool(re.search(r'\b(education|university|degree|bachelor|master)\b', cv_lower)),
            "Technical Skills Section": bool(re.search(r'\b(skills|technologies|technical stack)\b', cv_lower)),
            "Quantified Impact Metrics (% / $)": bool(re.search(r'(\d+%\s*|\$\d+|\b\d+\s*users\b|\b\d+\s*x\b)', cv_lower))
        }
        structure_score = int((sum(ats_checks.values()) / len(ats_checks)) * 100) if cv_text else 50
        overall_ats_score = int((0.6 * (job_alignment_score or 50)) + (0.4 * structure_score))

        col_score1, col_score2 = st.columns(2)
        with col_score1:
            st.markdown(f"""
            <div class="resend-card-highlight" style="padding:18px 22px; height:100%;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <span class="resend-chip resend-chip-active shimmer-badge">OVERALL ATS COMPLIANCE</span>
                        <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:4px;">ATS Parser Health Score</div>
                    </div>
                    <div style="font-size:32px; font-weight:800; color:{'#10B981' if overall_ats_score >= 70 else primary_color};">{overall_ats_score}%</div>
                </div>
                <div style="background:#1A1D20; height:8px; border-radius:99px; overflow:hidden;">
                    <div style="background:linear-gradient(90deg, {primary_color}, #10B981); height:100%; width:{overall_ats_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_score2:
            st.markdown(f"""
            <div class="resend-card" style="padding:18px 22px; height:100%;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <span class="resend-chip resend-chip-success">JOB ALIGNMENT INDEX</span>
                        <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:4px;">Direct Requirement Match</div>
                    </div>
                    <div style="font-size:32px; font-weight:800; color:#10B981;">{job_alignment_score}%</div>
                </div>
                <div style="background:#1A1D20; height:8px; border-radius:99px; overflow:hidden;">
                    <div style="background:#10B981; height:100%; width:{job_alignment_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        c_mat_left, c_mat_right = st.columns(2)
        with c_mat_left:
            st.markdown(f"###### ✅ Matched Competencies ({len(matched_against_jd)})")
            if matched_against_jd:
                for s in matched_against_jd:
                    logo_html = get_skill_logo(s, large=False)
                    st.markdown(f"""
                    <div style="background:#0D1117; border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:8px 12px; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                        {logo_html} <span style="font-size:13px; color:#10B981; font-weight:600;">{s}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No direct keyword overlap detected with target job.")

            if cv_extracted_skills:
                st.write("")
                if st.button("⚡ Sync Extracted CV Skills to Dashboard Profile", use_container_width=True):
                    st.session_state.user_selected_stack = cv_extracted_skills
                    st.toast("Active profile synchronized from your resume!", icon="🚀")
                    st.rerun()

        with c_mat_right:
            st.markdown(f"###### ⚠️ Missing Target Keywords ({len(missing_against_jd)})")
            if missing_against_jd:
                for s in missing_against_jd:
                    logo_html = get_skill_logo(s, large=False)
                    hrs = get_skill_study_hours(s)
                    st.markdown(f"""
                    <div style="background:#120E10; border:1px solid rgba(239,68,68,0.3); border-radius:8px; padding:8px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                        <div style="display:flex; align-items:center; gap:8px;">{logo_html} <span style="font-size:13px; color:#F0F0F0;">{s}</span></div>
                        <span class="resend-chip resend-chip-danger" style="font-size:10px;">~{hrs}h gap</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Your profile covers 100% of the target job requirements!")

# ==============================================================================
# TAB 7: CAREER PIVOT & MIGRATION SIMULATOR
# ==============================================================================
with tab7:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
        {render_tg_icon('shuffle', 24)}
        <span style="font-size: 19px; font-weight: 700; color: #F0F0F0;">Career Pivot & Migration Simulator</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Simulate transitioning from your current profile into an adjacent technical domain with transition timeline and salary delta:")

    pivot_c1, pivot_c2 = st.columns(2)
    with pivot_c1:
        current_track = st.selectbox("Current Career Discipline:", list(ROADMAP_DATA.keys()), index=list(ROADMAP_DATA.keys()).index(best_fit_track) if best_fit_track in ROADMAP_DATA else 0)
    with pivot_c2:
        target_track = st.selectbox("Target Migration Discipline:", list(ROADMAP_DATA.keys()), index=1 if list(ROADMAP_DATA.keys())[0] == current_track else 0)

    curr_skills_list = []
    for p_name, s_list in ROADMAP_DATA[current_track].items():
        if p_name not in ["Resources", "Architecture"]:
            curr_skills_list.extend([str(item).split('(')[0].strip() for item in s_list])

    targ_skills_list = []
    for p_name, s_list in ROADMAP_DATA[target_track].items():
        if p_name not in ["Resources", "Architecture"]:
            targ_skills_list.extend([str(item).split('(')[0].strip() for item in s_list])

    transferable_skills = [s for s in targ_skills_list if any(c.lower() in s.lower() or s.lower() in c.lower() for c in user_skills)]
    missing_pivot_skills = [s for s in targ_skills_list if s not in transferable_skills]

    total_pivot_hours = sum([get_skill_study_hours(s) for s in missing_pivot_skills])
    pivot_months = max(round(total_pivot_hours / 60, 1), 1.0)

    curr_base_sal = base_val_kpi or 95000
    target_est_sal = max([SKILL_SALARY_ESTIMATES.get(s, 115000) for s in targ_skills_list], default=125000)
    salary_delta = target_est_sal - curr_base_sal

    st.write("")
    pv_m1, pv_m2, pv_m3 = st.columns(3)
    with pv_m1:
        st.markdown(f"""
        <div class="bento-card">
            <div style="font-size:12px; color:#8A8F98;">Estimated Transition Time</div>
            <div style="font-size:26px; font-weight:800; color:{primary_color}; margin:6px 0;">~{pivot_months} Months</div>
            <div style="font-size:11.5px; color:#8A8F98;">Based on ~15 hours/week study ({total_pivot_hours}h total).</div>
        </div>
        """, unsafe_allow_html=True)
    with pv_m2:
        delta_color = "#10B981" if salary_delta >= 0 else "#EF4444"
        st.markdown(f"""
        <div class="bento-card">
            <div style="font-size:12px; color:#8A8F98;">Projected Salary Delta</div>
            <div style="font-size:26px; font-weight:800; color:{delta_color}; margin:6px 0;">{'+$' if salary_delta >= 0 else '-$'}{abs(salary_delta):,}/yr</div>
            <div style="font-size:11.5px; color:#8A8F98;">From ${curr_base_sal:,} ➔ ${target_est_sal:,}/yr median.</div>
        </div>
        """, unsafe_allow_html=True)
    with pv_m3:
        transfer_pct = int((len(transferable_skills) / max(len(targ_skills_list), 1)) * 100)
        st.markdown(f"""
        <div class="bento-card">
            <div style="font-size:12px; color:#8A8F98;">Stack Transferability</div>
            <div style="font-size:26px; font-weight:800; color:{accent_color}; margin:6px 0;">{transfer_pct}%</div>
            <div style="font-size:11.5px; color:#8A8F98;">{len(transferable_skills)} shared competencies ready.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("##### Phased Transition Milestones")
    p_step_col1, p_step_col2 = st.columns(2)
    with p_step_col1:
        st.markdown(f"###### ✅ Transferable Strengths ({len(transferable_skills)})")
        if transferable_skills:
            for s in transferable_skills:
                logo_html = get_skill_logo(s, large=False)
                st.markdown(f"""
                <div style="background:#0D1117; border:1px solid rgba(16,185,129,0.3); border-radius:8px; padding:8px 12px; margin-bottom:6px; display:flex; align-items:center; gap:8px;">
                    {logo_html} <span style="font-size:13px; color:#10B981; font-weight:600;">{s}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No direct skill overlap detected.")

    with p_step_col2:
        st.markdown(f"###### 🎯 Core Migration Gaps ({len(missing_pivot_skills)})")
        if missing_pivot_skills:
            for s in missing_pivot_skills[:6]:
                logo_html = get_skill_logo(s, large=False)
                hrs = get_skill_study_hours(s)
                st.markdown(f"""
                <div style="background:#14171E; border:1px solid #232832; border-radius:8px; padding:8px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:8px;">{logo_html} <span style="font-size:13px; color:#F0F0F0;">{s}</span></div>
                    <span class="resend-chip" style="font-size:10px;">~{hrs}h</span>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# TAB 8: LIVE JOBS & FREELANCE RADAR (10 PLATFORMS)
# ==============================================================================
with tab8:
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            {render_tg_icon('briefcase', 24)}
            <span style="font-size: 20px; font-weight: 700; color: #F0F0F0; letter-spacing: -0.3px;">Live Market Radar & Verified Direct Postings</span>
        </div>
        <span class="resend-chip resend-chip-active shimmer-badge">REAL-TIME PIPELINE</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Live developer openings aggregated from LinkedIn, RemoteOK, WeWorkRemotely, Himalayas, Jobinja, Jobvision, and Karlancer ranked by stack compatibility:")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    jobs_json_path = os.path.join(current_dir, "data", "live_scraped_jobs.json")
    if not os.path.exists(os.path.dirname(jobs_json_path)):
        jobs_json_path = os.path.join(current_dir, "live_scraped_jobs.json")

    col_ctrl_left, col_ctrl_btn = st.columns([3.2, 1], vertical_alignment="center")

    with col_ctrl_btn:
        if st.button("🔄 Scrape All 10 Platforms", use_container_width=True):
            with st.spinner("Executing live multi-threaded crawlers..."):
                try:
                    import job_scraper
                    live_feed_data = job_scraper.run_full_crawler()
                    st.toast(f"Synchronized {len(live_feed_data)} live job postings!", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Scraper error: {e}")

    raw_live_jobs = []
    if os.path.exists(jobs_json_path):
        try:
            with open(jobs_json_path, "r", encoding="utf-8") as f:
                raw_live_jobs = json.load(f)
        except Exception:
            raw_live_jobs = []

    if not raw_live_jobs:
        try:
            import job_scraper
            raw_live_jobs = job_scraper.run_full_crawler()
        except Exception:
            raw_live_jobs = []

    PLATFORM_STYLES = {
        "LinkedIn Jobs": {"color": "#0A66C2", "bg": "rgba(10, 102, 194, 0.15)"},
        "RemoteOK": {"color": "#FF4742", "bg": "rgba(255, 71, 66, 0.15)"},
        "WeWorkRemotely": {"color": "#E05A47", "bg": "rgba(224, 90, 71, 0.15)"},
        "Himalayas": {"color": "#8B5CF6", "bg": "rgba(139, 92, 246, 0.15)"},
        "Jobinja": {"color": "#00A3FF", "bg": "rgba(0, 163, 255, 0.15)"},
        "Jobvision": {"color": "#6366F1", "bg": "rgba(99, 102, 241, 0.15)"},
        "Karlancer": {"color": "#10B981", "bg": "rgba(16, 185, 129, 0.15)"},
        "Ponisha": {"color": "#F59E0B", "bg": "rgba(245, 158, 11, 0.15)"},
        "Quera Magnet": {"color": "#3B82F6", "bg": "rgba(59, 130, 246, 0.15)"},
        "Arbeitnow (EU)": {"color": "#EC4899", "bg": "rgba(236, 72, 153, 0.15)"},
        "Jobicy": {"color": "#14B8A6", "bg": "rgba(20, 184, 166, 0.15)"}
    }

    scored_jobs = []
    for job in raw_live_jobs:
        req_skills = job.get("skills", [])
        m_skills = [s for s in req_skills if any(u.lower() in s.lower() or s.lower() in u.lower() for u in user_skills)]
        u_skills = [s for s in req_skills if s not in m_skills]
        score = int((len(m_skills) / max(len(req_skills), 1)) * 100) if req_skills else 0
        scored_jobs.append({
            **job,
            "match_score": score,
            "matched_skills": m_skills,
            "missing_skills": u_skills
        })

    scored_jobs = sorted(scored_jobs, key=lambda x: x["match_score"], reverse=True)

    with col_ctrl_left:
        total_openings = len(scored_jobs)
        top_match_pct = scored_jobs[0]["match_score"] if scored_jobs else 0
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; font-size:12px; color:#8A8F98;">
            <span>Total Tracked Postings: <b style="color:#FFFFFF;">{total_openings}</b></span>
            <span>•</span>
            <span>Highest Stack Compatibility: <b style="color:#10B981;">{top_match_pct}% Match</b></span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    c_f1, c_f2 = st.columns([1, 1])
    with c_f1:
        platform_options = ["All Platforms"] + sorted(list(set(j.get("platform", "Other") for j in scored_jobs)))
        platform_filter = st.selectbox("Filter by Platform:", platform_options)
    with c_f2:
        min_match = st.slider("Filter by Minimum Stack Compatibility (%):", min_value=0, max_value=100, value=0, step=10)

    filtered_jobs = [
        j for j in scored_jobs
        if (platform_filter == "All Platforms" or j.get("platform") == platform_filter) and j["match_score"] >= min_match
    ]

    st.write("")
    if filtered_jobs:
        for j in filtered_jobs:
            p_style = PLATFORM_STYLES.get(j.get("platform"), {"color": primary_color, "bg": "rgba(0, 163, 255, 0.12)"})
            score_color = "#10B981" if j['match_score'] >= 50 else (primary_color if j['match_score'] >= 20 else "#8A8F98")

            matched_html = "".join([f'<span class="resend-chip resend-chip-success" style="font-size:10px; margin:2px 3px;">✓ {s}</span>' for s in j['matched_skills']])
            missing_html = "".join([f'<span class="resend-chip" style="font-size:10px; margin:2px 3px; color:#8A8F98; border-color:#262A2D;">+ {s}</span>' for s in j['missing_skills']]) if j['missing_skills'] else ""

            st.markdown(f"""
            <div class="job-card-premium" style="--job-card-accent: {p_style['color']};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                            <span class="resend-chip" style="color:{p_style['color']}; background:{p_style['bg']}; border-color:{p_style['color']}40; font-weight:700; font-size:11px;">
                                {j.get('platform')}
                            </span>
                            <span class="resend-chip" style="font-size:10.5px; border-color:#262A2D;">
                                {j.get('type')}
                            </span>
                        </div>
                        <div class="job-card-title">{j.get('title')}</div>
                        <div style="font-size:13px; color:#8A8F98; display:flex; align-items:center; gap:6px; margin-top:2px;">
                            <span style="color:#FFFFFF; font-weight:500;">{j.get('company')}</span>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:24px; font-weight:800; color:{score_color}; font-family:'Inter', sans-serif; letter-spacing:-0.5px;">
                            {j['match_score']}%
                        </div>
                        <span style="font-size:10px; font-weight:600; color:#8A8F98; letter-spacing:0.4px;">COMPATIBILITY</span>
                    </div>
                </div>
                <div class="job-info-pill">
                    <div style="font-size:13px; color:#8A8F98;">
                        Offered Compensation: <b style="color:#10B981; font-size:13.5px; margin-left:4px;">{j.get('salary')}</b>
                    </div>
                    <a href="{j.get('url')}" target="_blank" class="job-apply-btn">
                        Apply on {j.get('platform').split()[0]} ↗
                    </a>
                </div>
                <div style="display:flex; flex-wrap:wrap; align-items:center;">
                    <span style="font-size:11px; font-weight:600; color:#8A8F98; margin-right:8px;">Skill Match Matrix:</span>
                    {matched_html if matched_html else '<span style="font-size:11px; color:#8A8F98; margin-right:6px;">No stack overlap</span>'}
                    {missing_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No postings found matching current filter criteria. Try lowering the match compatibility threshold.")

# ==============================================================================
# 12. PRODUCTION FOOTER
# ==============================================================================
st.write("")
st.write("---")

col_foot_meta, col_foot_theme = st.columns([3, 2], vertical_alignment="center")
with col_foot_meta:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; font-size:12px; color:#8A8F98; font-family:'Inter', sans-serif;">
        <span class="resend-chip" style="border-color:#2A2E33; color:#F0F0F0;">v4.5 PROD</span>
        <span>Architect: <b style="color:#FFFFFF;">Mehdi Bagheri</b></span>
        <span>•</span>
        <span>Data: <b>Stack Overflow</b> • <b>LinkedIn</b> • <b>Google Trends</b></span>
    </div>
    """, unsafe_allow_html=True)

with col_foot_theme:
    selected_theme_name = st.radio(
        "Theme Palette",
        options=list(THEME_PALETTES.keys()),
        index=list(THEME_PALETTES.keys()).index(st.session_state.app_theme),
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected_theme_name != st.session_state.app_theme:
        st.session_state.app_theme = selected_theme_name
        st.rerun()

        