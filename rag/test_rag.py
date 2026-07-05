"""
Test CompanyIQ RAG Pipeline
"""

from rag.retriever import retrieve_documents


# ===================================================
# Test Questions
# ===================================================

TEST_QUERIES = [

    (
        "Microsoft",
        "What is Microsoft's cloud revenue growth?"
    ),

    (
        "Oracle",
        "What are Oracle's AI initiatives?"
    ),

    (
        "Adobe",
        "What is Adobe's business strategy?"
    ),

    (
        "Infosys",
        "What are Infosys strategic priorities?"
    ),

    (
        "SAP SE",
        "How did SAP perform financially?"
    )

]


# ===================================================
# Run Tests
# ===================================================

def run_tests():

    print("\n==========================================")
    print("CompanyIQ RAG Retrieval Test")
    print("==========================================\n")

    for company, question in TEST_QUERIES:

        print("=" * 80)
        print(f"Company : {company}")
        print(f"Question: {question}")
        print("=" * 80)

        docs = retrieve_documents(
            query=question,
            company=company
        )

        print(f"\nRetrieved {len(docs)} documents\n")

        for i, doc in enumerate(docs, start=1):

            print(f"Result {i}")

            print(
                f"Source : {doc.metadata.get('file_name')}"
            )

            print(
                f"Company: {doc.metadata.get('company')}"
            )

            print("\nContent Preview:\n")

            print(doc.page_content[:350])

            print("\n" + "-" * 80 + "\n")


# ===================================================
# MAIN
# ===================================================

if __name__ == "__main__":

    run_tests()