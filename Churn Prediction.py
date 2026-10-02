import numpy as np
from sklearn.ensemble import RandomForestClassifier

def secure_churn_prediction(customer_features, model):
    """
    Securely predicts whether a customer will churn or stay 
    with input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(customer_features, (list, np.ndarray)):
        raise TypeError("Security Error: Customer features must be a list or numpy array exclusively.")
    
    # Convert to numpy array with strict float type
    X = np.array(customer_features, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    # Assuming 4 expected features (e.g., Age, Balance, Products count, Active status)
    if X.ndim != 1 or X.shape[0] != 4:
        raise ValueError("Security Error: Invalid feature dimensions or unexpected feature count.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Data Structure & Algorithm]: Reshape to 2D array for scikit-learn compatibility O(1)
    X_reshaped = X.reshape(1, -1)

    # [Data Structure & Algorithm]: Random Forest ensemble prediction (Multiple Decision Trees)
    prediction = model.predict(X_reshaped)
    probabilities = model.predict_proba(X_reshaped)
    max_prob = np.max(probabilities)

    return int(prediction[0]), float(max_prob)

# Dummy model initialization for testing
model = RandomForestClassifier(n_estimators=10, random_state=42)
X_train_dummy = np.array([
    [35.0, 500.0, 2.0, 1.0], 
    [50.0, 100.0, 0.0, 0.0]
])
y_train_dummy = np.array([0, 1]) # 0: Stay, 1: Churn
model.fit(X_train_dummy, y_train_dummy)

# Test customer data (Age, Balance, Products, Active status)
user_data = [42.0, 350.0, 1.0, 1.0]

try:
    churn_status, confidence = secure_churn_prediction(user_data, model)
    result_text = "Likely to Churn" if churn_status == 1 else "Likely to Stay"
    print(f"Secure Churn Prediction Result: {result_text} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")