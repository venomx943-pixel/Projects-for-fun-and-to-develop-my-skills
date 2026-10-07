import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import Tuple, List

class MembershipInferenceSimulator:
    """
    Simulates a Membership Inference Attack (MIA) to test if an ML model
    leaks training data information through prediction confidence scores.
    """
    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold
        self.model = None

    def fit_target_model(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Trains the target machine learning model that will be audited for privacy leakage.
        """
        if X_train.size == 0 or y_train.size == 0:
            raise ValueError("Security error: Training dataset cannot be empty.")
        
        # Using a model prone to overfitting if unregularized to simulate vulnerability
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)

    def audit_sample_membership(self, sample_features: List[float], true_label: int) -> Tuple[bool, str]:
        """
        Audits a specific data sample to determine if it was likely part of the training dataset
        based on prediction probability confidence.
        """
        if self.model is None:
            raise RuntimeError("Target model must be fitted before running security audits.")

        x = np.array(sample_features, dtype=float)
        if x.ndim == 1:
            x = x.reshape(1, -1)

        # Get prediction probabilities across classes
        probabilities = self.model.predict_proba(x)[0]
        predicted_class = np.argmax(probabilities)
        max_confidence = np.max(probabilities)

        # Security audit logic: If confidence is suspiciously high and correct, 
        # it strongly indicates the sample was memorized during training (Member).
        if predicted_class == true_label and max_confidence >= self.confidence_threshold:
            return True, f"Privacy Leak Alert: High confidence ({max_confidence:.2f}). Sample was likely a TRAINING set MEMBER (Overfitted)."

        return False, f"Privacy Safe: Confidence ({max_confidence:.2f}) is within generalized boundaries. Sample is likely NON-MEMBER."

if __name__ == "__main__":
    # Simulate training data
    np.random.seed(42)
    X_train_data = np.random.normal(loc=10.0, scale=2.0, size=(150, 2))
    y_train_data = (X_train_data[:, 0] > 10.5).astype(int)

    simulator = MembershipInferenceSimulator(confidence_threshold=0.90)
    simulator.fit_target_model(X_train_data, y_train_data)

    # Test samples: One known training member sample vs one unseen sample
    member_sample = [12.5, 9.8]    # Closely matched to training distribution
    non_member_sample = [3.1, 15.6] # Outlier / unseen distribution

    try:
        print("Running Membership Inference Attack (MIA) Security Audit...\n")
        
        for name, sample, label in [("Training Member Sample", member_sample, 1), ("Unseen Non-Member Sample", non_member_sample, 0)]:
            is_member, message = simulator.audit_sample_membership(sample, label)
            print(f"Target: {name}")
            print(f"Audit Result: {message}\n")

    except Exception as error:
        print(f"Execution failed: {error}")