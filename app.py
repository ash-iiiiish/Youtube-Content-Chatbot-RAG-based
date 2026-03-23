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

# ── Styling ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] {
    background:#1e1e1e !important;
    color:#eaeaea !important;
    font-family: Inter, sans-serif;
}

.stApp {
    background:#1e1e1e;
}

.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.header h1 {
    font-size:22px;
}

.chat-window {
    display:flex;
    flex-direction:column;
    gap:14px;
    padding-bottom: 80px;
}

.chat-row {
    display:flex;
    width:100%;
    align-items: flex-end;
}

.user-row {
    justify-content:flex-end;
}

.bot-row {
    justify-content:flex-start;
}

.bubble {
    padding:10px 14px;
    border-radius:14px;
    max-width:65%;
    font-size:0.95rem;
    line-height:1.5;
    word-wrap:break-word;
}

.bubble-user {
    background:#00695c;
    border:1px solid #00897b;
    color:white;
}

.bubble-bot {
    background:#2a2a2a;
    border:1px solid #3a3a3a;
}

.avatar {
    width:30px;
    height:30px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:0.8rem;
    flex-shrink: 0;
    margin:0 8px;
}

.avatar-user {
    background:#00897b;
}

.avatar-bot {
    background:#3949ab;
}

/* ── FIXED: chat input now properly centered and full-width ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    bottom: 24px !important;
    width: min(730px, 90%) !important;
    max-width: 730px !important;
    z-index: 999 !important;
}

/* Fix the inner textarea border to look clean */
[data-testid="stChatInput"] > div {
    border: 1px solid #3a3a3a !important;
    border-radius: 12px !important;
    background: #2a2a2a !important;
}

[data-testid="stChatInput"] textarea {
    color: #eaeaea !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ── Sidebar ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📺 Video")
    video_id = st.text_input("YouTube Video ID")
    st.markdown("---")
    st.caption("Enter a video ID then ask questions about it.")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()


# ── Page Header ─────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
<h1 style="font-size:42px;">🎥 YouTube RAG Chatbot</h1>
<span>Ask questions about a YouTube video</span>
</div>
""", unsafe_allow_html=True)


# ── Chat Renderer ───────────────────────────────────────────────────────
# FIX: Do NOT escape bot messages — render them as plain text inside the bubble.
# Use html_lib.escape only for user input (untrusted), not for bot output.
def build_chat(messages):
    rows = []
    for msg in messages:
        # Escape user input to prevent XSS, preserve newlines
        safe = html_lib.escape(msg["content"]).replace("\n", "<br>")

        if msg["role"] == "user":
            rows.append(f"""
            <div class="chat-row user-row">
                <div class="bubble bubble-user">{safe}</div>
                <div class="avatar avatar-user">U</div>
            </div>
            """)
        else:
            # Bot content: already a plain string from LLM, safe to render as-is
            # Still escape to avoid any accidental HTML in LLM output
            rows.append(f"""
            <div class="chat-row bot-row">
                <div class="avatar avatar-bot">🤖</div>
                <div class="bubble bubble-bot">{safe}</div>
            </div>
            """)

    return '<div class="chat-window">' + "".join(rows) + "</div>"


# ── FIX: Use st.components.v1.html instead of st.markdown for chat window ──
import streamlit.components.v1 as components

def render_chat(messages):
    if not messages:
        return

    # Inject styles + chat HTML into an iframe-based component
    # This guarantees raw HTML renders correctly without Streamlit sanitizing it
    html_content = f"""
    <style>
        body {{ margin: 0; background: transparent; font-family: Inter, sans-serif; color: #eaeaea; }}
        .chat-window {{ display:flex; flex-direction:column; gap:14px; }}
        .chat-row {{ display:flex; width:100%; align-items:flex-end; }}
        .user-row {{ justify-content:flex-end; }}
        .bot-row {{ justify-content:flex-start; }}
        .bubble {{ padding:10px 14px; border-radius:14px; max-width:65%; font-size:0.95rem; line-height:1.5; word-wrap:break-word; }}
        .bubble-user {{ background:#00695c; border:1px solid #00897b; color:white; }}
        .bubble-bot {{ background:#2a2a2a; border:1px solid #3a3a3a; color:#eaeaea; }}
        .avatar {{ width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.8rem; flex-shrink:0; margin:0 8px; }}
        .avatar-user {{ background:#00897b; }}
        .avatar-bot {{ background:#3949ab; }}
    </style>
    {build_chat(messages)}
    """

    # Height scales with number of messages (rough estimate)
    estimated_height = max(200, len(messages) * 90)
    components.html(html_content, height=estimated_height, scrolling=True)


render_chat(st.session_state.messages)


# ── Chat Input ──────────────────────────────────────────────────────────
user_question = st.chat_input("Ask something about the video...")

if user_question:
    if not video_id:
        st.warning("Please enter a YouTube Video ID in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.spinner("Analyzing video and generating answer..."):
        answer = run_pipeline(video_id, user_question)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()