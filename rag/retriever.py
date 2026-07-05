"""
Retriever for CompanyIQ RAG Pipeline
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config.config import (
    CHROMA_DB_PATH,
    EMBEDDING_MODEL,
    TOP_K_RESULTS
)

# ===================================================
# Load Embedding Model
# ===================================================

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# ===================================================
# Load Chroma Database
# ===================================================

vector_db = Chroma(
    persist_directory=str(CHROMA_DB_PATH),
    embedding_function=embedding_model
)

# ===================================================
# Retrieve Documents
# ===================================================

def retrieve_documents(
    query: str,
    company: str = None,
    k: int = TOP_K_RESULTS
):

    if company:

        results = vector_db.similarity_search(
            query=query,
            k=k,
            filter={"company": company}
        )

    else:

        results = vector_db.similarity_search(
            query=query,
            k=k
        )

    return results


# ===================================================
# Pretty Print Results
# ===================================================

def print_results(results):

    print("\n===================================")
    print("Retrieved Documents")
    print("===================================")

    for i, doc in enumerate(results, start=1):

        print(f"\nResult {i}")

        print(f"Company : {doc.metadata.get('company')}")

        print(f"Source  : {doc.metadata.get('file_name')}")

        print("\nContent\n")

        print(doc.page_content[:500])

        print("\n-----------------------------------")


# ===================================================
# Test
# ===================================================

if __name__ == "__main__":

    query = "What is Microsoft's cloud revenue growth?"

    results = retrieve_documents(
        query=query,
        company="Microsoft"
    )

    print_results(results)