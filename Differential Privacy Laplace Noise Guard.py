import numpy as np
from typing import List, Union

class DifferentialPrivacyGuard:
    """
    Applies Differential Privacy (Laplace Mechanism) to numerical data 
    to prevent reconstruction attacks and protect individual data privacy.
    """
    def __init__(self, epsilon: float = 1.0, sensitivity: float = 1.0):
        self.epsilon = epsilon
        self.sensitivity = sensitivity

    def add_laplace_noise(self, true_value: Union[float, List[float]]) -> Union[float, List[float]]:
        """
        Adds calibrated Laplace noise based on epsilon and sensitivity parameters
        to obscure precise individual data points safely.
    """
        # Security check: Ensure privacy budget epsilon is valid
        if self.epsilon <= 0:
            raise ValueError("Security violation: Epsilon parameter must be greater than zero.")

        # Calculate scale parameter for Laplace distribution (Sensitivity / Epsilon)
        scale = self.sensitivity / self.epsilon

        if isinstance(true_value, (int, float)):
            noise = np.random.laplace(0, scale)
            return float(true_value + noise)
        
        elif isinstance(true_value, list):
            noisy_list = []
            for val in true_value:
                noise = np.random.laplace(0, scale)
                noisy_list.append(float(val + noise))
            return noisy_list
        
        else:
            raise TypeError("Invalid input type: Expected a numerical value or a list of numbers.")

if __name__ == "__main__":
    # Example execution simulating private metric release
    dp_guard = DifferentialPrivacyGuard(epsilon=0.5, sensitivity=1.0)
    
    sensitive_metrics = [85.5, 92.0, 78.4]
    print(f"Original Sensitive Metrics: {sensitive_metrics}")

    try:
        noisy_metrics = dp_guard.add_laplace_noise(sensitive_metrics)
        print(f"Differentially Private (Noised) Metrics: {noisy_metrics}")
    except Exception as error:
        print(f"Execution failed: {error}")