import numpy as np
from typing import Tuple, List

class DataPoisoningSanitizationGuard:
    """
    Filters and cleans training datasets using Interquartile Range (IQR) statistics
    to detect and remove poisoned, manipulated, or malicious outlier samples.
    """
    def __init__(self, iqr_multiplier: float = 1.5):
        self.iqr_multiplier = iqr_multiplier

    def sanitize_dataset(self, X_data: List[List[float]], y_labels: List[int]) -> Tuple[np.ndarray, np.ndarray, int]:
        """
        Scans feature distributions and filters out poisoned outliers.
        """
        X = np.array(X_data, dtype=float)
        y = np.array(y_labels, dtype=int)

        if X.size == 0 or y.size == 0:
            raise ValueError("Security error: Input dataset cannot be empty.")

        if X.shape[0] != y.shape[0]:
            raise ValueError("Security violation: Mismatch between features count and labels count.")

        # Compute Quartiles (Q1 and Q3) for each feature column to detect injection attacks
        q1 = np.percentile(X, 25, axis=0)
        q3 = np.percentile(X, 75, axis=0)
        iqr = q3 - q1

        # Define safe lower and upper bounds
        lower_bound = q1 - (self.iqr_multiplier * iqr)
        upper_bound = q3 + (self.iqr_multiplier * iqr)

        # Create a boolean mask identifying clean samples within acceptable boundaries
        mask = np.all((X >= lower_bound) & (X <= upper_bound), axis=1)

        cleaned_X = X[mask]
        cleaned_y = y[mask]
        dropped_count = np.sum(~mask)

        print(f"Data Poisoning Guard Audit: Removed {dropped_count} malicious/outlier samples from training set.")
        return cleaned_X, cleaned_y, dropped_count

if __name__ == "__main__":
    # Simulate a clean training dataset combined with intentional poisoned outliers
    clean_features = [[1.2, 2.1], [1.5, 2.3], [1.1, 1.9], [1.4, 2.2], [1.3, 2.0]]
    clean_labels = [0, 0, 0, 0, 0]

    # Poisoned injection samples with extreme malicious values
    poisoned_features = clean_features + [[50.5, -45.0], [-100.2, 80.1]]
    poisoned_labels = clean_labels + [1, 1]

    guard = DataPoisoningSanitizationGuard(iqr_multiplier=1.5)

    try:
        print("Running Data Poisoning Sanitization Guard...\n")
        safe_X, safe_y, dropped = guard.sanitize_dataset(poisoned_features, poisoned_labels)
        
        print(f"Original Dataset Size: {len(poisoned_features)}")
        print(f"Sanitized Safe Dataset Size: {len(safe_X)}")
        print(f"Sanitized Features Result:\n{safe_X}")

    except Exception as error:
        print(f"Execution failed: {error}")