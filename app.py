"""
NovaTech Role Mentor AI — Premium Streamlit Frontend
------------------------------------------------------
A chat-based mentor UI for the CAT-II Problem-Driven Industry AI Engineer
Program. Wraps the NovaTech Role Mentor AI system prompt around the
Google Gemini API and presents it in a polished, "premium" interface.

Run with:
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None


# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = r"""
You are **NovaTech Role Mentor AI**, an industry-style project mentor designed for students participating in the **CAT-II Problem-Driven Industry AI Engineer Program**.

Your purpose is to help students understand **their assigned role**, **their responsibilities**, **their daily tasks**, **their deliverables**, and **how their work fits into the overall AI project**.

## Program Context

The program follows a **10-day implementation roadmap** and progresses through these technical phases:

1. **Machine Learning (ML)**
2. **Deep Learning (DL)**
3. **Natural Language Processing (NLP)**
4. **Small Language Model (SLM)**
5. **Generative AI (GenAI)**
6. **Agentic AI**

Students work on a **client problem statement**, and **roles rotate between phases** so that every student experiences multiple responsibilities.

## Current Example Project

**Project Title:** AI-Powered Prediction of Energy Consumption in Smart Factories

### Project Goal
* Collects and processes industrial sensor data
* Predicts energy consumption
* Uses ML for baseline forecasting
* Enhances accuracy using DL models
* Extracts insights from unstructured documents using NLP
* Provides real-time summaries through SLMs
* Generates synthetic scenarios using GenAI
* Evolves into an autonomous Agentic AI system that can monitor, reason, and trigger workflows automatically

## Team Structure

Each phase uses **5 rotating roles**.

### Standard Roles
* Data Engineer
* EDA Engineer
* <Phase> Engineer (ML Engineer, DL Engineer, NLP Engineer, etc.)
* Evaluation Engineer
* Application Developer

### Agentic AI Roles
* Data/Knowledge Engineer
* Workflow Engineer
* Agent Engineer
* Evaluation Engineer
* Application Developer

### GenAI Roles
* Data Engineer
* EDA/Prompt Engineer
* GenAI Engineer
* Evaluation Engineer
* Application Developer

## Your Responsibilities

When a student asks a question, you must:

### 1. Identify
* Project
* Phase
* Role
* Optional day/checkpoint

### 2. Provide Practical Guidance
Always include: Objective, Inputs Required, Step-by-Step Tasks, Recommended Tools, Expected Deliverables, Coordination, Submission Checklist.

## Important Behavior Rules

### DO
* Act like a technical project mentor.
* Give implementation-focused guidance.
* Use industry terminology.
* Explain what to build, what to submit, and what to verify.
* Reference the current project context when giving examples.
* Keep answers structured and actionable.

### DO NOT
* Give generic textbook definitions unless explicitly requested.
* Explain unrelated AI concepts.
* Provide motivational speeches.
* Assume the student knows the project architecture.
* Give vague answers such as "learn TensorFlow" or "study NLP".

## Response Format

Use this exact structure whenever possible:

### <Phase> Phase — <Role Name>

#### Project Context
Briefly connect the role to the current project.

#### Your Objective
1–2 sentences.

#### What You Should Do
##### 1. <Task Group>
* Task
* Task
* Task

##### 2. <Task Group>
* Task
* Task

#### Recommended Tools
* Tool
* Tool
* Tool

#### Expected Deliverables
* `file1.ipynb`
* `report.pdf`
* `metrics.csv`

#### Coordinate With
* **Role A** — purpose
* **Role B** — purpose

#### Submission Checklist
* [ ] Item
* [ ] Item
* [ ] Item

#### Common Mistakes to Avoid
* Mistake
* Mistake

## Phase-Specific Guidance

### ML
 structured data, feature engineering, regression/classification, baseline predictive models, MAE/RMSE/R² evaluation.

### DL
LSTM/Transformer architectures, time-series forecasting, training pipelines, loss curves and checkpoints.

### NLP
Text preprocessing, tokenization, embeddings, classification, summarization, or document analysis.

### SLM
Lightweight transformer models, fine-tuning, quantization/optimization, real-time inference.

### GenAI
Prompt engineering, synthetic data generation, scenario simulation, report and insight generation.

### Agentic AI
Workflow orchestration, tool/API integration, reasoning pipelines, autonomous decision-making, monitoring and recovery logic.

## Tone
Professional, mentor-like, engineering-oriented: clear, precise, structured, practical, supportive but not overly casual. Avoid emojis unless explicitly requested by the user.

## Final Instruction
For every response, assume the student is asking: "What exactly should I do next for my assigned role in this project?"
Your answer must always provide specific next actions, expected outputs, and verification steps so the student can immediately continue working without needing additional clarification.
""".strip()


PHASES = {
    "ML": ["Data Engineer", "EDA Engineer", "ML Engineer", "Evaluation Engineer", "Application Developer"],
    "DL": ["Data Engineer", "EDA Engineer", "DL Engineer", "Evaluation Engineer", "Application Developer"],
    "NLP": ["Data Engineer", "EDA Engineer", "NLP Engineer", "Evaluation Engineer", "Application Developer"],
    "SLM": ["Data Engineer", "EDA Engineer", "SLM Engineer", "Evaluation Engineer", "Application Developer"],
    "GenAI": ["Data Engineer", "EDA/Prompt Engineer", "GenAI Engineer", "Evaluation Engineer", "Application Developer"],
    "Agentic AI": ["Data/Knowledge Engineer", "Workflow Engineer", "Agent Engineer", "Evaluation Engineer", "Application Developer"],
}


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NovaTech Role Mentor AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM CSS THEME
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --nv-bg-0: #05060a;
    --nv-bg-1: #0b0e17;
    --nv-bg-2: #10141f;
    --nv-accent: #6ee7ff;
    --nv-accent-2: #a78bfa;
    --nv-accent-3: #34d399;
    --nv-text: #e7ecf5;
    --nv-text-dim: #8a93a6;
    --nv-border: rgba(255,255,255,0.08);
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(110,231,255,0.10) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(167,139,250,0.10) 0%, transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(52,211,153,0.06) 0%, transparent 50%),
        var(--nv-bg-0);
    color: var(--nv-text);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--nv-bg-1) 0%, var(--nv-bg-0) 100%);
    border-right: 1px solid var(--nv-border);
}

/* Header */
.nv-hero {
    padding: 1.6rem 1.8rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(110,231,255,0.08), rgba(167,139,250,0.08));
    border: 1px solid var(--nv-border);
    margin-bottom: 1.4rem;
    backdrop-filter: blur(10px);
}
.nv-hero-eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.72rem;
    color: var(--nv-accent);
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.nv-hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, var(--nv-accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.nv-hero-sub {
    color: var(--nv-text-dim);
    font-size: 0.92rem;
    line-height: 1.5;
}

/* Glass cards */
.nv-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--nv-border);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.9rem;
}
.nv-card-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--nv-text-dim);
    margin-bottom: 0.35rem;
}
.nv-badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    background: linear-gradient(90deg, rgba(110,231,255,0.18), rgba(167,139,250,0.18));
    border: 1px solid rgba(110,231,255,0.3);
    color: var(--nv-accent);
    margin-right: 0.4rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--nv-border);
    border-radius: 16px;
    padding: 0.4rem 0.2rem;
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(90deg, var(--nv-accent), var(--nv-accent-2));
    color: #05060a;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(110,231,255,0.25);
}

/* Inputs */
.stTextInput>div>div>input, .stTextArea textarea, .stSelectbox>div>div {
    background: var(--nv-bg-2) !important;
    color: var(--nv-text) !important;
    border-radius: 10px !important;
    border: 1px solid var(--nv-border) !important;
}

/* Divider */
hr { border-color: var(--nv-border) !important; }

/* Footer note */
.nv-footer {
    color: var(--nv-text-dim);
    font-size: 0.78rem;
    text-align: center;
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# API KEY — pulled from Streamlit secrets, never shown to students
# ============================================================
# Locally: create a file at .streamlit/secrets.toml (never commit this) with:
#   GEMINI_API_KEY = "AIza..."
# On Streamlit Community Cloud: paste the same line into
#   App settings -> Secrets, in the dashboard (not in the repo).
API_KEY = st.secrets.get("GEMINI_API_KEY", None)


# ============================================================
# SESSION STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "phase" not in st.session_state:
    st.session_state.phase = "ML"
if "role" not in st.session_state:
    st.session_state.role = PHASES["ML"][0]


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🛰️ NovaTech Console")
    st.caption("CAT-II Problem-Driven Industry AI Engineer Program")

    st.divider()

    if API_KEY:
        st.success("Mentor AI is ready to use.")
    else:
        st.error(
            "Mentor AI isn't configured yet. The instructor needs to add "
            "GEMINI_API_KEY in Streamlit secrets."
        )

    st.divider()

    st.markdown("**Your Assignment**")
    phase = st.selectbox("Phase", list(PHASES.keys()), key="phase")
    role = st.selectbox("Role", PHASES[phase], key="role")

    st.markdown(
        f'<span class="nv-badge">{phase}</span><span class="nv-badge">{role}</span>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("**Project**")
    st.caption("AI-Powered Prediction of Energy Consumption in Smart Factories")

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<p class="nv-footer">Powered by Gemini · Google AI API</p>',
        unsafe_allow_html=True,
    )


# ============================================================
# HERO HEADER
# ============================================================
st.markdown(f"""
<div class="nv-hero">
    <div class="nv-hero-eyebrow">Role Mentor AI</div>
    <div class="nv-hero-title">Your Project Mentor</div>
    <div class="nv-hero-sub">
        Currently assigned as <b>{role}</b> in the <b>{phase}</b> phase.
        Ask what to do next — get objectives, tasks, tools, deliverables, and a submission checklist.
    </div>
</div>
""", unsafe_allow_html=True)

quick_col1, quick_col2, quick_col3 = st.columns(3)
quick_prompts = [
    "What should I do today for my role?",
    "What are my deliverables and checklist?",
    "Who should I coordinate with, and why?",
]
quick_clicked = None
with quick_col1:
    if st.button(quick_prompts[0], use_container_width=True):
        quick_clicked = quick_prompts[0]
with quick_col2:
    if st.button(quick_prompts[1], use_container_width=True):
        quick_clicked = quick_prompts[1]
with quick_col3:
    if st.button(quick_prompts[2], use_container_width=True):
        quick_clicked = quick_prompts[2]


# ============================================================
# CHAT HISTORY
# ============================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ============================================================
# CHAT INPUT / API CALL
# ============================================================
def call_mentor(user_text: str) -> str:
    if genai is None:
        return (
            "⚠️ The `google-genai` package isn't installed. "
            "Run `pip install google-genai` and restart the app."
        )

    if not API_KEY:
        return (
            "⚠️ Mentor AI isn't configured yet. The instructor needs to "
            "add GEMINI_API_KEY in Streamlit secrets."
        )

    context_note = (
        f"\n\n[Session context: The student's current Phase is '{phase}' and "
        f"Role is '{role}'. Assume this unless the student states otherwise.]"
    )

    try:
        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT + context_note,
                max_output_tokens=2000,
            ),
        )

        return response.text if response.text else "(No response text returned.)"

    except Exception as e:
        return f"⚠️ API error: {e}"


user_input = st.chat_input("Ask your mentor what to do next...")
final_input = quick_clicked or user_input

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.markdown(final_input)

    with st.chat_message("assistant"):
        with st.spinner("Consulting the mentor..."):
            reply = call_mentor(final_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

if not st.session_state.messages:
    st.markdown(
        f'<p class="nv-footer">No messages yet · {datetime.now().strftime("%b %d, %Y")}</p>',
        unsafe_allow_html=True,
    )
