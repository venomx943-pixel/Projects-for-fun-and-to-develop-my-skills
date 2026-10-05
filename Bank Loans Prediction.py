import numpy as np
from sklearn.tree import DecisionTreeClassifier

def secure_loan_prediction(applicant_features, model):
    """
    Securely predicts whether a bank loan should be approved or denied
    with rigorous input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(applicant_features, (list, np.ndarray)):
        raise TypeError("Security Error: Applicant features must be a list or numpy array exclusively.")
    
    # Convert to numpy array with strict float type
    X = np.array(applicant_features, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    # Expected features: [Income, Credit Score, Loan Amount, Employment Years]
    if X.ndim != 1 or X.shape[0] != 4:
        raise ValueError("Security Error: Invalid feature dimensions. Exactly 4 features are required.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Code Security & Vulnerability 4]: Financial Range/Bounds check to prevent negative or absurd numbers
    if np.any(X < 0.0):
        raise ValueError("Security Error: Feature values cannot contain negative numbers for financial metrics.")

    # [Data Structure & Algorithm]: Reshape to 2D array for scikit-learn compatibility O(1)
    X_reshaped = X.reshape(1, -1)

    # [Data Structure & Algorithm]: Decision Tree classification based on conditional splits
    prediction = model.predict(X_reshaped)
    probabilities = model.predict_proba(X_reshaped)
    max_prob = np.max(probabilities)

    return int(prediction[0]), float(max_prob)

# Dummy model initialization for testing
model = DecisionTreeClassifier(random_state=42)
X_train_dummy = np.array([
    [50000.0, 700.0, 15000.0, 5.0], 
    [20000.0, 550.0, 30000.0, 1.0]
])
y_train_dummy = np.array([1, 0]) # 1: Approved, 0: Denied
model.fit(X_train_dummy, y_train_dummy)

# Test applicant data [Income, Credit Score, Loan Amount, Employment Years]
user_applicant = [65000.0, 720.0, 20000.0, 4.0]

try:
    loan_status, confidence = secure_loan_prediction(user_applicant, model)
    result_text = "Loan Approved" if loan_status == 1 else "Loan Denied"
    print(f"Secure Loan Prediction Result: {result_text} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")