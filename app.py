# -*- coding: utf-8 -*-
import streamlit as st
import uuid
import html as html_lib
from rag.pipeline import run_pipeline

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg:           #212121;
    --bg-sidebar:   #171717;
    --bg-input:     #2F2F2F;
    --border:       #3A3A3A;
    --border2:      #484848;
    --text:         #ECECEC;
    --text-soft:    #B4B4B4;
    --text-muted:   #787878;
    --accent:       #5B9BF8;
    --accent-p:     rgba(91,155,248,0.08);
    --green:        #3DDC97;
    --green-g:      rgba(61,220,151,0.3);
    --red:          #F87171;
    --red-p:        rgba(248,113,113,0.10);
    --bubble-user:        #005C4B;
    --bubble-bot:         #1E2D3D;
    --bubble-user-border: #007A63;
    --bubble-bot-border:  #2A3F55;
    --r-sm:   10px;
    --r-pill: 999px;
    --sidebar-width: 244px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
    font-size: 16px !important;
}
.stApp { background: var(--bg) !important; }
.main .block-container {
    max-width: 860px !important;
    width: 100% !important;
    padding-bottom: 120px !important;
}
header[data-testid="stHeader"] { background: transparent !important; }

/* Wipe default Streamlit chat chrome */
[data-testid="stChatMessage"],
[data-testid="stChatMessage"] > div { all: unset !important; display: block !important; }
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatar"] { display: none !important; }

/* ── Chat window ── */
.chat-window {
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
}
.chat-row {
    display: flex;
    width: 100%;
    align-items: flex-end;
    gap: 8px;
}
.user-row { justify-content: flex-end; }
.bot-row  { justify-content: flex-start; }

/* ── Avatars ── */
.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700;
}
.avatar-user { background: #005C4B; color: #fff; border: 1px solid #007A63; }
.avatar-bot  { background: #1C2D3E; color: #5B9BF8; border: 1px solid #2A3F55; font-size: 1rem; }

/* ── Bubbles ── */
.bubble {
    max-width: 68%;
    min-width: 80px;
    padding: 0.72rem 1rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    line-height: 1.68;
    word-break: normal;
    overflow-wrap: break-word;
    white-space: normal;
}
.bubble-user {
    background: var(--bubble-user);
    border: 1px solid var(--bubble-user-border);
    color: #E9F5F3;
    border-radius: 16px 16px 2px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    animation: pop-right 0.22s cubic-bezier(0.34,1.5,0.64,1) both;
}
.bubble-bot {
    background: var(--bubble-bot);
    border: 1px solid var(--bubble-bot-border);
    color: var(--text);
    border-radius: 16px 16px 16px 2px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    animation: pop-left 0.22s cubic-bezier(0.34,1.5,0.64,1) both;
}
.bubble-meta {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    color: rgba(255,255,255,0.30);
    margin-top: 4px;
}
.user-row .bubble-meta { text-align: right; }
.bot-row  .bubble-meta { text-align: left; }

@keyframes pop-right {
    from { opacity:0; transform: translateX(18px) scale(0.95); }
    to   { opacity:1; transform: translateX(0) scale(1); }
}
@keyframes pop-left {
    from { opacity:0; transform: translateX(-18px) scale(0.95); }
    to   { opacity:1; transform: translateX(0) scale(1); }
}

/* ── Typing indicator ── */
.typing-wrap { display: flex; align-items: flex-end; gap: 8px; padding: 0.3rem 0; }
.typing-bubble {
    background: var(--bubble-bot);
    border: 1px solid var(--bubble-bot-border);
    border-radius: 16px 16px 16px 2px;
    padding: 0.7rem 1rem;
    display: inline-flex; align-items: center; gap: 5px;
}
.typing-bubble span {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--text-muted);
    animation: bounce 1.3s ease-in-out infinite;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.2s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%,60%,100% { transform: translateY(0);    opacity: 0.35; }
    30%          { transform: translateY(-7px); opacity: 1; }
}

/* ── Page header ── */
.page-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.85rem 0; margin-bottom: 1.4rem;
    border-bottom: 1px solid var(--border);
}
.page-header .left { display: flex; align-items: center; gap: 10px; }
.page-header .bot-icon {
    width: 38px; height: 38px; border-radius: 9px;
    background: #2A2A2A; border: 1px solid var(--border2);
    display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
}
.page-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.15rem !important; font-weight: 700 !important;
    color: var(--text) !important; margin: 0 !important;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green); box-shadow: 0 0 8px var(--green-g);
    display: inline-block; animation: blink 2.5s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.model-pill {
    font-family: 'JetBrains Mono', monospace; font-size: 0.67rem;
    font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase;
    color: var(--accent); background: var(--accent-p);
    border: 1px solid rgba(91,155,248,0.25);
    padding: 3px 10px; border-radius: var(--r-pill);
}

/* ── Empty state ── */
.empty-state { text-align: center; padding: 5rem 1rem 3rem; }
.empty-state .icon { font-size: 3rem; margin-bottom: 1.2rem; display: block; opacity: 0.18; }
.empty-state .title { font-size: 1.5rem; font-weight: 700; color: var(--text); font-family: 'Syne', sans-serif; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
.empty-state .sub { font-size: 0.9rem; color: var(--text-muted); line-height: 1.65; max-width: 320px; margin: 0 auto; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 1.4rem; }
.chip { font-size: 0.82rem; color: var(--text-soft); background: #2A2A2A; border: 1px solid var(--border2); border-radius: 99px; padding: 6px 16px; }
.empty-state .hint { margin-top: 1.6rem; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; color: #4A4A4A; letter-spacing: 0.05em; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 1.6rem 1.2rem !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important; font-weight: 600 !important;
    letter-spacing: 0.14em !important; text-transform: uppercase !important;
    color: var(--text-muted) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.6rem !important; margin-bottom: 0.9rem !important;
}
[data-testid="stSidebar"] button {
    background: #1C1C1C !important; border: 1px solid var(--border2) !important;
    color: var(--text-muted) !important; border-radius: var(--r-sm) !important;
    font-size: 0.88rem !important; font-weight: 500 !important; transition: all 0.18s !important;
}
[data-testid="stSidebar"] button:hover {
    background: var(--red-p) !important;
    border-color: var(--red) !important;
    color: var(--red) !important;
}

/* ════════════════════════════════════════
   CHAT INPUT — properly centered with
   sidebar offset + button inside box
════════════════════════════════════════ */
[data-testid="stChatInput"] {
    position: fixed !important;
    /* offset by half the sidebar so it centers in the content area */
    left: calc(50% + var(--sidebar-width) / 2) !important;
    transform: translateX(-50%) !important;
    bottom: 20px !important;
    width: min(780px, calc(100vw - var(--sidebar-width) - 48px)) !important;
    z-index: 999 !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Single unified pill wrapping textarea + button */
[data-testid="stChatInput"] > div {
    display: flex !important;
    align-items: center !important;
    background: var(--bg-input) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 14px !important;
    padding: 0 6px 0 0 !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.55) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    overflow: hidden !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 4px 28px rgba(0,0,0,0.6), 0 0 0 2px rgba(91,155,248,0.20) !important;
}

/* Textarea — no individual border */
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0.9rem 1.1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.96rem !important;
    color: var(--text) !important;
    flex: 1 !important;
    resize: none !important;
    min-height: unset !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Send button — tucked inside on the right */
[data-testid="stChatInput"] button {
    background: var(--accent) !important;
    border: none !important;
    border-radius: 9px !important;
    color: #fff !important;
    font-weight: 700 !important;
    flex-shrink: 0 !important;
    margin: 6px !important;
    padding: 0.42rem 0.78rem !important;
    box-shadow: 0 2px 8px rgba(91,155,248,0.35) !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
[data-testid="stChatInput"] button:hover {
    background: #78B4FF !important;
    transform: scale(1.07) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3A3A3A; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ── Build chat HTML ───────────────────────────────────────────────────────
def build_chat_html(messages: list, typing: bool = False) -> str:
    rows = []
    for msg in messages:
        safe = html_lib.escape(msg["content"]).replace("\n", "<br>")
        if msg["role"] == "user":
            rows.append(f"""
            <div class="chat-row user-row">
                <div>
                    <div class="bubble bubble-user">{safe}</div>
                    <div class="bubble-meta">You</div>
                </div>
                <div class="avatar avatar-user">Y</div>
            </div>""")
        else:
            rows.append(f"""
            <div class="chat-row bot-row">
                <div class="avatar avatar-bot">🎥</div>
                <div>
                    <div class="bubble bubble-bot">{safe}</div>
                    <div class="bubble-meta">Assistant</div>
                </div>
            </div>""")

    if typing:
        rows.append("""
        <div class="typing-wrap">
            <div class="avatar avatar-bot">🎥</div>
            <div class="typing-bubble">
                <span></span><span></span><span></span>
            </div>
        </div>""")

    return f'<div class="chat-window">{"".join(rows)}</div>'


# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📺 Video")
    video_id = st.text_input("YouTube Video ID", placeholder="e.g. dQw4w9WgXcQ")
    st.markdown("---")
    st.caption("Paste a YouTube video ID, then ask anything about it.")

    if st.button("🗑  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()


# ── Page header ───────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="left">
        <div class="bot-icon">🎥</div>
        <h1>YouTube RAG Chatbot</h1>
    </div>
    <div style="display:flex;align-items:center;gap:8px;">
        <span class="status-dot"></span>
        <span class="model-pill">RAG · Groq</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Empty state ───────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <span class="icon">🎥</span>
        <div class="title">Ask anything about a video</div>
        <div class="sub">Paste a YouTube video ID in the sidebar, then start asking questions.</div>
        <div class="chips">
            <span class="chip">Summarize the video</span>
            <span class="chip">Who are the speakers?</span>
            <span class="chip">Key takeaways</span>
            <span class="chip">Main topics covered</span>
        </div>
        <div class="hint">↓ &nbsp; enter a video ID and type below</div>
    </div>
    """, unsafe_allow_html=True)


# ── Chat window ───────────────────────────────────────────────────────────
chat_slot = st.empty()

if st.session_state.messages:
    chat_slot.markdown(
        build_chat_html(st.session_state.messages, typing=False),
        unsafe_allow_html=True,
    )


# ── Chat input ────────────────────────────────────────────────────────────
user_question = st.chat_input("Ask something about the video...")

if user_question:
    if not video_id:
        st.warning("Please enter a YouTube Video ID in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_question})
    chat_slot.markdown(
        build_chat_html(st.session_state.messages, typing=True),
        unsafe_allow_html=True,
    )

    answer = run_pipeline(video_id, user_question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()