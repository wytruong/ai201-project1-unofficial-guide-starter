import chromadb
from sentence_transformers import SentenceTransformer
from ingest import process_documents

def embed_and_store():
    chunks = process_documents()
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        client.delete_collection("unofficial_guide")
    except:
        pass
    
    collection = client.create_collection("unofficial_guide")
    
    texts = [c["text"] for c in chunks]
    ids = [f"{c['source']}_{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    
    print("Embedding chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection, model

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    collection, model = embed_and_store()
    
    test_query = "Which companies hire UCI data science students?"
    print(f"\nTest query: {test_query}")
    results = retrieve(test_query, collection, model)
    for r in results:
        print(f"\nSource: {r['source']} | Distance: {r['distance']:.3f}")
        print(f"Text: {r['text'][:200]}")
        print("-" * 40)