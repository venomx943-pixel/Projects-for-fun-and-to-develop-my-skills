import torch
import torch.nn as nn
import torch.optim as optim

class NetworkIntrusionClassifier(nn.Module):
    def __init__(self, input_dim: int):
        super(NetworkIntrusionClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return self.sigmoid(out)

if __name__ == "__main__":
    # 30 Synthetic Enterprise Network Traffic Training Samples (5 Features: Packet Size, Duration, Flag Count, Error Rate, Port Density)
    # Labels: 0 = Benign Traffic, 1 = Malicious Intrusion
    X_train = torch.tensor([
        [0.1, 0.2, 0.0, 0.01, 0.1], [0.2, 0.1, 0.0, 0.02, 0.1], [0.15, 0.15, 0.0, 0.0, 0.05],
        [0.1, 0.3, 0.0, 0.01, 0.2], [0.25, 0.2, 0.0, 0.0, 0.1], [0.05, 0.1, 0.0, 0.01, 0.05],
        [0.2, 0.2, 0.0, 0.02, 0.15], [0.1, 0.1, 0.0, 0.0, 0.1], [0.3, 0.25, 0.0, 0.01, 0.2],
        [0.15, 0.2, 0.0, 0.0, 0.1], [0.8, 0.9, 1.0, 0.85, 0.9], [0.9, 0.85, 1.0, 0.9, 0.85],
        [0.85, 0.95, 1.0, 0.8, 0.95], [0.75, 0.8, 1.0, 0.9, 0.8], [0.9, 0.9, 1.0, 0.85, 0.9],
        [0.8, 0.85, 1.0, 0.9, 0.85], [0.95, 0.9, 1.0, 0.95, 0.9], [0.85, 0.8, 1.0, 0.85, 0.8],
        [0.9, 0.95, 1.0, 0.9, 0.95], [0.8, 0.9, 1.0, 0.8, 0.9], [0.1, 0.15, 0.0, 0.01, 0.1],
        [0.2, 0.2, 0.0, 0.0, 0.05], [0.85, 0.9, 1.0, 0.85, 0.9], [0.75, 0.85, 1.0, 0.8, 0.85],
        [0.15, 0.1, 0.0, 0.02, 0.1], [0.9, 0.9, 1.0, 0.9, 0.9], [0.1, 0.2, 0.0, 0.0, 0.1],
        [0.8, 0.8, 1.0, 0.85, 0.8], [0.2, 0.15, 0.0, 0.01, 0.1], [0.95, 0.95, 1.0, 0.9, 0.95]
    ], dtype=torch.float32)

    y_train = torch.tensor([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=torch.float32)

    # Initialize model, loss function, and optimizer
    model = NetworkIntrusionClassifier(input_dim=5)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Training Loop (Quick Convergence)
    model.train()
    for epoch in range(150):
        optimizer.zero_grad()
        predictions = model(X_train)
        loss = criterion(predictions, y_train)
        loss.backward()
        optimizer.step()

    # 20 Distinct Test Network Traffic Samples
    X_test = torch.tensor([
        [0.12, 0.18, 0.0, 0.01, 0.1], [0.88, 0.92, 1.0, 0.88, 0.9],
        [0.18, 0.12, 0.0, 0.0, 0.05], [0.91, 0.89, 1.0, 0.9, 0.92],
        [0.1, 0.22, 0.0, 0.02, 0.15], [0.82, 0.86, 1.0, 0.8, 0.85],
        [0.2, 0.2, 0.0, 0.0, 0.1],   [0.94, 0.91, 1.0, 0.92, 0.94],
        [0.08, 0.12, 0.0, 0.0, 0.05], [0.86, 0.88, 1.0, 0.85, 0.88],
        [0.15, 0.15, 0.0, 0.01, 0.1], [0.9, 0.93, 1.0, 0.9, 0.91],
        [0.22, 0.18, 0.0, 0.0, 0.1],  [0.83, 0.87, 1.0, 0.82, 0.86],
        [0.11, 0.19, 0.0, 0.01, 0.1], [0.92, 0.9, 1.0, 0.91, 0.93],
        [0.14, 0.16, 0.0, 0.0, 0.05], [0.87, 0.85, 1.0, 0.86, 0.87],
        [0.19, 0.21, 0.0, 0.02, 0.15],[0.95, 0.94, 1.0, 0.93, 0.95]
    ], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        test_preds = model(X_test)

    print("--- PyTorch Deep Learning Network Intrusion Audit Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred.item())
        status = "MALICIOUS INTRUSION " if score > 0.5 else "BENIGN TRAFFIC "
        print(f"[Test Sample {i}] Score: {score:.4f} -> Classification: {status}")