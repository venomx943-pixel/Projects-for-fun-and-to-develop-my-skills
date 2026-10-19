import numpy as np


def detect_latency_outliers(
    latencies: np.ndarray, threshold_std: float = 3.0
) -> np.ndarray:
    mean_val = np.mean(latencies)
    std_val = np.std(latencies)
    outlier_mask = np.abs(latencies - mean_val) > (threshold_std * std_val)
    return outlier_mask


if __name__ == "__main__":
    server_latencies = np.array([45.2, 48.1, 46.0, 49.5, 120.5, 47.3, 51.0, 310.2])
    outliers = detect_latency_outliers(server_latencies)
    print("Detected latency outliers mask:", outliers)
    print("Actual outlier latency values:", server_latencies[outliers])