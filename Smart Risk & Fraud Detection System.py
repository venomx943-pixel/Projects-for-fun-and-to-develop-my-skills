import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import torch
import torch.nn as nn
import torch.optim as optim

print("--- الخطوة 1: تجهيز البيانات العشوائية للمشروع ---")
np.random.seed(42) # لضمان ثبات النتائج


num_samples = 1000
X_raw = np.random.randn(num_samples, 4) * 10 + 50 

y = np.random.randint(0, 2, size=num_samples)

# إضافة بعض القيم المفقودة (NaN) عمداً لتطبيق دوال التنظيف
X_raw[10, 2] = np.nan
X_raw[50, 1] = np.nan


col_means = np.nanmean(X_raw, axis=0)
indices_nan = np.isnan(X_raw)
X_raw[indices_nan] = np.take(col_means, np.where(indices_nan)[1])

print(f"شكل بيانات الخصائص بعد التنظيف: {X_raw.shape}")


print("\n--- الخطوة 2: التقسيم والتطبيع ---")
X_train, X_test, y_train, y_test = train_test_split(X_raw, y, test_size=0.2, random_state=42)

# استخدام StandardScaler لتطبيع المقاييس
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n--- الخطوة 3: تدريب نموذج التعلم الآلي الكلاسيكي ---")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# التنبؤ والتقييم
y_pred_rf = rf_model.predict(X_test_scaled)
acc_rf = accuracy_score(y_test, y_pred_rf)
print(f"دقة نموذج الغابات العشوائية (Random Forest Accuracy): {acc_rf * 100:.2f}%")



print("\n--- الخطوة 4: تجهيز موترات PyTorch وحساب التفاضل ---")

X_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)


weights = torch.randn(4, 1, requires_grad=True)
bias = torch.zeros(1, requires_grad=True)

# خطوة تدريب بسيطة (Forward & Backward عُرفية للتعلم)
optimizer = optim.SGD([weights, bias], lr=0.01)
criterion = nn.BCEWithLogitsLoss() # دالة خطس التصنيف الثنائي

for epoch in range(50):
    optimizer.zero_grad()
    outputs = torch.matmul(X_tensor, weights) + bias
    loss = criterion(outputs, y_tensor)
    
    # حساب التفاضل التلقائي
    loss.backward()
    optimizer.step()

print(f"قيمة الخطأ النهائي (Loss) في نموذج PyTorch الخطي: {loss.item():.4f}")


print("\n--- الخطوة 5: رسم النتائج بـ Matplotlib ---")
plt.figure(figsize=(10, 5))


plt.subplot(1, 2, 1)
plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], c=y_train, cmap='coolwarm', alpha=0.7)
plt.title("توزيع المعاملات (أحمر: مشبوهة، أزرق: سليمة)")
plt.xlabel("الميزة الأولى (مدخلات المعاملة)")
plt.xlabel("الميزة الثانية")
plt.grid(True)


plt.subplot(1, 2, 2)
models = ['Random Forest', 'PyTorch Linear']
accuracies = [acc_rf * 100, 75.5] # مثال افتراضي للمقارنة
plt.bar(models, accuracies, color=['#2ca02c', '#1f77b4'])
plt.ylim(0, 100)
plt.title("مقارنة دقة النماذج")
plt.ylabel("الدقة (%)")
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
print("تم تنفيذ المشروع بنجاح وعرض الرسومات البيانية!")