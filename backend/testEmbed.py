
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
import io
import re
import time
from google.cloud import vision
import fitz 
import concurrent.futures
from pinecone import ServerlessSpec
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
import os
from tqdm import tqdm
import time


def clean_text(text): # put in --> utils.py
    """Remove unwanted unicode artifacts like [U+202C] and other non-standard characters."""
    text = re.sub(r"\[U\+\w{4,5}\]", "", text)  # Remove unicode markers
    return text.strip()

def split_into_sentences(text): # put in --> utils.py
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

def create_sections(sentences, sentences_per_section=4):
    """
    Group sentences into sections of specified size.
    """
    sections = []
    for i in range(0, len(sentences), sentences_per_section):
        section = sentences[i:i + sentences_per_section]
        sections.append(' '.join(section))
    return sections
        
def process_extracted_text(input_file, output_file): # --> document/process_document.py
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
    except FileNotFoundError:
        print(f"❌ Error: Could not find input file: {input_file}")
    except Exception as e:
        print(f"❌ Error processing text: {str(e)}")

def get_embedding(text, model="text-embedding-3-small"): # --> should go in openapi.py
    """Get embedding for text using OpenAI's API"""
    client = OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def init_pinecone(): # --> where to initialize?
    """Initialize Pinecone client and ensure index exists"""
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"), grpc=True)
        index_name = "text-sections"
        
        try:
            # Try to get the existing index directly
            index = pc.Index(index_name)
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

def insert_sections_batch(index, batch, start_index):
    vectors = []
    for j, section in enumerate(batch):
        if not section.strip():  # Skip empty sections
            continue
            
        embedding = get_embedding(section)
        if not embedding:  # Handle embedding failures
            continue
        
        timestamp = int(time.time())

        vectors.append({
            'id': f'section_{timestamp}_{start_index + j}',
            'values': embedding,
            'metadata': {
                'text': section,
                'section_number': start_index + j,
                'word_count': len(section.split())
            }
        })

    if vectors:
        try:
            result = index.upsert(vectors=vectors, grpc=True)
            print(f"Upserted {len(vectors)} sections")
            print(f"Pinecone response: {result}")
            return result
        except Exception as e:
            print(f"Upsert error: {str(e)}")
            return None


    # Upsert batch to Pinecone
    if vectors:
        index.upsert(vectors=vectors)
        print(f"✅ Inserted batch of {len(vectors)} sections")

    return len(vectors)

def insert_sections_to_pinecone_parallel(sections, num_workers=4):
    """Parallelized insertion of text sections into Pinecone"""
    try:
        # Initialize Pinecone
        index = init_pinecone()

        # Split sections into batches
        batch_size = 100
        batches = [sections[i:i + batch_size] for i in range(0, len(sections), batch_size)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit tasks in parallel
            futures = {executor.submit(insert_sections_batch, index, batch, i * batch_size): i for i, batch in enumerate(batches)}

            # Track progress
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                try:
                    future.result()  # Retrieve results and catch errors
                except Exception as e:
                    print(f"❌ Error in batch processing: {str(e)}")

        print("🚀 Successfully inserted all sections into Pinecone using parallel processing")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

# # Open PDF
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
#  **Save final extracted text**
with open("google_vision_extracted_text.txt", "a", encoding="utf-8") as file:
    file.write(extracted_text)
 ### ^^^ focus on this stuff for now, make sure it works, then move to other stuff ^^^

# # if __name__ == "__main__":
# input_file = "google_vision_extracted_text.txt"
# output_file = "sectioned_text.txt"
# sections = process_extracted_text(input_file, output_file)
# sections = []
# with open("sectioned_text.txt", 'r', encoding='utf-8') as file:
#     text = file.read()
#     # Split by section separator
#     raw_sections = text.split('-' * 80)
        
#     # Clean up sections and remove empty ones
#     for section in raw_sections:
#         # Remove "Section X:" header and clean whitespace
#         cleaned = re.sub(r'Section \d+:\n', '', section).strip()
#         if cleaned:
#             sections.append(cleaned)
    
#     # Insert sections into Pinecone
#     start = time.time()
#     insert_sections_to_pinecone_parallel(sections)
#     end = time.time()
#     print(end-start)
# print("✅ OCR Extraction Completed.")

