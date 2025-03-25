import fitz

from vector_processing.file_processing import clean_text, split_into_sentences, create_sections
from vector_processing.embedding_service import insert_sections_to_pinecone_parallel

def process_document(selected_files, library_id=None):
    # Validate file type and size here if needed (e.g., check if it's a PDF and not too large)
    try:
        doc = fitz.open(stream=selected_files, filetype="pdf")
    except Exception as e:
        print(f"Failed to open PDF: {e}")
        raise IOError("Failed to open PDF file. The file might be corrupted or in an unsupported format.")

    try:
        # Determine if the PDF is scanned or digital
        is_scanned = not any(page.get_text("text").strip() for page in doc)
        extracted_text = ""
        if is_scanned:
            print("Detected Scanned PDF - performing OCR...")
            for page in doc:
                try:
                    pix = page.get_pixmap(dpi=100)
                    img_bytes = pix.tobytes("png")
                    # Assuming you have an OCR client (e.g., Google Vision); wrap its call in try/except.
                    image = vision.Image(content=img_bytes)
                    response = client.text_detection(image=image)
                    text = response.text_annotations[0].description if response.text_annotations else ""
                    extracted_text += f"{clean_text(text)}\n"
                except Exception as page_err:
                    print(f"OCR error on page: {page_err}")
                    continue  # Skip problematic pages
        else:
            print("Detected Digital PDF - extracting text directly...")
            extracted_text = "\n".join([clean_text(page.get_text("text")) for page in doc])
        
        if not extracted_text.strip():
            print("No text extracted from the document.")
            raise ValueError("No text extracted from the document.")
        
        sentences = split_into_sentences(extracted_text)
        sections = create_sections(sentences)
        insert_sections_to_pinecone_parallel(sections, library_id)
    except Exception as e:
        print(f"Error processing document: {e}")
        raise
    finally:
        if doc is not None:
            doc.close()
