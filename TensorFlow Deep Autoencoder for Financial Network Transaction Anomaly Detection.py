import numpy as np
import tensorflow as tf
from keras import layers, models

class FinancialAutoencoder(tf.keras.Model):
    def __init__(self, input_dim: int):
        super(FinancialAutoencoder, self).__init__()
        # Encoder: Compressing input dimensions to a latent representation
        self.encoder = models.Sequential([
            layers.Dense(16, activation='relu', input_shape=(input_dim,)),
            layers.Dense(8, activation='relu')
        ])
        # Decoder: Reconstructing original dimensions from latent space
        self.decoder = models.Sequential([
            layers.Dense(16, activation='relu'),
            layers.Dense(input_dim, activation='sigmoid')
        ])

    def call(self, inputs):
        encoded = self.encoder(inputs)
        decoded = self.decoder(encoded)
        return decoded

if __name__ == "__main__":
    # 30 Normal Financial Transaction Training Samples (4 Features: Transaction Amount, Frequency Rate, Location Risk Score, Device Age)
    # Autoencoders train primarily on normal/benign data to learn baseline reconstruction patterns.
    X_train = np.array([
        [0.1, 0.15, 0.05, 0.2], [0.12, 0.1, 0.02, 0.15], [0.08, 0.12, 0.04, 0.25],
        [0.15, 0.08, 0.01, 0.1], [0.11, 0.14, 0.06, 0.18], [0.09, 0.11, 0.03, 0.22],
        [0.13, 0.13, 0.05, 0.16], [0.07, 0.09, 0.02, 0.3],  [0.14, 0.12, 0.04, 0.12],
        [0.1, 0.16, 0.03, 0.19], [0.12, 0.11, 0.05, 0.21], [0.09, 0.13, 0.02, 0.17],
        [0.15, 0.1, 0.04, 0.14], [0.08, 0.14, 0.01, 0.23], [0.11, 0.09, 0.06, 0.2],
        [0.13, 0.15, 0.02, 0.15], [0.1, 0.12, 0.04, 0.18], [0.14, 0.08, 0.03, 0.13],
        [0.07, 0.13, 0.05, 0.27], [0.12, 0.14, 0.01, 0.16], [0.09, 0.1, 0.04, 0.22],
        [0.15, 0.11, 0.03, 0.11], [0.11, 0.15, 0.02, 0.19], [0.08, 0.12, 0.05, 0.24],
        [0.13, 0.09, 0.01, 0.17], [0.1, 0.13, 0.04, 0.2],  [0.14, 0.14, 0.03, 0.14],
        [0.07, 0.1, 0.02, 0.28],  [0.12, 0.12, 0.06, 0.18], [0.09, 0.15, 0.01, 0.21]
    ], dtype=np.float32)

    model = FinancialAutoencoder(input_dim=4)
    model.compile(optimizer='adam', loss='mse')

    # Training Autoencoder on Normal Data (Unsupervised baseline learning)
    model.fit(X_train, X_train, epochs=50, batch_size=10, verbose=0)

    # 20 Test Samples mixing Normal Transactions and Anomalous/Fraudulent Transactions
    X_test = np.array([
        [0.11, 0.13, 0.04, 0.18], [0.95, 0.9, 0.92, 0.02],  # Anomalous Fraud
        [0.09, 0.11, 0.02, 0.21], [0.88, 0.94, 0.89, 0.05],  # Anomalous Fraud
        [0.13, 0.12, 0.03, 0.15], [0.92, 0.91, 0.95, 0.01],  # Anomalous Fraud
        [0.1, 0.14, 0.05, 0.19],  [0.9, 0.95, 0.91, 0.03],   # Anomalous Fraud
        [0.08, 0.1, 0.01, 0.23],  [0.94, 0.89, 0.93, 0.04],  # Anomalous Fraud
        [0.12, 0.15, 0.04, 0.16], [0.91, 0.93, 0.9, 0.02],   # Anomalous Fraud
        [0.14, 0.09, 0.02, 0.14], [0.93, 0.92, 0.94, 0.01],  # Anomalous Fraud
        [0.09, 0.13, 0.03, 0.2],  [0.89, 0.96, 0.92, 0.05],  # Anomalous Fraud
        [0.11, 0.11, 0.05, 0.17], [0.95, 0.9, 0.91, 0.03],   # Anomalous Fraud
        [0.13, 0.14, 0.01, 0.15], [0.92, 0.94, 0.93, 0.02]   # Anomalous Fraud
    ], dtype=np.float32)

    # Reconstruct test data through the autoencoder
    reconstructions = model.predict(X_test, verbose=0)
    # Calculate Mean Squared Error (MSE) per sample as anomaly score
    mse_errors = np.mean(np.power(X_test - reconstructions, 2), axis=1)
    # Define an empirical anomaly threshold
    threshold = 0.05

    print("--- TensorFlow Financial Transaction Anomaly Detection Report (20 Test Samples) ---")
    for i, error in enumerate(mse_errors, 1):
        status = "FRAUDULENT ANOMALY " if error > threshold else "NORMAL TRANSACTION "
        print(f"[Test Transaction {i}] Reconstruction Error: {error:.5f} -> Classification: {status}")