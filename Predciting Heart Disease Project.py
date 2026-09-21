import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

def generate_synthetic_dataset(n_samples: int = 300) -> pd.DataFrame:
    """Generates a synthetic health dataset for demonstration purposes."""
    np.random.seed(42)
    data = {
        'Age': np.random.randint(30, 70, n_samples),
        'Blood_Pressure': np.random.randint(110, 180, n_samples),
        'Cholesterol': np.random.randint(150, 300, n_samples),
        'Max_Heart_Rate': np.random.randint(100, 190, n_samples),
        'Heart_Disease': np.random.choice([0, 1], size=n_samples, p=[0.6, 0.4])
    }
    return pd.DataFrame(data)

def train_heart_disease_model(df: pd.DataFrame):
    """Preprocesses data, trains a Random Forest classifier, and returns the model and test sets."""
    X = df[['Age', 'Blood_Pressure', 'Cholesterol', 'Max_Heart_Rate']]
    y = df['Heart_Disease']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # we using an optimized Random Forest estimator setup
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test) -> None:
    """Evaluates the trained model performance and prints metrics."""
    y_pred = model.predict(X_test)
    
    print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}\n")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred), "\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    #Load Dataset
    dataset = generate_synthetic_dataset()
    print("--- Sample Dataset ---")
    print(dataset.head(), "\n" + "="*50 + "\n")
    
    #Train Model
    trained_model, X_test, y_test = train_heart_disease_model(dataset)
    
    #Evaluate Performance
    print("--- Model Performance Metrics ---")
    evaluate_model(trained_model, X_test, y_test)
    
    #Predict on a New Patient Sample like Age, BP, Cholesterol, Max_HR
    new_patient = np.array([[55, 160, 240, 120]])
    prediction = trained_model.predict(new_patient)
    
    print("\n--- New Patient Inference ---")
    if prediction[0] == 1:
        print("Result: Alert! Potential heart disease risk detected. Immediate medical consultation recommended.")
    else:
        print("Result: Normal status. No critical risk indicators detected.")