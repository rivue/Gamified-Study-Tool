import re

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


def create_sections(sentences, sentences_per_section=4):
    """
    Group sentences into sections of specified size.
    """
    sections = []
    for i in range(0, len(sentences), sentences_per_section):
        section = sentences[i:i + sentences_per_section]
        sections.append(' '.join(section))
    return sections
