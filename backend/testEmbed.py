# # text-embedding-3-small model
# import pdfminer.six
# from pinecone import Pinecone, ServerlessSpec, enums
# import openai

# # Initialize APIs
# pc = Pinecone(api_key="pcsk_42u1w8_815CW2LEFJJaeVPwHuZXopj7s4eJiQVFrVHTyeba6NTWpcjvN6EvU6jYQKrjHoc")
# # pinecone.init(api_key="pcsk_42u1w8_815CW2LEFJJaeVPwHuZXopj7s4eJiQVFrVHTyeba6NTWpcjvN6EvU6jYQKrjHoc", environment="us-west1-gcp")  
# index_name = "quickstart"
# # pc.create_index(
# #     name=index_name,
# #     dimension=1536,
# #     metric="cosine",
# #     spec = ServerlessSpec(
# #         cloud="aws",
# #         region='us-east-1')
    
# # )

# index = pc.Index("quickstart")
# openai.api_key = "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"

# # Store textbook sections in Pinecone
# def store_textbook_sections(textbook_sections):
#     for i, section in enumerate(textbook_sections):
#         embedding = openai.Embedding.create(
#             model="text-embedding-3-small",
#             input=section
#         )["data"][0]["embedding"]

#         index.upsert([(str(i), embedding, {"text": section})])

# # Retrieve relevant sections from Pinecone
# def retrieve_relevant_sections(query):
#     query_embedding = openai.Embedding.create(
#         model="text-embedding-3-small",
#         input=query
#     )["data"][0]["embedding"]

#     search_results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
#     retrieved_texts = [match["metadata"]["text"] for match in search_results["matches"]]
    
#     return " ".join(retrieved_texts)  # Combine top results

# # Generate multiple-choice questions using GPT
# def generate_questions(query):
#     context_text = retrieve_relevant_sections(query)
#     print(context_text)
#     response = openai.ChatCompletion.create(
#         model="gpt-4-turbo",
#         messages=[
#             {"role": "system", "content": "Generate 20 multiple-choice questions based on the following textbook content."},
#             {"role": "user", "content": context_text}
#         ]
#     )
    
#     return response["choices"][0]["message"]["content"]

# # Example Usage
# textbook_sections = [
#     "Newton’s First Law states that an object in motion stays in motion unless acted upon by an external force.",
#     "Newton’s Second Law explains that force equals mass times acceleration (F=ma).",
#     "Newton’s Third Law states that for every action, there is an equal and opposite reaction."
# ]

# # Store sections
# store_textbook_sections(textbook_sections)

# # Retrieve relevant sections and generate questions
# question_set = generate_questions("Newton's Laws of Motion")
# print(question_set)

#  def extract_text_from_pdf(file):
#             # doc = fitz.open(stream=file.read(), filetype="pdf")  # Load PDF
#             text = extract_text(file)
#             # text = "\n\n".join([page.get_text() for page in doc])  # Extract text
#             return text
#         print("file content: " + file_content)
#         text = extract_text_from_pdf(file_content)  # Extract text from PDF
#         print("I did something")
#         print("text: " + text)
#         return jsonify({"error": f"No error, we're in the process of breaking things for now😭😭😭"}), 400
import pdf2image
import io
from google.cloud import vision
import resource
import psutil
import time

# vvv CODESPACE STUFF vvv

CPU_LIMIT = 50

MAX_MEMORY = 1 * 1024 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS (MAX_MEMORY, MAX_MEMORY)

def limit_cpu():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > CPU_LIMIT:
            time.sleep(0.5)  # Pause execution briefly if CPU is over limit

# Run CPU limit in a separate thread
import threading
cpu_thread = threading.Thread(target=limit_cpu, daemon=True)
cpu_thread.start()

# ^^^ CODESPACE STUFF ^^^

client = vision.ImageAnnotatorClient()
pdf_path = "./Duolingothing.pdf"
# Convert PDF to images in batches of 10 pages
batch_size = 10  # Adjust if needed
pages = pdf2image.convert_from_path(pdf_path, dpi=150)

extracted_text = ""


for i in range(0, len(pages), batch_size):

    process = psutil.Process()
    mem_usage = process.memory_info().rss / (1024 * 1024)
    MAX_PROCESS_MEMORY = 500

    if mem_usage > MAX_PROCESS_MEMORY:
        print(f"Memory usage high: {mem_usage}MB - Sleeping to free memory")
        time.sleep(2)  # Pause and let memory clear
    
    batch = pages[i : i + batch_size]
    print(f"Processing pages {i + 1} to {i + len(batch)}...")

    for j, page in enumerate(batch):
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        page.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        # Send image to Google Vision API
        image = vision.Image(content=img_byte_arr)
        response = client.text_detection(image=image)

        # Extract text if found
        text = response.text_annotations[0].description if response.text_annotations else "No text detected"
        extracted_text += f"Page {i + j + 1}:\n{text}\n{'-'*80}\n"

    # Save partially extracted text every batch
    with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
        file.write(extracted_text)
        extracted_text = ""  # Clear variable to free memory

print("OCR Extraction Completed.")
