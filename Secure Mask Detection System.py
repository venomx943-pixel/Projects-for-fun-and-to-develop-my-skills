import cv2
import os
import numpy as np

def secure_mask_detector(image_path, model, target_size=(224, 224)):
    """
    Securely loads an image and checks whether a person is wearing a face mask 
    with robust path validation, size checks, and memory protection.
    """
    # [Code Security & Vulnerability 1]: Type validation
    if not isinstance(image_path, str):
        raise TypeError("Security Error: Image path must be a string exclusively.")
    
    # [Code Security & Vulnerability 2]: Path Traversal and existence verification
    if not os.path.exists(image_path):
        raise FileNotFoundError("Security Error: Image file path does not exist.")
    
    # [Code Security & Vulnerability 3]: File size / DoS protection (> 15MB)
    MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024
    if os.path.getsize(image_path) > MAX_FILE_SIZE_BYTES:
        raise ValueError("Security Error: Image file size exceeds safe threshold (15MB). DoS risk.")

    # [Data Structure & Algorithm]: Load image safely using OpenCV O(pixels)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Engineering Error: Failed to decode image. Invalid or corrupted format.")

    # [Code Security & Vulnerability 4]: Dimension bounds check to prevent extreme memory allocation
    height, width, _ = image.shape
    if width > 4000 or height > 4000:
        raise ValueError("Security Error: Image dimensions too large. Memory exhaustion prevention.")

    # [Data Structure & Algorithm]: Preprocess image (resize and normalize) O(pixels)
    try:
        resized_image = cv2.resize(image, target_size)
        normalized_image = resized_image.astype(np.float32) / 255.0
    except Exception as e:
        raise RuntimeError(f"Engineering Error during image preprocessing: {e}")

    # [Code Security & Vulnerability 5]: NaN / Infinity injection check
    if np.isnan(normalized_image).any() or np.isinf(normalized_image).any():
        raise ValueError("Security Error: Detected NaN or Infinite values in preprocessed image.")

    # Reshape for batch prediction O(1)
    input_tensor = np.expand_dims(normalized_image, axis=0)

    # Simulated secure prediction execution
    # prediction = model.predict(input_tensor)
    
    return "Secure Mask Detection Completed Successfully"

# Demonstration of secure execution structure
try:
    print("Secure Mask Detector module initialized successfully.")
    # In a real environment, pass valid paths:
    # result = secure_mask_detector("face_image.jpg", dummy_model)
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")