from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load your personal text
with open("my_texts.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# 2. Split into chunks (simple split by paragraphs)
chunks = [c.strip() for c in raw_text.split("\n\n") if c.strip()]

if not chunks:
    raise ValueError("Your file 'my_texts.txt' is empty or has no paragraphs!")

# 3. Vectorize your chunks
vectorizer = TfidfVectorizer()
chunk_vectors = vectorizer.fit_transform(chunks)

def answer_like_me(question: str, top_k: int = 1):
    q_vec = vectorizer.transform([question])
    sims = cosine_similarity(q_vec, chunk_vectors)[0]
    # Get indices of most similar chunks
    idxs = sims.argsort()[::-1][:top_k]
    results = []
    for idx in idxs:
        results.append((sims[idx], chunks[idx]))
    return results

print("Personal AI twin ready. Type 'quit' to exit.\n")

while True:
    q = input("You ask: ")
    if q.lower().strip() in {"quit", "exit"}:
        break

    results = answer_like_me(q, top_k=3)
    print("\n--- Closest responses in your own style ---")
    for score, text in results:
        print(f"\n[similarity: {score:.3f}]\n{text}\n")
    print("-------------------------------------------\n")
