import pandas as pd


def mask_pii_data(df: pd.DataFrame) -> pd.DataFrame:
    masked_df = df.copy()
    masked_df["email"] = masked_df["email"].str.replace(
        r"(^[\w.%+-]{2})[\w.%+-]+(@[\w.-]+\.[a-zA-Z]{2,})", r"\1***\2", regex=True
    )
    masked_df["phone"] = masked_df["phone"].astype(str).str.slice_replace(0, -4, "*")
    return masked_df


if __name__ == "__main__":
    data = {
        "customer_id": [1, 2],
        "email": ["alice.smith@company.com", "bob.jones@secure.org"],
        "phone": ["+15552345678", "+447911123456"],
    }
    df = pd.DataFrame(data)
    secured_df = mask_pii_data(df)
    print("Masked PII dataframe preview:\n", secured_df)