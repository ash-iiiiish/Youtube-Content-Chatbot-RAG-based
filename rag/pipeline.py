from rag.loader import load_transcript
from rag.splitter import split_text
from rag.vectorstore import create_vectorstore, get_retriever
from rag.prompt import prompt
from rag.llm import call_llm

def answer_question(video_id: str, question: str) -> str:
    # Load data
    text = load_transcript(video_id)

    # Split
    chunks = split_text(text)

    # Vector store
    vector_store = create_vectorstore(chunks)
    retriever = get_retriever(vector_store)

    # Retrieve context
    docs = retriever.invoke(question)
    context = "\n".join([d.page_content for d in docs])

    # Prompt
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # LLM call
    return call_llm(final_prompt)
