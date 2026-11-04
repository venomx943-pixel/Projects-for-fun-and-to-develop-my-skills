import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class APITrafficDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
    def __len__(self):
        return len(self.features)
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class APIAnomalyDetector(nn.Module):
    def __init__(self, input_dim: int):
        super(APIAnomalyDetector, self).__init__()
        self.layer1 = nn.Linear(input_dim, 32)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.3)
        self.layer2 = nn.Linear(32, 16)
        self.layer3 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.layer1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.layer2(out)
        out = self.relu(out)
        out = self.layer3(out)
        return self.sigmoid(out)

if __name__ == "__main__":
    X_train = torch.tensor([
        [0.1, 0.05, 0.0, 1.0], [0.15, 0.02, 0.0, 1.0], [0.08, 0.01, 0.0, 1.0],
        [0.12, 0.04, 0.0, 1.0], [0.09, 0.03, 0.0, 1.0], [0.14, 0.06, 0.0, 1.0],
        [0.11, 0.02, 0.0, 1.0], [0.13, 0.05, 0.0, 1.0], [0.07, 0.01, 0.0, 1.0],
        [0.1, 0.04, 0.0, 1.0],  [0.85, 0.95, 1.0, 0.0], [0.9, 0.88, 1.0, 0.0],
        [0.88, 0.92, 1.0, 0.0], [0.92, 0.9, 1.0, 0.0],  [0.86, 0.94, 1.0, 0.0],
        [0.91, 0.87, 1.0, 0.0], [0.89, 0.93, 1.0, 0.0], [0.94, 0.89, 1.0, 0.0],
        [0.87, 0.91, 1.0, 0.0], [0.93, 0.95, 1.0, 0.0], [0.1, 0.03, 0.0, 1.0],
        [0.12, 0.05, 0.0, 1.0], [0.9, 0.91, 1.0, 0.0],  [0.88, 0.89, 1.0, 0.0],
        [0.09, 0.02, 0.0, 1.0], [0.92, 0.93, 1.0, 0.0], [0.11, 0.04, 0.0, 1.0],
        [0.86, 0.9, 1.0, 0.0],  [0.13, 0.01, 0.0, 1.0], [0.95, 0.94, 1.0, 0.0]
    ], dtype=torch.float32)

    y_train = torch.tensor([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=torch.float32)

    dataset = APITrafficDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

    model = APIAnomalyDetector(input_dim=4)
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

    X_test = torch.tensor([
        [0.11, 0.03, 0.0, 1.0], [0.89, 0.91, 1.0, 0.0],
        [0.16, 0.02, 0.0, 1.0], [0.92, 0.88, 1.0, 0.0],
        [0.09, 0.05, 0.0, 1.0], [0.85, 0.93, 1.0, 0.0],
        [0.12, 0.01, 0.0, 1.0], [0.94, 0.9, 1.0, 0.0],
        [0.08, 0.04, 0.0, 1.0], [0.87, 0.92, 1.0, 0.0],
        [0.1, 0.02, 0.0, 1.0],  [0.9, 0.94, 1.0, 0.0],
        [0.14, 0.03, 0.0, 1.0], [0.86, 0.89, 1.0, 0.0],
        [0.11, 0.05, 0.0, 1.0], [0.93, 0.91, 1.0, 0.0],
        [0.13, 0.01, 0.0, 1.0], [0.88, 0.95, 1.0, 0.0],
        [0.07, 0.03, 0.0, 1.0], [0.95, 0.93, 1.0, 0.0]
    ], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        test_preds = model(X_test)

    print("--- PyTorch API Payload Anomaly Detection Audit Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred.item())
        status = "MALICIOUS API ATTACK " if score > 0.5 else "LEGITIMATE REQUEST "
        print(f"[Test API Sample {i}] Score: {score:.4f} -> Classification: {status}")