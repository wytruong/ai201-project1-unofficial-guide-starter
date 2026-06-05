import os
from dotenv import load_dotenv
from groq import Groq
from embed import embed_and_store, retrieve

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question, collection, model):
    chunks = retrieve(question, collection, model, k=5)
    
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"
    
    prompt = f"""You are a helpful assistant for UCI students looking for 
unofficial advice about internships, professors, and career recruiting.

Answer the question using ONLY the information in the provided documents below.
If the documents do not contain enough information to answer the question, 
say exactly: "I don't have enough information in my documents to answer that."
Always end your response by listing which sources you used.

Documents:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    answer = response.choices[0].message.content
    sources = list(set([c["source"] for c in chunks]))
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    print("Loading vector store...")
    collection, model = embed_and_store()
    
    test_questions = [
        "Which companies hire UCI data science students?",
        "What is the best time to start applying for internships?",
        "What do students say about the UCI housing lottery?"
    ]
    
    for q in test_questions:
        print(f"\nQuestion: {q}")
        result = ask(q, collection, model)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("=" * 60)