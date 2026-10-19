import numpy as np


def clean_sensor_stream(raw_readings: np.ndarray, window_size: int = 3) -> np.ndarray:
    kernel = np.ones(window_size) / window_size
    smoothed = np.convolve(raw_readings, kernel, mode="same")
    noise_mask = np.abs(raw_readings - smoothed) > 2.0
    cleaned_readings = np.where(noise_mask, smoothed, raw_readings)
    return cleaned_readings


if __name__ == "__main__":
    sensor_data = np.array([22.1, 22.3, 45.0, 22.2, 22.4, 10.1, 22.5, 22.3])
    processed_data = clean_sensor_stream(sensor_data)
    print("Cleaned sensor readings:", processed_data)