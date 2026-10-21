import numpy as np
from sklearn.cluster import KMeans


def detect_rogue_network_devices(
    device_features: list, target_devices: list
) -> np.ndarray:
    model = KMeans(n_clusters=2, random_state=42, n_init=10)
    model.fit(device_features)
    predictions = model.predict(target_devices)
    return predictions


if __name__ == "__main__":
    known_enterprise_devices = [
        [1200.5, 45.0],
        [1150.0, 42.2],
        [1250.8, 48.5],
        [1180.2, 44.1],
    ]
    incoming_devices_to_check = [
        [1210.0, 46.0],
        [8500.4, 450.9],
    ]
    cluster_results = detect_rogue_network_devices(
        known_enterprise_devices, incoming_devices_to_check
    )
    print("Device cluster classification results:", cluster_results)