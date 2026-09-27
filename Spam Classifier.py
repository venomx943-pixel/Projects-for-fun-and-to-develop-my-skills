import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

def secure_spam_classifier_predict(email_text, model, vectorizer):
    """
    Secure function to analyze and classify email messages (spam or ham)
    with input validation and memory protection.
    """
    # [Code Security & Vulnerability 1]: Type confusion / Injection attack prevention
    if not isinstance(email_text, str):
        raise TypeError("Security Error: Input text must be a string exclusively.")
    
    # [Code Security & Vulnerability 2]: Maximum length limit to prevent Denial of Service (DoS) via memory exhaustion
    MAX_LENGTH = 5000
    if len(email_text) > MAX_LENGTH:
        raise ValueError(f"Security Error: Text size exceeds allowed limit ({MAX_LENGTH} characters), memory exhaustion attack risk.")

    # [Code Security & Vulnerability 3]: Sanitizing text from malicious or invisible control characters
    sanitized_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', email_text)

    # [Data Structure & Algorithm]: Converting text into a Sparse Matrix using TF-IDF for numerical representation
    try:
        vectorized_input = vectorizer.transform([sanitized_text])
    except Exception as e:
        raise RuntimeError(f"Engineering Error during mathematical text conversion: {e}")

    # [Data Structure & Algorithm]: Applying Naive Bayes algorithm for probabilistic classification O(n)
    prediction = model.predict(vectorized_input)
    confidence_scores = model.predict_proba(vectorized_input)
    
    # Extract highest confidence score for the decision
    max_confidence = np.max(confidence_scores)

    return int(prediction[0]), float(max_confidence)

# Dummy initialization of model and vectorizer for testing
vectorizer = TfidfVectorizer(max_features=1000)
X_train_dummy = ["win a free prize now click here", "hello meeting scheduled for tomorrow morning"]
y_train_dummy = [1, 0] # 1: Spam, 0: Ham
X_train_vec = vectorizer.fit_transform(X_train_dummy)

model = MultinomialNB()
model.fit(X_train_vec, y_train_dummy)

# Try secure text input
user_email = "Win a free iPhone now by clicking this suspicious link!!"

try:
    is_spam, confidence = secure_spam_classifier_predict(user_email, model, vectorizer)
    result_text = "Spam Message" if is_spam == 1 else "Ham (Safe) Message"
    print(f"Secure Classification Result: {result_text} (Confidence: {confidence:.2f})")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")