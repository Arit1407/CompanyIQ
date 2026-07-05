"""
Create Vector Database (ChromaDB)
CompanyIQ RAG Pipeline
"""

import shutil

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from rag.load_documents import load_documents
from rag.chunk_documents import chunk_documents

from config.config import (
    CHROMA_DB_PATH,
    EMBEDDING_MODEL
)


# ===================================================
# Step 1: Load + Chunk
# ===================================================

def prepare_data():

    print("\nLoading documents...")
    documents = load_documents()

    print(f"Total Documents: {len(documents)}")

    print("\nChunking documents...")
    chunks = chunk_documents(documents)

    print(f"Total Chunks: {len(chunks)}")

    return chunks


# ===================================================
# Step 2: Embedding Model
# ===================================================

def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


# ===================================================
# Step 3: Build Vector DB
# ===================================================

def build_vector_db(chunks, embeddings):

    # If DB exists → remove it (clean rebuild)
    if CHROMA_DB_PATH.exists():
        print("\nExisting vector DB found. Deleting...")
        shutil.rmtree(CHROMA_DB_PATH)

    print("\nCreating ChromaDB...")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH)
    )

    vectordb.persist()

    print("\n===================================")
    print("Vector DB Created Successfully")
    print("===================================")
    print(f"Location: {CHROMA_DB_PATH}")

    return vectordb


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    chunks = prepare_data()

    embeddings = get_embedding_model()

    vectordb = build_vector_db(chunks, embeddings)

    print("\nSample Retrieval Test:")

    query = "What is Microsoft's revenue growth strategy?"

    results = vectordb.similarity_search(query, k=3)

    for i, doc in enumerate(results):

        print(f"\nResult {i+1}")
        print("Company:", doc.metadata.get("company"))
        print(doc.page_content[:300])