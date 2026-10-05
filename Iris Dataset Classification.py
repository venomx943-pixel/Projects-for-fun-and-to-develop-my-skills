import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def secure_iris_classification(flower_features, model):
    """
    Securely classifies Iris flower species (setosa, versicolor, virginica)
    with rigorous input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(flower_features, (list, np.ndarray)):
        raise TypeError("Security Error: Flower features must be a list or numpy array exclusively.")
    
   
    X = np.array(flower_features, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    # Iris dataset expects exactly 4 features (sepal length, sepal width, petal length, petal width)
    if X.ndim != 1 or X.shape[0] != 4:
        raise ValueError("Security Error: Invalid feature dimensions. Exactly 4 features are required.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Code Security & Vulnerability 4]: Range/Bounds check to prevent anomalous or physical range abuse
    if np.any(X < 0.0) or np.any(X > 20.0):
        raise ValueError("Security Error: Feature values out of realistic physical biological range (0 to 20).")

    X_reshaped = X.reshape(1, -1)

  
    prediction = model.predict(X_reshaped)
    probabilities = model.predict_proba(X_reshaped)
    max_prob = np.max(probabilities)

    # Map prediction index to Iris class names
    class_names = ["Setosa", "Versicolor", "Virginica"]
    predicted_class_name = class_names[int(prediction[0])]

    return predicted_class_name, float(max_prob)

# Dummy model initialization for testing
model = KNeighborsClassifier(n_neighbors=3)
X_train_dummy = np.array([
    [5.1, 3.5, 1.4, 0.2], 
    [7.0, 3.2, 4.7, 1.4],
    [6.3, 3.3, 6.0, 2.5]
])
y_train_dummy = np.array([0, 1, 2]) 
model.fit(X_train_dummy, y_train_dummy)

# Test flower input features 
user_flower = [5.8, 2.7, 5.1, 1.9]

try:
    species, confidence = secure_iris_classification(user_flower, model)
    print(f"Secure Iris Classification Result: {species} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")