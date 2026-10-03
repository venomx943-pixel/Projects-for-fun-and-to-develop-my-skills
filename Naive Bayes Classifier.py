import numpy as np
from collections import defaultdict

class CustomNaiveBayes:
    def __init__(self):
        self.class_priors = {}
        self.feature_probabilities = {}
        self.classes = None

    def fit(self, X_text, y_labels):
        # Convert labels to numpy array
        y_labels = np.array(y_labels)
        self.classes = np.unique(y_labels)
        n_samples = len(y_labels)

        # Step 1: Tokenize text into vocabulary list
        vocabulary = self._build_vocabulary(X_text)
        n_vocab = len(vocabulary)

        # Step 2: Calculate prior probabilities for each class P(C)
        for c in self.classes:
            class_count = np.sum(y_labels == c)
            self.class_priors[c] = class_count / n_samples

            # Step 3: Calculate feature likelihoods with Laplace Smoothing (alpha = 1)
            c_texts = [X_text[i] for i in range(n_samples) if y_labels[i] == c]
            word_counts = defaultdict(int)
            total_words_in_class = 0

            for text in c_texts:
                words = text.lower().split()
                for word in words:
                    word_counts[word] += 1
                    total_words_in_class += 1

            # Store smoothed probabilities for each word given the class P(Word | C)
            self.feature_probabilities[c] = {}
            for word in vocabulary:
                count = word_counts[word]
                # Laplace smoothing prevents zero-probability issues for unseen words
                self.feature_probabilities[c][word] = (count + 1) / (total_words_in_class + n_vocab)

    def predict(self, X_text):
        predictions = []
        for text in X_text:
            words = text.lower().split()
            class_scores = {}

            for c in self.classes:
                # Start with log prior to prevent numerical underflow
                score = np.log(self.class_priors[c])

                for word in words:
                    if word in self.feature_probabilities[c]:
                        score += np.log(self.feature_probabilities[c][word])
                    # Ignore unseen words or handle with smoothing base probability

                class_scores[c] = score

            # Choose the class with the highest posterior probability score
            best_class = max(class_scores, key=class_scores.get)
            predictions.append(best_class)

        return np.array(predictions)

    def _build_vocabulary(self, X_text):
        vocab = set()
        for text in X_text:
            for word in text.lower().split():
                vocab.add(word)
        return list(vocab)

# --- Testing the Engine ---
if __name__ == "__main__":
    # Mock training dataset (Texts and labels: 1 for Positive, 0 for Negative)
    X_train_mock = [
        "amazing product love it",
        "great service excellent experience",
        "terrible quality hate it",
        "awful waste of money bad"
    ]
    y_train_mock = [1, 1, 0, 0]

    # Initialize and fit custom Naive Bayes engine
    nb_engine = CustomNaiveBayes()
    nb_engine.fit(X_train_mock, y_train_mock)

    # Test samples to classify
    X_test_mock = [
        "amazing service",
        "awful quality"
    ]
    preds = nb_engine.predict(X_test_mock)

    print(f"[RESULT] Predicted sentiment classes (1: Positive, 0: Negative): {preds}")