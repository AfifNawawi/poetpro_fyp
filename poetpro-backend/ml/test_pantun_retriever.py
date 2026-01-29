from pantun_retriever import PantunRetriever

retriever = PantunRetriever()

query = """
Bunga melati di tepi titi,
Harum mewangi disiram embun;
Budi pekerti jadi pekerti,
Bahasa santun tanda beradab.
"""

results = retriever.search(query, top_k=5)

print("\n🔎 Similar Pantun Found:\n")
for i, r in enumerate(results, 1):
    print(f"{i}. [{r['source']}]\n{r['pantun']}\n")
