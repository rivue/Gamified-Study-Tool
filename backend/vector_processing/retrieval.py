from openai import OpenAI
from pinecone.grpc import PineconeGRPC
import os

# Initialize global clients
client = OpenAI()
if os.getenv('FLASK_ENV') != "migration":
    pc = PineconeGRPC()
    if os.getenv("FLASK_ENV") == "production":
        index_name = "beta-testing"
    else:
        index_name = "text-sections"

    index = pc.Index(index_name)
else:
    pc = None
    index = None

def get_query_embedding(query):
    """Get embedding for the query text"""
    return client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding
    
def query_pinecone(query, library_id, top_k=5):
    """Query Pinecone for relevant sections"""
    query_embedding = get_query_embedding(query)
    print(query_embedding)
    library_id = int(library_id) if isinstance(library_id, str) else library_id
    try:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={
                "library_id": {"$eq": library_id}
            }
        )
        print(f"Query results: {results}")
        return results.matches
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []

def format_context(matches):
    """Format the retrieved contexts into a single string"""
    contexts = []
    for i, match in enumerate(matches, 1):
        text = match.metadata.get('text', '')
        score = match.score
        contexts.append(f"Context {i} (Relevance: {score:.2f}):\n{text}\n")
    return "\n".join(contexts)

def query_and_respond_pinecone(query, library_id, top_k=5):
    """Main function to process a query and generate a response"""
    print(f"🔍 Searching for relevant context...")
    matches = query_pinecone(query, library_id, top_k=top_k)

    if not matches:
        return ""
    
    print(f"✅ Found {len(matches)} relevant sections")
    context = format_context(matches)
    
    return context