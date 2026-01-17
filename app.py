import streamlit as st
from rag.pipeline import answer_question

st.set_page_config(page_title="YouTube RAG", page_icon="🎥")

st.title("🎥 YouTube Video Q&A (RAG)")

video_id = st.text_input("YouTube Video ID", value="hmtuvNfytjM")
question = st.text_input("Ask a question")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        answer = answer_question(video_id, question)

    st.subheader("Answer")
    st.success(answer)
