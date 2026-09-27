import re
from typing import Tuple, List

def secure_response_sanitizer(llm_output: str, restricted_patterns: List[str] = None) -> Tuple[bool, str]:
    """
    Scans model-generated text outputs for potential data leaks, exposed API keys,
    or dangerous patterns before sending them to the end user.
    """
    if not isinstance(llm_output, str):
        raise TypeError("Invalid input type: Expected a string output.")

    # Security check: Prevent Denial of Service via massive output strings
    if len(llm_output) > 10000:
        return False, "Security Alert: Model output size exceeds maximum safety threshold."

    if restricted_patterns is None:
        restricted_patterns = [
            "password=", 
            "secret_key", 
            "api_key", 
            "internal_ip"
        ]

    # Normalize text for safe uniform inspection
    normalized_output = llm_output.lower()

    # Security scan: Check for leaked internal credentials or sensitive keywords
    for pattern in restricted_patterns:
        if pattern in normalized_output:
            return False, f"Security Violation: Model leaked restricted internal pattern ('{pattern}'). Output blocked."

    # Advanced Security Sanitization: Regex scan to catch exposed API keys or tokens (e.g., sk-...)
    api_key_regex = r'sk-[a-zA-Z0-9]{32,}'
    if re.search(api_key_regex, llm_output):
        return False, "Security Violation: Exposed API key detected in model response. Output blocked."

    # General sanitization: Strip hidden control characters
    sanitized_output = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', llm_output)

    return True, sanitized_output.strip()

if __name__ == "__main__":
    # Test cases simulating safe vs leaking model responses
    safe_response = "Here is the summary of your requested technical report: System performance is optimal."
    leaking_response = "Access granted. Your admin secret_key is sk-proj-abcdef1234567890abcdef1234567890."

    for name, sample_text in [("Safe Response", safe_response), ("Leaking Response", leaking_response)]:
        print(f"\nEvaluating {name}: '{sample_text}'")
        is_safe, result = secure_response_sanitizer(sample_text)
        print(f"Status - Is Safe: {is_safe}")
        print(f"Result / Details: {result}")