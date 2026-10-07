import numpy as np
from xgboost import XGBClassifier

def secure_fraud_detection(transaction_features, model):
    """
    Securely detects whether a credit card transaction is fraudulent or legitimate
    with rigorous input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(transaction_features, (list, np.ndarray)):
        raise TypeError("Security Error: Transaction features must be a list or numpy array exclusively.")
    
    # Convert to numpy array with strict float type
    X = np.array(transaction_features, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    # Expected features: [Transaction Amount, Distance from Home, Hour of Day, Merchant Risk Score, Previous Declines]
    if X.ndim != 1 or X.shape[0] != 5:
        raise ValueError("Security Error: Invalid feature dimensions. Exactly 5 features are required.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Code Security & Vulnerability 4]: Range/Bounds check to prevent negative amounts or impossible hours/risks
    if X[0] < 0.0 or X[2] < 0.0 or X[2] > 23.0 or X[3] < 0.0 or X[3] > 10.0:
        raise ValueError("Security Error: Feature values out of realistic transaction boundaries.")

    # [Data Structure & Algorithm]: Reshape to 2D array for xgboost compatibility O(1)
    X_reshaped = X.reshape(1, -1)

    # [Data Structure & Algorithm]: XGBoost gradient boosting classification
    probabilities = model.predict_proba(X_reshaped)
    max_prob = np.max(probabilities)
    prediction = model.predict(X_reshaped)

    return int(prediction[0]), float(max_prob)

# Dummy model initialization for testing
model = XGBClassifier(n_estimators=10, random_state=42, eval_metric='logloss')
X_train_dummy = np.array([
    [45.50, 2.1, 14.0, 1.0, 0.0], 
    [5000.00, 1200.5, 3.0, 9.5, 4.0]
])
y_train_dummy = np.array([0, 1]) # 0: Legitimate, 1: Fraudulent
model.fit(X_train_dummy, y_train_dummy)

# Test transaction data [Amount, Distance, Hour, Merchant Risk, Previous Declines]
user_transaction = [120.0, 5.0, 21.0, 2.0, 0.0]

try:
    fraud_status, confidence = secure_fraud_detection(user_transaction, model)
    result_text = "Fraudulent Transaction Detected!" if fraud_status == 1 else "Legitimate Transaction"
    print(f"Secure Fraud Detection Result: {result_text} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")