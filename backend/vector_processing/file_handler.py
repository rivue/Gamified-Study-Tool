import fitz

from vector_processing.file_processing import clean_text, split_into_sentences, create_sections
from vector_processing.embedding_service import insert_sections_to_pinecone_parallel, init_pinecone

def process_document(selected_files, library_id=None):

    if not library_id:
        raise ValueError("Library ID is required to process the document.")

    # Open PDF
    doc = fitz.open(stream=selected_files, filetype="pdf")
    try:
        # **Check if PDF is scanned or digital**
        is_scanned = not any(page.get_text("text").strip() for page in doc)
        extracted_text = ""

        if is_scanned:
            print("📄 Detected Scanned PDF - Extracting text using OCR...")
            extracted_text = ""

            for page in doc:
                pix = page.get_pixmap(dpi=100)
                img_bytes = pix.tobytes("png")
                image = vision.Image(content=img_bytes)
                response = client.text_detection(image=image)
                text = response.text_annotations[0].description if response.text_annotations else "No text detected"
                extracted_text += f"{clean_text(text)}\n"

        else:
            print("📑 Detected Digital PDF - Extracting text directly...")
            extracted_text = "\n".join([clean_text(page.get_text("text")) for page in doc])
            
        sentences = split_into_sentences(extracted_text)
        sections = create_sections(sentences)

        insert_sections_to_pinecone_parallel(sections, library_id)
    finally:
        if doc is not None:
            doc.close()

# TODO eventually add a delete from library feature