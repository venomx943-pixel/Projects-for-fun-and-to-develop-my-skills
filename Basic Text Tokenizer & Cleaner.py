import re
from typing import List

def clean_and_tokenize_text(text: str, max_length: int = 5000) -> List[str]:
    """
    Cleans raw text input, enforces security length limits to prevent DoS attacks,
    and tokenizes it into clean lowercase words.
    """
    if not isinstance(text, str):
        raise TypeError("Invalid input type: Expected a string.")

    # Security check: Prevent Denial of Service (DoS) via excessively massive text inputs
    if len(text) > max_length:
        raise ValueError(f"Security violation: Input text exceeds maximum allowed length of {max_length} characters.")

    # Security check: Ensure text is not empty or consisting only of whitespace
    if not text.strip():
        raise ValueError("Provided text is empty or contains only whitespace.")

    # Convert text to lowercase for uniformity
    normalized_text = text.lower()

    # Security/Sanitization: Remove unwanted special characters, keeping only letters, numbers, and basic spaces
    sanitized_text = re.sub(r'[^a-z0-9\s]', '', normalized_text)

    # Tokenization: Split the cleaned text into individual word tokens
    tokens = sanitized_text.split()

    print(f"Successfully processed and tokenized text into {len(tokens)} tokens.")
    return tokens

if __name__ == "__main__":
    # Example execution
    raw_sample = "   Alert! AI-Security systems are evolving rapidly in 2026... Let's secure them!   "
    
    try:
        print(f"Original Text: '{raw_sample}'")
        word_tokens = clean_and_tokenize_text(raw_sample)
        print("\nExtracted Tokens:")
        print(word_tokens)
        
    except Exception as error:
        print(f"Execution failed: {error}")