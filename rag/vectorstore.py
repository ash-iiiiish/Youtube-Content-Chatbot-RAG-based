from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embedding_model

def create_vectorstore(chunks):
    embedding = get_embedding_model()
    vector_store = FAISS.from_texts(chunks, embedding)
    return vector_store

def get_retriever(vector_store):
    return vector_store.as_retriever(search_kwargs={"k": 4})
