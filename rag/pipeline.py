from rag.loader import load_transcript
from rag.splitter import split_text
from rag.vectorstore import create_vectorstore
from rag.prompt import build_prompt
from rag.llm import call_llm

def run_pipeline(video_id: str, question: str, ui_callback=None):

    def update(step, percent):
        if ui_callback:
            ui_callback(step, percent)

    update("Transcribing video", 10)
    text = load_transcript(video_id)

    update("Splitting text", 30)
    chunks = split_text(text)

    update("Creating embeddings", 50)
    vectorstore = create_vectorstore(chunks)

    update("Retrieving context", 70)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    update("Generating answer", 90)
    final_prompt = build_prompt(context, question)
    answer = call_llm(final_prompt)

    update("Done", 100)
    return answer
