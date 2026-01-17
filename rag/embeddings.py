from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
