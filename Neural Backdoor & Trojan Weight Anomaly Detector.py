import numpy as np
from sklearn.linear_model import LogisticRegression
from typing import Tuple, List

class BackdoorWeightDetector:
    """
    Scans machine learning model weights for statistical anomalies and outlier coefficients
    to detect injected backdoors (Trojan models) before deployment.
    """
    def __init__(self, z_score_threshold: float = 3.0):
        self.z_score_threshold = z_score_threshold

    def inspect_model_weights(self, model: LogisticRegression) -> Tuple[bool, str]:
        """
        Analyzes model coefficients using Z-score statistics to flag poisoned or abnormal weights.
        """
        if model is None or not hasattr(model, "coef_"):
            return False, "Security Alert: Invalid model object provided for backdoor inspection."

        weights = model.coef_[0]
        
        if weights.size == 0:
            return False, "Security Violation: Model weights are empty."

        # Compute statistical mean and standard deviation of model weights
        mean_val = np.mean(weights)
        std_val = np.std(weights)

        # Handle zero standard deviation edge case safely
        if std_val == 0:
            return True, "Model weights are uniform. No statistical anomalies detected."

        # Calculate Z-scores for each weight coefficient
        z_scores = np.abs((weights - mean_val) / std_val)
        
        # Check if any weight exceeds the danger z-score threshold (potential backdoor neuron)
        max_z_score = np.max(z_scores)
        if max_z_score > self.z_score_threshold:
            return False, f"Security Alert: Backdoor Trojan detected! Maximum weight Z-Score ({max_z_score:.2f}) exceeds safety threshold."

        return True, f"Model weight integrity verified. Max Z-Score ({max_z_score:.2f}) is within safe generalized boundaries."

if __name__ == "__main__":
    # Simulate a standard clean trained model
    np.random.seed(42)
    X_train = np.random.normal(loc=0.0, scale=1.0, size=(100, 3))
    y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)

    clean_model = LogisticRegression()
    clean_model.fit(X_train, y_train)

    detector = BackdoorWeightDetector(z_score_threshold=2.5)

    try:
        print("Inspecting clean model for backdoors...")
        is_safe, message = detector.inspect_model_weights(clean_model)
        print(f"Status - Is Safe: {is_safe}")
        print(f"Details: {message}\n")

        # Simulate a poisoned/trojaned model by manually injecting an abnormal outlier weight
        print("Injecting backdoor poison into model weights...")
        clean_model.coef_[0][0] = 25.5  # Artificial anomalous backdoor weight
        
        is_safe_poisoned, message_poisoned = detector.inspect_model_weights(clean_model)
        print(f"Status - Is Safe: {is_safe_poisoned}")
        print(f"Details: {message_poisoned}")

    except Exception as error:
        print(f"Execution failed: {error}")