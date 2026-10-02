import numpy as np

class CustomKMeans:
    def __init__(self, n_clusters=3, max_iters=100, tol=1e-4):
        # Initialize hyperparameters: number of clusters, max iterations, and convergence tolerance
        self.k = n_clusters
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None

    def fit_predict(self, X):
        X = np.array(X, dtype=float)
        n_samples, n_features = X.shape

        # Step 1: Randomly initialize centroids by picking K random points from the dataset
        random_indices = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[random_indices]

        for iteration in range(self.max_iters):
            # Step 2: Assign each data point to the closest centroid
            clusters = self._create_clusters(X)

            # Step 3: Compute new centroids as the mean of the points in each cluster
            new_centroids = np.array([X[cluster].mean(axis=0) if len(cluster) > 0 else self.centroids[i] 
                                      for i, cluster in enumerate(clusters)])

            # Step 4: Check for convergence (if centroids stop changing significantly)
            if np.max(np.abs(new_centroids - self.centroids)) < self.tol:
                print(f"[INFO] K-Means converged successfully at iteration {iteration}.")
                break

            self.centroids = new_centroids

        # Return final cluster labels for each data point
        return self._get_labels(X)

    def _create_clusters(self, X):
        # Assign all points to the nearest centroid using Euclidean distance
        clusters = [[] for _ in range(self.k)]
        for idx, x in enumerate(X):
            # Calculate distance to all centroids simultaneously
            distances = np.sqrt(np.sum((self.centroids - x) ** 2, axis=1))
            closest_centroid = np.argmin(distances)
            clusters[closest_centroid].append(idx)
        return clusters

    def _get_labels(self, X):
        # Generate a label array mapping each sample to its final cluster index
        labels = np.empty(X.shape[0])
        for cluster_idx, cluster in enumerate(self._create_clusters(X)):
            for sample_idx in cluster:
                labels[sample_idx] = cluster_idx
        return labels

# --- Testing the Engine ---
if __name__ == "__main__":
    # Mock dataset representing customer features (e.g., [income, spending_score])
    X_train_mock = [
        [2.0, 10.0], [1.5, 9.5], [1.8, 10.2],  # Group A
        [8.0, 2.0], [8.5, 1.5], [7.9, 2.2],   # Group B
        [5.0, 5.0], [5.2, 4.8], [4.9, 5.1]    # Group C
    ]

    # Initialize and run custom K-Means engine to group data into 3 clusters
    kmeans_engine = CustomKMeans(n_clusters=3)
    labels = kmeans_engine.fit_predict(X_train_mock)

    print(f"[RESULT] Cluster assignments for samples: {labels}")
    print(f"[RESULT] Final Centroids:\n{kmeans_engine.centroids}")