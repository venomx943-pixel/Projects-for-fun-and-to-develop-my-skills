import numpy as np


def quantize_embeddings(embeddings: np.ndarray) -> tuple:
    min_val = np.min(embeddings)
    max_val = np.max(embeddings)
    normalized = (embeddings - min_val) / (max_val - min_val)
    quantized = np.round(normalized * 255).astype(np.uint8)
    return quantized, min_val, max_val


if __name__ == "__main__":
    mock_embeddings = np.array(
        [[0.12, 0.45, 0.78, 0.91], [0.34, 0.11, 0.56, 0.82]], dtype=np.float32
    )
    q_data, mn, mx = quantize_embeddings(mock_embeddings)
    print("Quantized embeddings shape:", q_data.shape)
    print("Quantized data type:", q_data.dtype)