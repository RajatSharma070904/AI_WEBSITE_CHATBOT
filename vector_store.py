from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import VECTOR_DB_DIR

def get_vector_store(docs=None):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if docs:
        return Chroma.from_documents(
            docs,
            embeddings,
            persist_directory=VECTOR_DB_DIR
        )
    else:
        return Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings
        )
