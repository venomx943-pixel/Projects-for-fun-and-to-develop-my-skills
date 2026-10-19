import numpy as np


def compress_binary_image(binary_image: np.ndarray) -> bytes:
    flat_image = binary_image.astype(bool).flatten()
    packed_bytes = np.packbits(flat_image)
    return packed_bytes.tobytes()


if __name__ == "__main__":
    mock_image = np.array(
        [[0, 1, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]], dtype=np.uint8
    )
    compressed_data = compress_binary_image(mock_image)
    print("Compressed binary image bytes length:", len(compressed_data))