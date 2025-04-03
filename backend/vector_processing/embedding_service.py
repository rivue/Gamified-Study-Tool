from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
import time
import concurrent.futures
import os
import random
from openapi import get_embedding
import httpx

def insert_sections_to_pinecone_parallel(sections, library_id, batch_size=100, num_workers=5, max_retries=3):
    """Parallelized embedding and upserting to Pinecone with error handling and retry logic.""" 
    # Validate that sections is a list of strings 
    if not isinstance(sections, list) or not all(isinstance(sec, str) for sec in sections): raise ValueError("Sections must be a list of strings.")
    
    """Parallelized embedding and upserting to Pinecone."""
    index = init_pinecone()
  
    def embed_and_insert(batch, batch_start_idx):
        """Process and insert a batch of sections with retries."""
        retries = 0
        while retries < max_retries:
            try:
                # Generate embeddings for each section; each call may raise an exception
                embeddings = [get_embedding(section) for section in batch]
                vectors = [{
                    'id': f"{int(time.time()*1000)}_{random.randint(1000, 9999)}",
                    'values': emb,
                    'metadata': {'text': sec, 'library_id': library_id}
                } for sec, emb in zip(batch, embeddings)]
                
                # Upsert vectors to Pinecone
                index.upsert(vectors=vectors)
                print(f"Inserted batch of {len(vectors)} sections.")
                break  # exit loop if successful
            except httpx.HTTPError as http_err:
                retries += 1
                print(f"HTTP error during upsert: {http_err}. Retrying {retries}/{max_retries}...")
                time.sleep(2 ** retries)
            except Exception as e:
                retries += 1
                print(f"Error during embedding/upsert: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(2 ** retries)
        else:
            print(f"Failed to upsert batch after {max_retries} retries.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        batches = [sections[i:i+batch_size] for i in range(0, len(sections), batch_size)]
        futures = {executor.submit(embed_and_insert, batch, i*batch_size): i for i, batch in enumerate(batches)}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing a batch: {e}")
        
def init_pinecone():
    """Initialize Pinecone client and ensure index exists"""
    try:
        pc = PineconeGRPC(api_key=os.getenv("PINECONE_API_KEY"))

        if os.getenv("FLASK_ENV") == "production":
            index_name = "beta-testing"
        else:
            index_name = "text-sections"
        
        try:
            # Try to get the existing index directly
            index = pc.Index(index_name)
            # index_host = pc.describe_index(index_name).host
            # index = pc.Index(host=index_host, grpc_config=GRPCClientConfig(secure=False))
            print(f"Connected to existing index: {index_name}")
            return index
            
        except Exception as e:
            print(f"Error connecting to existing index: {e}")
            print("Attempting to create new index...")
            
            try:
                # Create new index
                pc.create_index(
                    name=index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                print(f"Created new Pinecone index: {index_name}")
                
                # Wait for index to be ready
                while True:
                    try:
                        status = pc.describe_index(index_name).status['ready']
                        if status:
                            break
                        print("Waiting for index to be ready...")
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error checking index status: {e}")
                        time.sleep(1)
                
                return pc.Index(index_name)
                
            except Exception as create_error:
                if "ALREADY_EXISTS" in str(create_error):
                    print("Index already exists, connecting to existing index...")
                    return pc.Index(index_name)
                else:
                    raise create_error
    
    except Exception as e:
        print(f"Fatal error initializing Pinecone: {e}")
        raise