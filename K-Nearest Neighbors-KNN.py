import numpy as np

class CustomKNN:
    def __init__(self, k_neighbors=3):
        # Initialize the model with hyperparameter k
        self.k = k_neighbors
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        # Store training data (Lazy learning approach: no heavy computation during training)
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)
        print(f"[INFO] Model fitted successfully with {len(self.X_train)} training samples.")

    def predict(self, X_test):
        # Predict labels for a batch of test samples
        X_test = np.array(X_test)
        predictions = [self._predict_single(x) for x in X_test]
        return np.array(predictions)

    def _predict_single(self, x):
        # Compute Euclidean distance between x and all training examples simultaneously
        # Formula: sqrt(sum((x1 - x2)^2))
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

        # Sort distances and get indices of the top k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]

        # Extract the labels of the k-nearest neighbors
        k_nearest_labels = self.y_train[k_indices]

        # Perform majority vote to determine the final class label
        most_common_label = np.bincount(k_nearest_labels).argmax()
        
        return most_common_label

# Testing the Engine
if __name__ == "__main__":
    # Mock training dataset 
    X_train_mock = [[1.0, 2.0], [1.5, 1.8], [8.0, 8.5], [8.5, 9.0]]
    y_train_mock = [0, 0, 1, 1] # 0 and 1 represent two different digit classes

    # Initialize and fit our custom KNN engine
    knn_engine = CustomKNN(k_neighbors=3)
    knn_engine.fit(X_train_mock, y_train_mock)

    # Test sample to classify
    X_test_mock = [[1.2, 1.9], [8.2, 8.8]]
    preds = knn_engine.predict(X_test_mock)
    
    print(f"[RESULT] Predicted classes for test samples: {preds}")