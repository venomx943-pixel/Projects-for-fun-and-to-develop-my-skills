import numpy as np
import torch 
import torch.nn as nn
import torch.optim as optim 

np.random.seed(42)
torch.manual_seed(42)

print("[-] First Stage: Generate Clean Data and Building the Basic Model")


X_clean = np.random.randn(200, 2).astype(np.float32)

y_clean = ((X_clean[:, 0] + X_clean[:, 1]) > 0).astype(np.float32)

X_tensor = torch.tensor(X_clean)
y_tensor = torch.tensor(y_clean).unsqueeze(1)


class SecureAIModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.linear(x))


model_clean = SecureAIModel()
criterion = nn.BCELoss()
optimizer = optim.SGD(model_clean.parameters(), lr=0.1)

for epoch in range(150):
    optimizer.zero_grad()
    predictions = model_clean(X_tensor)
    loss = criterion(predictions, y_tensor)
    loss.backward()
    optimizer.step()


with torch.no_grad():
    preds_before = (model_clean(X_tensor) > 0.5).float()
    accuracy_before = (preds_before.eq(y_tensor).sum() / y_tensor.shape[0]).item()

print(f"\n[+] The Accuracy of The Model in The Clean state (Before Poisoning): {accuracy_before * 100:.2f}%")

print("[-] Second Stage: Execution The Data Poisoning Attack")


poison_ratio = 0.25
num_poison = int(200 * poison_ratio)
poison_indices = np.random.choice(200, size=num_poison, replace=False)

X_poisoned = X_clean.copy()
X_poisoned[poison_indices] += np.random.normal(loc=3.5, scale=1.0, size=(num_poison, 2))

X_poisoned_tensor = torch.tensor(X_poisoned)

model_poisoned = SecureAIModel()
optimizer_poisoned = optim.SGD(model_poisoned.parameters(), lr=0.1)

for epoch in range (150):
    optimizer_poisoned.zero_grad()
    predictions_p = model_poisoned(X_poisoned_tensor)
    loss_p = criterion(predictions_p, y_tensor)
    loss_p.backward()
    optimizer_poisoned.step()



with torch.no_grad():
    preds_after = (model_poisoned(X_tensor) > 0.5).float()
    accuracy_after = (preds_after.eq(y_tensor).sum() / y_tensor.shape[0]).item()

print(f"[+] The Accuracy of The Model After Mathemtaic Poison Attack: {accuracy_after * 100:.2f}%")
print(f"[!] The Acccuracy of the Collapse in Performance: {(accuracy_before - accuracy_after) * 100:.2f}%")    