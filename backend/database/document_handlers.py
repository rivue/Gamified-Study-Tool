import fitz

client = vision.ImageAnnotatorClient()
pdf_path = "./shorterbook.pdf"

batch_size = 20  # Adjust to optimize for Google Vision API cost (higher = better)

# HANDLING WILL BE DONE HERE, AND WILL BE CALLED BY LIBRARY HANDLER WHEN WE NEED TO UPLOAD A LIBRARY W/ DOCUMENTS

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