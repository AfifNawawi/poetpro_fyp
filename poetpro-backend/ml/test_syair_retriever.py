from syair_retriever import SyairRetriever

def main():
    retriever = SyairRetriever()

    query = """
jika anakanda jadi menteri,
orang berilmu anakanda hampiri,
lawan mesyuarat lawan berperi,
supaya pekerjaan jadi ugahari.
"""

    results = retriever.search(query, top_k=3)

    print("\n🔍 Query:")
    print(query)

    print("\n📚 Top 3 Similar Syair:\n")
    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(r)
        print()

if __name__ == "__main__":
    main()
