import pandas as pd
import re
import os
from typing import List

def sanitize_dataset_pii(file_path: str, sensitive_columns: List[str] = None) -> pd.DataFrame:
    """
    Loads a dataset and strips or masks Personal Identifiable Information (PII)
    to protect data privacy before machine learning processing.
    """
    # Security check: Ensure file exists to prevent path manipulation crashes
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Critical error: File '{file_path}' not found.")
    
    # Security check: Prevent zero-byte file exploitation
    if os.path.getsize(file_path) == 0:
        raise ValueError("Critical error: Dataset file is empty.")

    df = pd.read_csv(file_path)

    if sensitive_columns is None:
        sensitive_columns = ["email", "phone", "name", "ssn", "credit_card"]

    # Normalize column names for safe and consistent matching
    df.columns = [col.strip().lower() for col in df.columns]

    # Mask known sensitive columns completely
    for col in sensitive_columns:
        if col in df.columns:
            df[col] = "[REDACTED_SECURE]"

    # Security scan: Use Regex to catch leaked emails hidden inside generic text columns
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    for col in df.select_dtypes(include=['object']).columns:
        if col not in sensitive_columns:
            df[col] = df[col].astype(str).apply(
                lambda val: re.sub(email_regex, '[EMAIL_REDACTED]', val)
            )

    print("Dataset successfully sanitized and PII stripped.")
    return df

if __name__ == "__main__":
    # Example execution with a synthetic dataset containing sensitive info
    sample_file = "user_data_sample.csv"
    try:
        raw_data = pd.DataFrame({
            "name": ["Alice Smith", "Bob Jones"],
            "email": ["alice@securebank.com", "bob.janes@internal-mail.org"],
            "score": [95, 88]
        })
        raw_data.to_csv(sample_file, index=False)

        cleaned_df = sanitize_dataset_pii(sample_file)
        print("\nSanitized DataFrame Preview:")
        print(cleaned_df)
        
    except Exception as error:
        print(f"Execution failed: {error}")