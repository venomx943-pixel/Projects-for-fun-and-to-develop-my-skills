import io
import pandas as pd


def aggregate_bug_reports(report_sources: list) -> pd.DataFrame:
    dataframes = [pd.read_csv(io.StringIO(src)) for src in report_sources]
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.fillna({"cvss_score": 0.0, "reporter": "ANONYMOUS"}, inplace=True)
    prioritized_df = combined_df.sort_values(by="cvss_score", ascending=False)
    return prioritized_df


if __name__ == "__main__":
    feed_1 = "report_id,severity,cvss_score,reporter\n1,High,8.5,Alice\n2,Medium,5.3,"
    feed_2 = "report_id,severity,cvss_score,reporter\n3,Critical,9.8,Bob\n4,Low,3.1,Charlie"
    aggregated = aggregate_bug_reports([feed_1, feed_2])
    print("Prioritized bug bounty reports:\n", aggregated)