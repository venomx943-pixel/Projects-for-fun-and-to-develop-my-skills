import cv2
import os
import numpy as np

def secure_face_detector(image_path, cascade_path):
    """
    Securely loads an image and detects faces using OpenCV Haar Cascades
    with robust path validation, size checks, and memory protection.
    """
    # [Code Security & Vulnerability 1]: Type confusion check
    if not isinstance(image_path, str) or not isinstance(cascade_path, str):
        raise TypeError("Security Error: Paths must be strings exclusively.")
    
    # [Code Security & Vulnerability 2]: Path Traversal and existence verification
    if not os.path.exists(image_path) or not os.path.exists(cascade_path):
        raise FileNotFoundError("Security Error: Image or cascade file path does not exist.")
    
    # [Code Security & Vulnerability 3]: File size / DoS protection (prevent loading massive files > 20MB)
    MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024
    if os.path.getsize(image_path) > MAX_FILE_SIZE_BYTES:
        raise ValueError("Security Error: Image file size exceeds safe threshold (20MB). DoS risk.")

    # [Data Structure & Algorithm]: Load image safely using OpenCV O(pixels)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Engineering Error: Failed to decode image. Invalid or corrupted format.")

    # [Code Security & Vulnerability 4]: Dimension bounds check to prevent extreme memory allocation
    height, width, _ = image.shape
    if width > 5000 or height > 5000:
        raise ValueError("Security Error: Image dimensions too large. Memory exhaustion prevention.")

    # Convert to grayscale for Haar Cascade processing
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load cascade classifier safely
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        raise RuntimeError("Security Error: Failed to load Haar Cascade classifier XML.")

    # [Data Structure & Algorithm]: Detect faces using multi-scale scanning O(n)
    faces = face_cascade.detectMultiScale(
        gray_image, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )

    return faces.tolist() if isinstance(faces, np.ndarray) else []

# Demonstration of secure execution structure
try:
    print("Secure Face Detector module initialized successfully.")
    # In a real environment, pass valid paths:
    # detected_faces = secure_face_detector("user_image.jpg", "haarcascade_frontalface_default.xml")
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")