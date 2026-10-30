from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class NetworkIntrusionDetector:
    def __init__(self):
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    def train_model(self, traffic_data: list, attack_labels: list):
        X_train, X_test, y_train, y_test = train_test_split(
            traffic_data, attack_labels, test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return round(float(accuracy), 4)

    def audit_traffic(self, live_traffic: list) -> list:
        predictions = self.model.predict(live_traffic)
        probabilities = self.model.predict_proba(live_traffic)
        
        results = []
        for idx, traffic in enumerate(live_traffic):
            pred = predictions[idx]
            confidence = float(max(probabilities[idx]))
            is_attack = pred == 1
            
            results.append({
                "id": idx + 1,
                "metrics": {
                    "packet_size_bytes": traffic[0],
                    "flow_duration_sec": traffic[1],
                    "destination_port": traffic[2],
                    "packet_count": traffic[3]
                },
                "status": "DETECTED_MALICIOUS_INTRUSION" if is_attack else "NORMAL_NETWORK_TRAFFIC",
                "confidence_score": round(confidence, 4)
            })
        return results


if __name__ == "__main__":
    # Features format: [Packet_Size_Bytes, Flow_Duration_Sec, Destination_Port, Packet_Count]
    # Labels: 0 = Normal Traffic, 1 = Malicious Intrusion / Port Scan / Flood
    
    historical_traffic = [
        [512.0, 0.5, 443, 10], [1024.0, 1.2, 80, 25], [256.0, 0.1, 22, 2], [128.0, 0.2, 53, 5],
        [768.0, 0.8, 443, 15], [512.0, 0.4, 80, 8], [300.0, 0.3, 443, 6], [1024.0, 1.5, 80, 30],
        [600.0, 0.6, 443, 12], [400.0, 0.5, 80, 10], [512.0, 0.5, 443, 10], [1024.0, 1.2, 80, 25],
        [256.0, 0.1, 22, 2], [128.0, 0.2, 53, 5], [768.0, 0.8, 443, 15], [512.0, 0.4, 80, 8],
        [300.0, 0.3, 443, 6], [1024.0, 1.5, 80, 30], [600.0, 0.6, 443, 12], [400.0, 0.5, 80, 10],
        [512.0, 0.5, 443, 10], [1024.0, 1.2, 80, 25], [256.0, 0.1, 22, 2], [128.0, 0.2, 53, 5],
        [768.0, 0.8, 443, 15], [512.0, 0.4, 80, 8], [300.0, 0.3, 443, 6], [1024.0, 1.5, 80, 30],
        [600.0, 0.6, 443, 12], [400.0, 0.5, 80, 10], [512.0, 0.5, 443, 10], [1024.0, 1.2, 80, 25],
        [256.0, 0.1, 22, 2], [128.0, 0.2, 53, 5], [768.0, 0.8, 443, 15], [512.0, 0.4, 80, 8],
        [300.0, 0.3, 443, 6], [1024.0, 1.5, 80, 30], [600.0, 0.6, 443, 12], [400.0, 0.5, 80, 10],
        # Malicious Intrusion / Port Scan / DDoS Samples (Abnormal packet counts, short durations, brute force ports)
        [40.0, 0.01, 445, 5000], [64.0, 0.02, 3389, 4200], [40.0, 0.01, 21, 6000],
        [64.0, 0.01, 22, 5500], [40.0, 0.02, 80, 4800], [64.0, 0.01, 443, 5100],
        [40.0, 0.01, 3306, 6200], [64.0, 0.02, 5432, 4900], [40.0, 0.01, 1433, 5800],
        [64.0, 0.01, 8080, 5300]
    ]

    labels = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    realtime_traffic = [
        [512.0, 0.5, 443, 12],    # Normal web browsing traffic
        [40.0, 0.01, 445, 5400]   # Malicious port scan / intrusion flood
    ]

    ids_system = NetworkIntrusionDetector()
    train_acc = ids_system.train_model(historical_traffic, labels)
    print(f"IDS Model Training Accuracy on Test Split: {train_acc * 100}%\n")

    audit_report = ids_system.audit_traffic(realtime_traffic)

    print("--- Enterprise Network Intrusion Detection Audit Report ---")
    for res in audit_report:
        print(f"Traffic [{res['id']}] | Status: {res['status']} | Confidence: {res['confidence_score']} | Metrics: {res['metrics']}")