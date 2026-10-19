import numpy as np


def simulate_attack_probabilities(
    avg_normal_rate: float, sample_size: int
) -> np.ndarray:
    np.random.seed(42)
    simulated_traffic = np.random.poisson(
        lam=avg_normal_rate, size=sample_size
    )
    anomaly_threshold = avg_normal_rate + (2.5 * np.std(simulated_traffic))
    attack_probabilities = np.mean(simulated_traffic > anomaly_threshold)
    return simulated_traffic, attack_probabilities


if __name__ == "__main__":
    traffic_samples, prob = simulate_attack_probabilities(
        avg_normal_rate=50.0, sample_size=1000
    )
    print("Simulated traffic max peak:", np.max(traffic_samples))
    print("Calculated attack probability ratio:", prob)