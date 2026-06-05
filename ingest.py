import os

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"source": filename, "text": text})
    print(f"Loaded {len(docs)} documents")
    return docs

def clean_text(text):
    lines = text.splitlines()
    cleaned = []
    skip_phrases = [
        "promoted", "sign up", "shopify", "microsoft_azure", 
        "clickable image", "collapse video", "0:00", "upvote", 
        "downvote", "award", "thumbs up", "thumbs down", "helpful\n",
        "go to comments", "sort by", "community info", "moderators",
        "privacy policy", "user agreement", "reddit rules",
        "reddit, inc"
    ]
    for line in lines:
        lower = line.lower().strip()
        if not lower:
            continue
        if any(phrase in lower for phrase in skip_phrases):
            continue
        cleaned.append(line.strip())
    return " ".join(cleaned)

def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_documents():
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            if len(chunk) > 0:
                all_chunks.append({
                    "source": doc["source"],
                    "chunk_index": i,
                    "text": chunk
                })
    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = process_documents()
    print("\n--- 5 sample chunks ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Text: {chunk['text']}")
        print("-" * 40)