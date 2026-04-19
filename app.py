import streamlit as st
import json
import random
import time
import os
import re
from pathlib import Path

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --border:    #232736;
    --accent:    #7c6aff;
    --accent2:   #ff6ab0;
    --accent3:   #6affe0;
    --text:      #e8eaf0;
    --muted:     #7a7f96;
    --success:   #4ade80;
    --warning:   #facc15;
    --danger:    #f87171;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Typography ── */
h1,h2,h3 { font-family: 'Syne', sans-serif; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1233 0%, #0d0f14 60%, #0f1a1a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(124,106,255,.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 200px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(106,255,224,.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #f472b6, #6affe0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
}
.hero p { color: var(--muted); font-size: 1rem; margin: 0; }

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: border-color .2s;
}
.card:hover { border-color: var(--accent); }

/* ── Section label ── */
.section-label {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .15em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── Tab styling ── */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px;
    border: 1px solid var(--border);
    padding: 4px;
    gap: 4px;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: .85rem !important;
    padding: 8px 18px !important;
    border: none !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--accent) !important;
    color: white !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: .85rem;
    padding: 10px 24px;
    transition: opacity .15s, transform .1s;
    width: 100%;
}
.stButton > button:hover { opacity: .88; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0); }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1a1d27 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,106,255,.2) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #1a1d27;
    border: 1.5px dashed var(--border);
    border-radius: 14px;
    padding: 16px;
    transition: border-color .2s;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent); }

/* ── Progress ── */
.stProgress > div > div { background: var(--accent) !important; }

/* ── Metric ── */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
}

/* ── Flashcard ── */
.flashcard {
    perspective: 1000px;
    width: 100%;
    min-height: 220px;
    cursor: pointer;
    margin-bottom: 20px;
}
.flashcard-inner {
    position: relative;
    width: 100%;
    min-height: 220px;
    transition: transform .6s cubic-bezier(.4,0,.2,1);
    transform-style: preserve-3d;
}
.flashcard.flipped .flashcard-inner { transform: rotateY(180deg); }
.flashcard-front, .flashcard-back {
    position: absolute;
    width: 100%;
    min-height: 220px;
    backface-visibility: hidden;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px;
    text-align: center;
}
.flashcard-front {
    background: linear-gradient(135deg, #1a1233, #1c1a35);
    border: 1px solid var(--accent);
}
.flashcard-back {
    background: linear-gradient(135deg, #0f1f1a, #121f1a);
    border: 1px solid var(--accent3);
    transform: rotateY(180deg);
}
.flashcard-label {
    font-size: .65rem;
    letter-spacing: .15em;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 16px;
    opacity: .6;
}
.flashcard-text { font-size: 1.1rem; font-weight: 600; line-height: 1.5; }

/* ── Quiz answer options ── */
.quiz-option {
    background: #1a1d27;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all .2s;
    font-size: .9rem;
}
.quiz-option:hover { border-color: var(--accent); background: #1f2235; }
.quiz-option.correct { border-color: var(--success) !important; background: rgba(74,222,128,.1) !important; color: var(--success); }
.quiz-option.wrong { border-color: var(--danger) !important; background: rgba(248,113,113,.1) !important; color: var(--danger); }

/* ── Summary output ── */
.summary-box {
    background: #1a1d27;
    border-left: 3px solid var(--accent);
    border-radius: 0 14px 14px 0;
    padding: 24px;
    font-family: 'DM Mono', monospace;
    font-size: .88rem;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    background: rgba(124,106,255,.15);
    border: 1px solid rgba(124,106,255,.3);
    color: var(--accent);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    margin-right: 6px;
}
.badge.green { background: rgba(74,222,128,.1); border-color: rgba(74,222,128,.3); color: var(--success); }
.badge.pink  { background: rgba(244,114,182,.1); border-color: rgba(244,114,182,.3); color: var(--accent2); }

/* ── Sidebar nav items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: background .15s;
}
.nav-item:hover { background: rgba(124,106,255,.12); }
.nav-item.active { background: rgba(124,106,255,.2); border: 1px solid rgba(124,106,255,.3); }

/* ── Score ring ── */
.score-ring { display: flex; align-items: center; justify-content: center; gap: 24px; padding: 24px; }
.ring-container { text-align: center; }
.ring-number { font-size: 3rem; font-weight: 800; color: var(--accent3); }
.ring-label { font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .1em; }

/* Spinner override */
.stSpinner > div { border-color: var(--accent) transparent transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Lazy imports with friendly error ────────────────────────────────────────
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    import pdfplumber
    DEPS_OK = True
except ImportError as e:
    DEPS_OK = False
    MISSING = str(e)

# ── Session state defaults ───────────────────────────────────────────────────
defaults = {
    "api_key": "",
    "extracted_text": "",
    "summary": "",
    "flashcards": [],
    "quiz": [],
    "fc_index": 0,
    "fc_flipped": False,
    "quiz_answers": {},
    "quiz_submitted": False,
    "doc_name": "",
    "history": [],         # [(role, msg)]
    "chat_context": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_llm():
    key = st.session_state.api_key.strip()
    if not key:
        return None
    return ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
        google_api_key=key,
        temperature=0.4,
    )

def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        import io
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        return "\n".join(pages)
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

def chunk_text(text: str, max_chars=12000) -> str:
    """Return a representative chunk for prompting."""
    return text[:max_chars]

def run_chain(template: str, variables: dict) -> str:
    llm = get_llm()
    if llm is None:
        return "⚠️ Please enter your Google API key in the sidebar first."
    prompt = PromptTemplate(input_variables=list(variables.keys()), template=template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(variables)

def parse_json_block(text: str):
    """Extract JSON from LLM output robustly."""
    # strip markdown fences
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    # find first [ or {
    for char in ["[", "{"]:
        idx = text.find(char)
        if idx != -1:
            try:
                return json.loads(text[idx:])
            except Exception:
                pass
    return None

# ── Prompt templates ─────────────────────────────────────────────────────────
SUMMARY_TEMPLATE = """You are an expert tutor. Given the study material below, produce a clear, structured summary.
Format it with:
- A one-line TL;DR
- 3-5 Key Concepts (bold the term, then explain in 1-2 sentences)
- Important Takeaways as bullet points

Study Material:
{text}

Summary:"""

FLASHCARD_TEMPLATE = """You are a study coach. Create {num} high-quality flashcards from the material.
Return ONLY a JSON array, no other text, in this exact format:
[
  {{"front": "Question or term", "back": "Answer or definition"}},
  ...
]

Study Material:
{text}"""

QUIZ_TEMPLATE = """You are an exam question writer. Create {num} multiple-choice questions from the material.
Return ONLY a JSON array:
[
  {{
    "question": "...",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "A"
  }},
  ...
]

Study Material:
{text}"""

CHAT_TEMPLATE = """You are a helpful study buddy. Use the provided study material as context to answer the student's question.
Be concise, accurate, and encouraging.

Study Material Context:
{context}

Student Question: {question}

Answer:"""

# ────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">🔑 API Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key, 
        type="password",
        placeholder="AIza...",
        help="Get your free key at https://aistudio.google.com",
    )
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key

    if st.session_state.api_key:
        st.markdown('<span class="badge green">✓ Key Saved</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge">No Key</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">📄 Upload Material</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop PDF or TXT",
        type=["pdf", "txt"],
        help="Upload your notes, textbook chapters, or any study material.",
    )
    if uploaded:
        if uploaded.name != st.session_state.doc_name:
            with st.spinner("Extracting text…"):
                text = extract_text(uploaded)
            st.session_state.extracted_text = text
            st.session_state.doc_name = uploaded.name
            # reset outputs
            for k in ["summary","flashcards","quiz","quiz_answers","quiz_submitted","history","chat_context"]:
                st.session_state[k] = defaults[k]
            st.session_state.fc_index = 0
            st.session_state.fc_flipped = False
            st.success(f"✓ Loaded: {uploaded.name}")

    if st.session_state.extracted_text:
        chars = len(st.session_state.extracted_text)
        words = len(st.session_state.extracted_text.split())
        st.markdown(f"""
        <div class="card" style="margin-top:12px;padding:16px;">
            <div style="font-size:.7rem;color:var(--muted);margin-bottom:8px;">DOCUMENT INFO</div>
            <div style="font-size:.85rem;">📄 <b>{st.session_state.doc_name}</b></div>
            <div style="font-size:.75rem;color:var(--muted);margin-top:6px;">
                {words:,} words · {chars:,} chars
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">⚙️ Generation Settings</div>', unsafe_allow_html=True)
    num_flashcards = st.slider("Flashcards to generate", 4, 20, 8)
    num_quiz = st.slider("Quiz questions", 3, 15, 5)

    st.markdown("---")
    

# ────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ────────────────────────────────────────────────────────────────────────────
if not DEPS_OK:
    st.error(f"Missing dependency: {MISSING}\nRun: pip install -r requirements.txt")
    st.stop()

# Hero
st.markdown("""
<div class="hero">
    <h1>📚 AI Study Buddy</h1>
    <p>Upload your notes → get summaries, flashcards, quizzes, and an AI tutor — instantly.</p>
</div>
""", unsafe_allow_html=True)

# Guard: no content uploaded
if not st.session_state.extracted_text:
    st.markdown("""
    <div class="card" style="text-align:center;padding:48px;">
        <div style="font-size:3rem;margin-bottom:16px;">⬆️</div>
        <div style="font-size:1.1rem;font-weight:700;margin-bottom:8px;">No material loaded</div>
        <div style="color:var(--muted);font-size:.9rem;">Upload a PDF or TXT file in the sidebar to get started.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_sum, tab_flash, tab_quiz, tab_chat, tab_raw = st.tabs([
    "📝 Summary", "🃏 Flashcards", "🎯 Quiz", "💬 Chat Tutor", "🔍 Raw Text"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – SUMMARY
# ════════════════════════════════════════════════════════════════════════════
with tab_sum:
    st.markdown('<div class="section-label">Intelligent Summary</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        gen_summary = st.button("✨ Generate Summary", key="btn_summary")

    if gen_summary:
        if not st.session_state.api_key:
            st.warning("Enter your API key in the sidebar first.")
        else:
            with st.spinner("Reading and summarising…"):
                chunk = chunk_text(st.session_state.extracted_text)
                result = run_chain(SUMMARY_TEMPLATE, {"text": chunk})
                st.session_state.summary = result

    if st.session_state.summary:
        st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download Summary",
            st.session_state.summary,
            file_name=f"summary_{st.session_state.doc_name}.txt",
            mime="text/plain",
        )
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:36px;color:var(--muted);">
            Click <b>Generate Summary</b> to produce an AI-powered summary of your material.
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – FLASHCARDS
# ════════════════════════════════════════════════════════════════════════════
with tab_flash:
    st.markdown('<div class="section-label">Interactive Flashcards</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        gen_fc = st.button(f"✨ Generate {num_flashcards} Cards", key="btn_flash")

    if gen_fc:
        if not st.session_state.api_key:
            st.warning("Enter your API key in the sidebar first.")
        else:
            with st.spinner("Creating flashcards…"):
                chunk = chunk_text(st.session_state.extracted_text)
                result = run_chain(FLASHCARD_TEMPLATE, {"text": chunk, "num": num_flashcards})
                parsed = parse_json_block(result)
                if parsed and isinstance(parsed, list):
                    st.session_state.flashcards = parsed
                    st.session_state.fc_index = 0
                    st.session_state.fc_flipped = False
                else:
                    st.error("Couldn't parse flashcards. Try again.")

    cards = st.session_state.flashcards
    if cards:
        idx = st.session_state.fc_index
        card = cards[idx]
        total = len(cards)
        flipped = st.session_state.fc_flipped

        # Progress
        st.progress((idx + 1) / total)
        st.markdown(f"<div style='text-align:right;font-size:.8rem;color:var(--muted);margin-bottom:12px;'>{idx+1} / {total}</div>", unsafe_allow_html=True)

        # Flashcard (pure HTML – clicking handled via button below)
        flip_class = "flipped" if flipped else ""
        st.markdown(f"""
        <div class="flashcard {flip_class}" id="fc">
          <div class="flashcard-inner">
            <div class="flashcard-front">
              <div class="flashcard-label">Question</div>
              <div class="flashcard-text">{card['front']}</div>
            </div>
            <div class="flashcard-back">
              <div class="flashcard-label" style="color:var(--accent3);">Answer</div>
              <div class="flashcard-text">{card['back']}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Controls
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("⬅️ Prev", key="fc_prev"):
                st.session_state.fc_index = max(0, idx - 1)
                st.session_state.fc_flipped = False
                st.rerun()
        with c2:
            label = "👁️ Hide" if flipped else "👁️ Reveal"
            if st.button(label, key="fc_flip"):
                st.session_state.fc_flipped = not flipped
                st.rerun()
        with c3:
            if st.button("➡️ Next", key="fc_next"):
                st.session_state.fc_index = min(total - 1, idx + 1)
                st.session_state.fc_flipped = False
                st.rerun()
        with c4:
            if st.button("🔀 Shuffle", key="fc_shuffle"):
                random.shuffle(st.session_state.flashcards)
                st.session_state.fc_index = 0
                st.session_state.fc_flipped = False
                st.rerun()

        # All cards list
        with st.expander("📋 View all cards"):
            for i, c in enumerate(cards):
                st.markdown(f"""
                <div class="card" style="padding:16px;margin-bottom:10px;">
                    <div style="font-size:.7rem;color:var(--muted);margin-bottom:4px;">Card {i+1}</div>
                    <div style="font-weight:700;margin-bottom:6px;">{c['front']}</div>
                    <div style="color:var(--accent3);font-size:.9rem;">{c['back']}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:36px;color:var(--muted);">
            Click <b>Generate Cards</b> to create interactive flashcards from your material.
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 – QUIZ
# ════════════════════════════════════════════════════════════════════════════
with tab_quiz:
    st.markdown('<div class="section-label">Knowledge Quiz</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        gen_quiz = st.button(f"✨ Generate {num_quiz}-Q Quiz", key="btn_quiz")

    if gen_quiz:
        if not st.session_state.api_key:
            st.warning("Enter your API key in the sidebar first.")
        else:
            with st.spinner("Writing quiz questions…"):
                chunk = chunk_text(st.session_state.extracted_text)
                result = run_chain(QUIZ_TEMPLATE, {"text": chunk, "num": num_quiz})
                parsed = parse_json_block(result)
                if parsed and isinstance(parsed, list):
                    st.session_state.quiz = parsed
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                else:
                    st.error("Couldn't parse quiz. Try again.")

    quiz = st.session_state.quiz
    if quiz:
        answered = st.session_state.quiz_answers
        submitted = st.session_state.quiz_submitted

        for i, q in enumerate(quiz):
            st.markdown(f"""
            <div class="card">
                <div style="font-size:.7rem;color:var(--muted);margin-bottom:6px;">Question {i+1} of {len(quiz)}</div>
                <div style="font-weight:700;font-size:1rem;margin-bottom:16px;">{q['question']}</div>
            </div>""", unsafe_allow_html=True)

            correct = q.get("answer", "A").strip().upper()[0]

            for opt in q.get("options", []):
                opt_letter = opt.strip()[0].upper()
                chosen = answered.get(i) == opt_letter

                if submitted:
                    if opt_letter == correct:
                        css = "quiz-option correct"
                    elif chosen:
                        css = "quiz-option wrong"
                    else:
                        css = "quiz-option"
                    st.markdown(f'<div class="{css}">{opt}</div>', unsafe_allow_html=True)
                else:
                    if st.button(opt, key=f"q{i}_{opt_letter}"):
                        st.session_state.quiz_answers[i] = opt_letter
                        st.rerun()
                    if chosen:
                        st.markdown(f'<div style="margin-top:-12px;margin-bottom:4px;font-size:.75rem;color:var(--accent);">← Your answer</div>', unsafe_allow_html=True)

        # Submit / Score
        if not submitted:
            if len(answered) == len(quiz):
                if st.button("🎯 Submit Quiz", key="quiz_submit"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                st.info(f"Answer all {len(quiz)} questions to submit. ({len(answered)}/{len(quiz)} done)")
        else:
            score = sum(1 for i, q in enumerate(quiz) if answered.get(i) == q.get("answer","A").strip().upper()[0])
            pct = int(score / len(quiz) * 100)
            grade = "🏆 Excellent!" if pct >= 80 else "👍 Good effort!" if pct >= 60 else "📖 Keep studying!"

            st.markdown(f"""
            <div class="card score-ring">
                <div class="ring-container">
                    <div class="ring-number">{pct}%</div>
                    <div class="ring-label">{grade}</div>
                </div>
                <div>
                    <div style="font-size:1.1rem;font-weight:700;margin-bottom:8px;">{score} / {len(quiz)} correct</div>
                    <div style="color:var(--muted);font-size:.85rem;">
                        {'Great command of the material!' if pct>=80 else 'Review the highlighted answers above and try again!'}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            if st.button("🔄 Retake Quiz", key="quiz_retry"):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:36px;color:var(--muted);">
            Click <b>Generate Quiz</b> to create a scored multiple-choice quiz.
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 – CHAT TUTOR
# ════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown('<div class="section-label">AI Chat Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--muted);font-size:.85rem;margin-bottom:16px;">Ask anything about your uploaded material — your tutor has read it all.</div>', unsafe_allow_html=True)

    # Render history
    for role, msg in st.session_state.history:
        if role == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:12px;">
                <div style="background:var(--accent);color:white;border-radius:16px 16px 4px 16px;padding:12px 18px;max-width:75%;font-size:.9rem;">{msg}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:12px;">
                <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px 16px 16px 4px;padding:12px 18px;max-width:75%;font-size:.9rem;line-height:1.6;">{msg}</div>
            </div>""", unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_q = st.text_input("Your question", placeholder="e.g. What are the main causes of X?", label_visibility="collapsed")
        submitted_chat = st.form_submit_button("Send →")

    if submitted_chat and user_q.strip():
        if not st.session_state.api_key:
            st.warning("Enter your API key in the sidebar.")
        else:
            context = chunk_text(st.session_state.extracted_text, 8000)
            st.session_state.history.append(("user", user_q))
            with st.spinner("Thinking…"):
                answer = run_chain(CHAT_TEMPLATE, {"context": context, "question": user_q})
            st.session_state.history.append(("assistant", answer))
            st.rerun()

    if st.session_state.history:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.history = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 – RAW TEXT
# ════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.markdown('<div class="section-label">Extracted Text</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='color:var(--muted);font-size:.8rem;margin-bottom:12px;'>{len(st.session_state.extracted_text):,} characters extracted from <b>{st.session_state.doc_name}</b></div>", unsafe_allow_html=True)
    st.text_area("Raw content", st.session_state.extracted_text, height=500, label_visibility="collapsed")
    st.download_button(
        "⬇️ Download Raw Text",
        st.session_state.extracted_text,
        file_name=f"raw_{st.session_state.doc_name}.txt",
        mime="text/plain",
    )