import numpy as np 
from sklearn. linear_model import LogisticRegression
from typing import List, Tuple 

class FGSMAttackSimulator:

    def __init__(self, epilson: float= 0.1):
        self.epilson = epilson 
        self.model = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:

        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            X, y = np.array(X), np.array(y)

        if X.size == 0 or y.size == 0:
            raise ValueError("Security error: Training data cannot be empty.")

        self.model = LogisticRegression()
        self.model.fit(X, y)

    def generate_adversarial_example(self, x_sample: List[float]) -> np.ndarray:

        if self.model is None:
            raise RuntimeError("Model must be fitted before generating adversarial examples.")

        x = np.array(x_sample, dtype=float)

        if x.ndm == 1:
            x = x.reshape(1, -1)

            weights = self.model.coef_[0]
            if x.shape[1] != weights.shape[0]:
                raise ValueError("Security violation: Feature dimension mismatch between sample and model.")

            gradient_sign = np.sign(weights)

            x_adversarial = x + (self.epilson * gradient_sign)

            print(f"FGSM Attack successfully generated with perturbation epsilon={self.epsilon}")
            return x_adversarial[0]



if __name__ == "__main__":
    np.random.seed(42)
    X_train = np.random.normal(loc=0.0, scale=1.0, size=(100, 2))      
    y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)

    simulator = FGSMAttackSimulator(epilson=0.15)
    simulator.fit(X_train, y_train)

    claen_sample = [0.4, -0.2]

    try:
        print(f"Original Clean Sample: {claen_sample}")
        adv_sample = simulator.generate_adversarial_example(claen_sample)
        print(f"crafted Adversarial Sample: {adv_sample}")

        clean_pred = simulator.model.predict([claen_sample])[0]
        adv_pred = simulator.model.predict([adv_sample])[0]
        print(f"Model Prediction on Clean: {clean_pred} | Prediction on Adversarial: {adv_pred}")

    except Exception as error:
        print(f"Execution failed: {error}")    

