import numpy as np
import tensorflow as tf
import keras 
from keras import layers, models

class MalwareBehaviorClassifier(tf.keras.Model):
    def __init__(self, input_dim: int):
        super(MalwareBehaviorClassifier, self).__init__()
        self.dense1 = layers.Dense(32, activation='relu', input_shape=(input_dim,))
        self.dropout = layers.Dropout(0.3)
        self.dense2 = layers.Dense(16, activation='relu')
        self.output_layer = layers.Dense(1, activation='sigmoid')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dropout(x)
        x = self.dense2(x)
        return self.output_layer(x)

if __name__ == "__main__":
    # 30 Synthetic Behavioral Training Samples (4 Features: API Call Density, Registry Writes, Network Beacons, Process Injection Signs)
    # Labels: 0 = Benign Software, 1 = Malicious Malware Threat
    X_train = np.array([
        [0.05, 0.0, 0.1, 0.02], [0.02, 0.0, 0.05, 0.01], [0.08, 0.0, 0.03, 0.02],
        [0.01, 0.0, 0.02, 0.0],  [0.04, 0.0, 0.06, 0.01], [0.06, 0.0, 0.04, 0.02],
        [0.03, 0.0, 0.08, 0.01], [0.07, 0.0, 0.01, 0.0],  [0.02, 0.0, 0.05, 0.01],
        [0.05, 0.0, 0.03, 0.02], [0.91, 1.0, 0.89, 0.95], [0.88, 1.0, 0.92, 0.91],
        [0.93, 1.0, 0.87, 0.94], [0.86, 1.0, 0.94, 0.9],  [0.9, 1.0, 0.91, 0.93],
        [0.95, 1.0, 0.88, 0.92], [0.87, 1.0, 0.93, 0.96], [0.92, 1.0, 0.86, 0.89],
        [0.89, 1.0, 0.95, 0.94], [0.96, 1.0, 0.9, 0.95],  [0.03, 0.0, 0.04, 0.01],
        [0.05, 0.0, 0.02, 0.02], [0.9, 1.0, 0.91, 0.93],  [0.88, 1.0, 0.89, 0.92],
        [0.02, 0.0, 0.06, 0.01], [0.93, 1.0, 0.94, 0.95], [0.04, 0.0, 0.03, 0.0],
        [0.87, 1.0, 0.9, 0.91],  [0.01, 0.0, 0.05, 0.02], [0.95, 1.0, 0.93, 0.96]
    ], dtype=np.float32)

    y_train = np.array([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=np.float32)

    model = MalwareBehaviorClassifier(input_dim=4)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Training Model
    model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=0)

    # 20 Distinct Test Behavioral Samples
    X_test = np.array([
        [0.03, 0.0, 0.05, 0.01], [0.92, 1.0, 0.9, 0.94],
        [0.06, 0.0, 0.03, 0.02], [0.9, 1.0, 0.93, 0.91],
        [0.02, 0.0, 0.04, 0.0],  [0.94, 1.0, 0.92, 0.95],
        [0.04, 0.0, 0.07, 0.01], [0.87, 1.0, 0.88, 0.9],
        [0.01, 0.0, 0.02, 0.02], [0.91, 1.0, 0.94, 0.93],
        [0.05, 0.0, 0.03, 0.01], [0.89, 1.0, 0.91, 0.92],
        [0.02, 0.0, 0.06, 0.02], [0.93, 1.0, 0.92, 0.91],
        [0.04, 0.0, 0.01, 0.01], [0.88, 1.0, 0.89, 0.9],
        [0.03, 0.0, 0.05, 0.03], [0.95, 1.0, 0.96, 0.95],
        [0.02, 0.0, 0.04, 0.01], [0.92, 1.0, 0.9, 0.92]
    ], dtype=np.float32)

    test_preds = model.predict(X_test, verbose=0)

    print("--- TensorFlow Cyber Threat Behavioral Classification Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred[0])
        status = "MALICIOUS MALWARE DETECTED " if score > 0.5 else "BENIGN SOFTWARE "
        print(f"[Test Sample {i}] Score: {score:.4f} -> Classification: {status}")