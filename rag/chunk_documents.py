"""
Chunk Documents for RAG Pipeline
CompanyIQ
"""

import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    REPORT_CHUNKS_PATH
)
from rag.load_documents import load_documents


# ===================================================
# Chunk Documents
# ===================================================

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    print("\n===================================")
    print("Chunking Completed")
    print("===================================")
    print(f"Total Chunks : {len(chunks)}")

    return chunks


# ===================================================
# Save Chunks (Optional)
# ===================================================

def save_chunks(chunks):

    REPORT_CHUNKS_PATH.mkdir(parents=True, exist_ok=True)

    output_file = REPORT_CHUNKS_PATH / "chunks.json"

    chunk_data = []

    for chunk in chunks:

        chunk_data.append({

            "text": chunk.page_content,
            "metadata": chunk.metadata

        })

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(
            chunk_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nChunks saved at:\n{output_file}")


# ===================================================
# Main
# ===================================================

if __name__ == "__main__":

    print("Loading documents...\n")

    documents = load_documents()

    print(f"\nTotal Documents Loaded : {len(documents)}")

    print("\n===================================")
    print("Document Statistics")
    print("===================================")

    for doc in documents:

        print(
            f"{doc.metadata['company']:<20}"
            f"{doc.metadata['file_name']:<20}"
            f"{len(doc.page_content):,} characters"
        )

    chunks = chunk_documents(documents)

    # ------------------------------------------------
    # Save only for debugging
    # ------------------------------------------------
    #save_chunks(chunks)

    print("\n===================================")
    print("Sample Chunk")
    print("===================================\n")

    print(chunks[0].page_content[:500])