import numpy as np

class CustomPCA:
    def __init__(self, n_components):
        # Initialize PCA with the target number of dimensions to keep
        self.n_components = n_components
        self.mean = None
        self.components = None

    def fit_transform(self, X):
        # Convert input to numpy array
        X = np.array(X, dtype=float)
        
        
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

       
        n_samples = X.shape[0]
        covariance_matrix = np.dot(X_centered.T, X_centered) / (n_samples - 1)

       
        eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

      
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, sorted_indices]

       
        self.components = eigenvectors[:, :self.n_components]

        
        X_projected = np.dot(X_centered, self.components)
        
        print(f"[INFO] PCA transformed data shape from {X.shape} to {X_projected.shape}.")
        return X_projected

#Testing the Engine
if __name__ == "__main__":
    # Mock high-dimensional dataset 
    X_train_mock = [
        [2.5, 2.4, 0.5, 1.2],
        [0.5, 0.7, 0.1, 0.4],
        [2.2, 2.9, 0.4, 1.0],
        [1.9, 2.2, 0.3, 0.9],
        [3.1, 3.0, 0.6, 1.5]
    ]

    # Initialize custom PCA to reduce from 4 dimensions down to 2 dimensions
    pca_engine = CustomPCA(n_components=2)
    X_reduced = pca_engine.fit_transform(X_train_mock)

    print(f"[RESULT] Reduced Data Matrix:\n{X_reduced}")