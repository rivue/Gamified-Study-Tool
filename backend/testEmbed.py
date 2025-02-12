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
# import pdf2image
# import io
# from google.cloud import vision
# import resource
# import psutil
# import time
# import fitz
# vvv CODESPACE STUFF vvv

# CPU_LIMIT = 50

# MAX_MEMORY = 1 * 1024 * 1024 * 1024
# resource.setrlimit(resource.RLIMIT_AS (MAX_MEMORY, MAX_MEMORY))

# def limit_cpu():
#     while True:
#         cpu_usage = psutil.cpu_percent(interval=1)
#         if cpu_usage > CPU_LIMIT:
#             time.sleep(0.5)  # Pause execution briefly if CPU is over limit

# # Run CPU limit in a separate thread
# import threading
# cpu_thread = threading.Thread(target=limit_cpu, daemon=True)
# cpu_thread.start()

# ^^^ CODESPACE STUFF ^^^

# client = vision.ImageAnnotatorClient()
# pdf_path = "./Duolingothing.pdf"
# # Convert PDF to images in batches of 10 pages
# batch_size = 10  # Adjust if needed
# pages = pdf2image.convert_from_path(pdf_path, dpi=150)

# extracted_text = ""
# for i in range(0, len(pages), batch_size):

#     process = psutil.Process()
#     mem_usage = process.memory_info().rss / (1024 * 1024)
#     MAX_PROCESS_MEMORY = 500

#     if mem_usage > MAX_PROCESS_MEMORY:
#         print(f"Memory usage high: {mem_usage}MB - Sleeping to free memory")
#         time.sleep(2)  # Pause and let memory clear
    
#     batch = pages[i : i + batch_size]
#     print(f"Processing pages {i + 1} to {i + len(batch)}...")

#     for j, page in enumerate(batch):
#         # Convert image to bytes
#         img_byte_arr = io.BytesIO()
#         page.save(img_byte_arr, format="PNG")
#         img_byte_arr = img_byte_arr.getvalue()

#         # Send image to Google Vision API
#         image = vision.Image(content=img_byte_arr)
#         response = client.text_detection(image=image)

#         # Extract text if found
#         text = response.text_annotations[0].description if response.text_annotations else "No text detected"
#         extracted_text += f"Page {i + j + 1}:\n{text}\n{'-'*80}\n"

#     # Save partially extracted text every batch
#     with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
#         file.write(extracted_text)
#         extracted_text = ""  # Clear variable to free memory

# # print("OCR Extraction Completed.")
# import fitz  # PyMuPDF
# import io
# import time
# import psutil
# from google.cloud import vision

# # Initialize Google Vision API client
# client = vision.ImageAnnotatorClient()

# # PDF Path
# pdf_path = "./datapython.pdf"

# # Batch processing configuration
# batch_size = 10  # Adjust as needed
# extracted_text = ""

# # Open PDF with PyMuPDF
# doc = fitz.open(pdf_path)
# total_pages = len(doc)

# total_pages = min(200, total_pages) # for speed for testing purposes

# print(f"Total pages: {total_pages}")

# # Process PDF in batches
# for i in range(0, total_pages, batch_size):

#     # process = psutil.Process()
#     # mem_usage = process.memory_info().rss / (1024 * 1024)
#     # MAX_PROCESS_MEMORY = 500  # MB

#     # if mem_usage > MAX_PROCESS_MEMORY:
#     #     print(f"Memory usage high: {mem_usage}MB - Sleeping to free memory")
#     #     time.sleep(2)  # Pause to free memory

#     print(f"Processing pages {i + 1} to {min(i + batch_size, total_pages)}...")

#     batch = doc[i : i + batch_size]

#     for j, page in enumerate(batch):
#         # Convert page to image
#         pix = page.get_pixmap(dpi=100)  # Adjust DPI if needed
#         img_byte_arr = io.BytesIO(pix.tobytes("png"))

#         # Send image to Google Vision API
#         image = vision.Image(content=img_byte_arr.getvalue())
#         response = client.document_text_detection(image=image)

#         # Extract text if found
#         text = response.text_annotations[0].description if response.text_annotations else "No text detected"
#         extracted_text += f"Page {i + j + 1}:\n{text}\n{'-'*80}\n"

#     # Save partially extracted text every batch
#     with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
#         file.write(extracted_text)
#         extracted_text = ""  # Clear variable to free memory

# print("OCR Extraction Completed.")
# import io
# from google.cloud import vision

# client = vision.ImageAnnotatorClient()

# pdf_path = "./duo.pdf"

# # Read PDF as bytes
# with open(pdf_path, "rb") as pdf_file:
#     pdf_content = pdf_file.read()

# # Send PDF directly to Vision API
# image = vision.Image(content=pdf_content)
# print(image)
# response = client.document_text_detection(image=image)

# # Extract text
# extracted_text = response.full_text_annotation.text
# print(response)
# # Save to file
# with open("google_vision_extracted_text.txt", "w", encoding="utf-8") as file:
#     file.write(extracted_text)

# print("OCR Extraction Completed.")import fitz  # PyMuPDF
import io
import re
import time
from google.cloud import vision
import fitz 
# import pinecone
from pinecone import Pinecone
from openai import OpenAI
import os
from tqdm import tqdm
import time
client = vision.ImageAnnotatorClient()
pdf_path = "./datapython.pdf"
batch_size = 20  # Adjust to optimize for Google Vision API cost

def is_scanned_pdf(pdf_path):
    """
    Determines if the PDF is scanned (image-based) or digital (text-based).
    Returns True if scanned, False if digital.
    """
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text("text")
        if text.strip():  # If text exists, it's a digital PDF
            return False
    return True  # No text found, likely a scanned PDF

def clean_text(text):
    """Remove unwanted unicode artifacts like [U+202C] and other non-standard characters."""
    text = re.sub(r"\[U\+\w{4,5}\]", "", text)  # Remove unicode markers
    return text.strip()

def split_into_sentences(text):
    """
    Split text into sentences using regex pattern that handles common abbreviations
    and multiple punctuation cases.
    """
    # Remove page markers and separators
    text = re.sub(r'Page \d+:\n', '', text)
    text = re.sub(r'-{80}\n', '', text)
    
    # Pattern for splitting sentences while preserving abbreviations
    pattern = r'(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+(?=[A-Z])'
    sentences = re.split(pattern, text)
    
    # Clean up sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def create_sections(sentences, sentences_per_section=8):
    """
    Group sentences into sections of specified size.
    """
    sections = []
    for i in range(0, len(sentences), sentences_per_section):
        section = sentences[i:i + sentences_per_section]
        sections.append(' '.join(section))
    return sections

def process_extracted_text(input_file, output_file):
    """
    Read extracted text file, break into 8-sentence sections,
    and save to new file.
    """
    try:
        # Read the extracted text
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Split into sentences
        sentences = split_into_sentences(text)
        
        # Create sections
        sections = create_sections(sentences)
        
        # Write sections to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            for i, section in enumerate(sections, 1):
                file.write(f"Section {i}:\n")
                file.write(section)
                file.write('\n\n' + '-'*80 + '\n\n')
        
        print(f"✅ Successfully created {len(sections)} sections")
        print(f"📝 Output saved to: {output_file}")
        
        return sections  # Return sections for further processing if needed
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find input file: {input_file}")
    except Exception as e:
        print(f"❌ Error processing text: {str(e)}")

def get_embedding(text, model="text-embedding-3-small"):
    """Get embedding for text using OpenAI's API"""
    client = OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def init_pinecone():
    """Initialize Pinecone client and ensure index exists"""
    # pinecone.init(
    #     api_key=os.getenv("PINECONE_API_KEY"),
    #     # environment=os.getenv("PINECONE_ENVIRONMENT")
    # )
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "text-sections"
    
    # Create index if it doesn't exist
    if index_name not in pclist_indexes():
        pc.create_index(
            name=index_name,
            dimension=1536,  # dimension for text-embedding-3-small
            metric="cosine"
        )
        print(f"Created new Pinecone index: {index_name}")
    
    return pc.Index(index_name)

def insert_sections_to_pinecone(sections):
    """Insert text sections into Pinecone with embeddings"""
    try:
        # Initialize Pinecone
        index = init_pinecone()
        
        # Process sections in batches
        batch_size = 100
        for i in tqdm(range(0, len(sections), batch_size)):
            batch = sections[i:i + batch_size]
            vectors = []
            
            # Prepare vectors for batch
            for j, section in enumerate(batch):
                try:
                    # Get embedding for section
                    embedding = get_embedding(section)
                    
                    # Create vector with metadata
                    vector = {
                        'id': f'section_{i + j}',
                        'values': embedding,
                        'metadata': {
                            'text': section,
                            'section_number': i + j,
                            'word_count': len(section.split())
                        }
                    }
                    vectors.append(vector)
                    
                except Exception as e:
                    print(f"Error processing section {i + j}: {str(e)}")
                    continue
                
                # Rate limiting for API calls
                time.sleep(0.1)
            
            # Upsert batch to Pinecone
            if vectors:
                index.upsert(vectors=vectors)
                print(f"Inserted batch of {len(vectors)} sections")
        
        print("✅ Successfully inserted all sections into Pinecone")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


# Open PDF
doc = fitz.open(pdf_path)

# **Check if PDF is scanned or digital**
if is_scanned_pdf(pdf_path):
    print("📄 Detected Scanned PDF - Extracting text using OCR...")
    extracted_text = ""

    for i in range(0, max(len(doc), 100), batch_size):
        batch = doc[i : i + batch_size]
        print(f"Processing pages {i + 1} to {i + len(batch)}...")

        for j, page in enumerate(batch):
            # Convert PDF page to an image
            pix = page.get_pixmap(dpi=100)
            img_bytes = pix.tobytes("png")

            # Send image to Google Vision API
            image = vision.Image(content=img_bytes)
            response = client.text_detection(image=image)

            # Extract and clean text
            text = response.text_annotations[0].description if response.text_annotations else "No text detected"
            text = clean_text(text)

            extracted_text += f"Page {i + j + 1}:\n{text}\n{'-'*80}\n"

        # Save partially extracted text every batch to free memory
        with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
            file.write(extracted_text)
            extracted_text = ""  # Clear variable

        time.sleep(1)  # Prevent excessive API requests

else:
    print("📑 Detected Digital PDF - Extracting text directly...")
    extracted_text = ""
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        text = clean_text(text)
        extracted_text += f"Page {page_num + 1}:\n{text}\n{'-'*80}\n"

# **Save final extracted text**
with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
    file.write(extracted_text)

# if __name__ == "__main__":
input_file = "google_vision_extracted_text.txt"
output_file = "sectioned_text.txt"
sections = process_extracted_text(input_file, output_file)
sections = []
with open("sectioned_text.txt", 'r', encoding='utf-8') as file:
    text = file.read()
    # Split by section separator
    raw_sections = text.split('-' * 80)
        
    # Clean up sections and remove empty ones
    for section in raw_sections:
        # Remove "Section X:" header and clean whitespace
        cleaned = re.sub(r'Section \d+:\n', '', section).strip()
        if cleaned:
            sections.append(cleaned)
    
    # Insert sections into Pinecone
    insert_sections_to_pinecone(sections)
print("✅ OCR Extraction Completed.")