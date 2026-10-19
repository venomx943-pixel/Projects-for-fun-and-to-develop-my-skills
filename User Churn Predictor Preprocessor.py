import pandas as pd


def preprocess_user_churn_data(user_logs_df: pd.DataFrame) -> pd.DataFrame:
    user_logs_df.fillna(
        {"login_count": 0, "session_duration_avg": 0.0}, inplace=True
    )
    user_logs_df["engagement_score"] = (
        user_logs_df["login_count"] * user_logs_df["session_duration_avg"]
    )
    churn_risk_df = user_logs_df[user_logs_df["engagement_score"] < 50.0].copy()
    return churn_risk_df


if __name__ == "__main__":
    data = {
        "user_id": [101, 102, 103, 104],
        "login_count": [25, 2, None, 40],
        "session_duration_avg": [15.5, 2.0, 5.0, None],
    }
    df = pd.DataFrame(data)
    processed = preprocess_user_churn_data(df)
    print("At-risk churn users preview:\n", processed)