import io
import pandas as pd


def sanitize_security_logs(log_source) -> pd.DataFrame:
    df = pd.read_csv(log_source)
    df.fillna("UNKNOWN_ENTITY", inplace=True)
    df["user_payload"] = (
        df["user_payload"].astype(str).str.replace(r"[<>'\";]", "", regex=True)
    )
    return df


if __name__ == "__main__":
    raw_csv_data = "log_id,ip_address,user_payload\n101,192.168.1.15,<script>alert('XSS')</script>\n102,10.0.0.4,Normal login request\n103,,DROP TABLE users;"
    mock_file = io.StringIO(raw_csv_data)
    cleaned_logs = sanitize_security_logs(mock_file)
    print("Sanitized logs dataframe preview:\n", cleaned_logs)