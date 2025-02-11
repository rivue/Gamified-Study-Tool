# text-embedding-3-small model

from pinecone import Pinecone, ServerlessSpec, enums
import openai

# Initialize APIs
pc = Pinecone(api_key="pcsk_42u1w8_815CW2LEFJJaeVPwHuZXopj7s4eJiQVFrVHTyeba6NTWpcjvN6EvU6jYQKrjHoc")
# pinecone.init(api_key="pcsk_42u1w8_815CW2LEFJJaeVPwHuZXopj7s4eJiQVFrVHTyeba6NTWpcjvN6EvU6jYQKrjHoc", environment="us-west1-gcp")  
index_name = "quickstart"
# pc.create_index(
#     name=index_name,
#     dimension=1536,
#     metric="cosine",
#     spec = ServerlessSpec(
#         cloud="aws",
#         region='us-east-1')
    
# )

index = pc.Index("quickstart")
openai.api_key = "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"

# Store textbook sections in Pinecone
def store_textbook_sections(textbook_sections):
    for i, section in enumerate(textbook_sections):
        embedding = openai.Embedding.create(
            model="text-embedding-3-small",
            input=section
        )["data"][0]["embedding"]

        index.upsert([(str(i), embedding, {"text": section})])

# Retrieve relevant sections from Pinecone
def retrieve_relevant_sections(query):
    query_embedding = openai.Embedding.create(
        model="text-embedding-3-small",
        input=query
    )["data"][0]["embedding"]

    search_results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    retrieved_texts = [match["metadata"]["text"] for match in search_results["matches"]]
    
    return " ".join(retrieved_texts)  # Combine top results

# Generate multiple-choice questions using GPT
def generate_questions(query):
    context_text = retrieve_relevant_sections(query)
    print(context_text)
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Generate 20 multiple-choice questions based on the following textbook content."},
            {"role": "user", "content": context_text}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Example Usage
textbook_sections = [
    "Newton’s First Law states that an object in motion stays in motion unless acted upon by an external force.",
    "Newton’s Second Law explains that force equals mass times acceleration (F=ma).",
    "Newton’s Third Law states that for every action, there is an equal and opposite reaction."
]

# Store sections
store_textbook_sections(textbook_sections)

# Retrieve relevant sections and generate questions
question_set = generate_questions("Newton's Laws of Motion")
print(question_set)
