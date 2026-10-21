import numpy as np
from sklearn.linear_model import LinearRegression


def train_and_predict_resources(
    historical_requests: list,
    historical_connections: list,
    historical_cpu: list,
    target_requests: list,
    target_connections: list,
) -> np.ndarray:
    X_train = np.column_stack((historical_requests, historical_connections))
    y_train = np.array(historical_cpu)
    
    X_target = np.column_stack((target_requests, target_connections))
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_target)
    return predictions


if __name__ == "__main__":
    train_reqs = [100, 500, 1000, 2000, 5000]
    train_conns = [10, 50, 100, 250, 600]
    train_cpu = [15.5, 35.0, 55.2, 78.4, 98.9]
    
    target_reqs = [1200, 4500]
    target_conns = [120, 500]
    
    predicted_cpu = train_and_predict_resources(
        train_reqs, train_conns, train_cpu, target_reqs, target_conns
    )
    print("Predicted CPU usage percentages:", predicted_cpu)