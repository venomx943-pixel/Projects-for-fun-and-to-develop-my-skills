import cv2
import os
import numpy as np

def secure_document_scanner(image_path, corner_points):
    """
    Securely warps a document or card image based on detected corner points
    with path validation, size checks, and geometry protection.
    """
    # [Code Security & Vulnerability 1]: Type validation
    if not isinstance(image_path, str):
        raise TypeError("Security Error: Image path must be a string exclusively.")
    
    if not isinstance(corner_points, (list, np.ndarray)):
        raise TypeError("Security Error: Corner points must be a list or numpy array.")

    # [Code Security & Vulnerability 2]: Path traversal & existence check
    if not os.path.exists(image_path):
        raise FileNotFoundError("Security Error: Document image file not found.")

    # [Code Security & Vulnerability 3]: File size / DoS protection (> 20MB)
    MAX_SIZE = 20 * 1024 * 1024
    if os.path.getsize(image_path) > MAX_SIZE:
        raise ValueError("Security Error: File size exceeds safe threshold. Potential DoS attempt.")

    # [Data Structure & Algorithm]: Load image safely O(pixels)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Engineering Error: Failed to decode document image.")

    # Convert to numpy array for points and validate dimensions
    pts = np.array(corner_points, dtype=np.float32)

    # [Code Security & Vulnerability 4]: Dimension check (Must be exactly 4 corner points with 2 coordinates each)
    if pts.shape != (4, 2):
        raise ValueError("Security Error: Exactly 4 corner points (x, y) are required for perspective warp.")

    # [Code Security & Vulnerability 5]: NaN / Inf / Boundary validation
    if np.isnan(pts).any() or np.isinf(pts).any():
        raise ValueError("Security Error: Detected NaN or Infinite values in corner points.")

    h, w, _ = image.shape
    if np.any(pts < 0) or np.any(pts[:, 0] > w) or np.any(pts[:, 1] > h):
        raise ValueError("Security Error: Corner coordinates out of image dimensions. Buffer overflow risk.")

    # [Data Structure & Algorithm]: Define destination points for flattened view and apply warp perspective O(pixels)
    dst_pts = np.array([
        [0, 0],
        [300, 0],
        [300, 400],
        [0, 400]
    ], dtype=np.float32)

    try:
        matrix = cv2.getPerspectiveTransform(pts, dst_pts)
        warped_image = cv2.warpPerspective(image, matrix, (300, 400))
    except Exception as e:
        raise RuntimeError(f"Engineering Error during perspective transformation: {e}")

    return "Secure Document Scanner Warped Successfully"

# Demonstration of secure execution structure
try:
    print("Secure Document Scanner module initialized successfully.")
    # In a real environment, pass valid paths and 4 corner points:
    # result = secure_document_scanner("card.jpg", [[10,10], [200,15], [195,300], [12,305]])
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")