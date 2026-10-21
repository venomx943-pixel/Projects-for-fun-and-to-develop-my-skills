import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def extract_string_features(texts: list) -> np.ndarray:
    features = []
    for text in texts:
        length = len(text)
        special_chars_count = sum(1 for char in text if char in ";|&<>`$")
        features.append([length, special_chars_count])
    return np.array(features)


def train_and_detect_command_injection(
    train_texts: list, train_labels: list, target_texts: list
) -> np.ndarray:
    X_train = extract_string_features(train_texts)
    X_target = extract_string_features(target_texts)
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, train_labels)
    predictions = model.predict(X_target)
    return predictions


if __name__ == "__main__":
    training_corpus = [
        "john_doe",
        "user_profile_update",
        "cat /etc/passwd; ls -la",
        "ping -c 1 127.0.0.1 & id",
        "standard_search_query",
    ]
    training_labels = [0, 0, 1, 1, 0]
    incoming_inputs = [
        "normal_username_input",
        "rm -rf / && wget malicious_payload.sh",
    ]
    results = train_and_detect_command_injection(
        training_corpus, training_labels, incoming_inputs
    )
    print("Command injection classification results (1=Attack, 0=Safe):", results)