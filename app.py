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

/* Header */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.header h1 {
    font-size:22px;
}

/* Chat container */
.chat-window {
    display:flex;
    flex-direction:column;
    gap:14px;
}

/* Chat row */
.chat-row {
    display:flex;
    width:100%;
}

.user-row {
    justify-content:flex-end;
}

.bot-row {
    justify-content:flex-start;
}

/* Bubbles */
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

/* Avatar */
.avatar {
    width:30px;
    height:30px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:0.8rem;
    margin:0 8px;
}

.avatar-user {
    background:#00897b;
}

.avatar-bot {
    background:#3949ab;
}

/* Chat input center */
[data-testid="stChatInput"] {
    position: fixed !important;
    left: calc(50% + 150px) !important;
    transform: translateX(-50%) !important;
    bottom: 24px !important;
    width: min(900px, 90%) !important;
    max-width: 900px !important;
    z-index: 999 !important;
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
def build_chat(messages):

    rows = []

    for msg in messages:

        safe = html_lib.escape(msg["content"]).replace("\n", "<br>")

        if msg["role"] == "user":
            rows.append(f"""
            <div class="chat-row user-row">
                <div class="bubble bubble-user">{safe}</div>
                <div class="avatar avatar-user">U</div>
            </div>
            """)

        else:
            rows.append(f"""
            <div class="chat-row bot-row">
                <div class="avatar avatar-bot">🤖</div>
                <div class="bubble bubble-bot">{safe}</div>
            </div>
            """)

    return '<div class="chat-window">' + "".join(rows) + "</div>"


chat_container = st.empty()

if st.session_state.messages:
    chat_container.markdown(
        build_chat(st.session_state.messages),
        unsafe_allow_html=True
    )


# ── Chat Input ──────────────────────────────────────────────────────────
user_question = st.chat_input("Ask something about the video...")

if user_question:

    if not video_id:
        st.warning("Please enter a YouTube Video ID in the sidebar first.")
        st.stop()

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    chat_container.markdown(
        build_chat(st.session_state.messages),
        unsafe_allow_html=True
    )

    # Run pipeline
    with st.spinner("Analyzing video and generating answer..."):

        answer = run_pipeline(
            video_id,
            user_question
        )

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()