import numpy as np
from typing import Tuple, List

class AdversarialInputDetector:
    """
    A statistical defense mechanism to detect outlier or adversarial input features
    based on training data distribution (Z-score thresholding).
    """
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean_vector = None
        self.std_vector = None

    def fit(self, training_data: np.ndarray) -> None:
        """
        Learns the normal statistical distribution (mean and standard deviation) 
        from safe training data.
        """
        if not isinstance(training_data, np.ndarray):
            training_data = np.array(training_data)
            
        if training_data.size == 0:
            raise ValueError("Training data cannot be empty.")

        self.mean_vector = np.mean(training_data, axis=0)
        self.std_vector = np.std(training_data, axis=0)
        
        # Security sanitization: Prevent division by zero if a feature has zero variance
        self.std_vector = np.where(self.std_vector == 0, 1e-8, self.std_vector)

    def detect_anomaly(self, sample_input: List[float]) -> Tuple[bool, str]:
        """
        Scans a new incoming sample against learned safe distributions 
        to detect potential adversarial manipulation.
        """
        if self.mean_vector is None or self.std_vector is None:
            raise RuntimeError("Detector must be fitted with training data before detection.")

        sample = np.array(sample_input)
        
        if sample.shape[0] != self.mean_vector.shape[0]:
            return True, "Security Violation: Input feature dimension mismatch."

        # Calculate absolute Z-scores for each feature
        z_scores = np.abs((sample - self.mean_vector) / self.std_vector)

        # Check if any feature exceeds the anomalous threshold
        if np.any(z_scores > self.threshold):
            return True, f"Alert: Potential adversarial outlier detected! Max Z-score: {np.max(z_scores):.2f}"

        return False, "Input data is within safe statistical boundaries."

if __name__ == "__main__":
    # Simulate safe training dataset (e.g., normal server traffic or sensor metrics)
    np.random.seed(42)
    safe_baseline = np.random.normal(loc=50.0, scale=5.0, size=(100, 3))

    detector = AdversarialInputDetector(threshold=3.0)
    detector.fit(safe_baseline)

    # Test cases: One normal sample and one adversarially manipulated sample
    normal_sample = [51.2, 49.8, 50.5]
    adversarial_sample = [85.0, 48.0, 10.2] # Contains extreme manipulated values

    for name, test_data in [("Normal Input", normal_sample), ("Adversarial Input", adversarial_sample)]:
        print(f"\nEvaluating {name}: {test_data}")
        is_anomaly, message = detector.detect_anomaly(test_data)
        print(f"Is Anomaly/Attack: {is_anomaly}")
        print(f"Details: {message}")