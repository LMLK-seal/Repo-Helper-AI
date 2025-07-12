# vector_db_simplified.py
import os
import chromadb
from chromadb.utils import embedding_functions
from config import GEMINI_API_KEY

# Setup Gemini embedding function
gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GEMINI_API_KEY)

# Setup ChromaDB client
client = chromadb.PersistentClient(path="./chroma")
collection = client.get_or_create_collection(
    name="repo_docs_collection",
    embedding_function=gemini_ef
)

def split_text_manually(text: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    """A simple text splitter that doesn't need external libraries."""
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def index_repository_docs():
    """Loads docs, splits them manually, and stores them in ChromaDB."""
    print("Starting to index repository documentation...")
    all_docs_content = []
    
    for filename in os.listdir('./docs'):
        if filename.endswith(".md"):
            filepath = os.path.join('./docs', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                all_docs_content.append(f.read())

    full_text = "\n\n---\n\n".join(all_docs_content)
    
    if not full_text:
        print("No documents found to index.")
        return

    # Use our new manual splitter
    docs_split = split_text_manually(full_text)
    
    print(f"Split documents into {len(docs_split)} chunks.")

    ids = [f"chunk_{i}" for i in range(len(docs_split))]

    # Add to the collection
    collection.add(
        ids=ids,
        documents=docs_split
    )
    print("Indexing complete!")

def query_vector_db(query_text: str, n_results: int = 3) -> str:
    """Queries the vector DB to find relevant context."""
    print(f"Querying vector DB for: '{query_text}'")
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        context = "\n---\n".join(results['documents'][0])
        return context
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return "Could not retrieve context from the knowledge base."

if __name__ == "__main__":
    index_repository_docs()