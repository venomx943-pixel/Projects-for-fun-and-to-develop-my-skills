from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class CloudServerPredictiveMaintenance:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train_model(self, telemetry_data: list, failure_labels: list):
        X_train, X_test, y_train, y_test = train_test_split(
            telemetry_data, failure_labels, test_size=0.2, random_state=42
        )
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return round(float(accuracy), 4)

    def audit_servers(self, server_metrics: list) -> list:
        predictions = self.model.predict(server_metrics)
        probabilities = self.model.predict_proba(server_metrics)
        
        results = []
        for idx, metrics in enumerate(server_metrics):
            pred = predictions[idx]
            confidence = float(max(probabilities[idx]))
            is_failing = pred == 1
            
            results.append({
                "id": idx + 1,
                "metrics": {
                    "cpu_usage_pct": metrics[0],
                    "memory_usage_pct": metrics[1],
                    "temperature_c": metrics[2],
                    "disk_io_errors": metrics[3]
                },
                "status": "PREDICTED_CRITICAL_FAILURE" if is_failing else "HEALTHY_STABLE",
                "confidence_score": round(confidence, 4)
            })
        return results


if __name__ == "__main__":
    # Telemetry Features format: [CPU_Usage_Pct, Memory_Usage_Pct, Temperature_C, Disk_IO_Errors]
    # Labels: 0 = Healthy/Stable, 1 = Predicted Hardware/Software Failure
    
    historical_telemetry = [
        [45.2, 50.1, 62.0, 0], [30.1, 40.5, 58.0, 0], [60.5, 65.0, 70.0, 0], [25.0, 35.2, 55.0, 0],
        [50.0, 55.0, 65.0, 0], [40.2, 45.0, 60.0, 0], [35.5, 42.1, 59.0, 0], [65.0, 70.2, 72.0, 0],
        [55.1, 60.0, 68.0, 0], [48.0, 52.5, 63.5, 0], [38.2, 44.0, 61.0, 0], [52.0, 58.0, 66.0, 0],
        [28.5, 38.0, 56.5, 0], [42.0, 48.2, 62.5, 0], [62.0, 68.0, 71.0, 0], [33.0, 41.0, 57.5, 0],
        [46.5, 51.0, 63.0, 0], [58.0, 62.5, 69.0, 0], [36.0, 43.0, 59.5, 0], [54.0, 59.0, 67.0, 0],
        [22.0, 30.5, 53.0, 0], [44.0, 49.0, 61.5, 0], [68.0, 74.0, 75.0, 0], [49.0, 53.0, 64.0, 0],
        [51.0, 56.0, 65.5, 0], [31.0, 39.0, 56.0, 0], [41.0, 46.5, 60.5, 0], [57.0, 63.0, 68.5, 0],
        [59.0, 64.0, 69.5, 0], [34.0, 42.0, 58.5, 0], [47.0, 51.5, 63.2, 0], [61.0, 67.0, 70.5, 0],
        [39.0, 45.0, 60.2, 0], [53.0, 57.5, 66.5, 0], [43.0, 47.5, 62.0, 0], [63.0, 69.0, 71.5, 0],
        [26.0, 36.0, 54.5, 0], [48.5, 53.5, 63.8, 0], [66.0, 72.0, 73.5, 0], [37.0, 43.5, 59.8, 0],
        # Failing / Critical Server Samples (High temp, high errors, overloaded CPU/RAM)
        [98.5, 95.0, 91.5, 14], [96.0, 92.5, 89.0, 12], [99.1, 97.0, 94.0, 18],
        [95.5, 91.0, 88.5, 11], [97.8, 94.2, 92.0, 15], [96.5, 93.0, 90.0, 13],
        [98.0, 96.0, 93.5, 16], [95.0, 90.5, 87.0, 10], [98.9, 95.8, 92.8, 17],
        [99.5, 98.0, 96.0, 20]
    ]

    labels = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    realtime_server_telemetry = [
        [42.5, 48.0, 61.0, 0],   # Healthy server
        [98.2, 96.5, 93.0, 16]   # Server on the verge of critical failure
    ]

    maintenance_system = CloudServerPredictiveMaintenance()
    train_accuracy = maintenance_system.train_model(historical_telemetry, labels)
    print(f"Model Training Accuracy on Test Split: {train_accuracy * 100}%\n")

    audit_report = maintenance_system.audit_servers(realtime_server_telemetry)

    print("--- Enterprise Cloud Infrastructure Maintenance Audit Report ---")
    for res in audit_report:
        print(f"Server [{res['id']}] | Status: {res['status']} | Confidence: {res['confidence_score']} | Metrics: {res['metrics']}")