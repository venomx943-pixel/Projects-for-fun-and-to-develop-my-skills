import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class MemoryFeatureDataset(Dataset):
    def __init__(self, mem_features, mem_labels):
        self.mem_features = mem_features
        self.mem_labels = mem_labels
    def __len__(self):
        return len(self.mem_features)
    def __getitem__(self, idx):
        return self.mem_features[idx], self.mem_labels[idx]

class MemoryAnomalyClassifier(nn.Module):
    def __init__(self, input_dim: int):
        super(MemoryAnomalyClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 32)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.25)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return self.sigmoid(out)

if __name__ == "__main__":
    # 30 Synthetic Memory Inspection Samples (4 Features: Executable Heap Flag, Stack Overflow Indicator, Unusual Pointer Jump, Permission Mismatch)
    # Labels: 0 = Normal Memory State, 1 = Code Injection / Memory Anomaly
    X_train = torch.tensor([
        [0.01, 0.0, 0.05, 0.02], [0.03, 0.0, 0.02, 0.01], [0.02, 0.0, 0.06, 0.03],
        [0.04, 0.0, 0.01, 0.01], [0.01, 0.0, 0.04, 0.02], [0.05, 0.0, 0.03, 0.0],
        [0.02, 0.0, 0.07, 0.01], [0.03, 0.0, 0.02, 0.04], [0.01, 0.0, 0.05, 0.02],
        [0.04, 0.0, 0.04, 0.01], [0.92, 1.0, 0.88, 0.95], [0.89, 1.0, 0.91, 0.92],
        [0.94, 1.0, 0.86, 0.9],  [0.87, 1.0, 0.93, 0.94], [0.91, 1.0, 0.89, 0.91],
        [0.95, 1.0, 0.9, 0.88],  [0.88, 1.0, 0.92, 0.96], [0.93, 1.0, 0.87, 0.89],
        [0.9, 1.0, 0.94, 0.93],  [0.96, 1.0, 0.91, 0.95], [0.02, 0.0, 0.04, 0.02],
        [0.03, 0.0, 0.05, 0.01], [0.91, 1.0, 0.9, 0.92],  [0.89, 1.0, 0.93, 0.9],
        [0.01, 0.0, 0.03, 0.02], [0.94, 1.0, 0.92, 0.95], [0.04, 0.0, 0.06, 0.01],
        [0.88, 1.0, 0.89, 0.91], [0.02, 0.0, 0.02, 0.03], [0.95, 1.0, 0.94, 0.96]
    ], dtype=torch.float32)

    y_train = torch.tensor([
        [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0],
        [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0], [1.0],
        [0.0], [0.0], [1.0], [1.0], [0.0], [1.0], [0.0], [1.0], [0.0], [1.0]
    ], dtype=torch.float32)

    dataset = MemoryFeatureDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

    model = MemoryAnomalyClassifier(input_dim=4)
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

    # 20 Distinct Test Memory Samples
    X_test = torch.tensor([
        [0.02, 0.0, 0.03, 0.01], [0.91, 1.0, 0.89, 0.93],
        [0.04, 0.0, 0.05, 0.02], [0.93, 1.0, 0.91, 0.9],
        [0.01, 0.0, 0.02, 0.03], [0.95, 1.0, 0.93, 0.95],
        [0.03, 0.0, 0.06, 0.01], [0.89, 1.0, 0.88, 0.92],
        [0.02, 0.0, 0.04, 0.02], [0.92, 1.0, 0.9, 0.94],
        [0.05, 0.0, 0.03, 0.01], [0.9, 1.0, 0.92, 0.89],
        [0.01, 0.0, 0.07, 0.02], [0.94, 1.0, 0.94, 0.91],
        [0.03, 0.0, 0.02, 0.01], [0.88, 1.0, 0.87, 0.9],
        [0.04, 0.0, 0.05, 0.03], [0.96, 1.0, 0.95, 0.96],
        [0.02, 0.0, 0.03, 0.01], [0.93, 1.0, 0.91, 0.92]
    ], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        test_preds = model(X_test)

    print("--- PyTorch Memory Anomaly & Code Injection Audit Report (20 Test Samples) ---")
    for i, pred in enumerate(test_preds, 1):
        score = float(pred.item())
        status = "MEMORY INJECTION DETECTED " if score > 0.5 else "NORMAL MEMORY STATE "
        print(f"[Test Memory Sample {i}] Score: {score:.4f} -> Classification: {status}")