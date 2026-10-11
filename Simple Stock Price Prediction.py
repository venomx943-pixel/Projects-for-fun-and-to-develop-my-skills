import numpy as np
from sklearn.linear_model import LinearRegression

def secure_stock_prediction(days_input, model):
    """
    Securely predicts future stock prices based on historical day indices
    with rigorous input validation, shape checking, and safety barriers.
    """
    # [Code Security & Vulnerability 1]: Type validation / Injection prevention
    if not isinstance(days_input, (list, np.ndarray, int, float)):
        raise TypeError("Security Error: Days input must be numeric or a list/array exclusively.")
    
    # Convert to numpy array with strict float type
    if isinstance(days_input, (int, float)):
        X = np.array([days_input], dtype=np.float64)
    else:
        X = np.array(days_input, dtype=np.float64)

    # [Code Security & Vulnerability 2]: Dimension check (prevent dimension mismatch / out-of-bounds)
    if X.ndim != 1 or X.shape[0] == 0:
        raise ValueError("Security Error: Invalid feature dimensions or empty input.")

    # [Code Security & Vulnerability 3]: NaN / Infinity Injection prevention (Data Poisoning)
    if np.isnan(X).any() or np.isinf(X).any():
        raise ValueError("Security Error: Detected NaN or Infinite values. Potential data poisoning attempt.")

    # [Code Security & Vulnerability 4]: Range check to prevent negative or absurd day values
    if np.any(X < 0.0) or np.any(X > 10000.0):
        raise ValueError("Security Error: Day values out of realistic operational boundaries (0 to 10000).")

    # [Data Structure & Algorithm]: Reshape to 2D array for scikit-learn compatibility O(1)
    X_reshaped = X.reshape(-1, 1)

    # [Data Structure & Algorithm]: Linear regression trend prediction O(n)
    predictions = model.predict(X_reshaped)

    return predictions.tolist() if len(predictions) > 1 else float(predictions[0])

# Dummy model initialization for testing
model = LinearRegression()
X_train_dummy = np.array([[1], [2], [3], [4], [5]], dtype=np.float64)
y_train_dummy = np.array([100.0, 102.5, 105.0, 107.5, 110.0], dtype=np.float64)
model.fit(X_train_dummy, y_train_dummy)

# Test future day input
user_day = 10.0

try:
    predicted_price = secure_stock_prediction(user_day, model)
    print(f"Secure Stock Prediction for Day {user_day}: ${predicted_price:.2f}")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")