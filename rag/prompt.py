from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""You are a helpful assistant.
Answer ONLY from the following context.
If the context is insufficient, say: I don't know.

Context:
{context}

Question:
{question}
""",
    input_variables=["context", "question"]
)
