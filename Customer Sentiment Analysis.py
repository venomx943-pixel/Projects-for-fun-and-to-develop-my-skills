import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def secure_sentiment_analysis(review_text, model, vectorizer):
    """
    Securely analyzes and classifies customer review sentiment (Positive or Negative)
    with input validation, memory protection, and sanitization.
    """
    # [Code Security & Vulnerability 1]: Type validation to prevent Type Confusion / Injection
    if not isinstance(review_text, str):
        raise TypeError("Security Error: Input review must be a string exclusively.")
    
    # [Code Security & Vulnerability 2]: Maximum length control to prevent Denial of Service (DoS) attacks
    MAX_LENGTH = 3000
    if len(review_text) > MAX_LENGTH:
        raise ValueError(f"Security Error: Review length exceeds allowed limit ({MAX_LENGTH} characters). Memory exhaustion risk.")

    # [Code Security & Vulnerability 3]: Sanitizing control characters to prevent hidden payload injections
    sanitized_review = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', review_text)

    # [Data Structure & Algorithm]: Bag-of-Words transformation using CountVectorizer O(n) memory
    try:
        vectorized_input = vectorizer.transform([sanitized_review])
    except Exception as e:
        raise RuntimeError(f"Engineering Error during vectorization: {e}")

    # [Data Structure & Algorithm]: Logistic Regression probabilistic classification
    prediction = model.predict(vectorized_input)
    probability_scores = model.predict_proba(vectorized_input)
    
    max_probability = np.max(probability_scores)

    return int(prediction[0]), float(max_probability)

# Dummy model and vectorizer initialization for testing
vectorizer = CountVectorizer()
X_train_dummy = ["I love this product it is amazing", "Terrible experience worst service ever"]
y_train_dummy = [1, 0] # 1: Positive, 0: Negative
X_train_vec = vectorizer.fit_transform(X_train_dummy)

model = LogisticRegression()
model.fit(X_train_vec, y_train_dummy)

# Test input
user_review = "This product is absolute garbage, totally hate it!"

try:
    sentiment, confidence = secure_sentiment_analysis(user_review, model, vectorizer)
    result_label = "Positive Sentiment" if sentiment == 1 else "Negative Sentiment"
    print(f"Secure Sentiment Result: {result_label} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")