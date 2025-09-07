import fitz

from vector_processing.file_processing import clean_text, split_into_sentences, create_sections
from vector_processing.embedding_service import insert_sections_to_pinecone_parallel

def extract_text(selected_files, ocr_callback=None, dpi=150, assume_scanned=None):
    """
    Central text extraction logic.
    - selected_files: PDF bytes
    - ocr_callback: optional callable(bytes) -> str used for OCR per page if scanned
    - dpi: rasterization DPI for OCR workflow
    - assume_scanned: override auto-detection if True/False
    """
    doc = None
    try:
        try:
            doc = fitz.open(stream=selected_files, filetype="pdf")
        except Exception as e:
            raise IOError(f"Failed to open PDF file: {e}")

        # Determine if scanned
        if assume_scanned is None:
            is_scanned = not any(page.get_text("text").strip() for page in doc)
        else:
            is_scanned = bool(assume_scanned)

        extracted_text = ""

        if is_scanned:
            if ocr_callback is None:
                raise ValueError("Scanned PDF detected but no OCR callback was provided.")
            for page in doc:
                try:
                    pix = page.get_pixmap(dpi=dpi, alpha=False)
                    img_bytes = pix.tobytes("png")
                    text = ocr_callback(img_bytes) or ""
                    extracted_text += f"{clean_text(text)}\n"
                except Exception:
                    # Skip problematic pages during OCR
                    continue
        else:
            extracted_text = "\n".join(clean_text(page.get_text("text")) for page in doc)

        if not extracted_text.strip():
            raise ValueError("No text extracted from the document.")

        return extracted_text
    finally:
        if doc is not None:
            doc.close()

def process_document(selected_files, library_id=None, ocr_callback=None, dpi=150, assume_scanned=None):
    """
    Extracts text, splits into sentences, creates sections, and uploads to Pinecone.
    """
    try:
        extracted_text = extract_text(
            selected_files,
            ocr_callback=ocr_callback,
            dpi=dpi,
            assume_scanned=assume_scanned,
        )
        sentences = split_into_sentences(extracted_text)
        sections = create_sections(sentences)
        insert_sections_to_pinecone_parallel(sections, library_id)
        return sections
    except Exception:
        raise

def process_document_no_pinecone(selected_files, ocr_callback=None, dpi=150, assume_scanned=None):
    """
    Extracts text only (no split, no sections, no upload).
    """
    try:
        return extract_text(
            selected_files,
            ocr_callback=ocr_callback,
            dpi=dpi,
            assume_scanned=assume_scanned,
        )
    except Exception:
        raise