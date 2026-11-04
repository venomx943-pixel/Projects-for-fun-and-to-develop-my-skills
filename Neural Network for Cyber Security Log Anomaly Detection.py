import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class SecurityLogDataset(Dataset):
    def __init__(self, log_features, log_labels):
        self.log_features = log_features
        self.log_labels = log_labels
    def __len__(self):
        return len(self.log_features)
    def __getitem__(self, idx):
        return self.log_features[idx], self.log_labels[idx]

class LogAnomalyClassifier(nn.Module):
    def __init__(self, input_dim: int):
        super(LogAnomalyClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 24)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(24, 12)
        self.fc3 = nn.Linear(12, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return self.sigmoid(out)

if __name__ == "__main__":
    # 30 Synthetic Security Log Training Samples (4 Features: Failed Login Count, Privilege Escalation Flag, Unusual Port Access, Error Rate)
    # Labels: 0 = Normal Log, 1 = Security Breach / Anomalous Log
    X_train = torch.tensor([
        [0.05, 0.0, 0.1, 0.01], [0.02, 0.0, 0.05, 0.02], [0.08, 0.0, 0.1, 0.0],
        [0.01, 0.0, 0.02, 0.01], [0.04, 0.0, 0.08, 0.03], [0.06, 0.0, 0.05, 0.01],
        [0.03, 0.0, 0.1, 0.02], [0.07, 0.0, 0.03, 0.0], [0.02, 0.0, 0.06, 0.01],
        [0.05, 0.0, 0.04, 0.02], [0.95, 1.0, 0.85, 0.9], [0.9, 1.0, 0.92, 0.85],
        [0.92, 1.0, 0.88, 0.95], [0.88, 1.0, 0.9, 0.88], [0.96, 1.0, 0.95, 0.92],
        [0.91, 1.0, 0.87, 0.89], [0.94, 1.0, 0.91, 0.93], [0.89, 1.0, 0.86, 0.87],
        [0.93, 1.0, 0.94, 0.91], [0.97, 1.0, 0.89, 0.94], [0.04, 0.0, 0.07, 0.01],
        [0.06, 0.0, 0.03, 0.02], [0.92, 1.0, 0.9, 0.89],  [0.9, 1.0, 0.88, 0.92],
        [0.03, 0.0, 0.09, 0.01], [0.95, 1.0, 0.93, 0.94], [0.05, 0.0, 0.02, 0.0],
        [0.88, 1.0, 0.91, 0.87], [0.02, 0.0, 0.06, 0.01], [0.96, 1.0, 0.94, 0.95]
    ], dtype=torch.float32)

    y_train = torch.tensor([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=torch.float32)

    dataset = SecurityLogDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

    model = LogAnomalyClassifier(input_dim=4)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for epoch in range(100):
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()

    # 20 Distinct Test Log Samples
    X_test = torch.tensor([
        [0.04, 0.0, 0.08, 0.01], [0.93, 1.0, 0.89, 0.92],
        [0.07, 0.0, 0.05, 0.02], [0.91, 1.0, 0.92, 0.9],
        [0.02, 0.0, 0.03, 0.0],  [0.96, 1.0, 0.94, 0.93],
        [0.05, 0.0, 0.1, 0.01],  [0.89, 1.0, 0.88, 0.86],
        [0.03, 0.0, 0.02, 0.02], [0.94, 1.0, 0.91, 0.95],
        [0.06, 0.0, 0.07, 0.0],  [0.92, 1.0, 0.9, 0.89],
        [0.01, 0.0, 0.04, 0.01], [0.95, 1.0, 0.93, 0.91],
        [0.04, 0.0, 0.06, 0.02], [0.9, 1.0, 0.87, 0.88],
        [0.08, 0.0, 0.09, 0.01], [0.97, 1.0, 0.95, 0.94],
        [0.02, 0.0, 0.05, 0.0],  [0.93, 1.0, 0.92, 0.92]
    ], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        test_preds = model(X_test)

    print("--- PyTorch Security Log Anomaly Detection Audit Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred.item())
        status = "SECURITY BREACH DETECTED " if score > 0.5 else "NORMAL LOG EVENT "
        print(f"[Test Log Sample {i}] Score: {score:.4f} -> Classification: {status}")