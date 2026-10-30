import numpy as np
from sklearn.ensemble import IsolationForest


class FinancialFraudAnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def train(self, transaction_features: list):
        self.model.fit(transaction_features)

    def audit_transactions(self, transactions: list) -> list:
        predictions = self.model.predict(transactions)
        anomaly_scores = self.model.decision_function(transactions)
        
        results = []
        for idx, tx in enumerate(transactions):
            pred = predictions[idx]
            score = float(anomaly_scores[idx])
            is_fraud = pred == -1
            
            results.append({
                "id": idx + 1,
                "features": tx,
                "status": "FLAGGED_FRAUD_ANOMALY" if is_fraud else "NORMAL_TRANSACTION",
                "anomaly_score": round(score, 4)
            })
        return results


if __name__ == "__main__":
    # Features format: [Transaction_Amount ($), Hour_of_Day (0-23), Distance_from_Home_km, Failed_Login_Attempts]
    historical_transactions = [
        [45.5, 14, 2.1, 0], [120.0, 10, 5.0, 0], [15.0, 12, 1.2, 0], [85.0, 15, 3.0, 0],
        [200.0, 11, 4.5, 0], [50.0, 13, 0.5, 0], [30.0, 9, 2.0, 0], [90.0, 16, 6.1, 0],
        [110.0, 14, 3.2, 0], [75.0, 12, 1.0, 0], [60.0, 15, 2.5, 0], [130.0, 11, 4.0, 0],
        [25.0, 10, 0.8, 0], [95.0, 13, 3.5, 0], [150.0, 14, 5.5, 0], [40.0, 16, 1.5, 0],
        [80.0, 12, 2.2, 0], [105.0, 9, 3.8, 0], [55.0, 11, 1.8, 0], [140.0, 15, 4.8, 0],
        [20.0, 10, 0.2, 0], [70.0, 14, 2.9, 0], [160.0, 13, 5.2, 0], [85.0, 12, 3.1, 0],
        [100.0, 11, 4.1, 0], [35.0, 15, 1.1, 0], [65.0, 10, 2.0, 0], [115.0, 16, 3.9, 0],
        [125.0, 14, 4.6, 0], [45.0, 9, 1.9, 0], [90.0, 13, 3.3, 0], [135.0, 12, 4.9, 0],
        [55.0, 11, 2.4, 0], [105.0, 15, 3.7, 0], [75.0, 10, 2.6, 0], [145.0, 14, 5.1, 0],
        [30.0, 16, 0.9, 0], [80.0, 12, 3.0, 0], [155.0, 11, 5.4, 0], [50.0, 13, 1.7, 0],
        # Anomaly / Fraudulent Injection Samples
        [9500.0, 3, 1200.5, 5], [8200.0, 2, 950.0, 4], [10500.0, 4, 1500.0, 6],
        [7800.0, 1, 880.2, 5], [11000.0, 3, 1340.0, 7], [9200.0, 2, 1100.0, 4],
        [8900.0, 4, 980.5, 6], [10200.0, 1, 1450.0, 5], [9900.0, 3, 1250.0, 5],
        [12000.0, 2, 1600.0, 8]
    ]

    new_test_transactions = [
        [65.0, 14, 2.0, 0],       # Normal transaction
        [9800.0, 3, 1250.0, 6]    # Highly suspicious fraudulent anomaly
    ]

    detector = FinancialFraudAnomalyDetector(contamination=0.1)
    detector.train(historical_transactions)

    audit_report = detector.audit_transactions(new_test_transactions)

    print("--- Enterprise Financial Fraud & Anomaly Audit Report ---")
    for res in audit_report:
        print(f"[{res['id']}] Status: {res['status']} | Anomaly Score: {res['anomaly_score']} | Features: {res['features']}")