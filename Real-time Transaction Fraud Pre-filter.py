import pandas as pd


def prefilter_fraudulent_transactions(transactions_df: pd.DataFrame) -> pd.DataFrame:
    mean_amount = transactions_df["amount"].mean()
    std_amount = transactions_df["amount"].std()
    risk_threshold = mean_amount + (3.0 * std_amount)
    
    suspicious_df = transactions_df[
        (transactions_df["amount"] > risk_threshold) | 
        (transactions_df["failed_attempts"] > 2)
    ].copy()
    
    suspicious_df["flag_reason"] = "HIGH_RISK_ANOMALY"
    return suspicious_df


if __name__ == "__main__":
    data = {
        "tx_id": [1, 2, 3, 4, 5],
        "amount": [45.0, 120.0, 50.0, 15000.0, 60.0],
        "failed_attempts": [0, 0, 1, 4, 0]
    }
    df = pd.DataFrame(data)
    flagged_txs = prefilter_fraudulent_transactions(df)
    print("Flagged fraudulent transactions preview:\n", flagged_txs)