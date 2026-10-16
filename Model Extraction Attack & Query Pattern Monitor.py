import time
from typing import Dict, Tuple, List
import numpy as np

class ModelExtractionMonitor:
    """
    Monitors incoming API query patterns and feature space diversity 
    to detect and block Model Extraction (Stealing) black-box probing attacks.
    """
    def __init__(self, time_window_seconds: float = 60.0, max_queries_per_window: int = 50, diversity_threshold: float = 0.05):
        self.time_window = time_window_seconds
        self.max_queries = max_queries_per_window
        self.diversity_threshold = diversity_threshold
        # Tracks client histories: {client_id: [(timestamp, feature_vector), ...]}
        self.client_logs: Dict[str, List[Tuple[float, np.ndarray]]] = {}

    def audit_query(self, client_id: str, feature_vector: List[float]) -> Tuple[bool, str]:
        """
        Audits incoming queries for high-velocity and systematic boundary probing.
        """
        if not client_id:
            raise ValueError("Security violation: Client identifier cannot be empty.")

        current_time = time.time()
        x = np.array(feature_vector, dtype=float)

        if client_id not in self.client_logs:
            self.client_logs[client_id] = []

        # Clean old queries outside the rolling time window
        history = self.client_logs[client_id]
        history = [entry for entry in history if current_time - entry[0] <= self.time_window]
        history.append((current_time, x))
        self.client_logs[client_id] = history

        # Security Check 1: Query velocity (Rate limiting extraction probes)
        if len(history) > self.max_queries:
            return False, f"Security Alert: Model Extraction blocked! Client '{client_id}' exceeded query velocity limit."

        # Security Check 2: Feature space probing diversity analysis (Detecting grid/systematic scans)
        if len(history) >= 10:
            vectors = np.array([entry[1] for entry in history])
            # Compute variance across recent queries to check if the client is methodically scanning space
            feature_variance = np.var(vectors, axis=0)
            mean_variance = np.mean(feature_variance)

            # Abnormally low variance combined with high frequency indicates automated grid probing (Extraction)
            if mean_variance < self.diversity_threshold and len(history) > 20:
                return False, f"Security Alert: Systematic model probing detected! Low feature variance ({mean_variance:.4f}) indicates extraction cloning attempt."

        return True, "Query authorized. Access pattern within normal operational parameters."

if __name__ == "__main__":
    monitor = ModelExtractionMonitor(time_window_seconds=60.0, max_queries_per_window=30, diversity_threshold=0.01)
    
    client_proxy = "attacker_client_99"

    try:
        print("Simulating normal user queries...")
        for i in range(5):
            # Normal users query varied, natural points
            features = [np.random.uniform(-5, 5), np.random.uniform(-5, 5)]
            is_safe, msg = monitor.audit_query(client_proxy, features)
            print(f"Query {i+1}: {msg}")

        print("\nSimulating automated systematic model extraction probing attack...")
        # Attacker systematically probing a grid or dense cluster
        for i in range(35):
            probing_features = [1.0 + (i * 0.001), 2.0 + (i * 0.001)] # Extremely low variance systematic scan
            is_safe, msg = monitor.audit_query(client_proxy, probing_features)
            if not is_safe:
                print(f"Query {i+1}: {msg}")
                break

    except Exception as error:
        print(f"Execution failed: {error}")