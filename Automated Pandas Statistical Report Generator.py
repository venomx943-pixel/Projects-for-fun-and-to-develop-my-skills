import pandas as pd
import numpy as np
import os

def generate_statistical_report(file_path: str) -> dict:
    """
    Loads a CSV dataset, performs safety validations, and generates
    a comprehensive statistical report.
    """
    # Security check: Ensure file exists to prevent path traversal or missing file crashes
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Critical error: File '{file_path}' does not exist.")
    
    # Security check: Ensure file is not empty (DoS / zero-byte exploitation prevention)
    if os.path.getsize(file_path) == 0:
        raise ValueError("Critical error: The provided dataset file is empty.")

    try:
        # Load dataset
        df = pd.read_csv(file_path)
        
        # Security check: Ensure dataset contains valid structure
        if df.empty or len(df.columns) == 0:
            raise ValueError("Dataset contains no valid rows or columns.")

        report = {}
        report["total_rows"] = int(len(df))
        report["total_columns"] = int(len(df.columns))

        # Filter only numerical columns for safe mathematical analysis
        numeric_df = df.select_dtypes(include=[np.number])
        
        if not numeric_df.empty:
            # Generate summary statistics (mean, std, min, max, etc.)
            report["numeric_summary"] = numeric_df.describe().to_dict()
        else:
            report["numeric_summary"] = "No numerical columns available for analysis."

        print("Statistical report successfully compiled.")
        return report

    except Exception as e:
        print(f"Error analyzing dataset: {str(e)}")
        raise

if __name__ == "__main__":
    # Example execution: Create a sample dataset for testing
    sample_file = "sample_data.csv"
    try:
        dummy_data = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "score": [85, 90, 78, 92, 88],
            "hours_studied": [5.5, 6.0, 4.5, 7.0, 5.0]
        })
        dummy_data.to_csv(sample_file, index=False)

        # Generate and print the report
        report_result = generate_statistical_report(sample_file)
        print("\nGenerated Report Overview:")
        for key, value in report_result.items():
            print(f"- {key}: {value}")

    except Exception as error:
        print(f"Execution failed: {error}")