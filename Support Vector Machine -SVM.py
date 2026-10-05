import numpy as np

class CustomLinearSVM:
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        # Initialize hyperparameters: learning rate, regularization parameter, and iterations
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        # Fix: Convert y explicitly to a numpy array to support numerical operations and comparisons
        y = np.array(y)
        
        # Convert labels from {0, 1} to {-1, 1} for mathematical optimization in SVM
        y_transformed = np.where(y <= 0, -1, 1)
        
        n_samples, n_features = X.shape

        # Step 1: Initialize weights and bias to zeros
        self.w = np.zeros(n_features)
        self.b = 0.0

        # Step 2: Gradient Descent optimization loop
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # Condition for margin violation: y_i * (w * x_i - b) >= 1
                condition = y_transformed[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                
                if condition:
                    dW = 2 * self.lambda_param * self.w
                    db = 0
                else:
                    dW = 2 * self.lambda_param * self.w - np.dot(x_i, y_transformed[idx])
                    db = y_transformed[idx]

                # Step 3: Update model parameters using gradient descent step
                self.w -= self.lr * dW
                self.b -= self.lr * db

        print(f"[INFO] SVM training completed successfully over {self.n_iters} iterations.")

        
    def predict(self, X):
        X = np.array(X, dtype=float)
        # Compute linear output: w * x - b
        approx = np.dot(X, self.w) - self.b
        # Return sign of the output mapped back to {0, 1}
        return np.sign(approx)

# --- Testing the Engine ---
if __name__ == "__main__":
    # Mock training dataset (2D features and binary labels)
    X_train_mock = [
        [1.0, 2.0],
        [1.5, 1.8],
        [8.0, 8.5],
        [8.5, 9.0]
    ]
    y_train_mock = [0, 0, 1, 1] # Classes mapped to 0 and 1

    # Initialize and fit custom SVM engine
    svm_engine = CustomLinearSVM(learning_rate=0.001, lambda_param=0.01, n_iters=1000)
    svm_engine.fit(X_train_mock, y_train_mock)

    # Test samples to classify
    X_test_mock = [
        [1.2, 1.9],
        [8.2, 8.8]
    ]
    preds = svm_engine.predict(X_test_mock)
    # Map predictions back to 0/1 for readable output
    preds_mapped = np.where(preds <= 0, 0, 1)

    print(f"[RESULT] Predicted classes for test samples: {preds_mapped}")