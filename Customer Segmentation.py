import numpy as np
from sklearn.cluster import KMeans

def secure_customer_segmentation(customer_features, model):
    """
    Securely predicts the customer cluster/segment based on behavior metrics
    with rigorous input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(customer_features, (list, np.ndarray)):
        raise TypeError("Security Error: Customer features must be a list or numpy array exclusively.")
    
    # Convert to numpy array with strict float type
    X = np.array(customer_features, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    # Expected features: [Age, Annual Income ($k), Spending Score (1-100), Years as Customer]
    if X.ndim != 1 or X.shape[0] != 4:
        raise ValueError("Security Error: Invalid feature dimensions. Exactly 4 features are required.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Code Security & Vulnerability 4]: Behavioral Range check to prevent absurd or negative numbers
    if np.any(X < 0.0) or X[0] > 120.0 or X[2] > 100.0:
        raise ValueError("Security Error: Feature values out of realistic behavioral range.")

    # [Data Structure & Algorithm]: Reshape to 2D array for scikit-learn compatibility O(1)
    X_reshaped = X.reshape(1, -1)

    # [Data Structure & Algorithm]: K-Means centroid assignment algorithm O(k * d)
    cluster_label = model.predict(X_reshaped)

    return int(cluster_label[0])

# Dummy model initialization for testing
model = KMeans(n_clusters=3, random_state=42, n_init=10)
X_train_dummy = np.array([
    [25.0, 30.0, 85.0, 1.0], 
    [45.0, 80.0, 50.0, 5.0],
    [60.0, 120.0, 20.0, 10.0]
])
model.fit(X_train_dummy)

# Test customer data [Age, Annual Income, Spending Score, Years as Customer]
user_customer = [30.0, 45.0, 75.0, 2.0]

try:
    cluster_id = secure_customer_segmentation(user_customer, model)
    print(f"Secure Customer Segmentation Result: Assigned to Cluster ID {cluster_id}")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")