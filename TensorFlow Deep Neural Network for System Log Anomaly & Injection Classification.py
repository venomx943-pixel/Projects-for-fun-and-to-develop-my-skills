import numpy as np
import tensorflow as tf
from keras import layers, models

class LogInjectionDefenseModel(tf.keras.Model):
    def __init__(self, input_dim: int):
        super(LogInjectionDefenseModel, self).__init__()
        self.dense1 = layers.Dense(36, activation='relu', input_shape=(input_dim,))
        self.dropout = layers.Dropout(0.25)
        self.dense2 = layers.Dense(18, activation='relu')
        self.output_layer = layers.Dense(1, activation='sigmoid')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dropout(x)
        x = self.dense2(x)
        return self.output_layer(x)

if __name__ == "__main__":
    # 30 Synthetic System Log Training Samples (4 Features: Failed Auth Rate, Suspicious Command Flag, Privilege Escalation Indicator, File Integrity Mismatch)
    # Labels: 0 = Normal System Log, 1 = Log Injection / Security Breach
    X_train = np.array([
        [0.02, 0.0, 0.01, 0.03], [0.04, 0.0, 0.02, 0.01], [0.01, 0.0, 0.03, 0.02],
        [0.03, 0.0, 0.01, 0.0],  [0.05, 0.0, 0.02, 0.01], [0.02, 0.0, 0.04, 0.03],
        [0.06, 0.0, 0.01, 0.02], [0.01, 0.0, 0.02, 0.01], [0.04, 0.0, 0.03, 0.0],
        [0.03, 0.0, 0.01, 0.04], [0.94, 1.0, 0.91, 0.89], [0.91, 1.0, 0.88, 0.93],
        [0.96, 1.0, 0.93, 0.9],  [0.89, 1.0, 0.95, 0.92], [0.92, 1.0, 0.9, 0.94],
        [0.95, 1.0, 0.87, 0.91], [0.9, 1.0, 0.94, 0.95],  [0.93, 1.0, 0.89, 0.88],
        [0.88, 1.0, 0.92, 0.93], [0.97, 1.0, 0.94, 0.96], [0.03, 0.0, 0.02, 0.01],
        [0.02, 0.0, 0.01, 0.03], [0.92, 1.0, 0.9, 0.91],  [0.9, 1.0, 0.93, 0.89],
        [0.04, 0.0, 0.03, 0.02], [0.94, 1.0, 0.92, 0.95], [0.01, 0.0, 0.02, 0.0],
        [0.89, 1.0, 0.91, 0.92], [0.05, 0.0, 0.04, 0.01], [0.96, 1.0, 0.95, 0.94]
    ], dtype=np.float32)

    y_train = np.array([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=np.float32)

    model = LogInjectionDefenseModel(input_dim=4)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Training Model on System Log Data
    model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=0)

    # 20 Distinct Test System Log Samples
    X_test = np.array([
        [0.03, 0.0, 0.02, 0.01], [0.93, 1.0, 0.91, 0.92],
        [0.05, 0.0, 0.01, 0.03], [0.91, 1.0, 0.89, 0.94],
        [0.02, 0.0, 0.03, 0.0],  [0.95, 1.0, 0.93, 0.91],
        [0.04, 0.0, 0.02, 0.02], [0.89, 1.0, 0.9, 0.88],
        [0.01, 0.0, 0.01, 0.01], [0.92, 1.0, 0.94, 0.95],
        [0.03, 0.0, 0.04, 0.02], [0.9, 1.0, 0.88, 0.93],
        [0.02, 0.0, 0.02, 0.01], [0.94, 1.0, 0.92, 0.9],
        [0.04, 0.0, 0.01, 0.03], [0.88, 1.0, 0.91, 0.89],
        [0.03, 0.0, 0.03, 0.01], [0.96, 1.0, 0.95, 0.96],
        [0.02, 0.0, 0.02, 0.02], [0.92, 1.0, 0.9, 0.92]
    ], dtype=np.float32)

    test_preds = model.predict(X_test, verbose=0)

    print("--- TensorFlow System Log Injection Defense Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred[0])
        status = "LOG INJECTION DETECTED " if score > 0.5 else "NORMAL SYSTEM LOG "
        print(f"[Test Log Sample {i}] Score: {score:.4f} -> Classification: {status}")