import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class RackCableIntegrityInspector:
    def __init__(self, target_color_lower=(35, 50, 50), target_color_upper=(85, 255, 255)):
        # Default green spectrum for active connected patch cables, deviation indicates disconnection/fault
        self.lower_bound = np.array(target_color_lower, dtype=np.uint8)
        self.upper_bound = np.array(target_color_upper, dtype=np.uint8)
        logging.info("Initialized RackCableIntegrityInspector with HSV color-masking topology.")

    def inspect_rack_frame(self, frame: np.ndarray, expected_ports_count: int) -> dict:
        """Inspect server rack frame to verify cable attachment and port link status."""
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Mask out active connected cables based on color signature
        mask = cv2.inRange(hsv_frame, self.lower_bound, self.upper_bound)
        
        # Apply morphological operations to clean noise
        kernel = np.ones((5, 5), np.uint8)
        cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours of connected link cables
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_links = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Filter out trivial noise specks
                detected_links += 1

        integrity_ratio = detected_links / expected_ports_count
        status = "RACK INTEGRITY SECURE " if integrity_ratio >= 0.9 else "CABLE DISCONNECTION ALERT "

        inspection_report = {
            "expected_ports": expected_ports_count,
            "detected_links": detected_links,
            "integrity_score": round(integrity_ratio * 100, 2),
            "status": status
        }
        return inspection_report

if __name__ == "__main__":
    # Simulation: Generating synthetic server rack images with 10 ports
    inspector = RackCableIntegrityInspector()
    height, width = 300, 600
    expected_ports = 10

    logging.info("Starting OpenCV Server Rack Cable & Port Integrity Audit Simulation...")
    
    # Simulate a healthy rack frame with green connected patch cables
    healthy_frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(expected_ports):
        x_pos = 50 + (i * 50)
        # Draw simulated active cable in green HSV range (Hue ~ 60)
        cv2.rectangle(healthy_frame, (x_pos, 100), (x_pos + 20, 250), (0, 255, 0), -1)

    report_healthy = inspector.inspect_rack_frame(healthy_frame, expected_ports)
    logging.info(f"[Healthy Audit] Expected: {report_healthy['expected_ports']} | Detected Links: {report_healthy['detected_links']} | Score: {report_healthy['integrity_score']}% -> {report_healthy['status']}")

    # Simulate a degraded rack frame where 3 cables are unplugged / missing
    degraded_frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(expected_ports):
        if i in [2, 5, 7]:  # Unplugged ports
            continue
        x_pos = 50 + (i * 50)
        cv2.rectangle(degraded_frame, (x_pos, 100), (x_pos + 20, 250), (0, 255, 0), -1)

    report_degraded = inspector.inspect_rack_frame(degraded_frame, expected_ports)
    logging.info(f"[Degraded Audit] Expected: {report_degraded['expected_ports']} | Detected Links: {report_degraded['detected_links']} | Score: {report_degraded['integrity_score']}% -> {report_degraded['status']}")