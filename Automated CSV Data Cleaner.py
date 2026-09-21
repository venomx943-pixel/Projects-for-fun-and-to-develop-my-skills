import pandas as pd
import numpy as np

def clean_dataset(file_path: str, output_path: str) -> pd.DataFrame:
    """
    Loads a raw CSV dataset, handles missing values, removes duplicates,
    and exports the cleaned data.
    """
    try:
       
        df = pd.read_csv(file_path)
        initial_rows = len(df)
        print(f"Loaded dataset with {initial_rows} rows.")

        
        df.drop_duplicates(inplace=True)
        print(f"Removed {initial_rows - len(df)} duplicate rows.")

        
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)

        
        df.to_csv(output_path, index=False)
        print(f"Cleaned dataset successfully saved to {output_path}")

        return df

    except Exception as e:
        print(f"Error processing dataset: {str(e)}")
        raise

if __name__ == "__main__":
    # Example execution (Ensure 'raw_data.csv' exists or adjust path)
    input_file = "raw_data.csv"
    output_file = "cleaned_data.csv"

    
    try:
        dummy_data = pd.DataFrame({
            "age": [25, 25, np.nan, 35, 45],
            "salary": [50000, 50000, 60000, np.nan, 80000],
            "department": ["IT", "IT", "HR", "Finance", np.nan]
        })
        dummy_data.to_csv(input_file, index=False)
        
        
        cleaned_df = clean_dataset(input_file, output_file)
        print("\nCleaned Data Preview:")
        print(cleaned_df.head())
        
    except Exception as error:
        print(f"Execution failed: {error}")