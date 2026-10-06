import numpy as np

class SimpleRegressionStump:
    def __init__(self):
        self.feature_idx = None
        self.threshold = None
        self.left_val = None
        self.right_val = None

    def fit(self, X, residuals):
        n_samples, n_features = X.shape
        best_variance = float('inf')
        
        for feat_idx in range(n_features):
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)
            for threshold in thresholds:
                left_mask = X_column <= threshold
                if np.sum(left_mask) == 0 or np.sum(left_mask) == n_samples:
                    continue
                
                # Split residuals and find the mean for each leaf node
                left_residuals = residuals[left_mask]
                right_residuals = residuals[~left_mask]
                
                # Variance as splitting criterion for regression
                variance = np.var(left_residuals) * len(left_residuals) + np.var(right_residuals) * len(right_residuals)
                
                if variance < best_variance:
                    best_variance = variance
                    self.feature_idx = feat_idx
                    self.threshold = threshold
                    self.left_val = np.mean(left_residuals)
                    self.right_val = np.mean(right_residuals)

    def predict(self, X):
        predictions = []
        for x in X:
            if x[self.feature_idx] <= self.threshold:
                predictions.append(self.left_val)
            else:
                predictions.append(self.right_val)
        return np.array(predictions)

class CustomGradientBoostingRegressor:
    def __init__(self, n_estimators=5, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.trees = []
        self.initial_prediction = None

    def fit(self, X, y):
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        # Step 1: Initialize baseline prediction as the mean of target values
        self.initial_prediction = np.mean(y)
        current_predictions = np.full(y.shape, self.initial_prediction)

        for i in range(self.n_estimators):
            # Step 2: Calculate residuals (errors) of the current model
            residuals = y - current_predictions

            # Step 3: Train a regression stump on the residuals
            tree = SimpleRegressionStump()
            tree.fit(X, residuals)

            # Step 4: Update predictions using the new tree scaled by learning rate
            update = tree.predict(X)
            current_predictions += self.learning_rate * update

            self.trees.append(tree)

        print(f"[INFO] Gradient Boosting trained successfully with {self.n_estimators} sequential trees.")

    def predict(self, X):
        X = np.array(X, dtype=float)
        # Start with the initial baseline prediction
        predictions = np.full(X.shape[0], self.initial_prediction)

        # Add contributions from all sequential trees scaled by learning rate
        for tree in self.trees:
            predictions += self.learning_rate * tree.predict(X)

        return predictions

# --- Testing the Engine ---
if __name__ == "__main__":
    # Mock dataset for Annual Sales Prediction (Features: [Advertising_Budget, Store_Size])
    X_train_mock = [
        [10.0, 100.0],
        [20.0, 150.0],
        [30.0, 200.0],
        [40.0, 250.0],
        [50.0, 300.0]
    ]
    y_train_mock = [15.0, 28.0, 42.0, 55.0, 70.0] # Annual Sales in thousands

    # Initialize and fit custom Gradient Boosting engine
    gb_engine = CustomGradientBoostingRegressor(n_estimators=3, learning_rate=0.1)
    gb_engine.fit(X_train_mock, y_train_mock)

    # Test samples to predict annual sales
    X_test_mock = [
        [25.0, 175.0],
        [45.0, 280.0]
    ]
    preds = gb_engine.predict(X_test_mock)

    print(f"[RESULT] Predicted Annual Sales: {preds}")