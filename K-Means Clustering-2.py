import numpy as np 
from sklearn.cluster import KMeans

def secure_customer_segmentation(customer_features, model):

    if not isinstance(customer_features, (list, np.ndarray)):
        raise TypeError("Security Error: Customer features must be a list or numpy array exclusively.")

    X = np.array(customer_features, dtype=np.float64)

    if X.ndim != 1 or X.shape[0] != 4:
        raise ValueError("Security Error: Invalid feature  dimensions. Exactly 4 features are required.")

    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data posioning attempt.")

    if np.any(X < 0.0) or X[0] > 120.0 or X[2] > 100.0:
        raise ValueError("Security Error: Feature values out of realistic behavioral range.")

    X_reshaped = X.reshape(1, -1)

    cluster_label = model.predict(X_reshaped)

    return int(cluster_label[0])

model = KMeans(n_clusters=3, random_state=42, n_init=10)
X_train_dummy = np.array([
        [1.0 ,85.0 ,30.0 ,25.0],
        [5.0 ,50.0 ,80.0 ,45.0],
        [10.0 ,20.0 ,120.0 ,60.0]
    ])

model.fit(X_train_dummy)

user_customer = [30.0, 45.0, 75.0, 2.0]

try:
    cluster_id = secure_customer_segmentation(user_customer, model)
    print(f"Secure Customer Segmentation Result: Assigned t Clustor ID {cluster_id}")

except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")