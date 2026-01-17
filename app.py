import streamlit as st
from rag.pipeline import run_pipeline

st.set_page_config(layout="wide")

# Top Heading
st.title("🎥 YouTube RAG Chatbot")

# Bottom Layout (Left smaller, Right bigger)
left_col, right_col = st.columns([1, 2])  # <-- 1:2 ratio

# LEFT COLUMN (Nav / Video Info)
with left_col:
    st.header("📌 Video Info")

    video_id = st.text_input("Enter YouTube Video ID")

    if video_id:
        st.markdown(f"**Video ID:** `{video_id}`")

# RIGHT COLUMN (Main: Question + Answer)
with right_col:
    st.header("💬 Ask & Answer")

    question = st.text_input("Ask a question")
    start = st.button("Start")

    if start:
        if not video_id or not question:
            st.warning("Please enter both Video ID and Question")
        else:
            progress_bar = st.progress(0)
            step_container = st.empty()

            def render_step(step, percent):
                step_container.markdown(f"🟡 **{step}** ({percent}%)")
                progress_bar.progress(percent)

            with st.spinner("Processing..."):
                answer = run_pipeline(
                    video_id,
                    question,
                    ui_callback=render_step
                )

            step_container.markdown("✅ **All steps completed**")
            progress_bar.progress(100)

            st.success("Answer")
            st.write(answer)
