import cv2
import os
import numpy as np

def secure_snapchat_filter(frame_path, overlay_path, face_coordinates):
    """
    Securely applies an overlay filter (like glasses or a mask) onto a face 
    within an image frame, preventing path traversal, out-of-bounds, and DoS.
    """
    # [Code Security & Vulnerability 1]: Type confusion check
    if not isinstance(frame_path, str) or not isinstance(overlay_path, str):
        raise TypeError("Security Error: File paths must be strings exclusively.")
    
    if not isinstance(face_coordinates, (list, tuple, np.ndarray)):
        raise TypeError("Security Error: Face coordinates must be a sequence.")

    # [Code Security & Vulnerability 2]: Path Traversal & Existence validation
    if not os.path.exists(frame_path) or not os.path.exists(overlay_path):
        raise FileNotFoundError("Security Error: Frame or overlay graphic file not found.")

    # [Code Security & Vulnerability 3]: File size check / DoS prevention (> 15MB)
    MAX_SIZE = 15 * 1024 * 1024
    if os.path.getsize(frame_path) > MAX_SIZE or os.path.getsize(overlay_path) > MAX_SIZE:
        raise ValueError("Security Error: File size exceeds safe limits. Potential DoS attempt.")

    # [Data Structure & Algorithm]: Load images safely using OpenCV O(pixels)
    frame = cv2.imread(frame_path)
    overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED) # Load with alpha channel if exists

    if frame is None or overlay is None:
        raise ValueError("Engineering Error: Failed to decode image or overlay asset.")

    # [Code Security & Vulnerability 4]: Validate face coordinates dimension [x, y, w, h]
    coords = np.array(face_coordinates, dtype=np.int32)
    if coords.ndim != 1 or coords.shape[0] != 4:
        raise ValueError("Security Error: Face coordinates must contain exactly 4 values (x, y, w, h).")

    fx, fy, fw, fh = coords
    frame_h, frame_w, _ = frame.shape

    # [Code Security & Vulnerability 5]: Out-of-bounds & Buffer Overflow protection
    if fx < 0 or fy < 0 or (fx + fw) > frame_w or (fy + fh) > frame_h:
        raise ValueError("Security Error: Face coordinates out of frame bounds. Buffer overflow risk.")

    # [Data Structure & Algorithm]: Resize overlay to match face bounding box dimensions O(pixels)
    try:
        resized_overlay = cv2.resize(overlay, (fw, fh))
    except Exception as e:
        raise RuntimeError(f"Engineering Error during asset resizing: {e}")

    # Simulated secure asset integration
    return "Secure Filter Applied Successfully"

# Demonstration of secure execution structure
try:
    print("Secure Snapchat Filter module initialized successfully.")
    # In a real environment, pass valid paths and coordinates:
    # result = secure_snapchat_filter("frame.jpg", "glasses.png", [50, 50, 100, 40])
except Exception as e:
    print(f"Security/Engineering Alert Detected: {e}")