import torch
import torch.nn as nn

class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(3, 1)
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        return self.sigmoid(self.linear(x))


torch.manual_seed(42)
model = SimpleClassifier()
criterion = nn.BCELoss()


x_original = torch.tensor([[0.5, -1.2, 1.8]], requires_grad=True)
y_target = torch.tensor([[1.0]])

prediction_original = model(x_original)
loss_original = criterion(prediction_original, y_target)

model.zero_grad()
loss_original.backward()

data_grad = x_original.grad.data
epilson = 0.2
perturbation = epilson * data_grad.sign()

x_adversarial = x_original + perturbation

with torch.no_grad():
    prediction_adversarial = model(x_adversarial)

print(f"[-] The Original Value of The Model: {prediction_original.item():.4f}")
print(f"[-] The Value After FGSM Attack: {prediction_adversarial.item():.4f}")