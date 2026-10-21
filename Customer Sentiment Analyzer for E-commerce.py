import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train_and_analyze_sentiment(
    train_texts: list, train_labels: list, target_texts: list
) -> np.ndarray:
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression()),
    ])
    model.fit(train_texts, train_labels)
    predictions = model.predict(target_texts)
    return predictions


if __name__ == "__main__":
    training_corpus = [
        "This product is absolute garbage and broke immediately",
        "Amazing quality and fast shipping highly recommended",
        "Terrible customer service and poor material",
        "Exceeded my expectations, works perfectly",
    ]
    training_labels = ["NEGATIVE", "POSITIVE", "NEGATIVE", "POSITIVE"]
    incoming_reviews = [
        "Awful experience, do not buy this",
        "Very satisfied with the performance",
    ]
    results = train_and_analyze_sentiment(
        training_corpus, training_labels, incoming_reviews
    )
    print("Customer sentiment classification results:", results)