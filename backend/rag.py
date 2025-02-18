from openai import OpenAI
from pinecone.grpc import PineconeGRPC
import os

class RAGQuerySystem:
    def __init__(self):
        self.client = OpenAI()
        self.pc = PineconeGRPC(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index("text-sections")
        
    def get_query_embedding(self, query):
        """Get embedding for the query text"""
        return self.client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"
        ).data[0].embedding
    
    def query_pinecone(self, query, top_k=5):
        """Query Pinecone for relevant sections"""
        query_embedding = self.get_query_embedding(query)
        
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            return results.matches
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return []
    
    def format_context(self, matches): # added to retrieval.py
        """Format the retrieved contexts into a single string"""
        contexts = []
        for i, match in enumerate(matches, 1):
            text = match.metadata.get('text', '')
            score = match.score
            contexts.append(f"Context {i} (Relevance: {score:.2f}):\n{text}\n")
        return "\n".join(contexts)
    
    def generate_response(self, query, context): # not needed I think
        """Generate a response using ChatGPT with the retrieved context"""
        try:
            system_prompt = """You are a helpful assistant that answers questions based on the provided context. 
            Always base your answers on the given context and acknowledge if the context doesn't contain enough 
            information to fully answer the question. If you use information from the context, try to indicate
            which context number you're referring to."""
            print(context)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"""Context:\n{context}\n\nQuestion: {query}
                    
                    Please answer the question based on the provided context. If the context doesn't
                    contain enough information, please say so."""}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error generating the response."
    
    def query_and_respond(self, query, top_k=5): # added in retrieval.py
        """Main function to process a query and generate a response"""
        print(f"🔍 Searching for relevant context...")
        matches = self.query_pinecone(query, top_k=top_k)
        
        if not matches:
            return "Sorry, I couldn't find any relevant information in the database."
        
        print(f"✅ Found {len(matches)} relevant sections")
        context = self.format_context(matches)
        
        print("🤔 Generating response...")
        response = self.generate_response(query, context)
        
        return response

def main():
    # Initialize the RAG system
    rag = RAGQuerySystem()
    
    print("📚 RAG System initialized! Type 'exit' to quit.")
    
    while True:
        query = input("\n❓ Enter your question: ").strip()
        
        if query.lower() == 'exit':
            print("👋 Goodbye!")
            break
            
        if not query:
            continue
            
        try:
            response = rag.query_and_respond(query)
            print("\n🤖 Answer:")
            print(response)
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")

if __name__ == "__main__":
    main()