
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = {
    'Study_Hours': [2, 10, 4, 15, 6, 8, 3, 12, 5, 14],
    'Attendance': [50, 95, 60, 98, 70, 85, 40, 90, 65, 92],
    'Previous_Grade': [55, 90, 62, 95, 75, 80, 50, 88, 70, 91],
    'Passed': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)


X = df[['Study_Hours', 'Attendance', 'Previous_Grade']]
y = df['Passed'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

 
model = LogisticRegression()


model.fit(X_train, y_train)


y_pred = model.predict(X_test)

print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


new_student = [[11, 91, 85]]
prediction = model.predict(new_student)

print("\nPrediction for new student (1 = Pass, 0 = Fail):", prediction[0])
