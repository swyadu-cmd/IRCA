"""
Intergalactic Riksbanken Chip Authenticator - Camera System
Real-time camera-based chip authentication and value calculation
"""

import cv2
import time
import numpy as np
from collections import deque
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from sensorproject.camera_setup import CameraManager
    from sensorproject.centroid_tracker import CentroidTracker
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    print("⚠️  Warning: Camera modules not found. Will use demo mode.")


class ChipDetector:
    """Detect and classify chips by color"""
    
    def __init__(self, color_ranges=None):
        """Initialize chip detector"""
        # Default HSV color ranges (will be overridden by calibration)
        if color_ranges is None:
            self.color_ranges = {
                'GOLD': {
                    'lower': np.array([20, 100, 100]),
                    'upper': np.array([35, 255, 255]),
                    'bgr_color': (0, 215, 255),  # Display color
                    'value_multiplier': 10
                },
                'SILVER': {
                    'lower': np.array([0, 0, 100]),
                    'upper': np.array([180, 50, 255]),
                    'bgr_color': (200, 200, 200),
                    'value_multiplier': 1
                },
                'BRONZE': {
                    'lower': np.array([5, 50, 50]),
                    'upper': np.array([25, 255, 200]),
                    'bgr_color': (0, 100, 200),
                    'value_multiplier': 0  # Special multiply rule
                }
            }
        else:
            self.color_ranges = color_ranges
        
        self.min_area = 2000
        self.max_area = 50000
    
    def calibrate_chip_color(self, frame, chip_type):
        """
        Calibrate color range for a chip type by sampling from frame
        
        Args:
            frame: BGR image with chip visible
            chip_type: 'GOLD', 'SILVER', or 'BRONZE'
            
        Returns:
            dict: Color range info with lower/upper HSV bounds
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get center region (where chip should be)
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        roi_size = 100
        
        # Extract ROI
        roi = hsv[center_y-roi_size:center_y+roi_size, 
                  center_x-roi_size:center_x+roi_size]
        
        # Calculate mean and std of HSV values
        mean_hsv = np.mean(roi.reshape(-1, 3), axis=0)
        std_hsv = np.std(roi.reshape(-1, 3), axis=0)
        
        # Create bounds with tolerance
        tolerance = [15, 50, 50]  # H, S, V tolerance
        lower = np.maximum(mean_hsv - std_hsv - tolerance, [0, 0, 0])
        upper = np.minimum(mean_hsv + std_hsv + tolerance, [180, 255, 255])
        
        return {
            'lower': lower.astype(np.uint8),
            'upper': upper.astype(np.uint8),
            'mean_hsv': mean_hsv
        }
        
    def detect_chips(self, frame):
        """
        Detect chips in frame by color
        
        Args:
            frame: BGR image
            
        Returns:
            detections: List of dicts with chip info
        """
        # Preprocess
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        detections = []
        
        # Detect each chip type
        for chip_type, color_info in self.color_ranges.items():
            # Create color mask
            mask = cv2.inRange(hsv, color_info['lower'], color_info['upper'])
            
            # Clean up mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by area
                if area < self.min_area or area > self.max_area:
                    continue
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Extract ROI for digit detection
                roi = frame[y:y+h, x:x+w]
                digits = self.extract_digits(roi)
                value = self.calculate_value(chip_type, digits)
                
                # Check if fake (random 20% chance for demo)
                is_fake = np.random.random() < 0.2
                
                detections.append({
                    'chip_type': chip_type,
                    'bbox': (x, y, w, h),
                    'centroid': (x + w//2, y + h//2),
                    'area': area,
                    'digits': digits,
                    'value': value if not is_fake else 0,
                    'is_fake': is_fake,
                    'color': color_info['bgr_color']
                })
        
        return detections
    
    def extract_digits(self, roi):
        """
        Extract 3 digits from chip ROI
        
        Args:
            roi: Chip region of interest
            
        Returns:
            tuple: (d1, d2, d3)
        """
        # Simple random digits for now (can be replaced with OCR)
        # In production, use pytesseract or deep learning model
        return (np.random.randint(1, 10), np.random.randint(0, 10), np.random.randint(0, 10))
    
    def calculate_value(self, chip_type, digits):
        """
        Calculate chip value based on type and digits
        
        Args:
            chip_type: 'GOLD', 'SILVER', or 'BRONZE'
            digits: Tuple of (d1, d2, d3)
            
        Returns:
            int: Chip value
        """
        d1, d2, d3 = digits
        
        if chip_type == 'GOLD':
            # Concatenate and multiply by 10
            return int(f"{d1}{d2}{d3}") * 10
        elif chip_type == 'SILVER':
            # Concatenate as-is
            return int(f"{d1}{d2}{d3}")
        elif chip_type == 'BRONZE':
            # Multiply all digits
            return d1 * d2 * d3
        
        return 0


class CameraChipSystem:
    """Main camera-based chip detection system"""
    
    def __init__(self, camera_type="WEBCAM", webcam_index=0):
        """
        Initialize system
        
        Args:
            camera_type: "BASLER" or "WEBCAM"
            webcam_index: Camera index for webcam
        """
        print("\n" + "="*60)
        print("🎬 INTERGALACTIC RIKSBANKEN CHIP AUTHENTICATOR")
        print("         Camera Detection System")
        print("="*60)
        
        # Initialize camera
        if CAMERA_AVAILABLE:
            print(f"[1/4] Connecting to {camera_type}...")
            self.camera = CameraManager(
                camera_type=camera_type,
                webcam_index=webcam_index,
                width=1280,
                height=720,
                fps=30
            )
        else:
            print("[1/4] Camera unavailable - using demo mode")
            self.camera = None
        
        # Calibrate chip colors
        print("[2/4] Calibrating chip colors...")
        color_ranges = None
        if self.camera:
            color_ranges = self.calibrate_colors()
        
        # Initialize detector
        print("[3/4] Initializing chip detector...")
        self.detector = ChipDetector(color_ranges=color_ranges)
        
        # Initialize tracker
        print("[4/4] Initializing tracking system...")
        if CAMERA_AVAILABLE:
            self.tracker = CentroidTracker(maxDisappeared=30, maxDistance=50)
        else:
            self.tracker = None
        
        # Stats
        self.total_value = 0
        self.real_count = 0
        self.fake_count = 0
        self.fps_queue = deque(maxlen=30)
        
        print("\n✅ System ready!")
        print("="*60)
        print("\nControls:")
        print("  Q - Quit")
        print("  R - Reset statistics")
        print("  SPACE - Pause/Resume")
        print("="*60 + "\n")
    
    def calibrate_colors(self):
        """
        Calibrate colors for each chip type
        
        Returns:
            dict: Color ranges for each chip type
        """
        print("\n" + "="*60)
        print("📸 CHIP AUTHENTICATOR CALIBRATION")
        print("="*60)
        print("\nPlace each chip in the CENTER of the camera view.")
        print("Press SPACE to capture when ready.")
        print("="*60 + "\n")
        
        color_ranges = {}
        chip_types = [
            ('GOLD', (0, 215, 255), 10),
            ('SILVER', (200, 200, 200), 1),
            ('BRONZE', (0, 100, 200), 0)
        ]
        
        temp_detector = ChipDetector()
        
        for chip_type, bgr_color, multiplier in chip_types:
            print(f"\n🎯 Calibrating {chip_type} chip...")
            print(f"   1. Place {chip_type} chip in CENTER of camera")
            print(f"   2. Press SPACE to capture")
            
            # Show live preview
            while True:
                success, frame = self.camera.read_frame()
                if not success:
                    continue
                
                # Draw crosshair in center
                h, w = frame.shape[:2]
                center_x, center_y = w // 2, h // 2
                cv2.circle(frame, (center_x, center_y), 100, (0, 255, 0), 2)
                cv2.line(frame, (center_x-120, center_y), (center_x+120, center_y), (0, 255, 0), 2)
                cv2.line(frame, (center_x, center_y-120), (center_x, center_y+120), (0, 255, 0), 2)
                
                # Add instructions
                cv2.putText(frame, f"Calibrating: {chip_type}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                cv2.putText(frame, "Place chip in GREEN CIRCLE", (20, 80),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, "Press SPACE to capture", (20, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow("Calibration", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):
                    # Capture and calibrate
                    color_info = temp_detector.calibrate_chip_color(frame, chip_type)
                    color_ranges[chip_type] = {
                        'lower': color_info['lower'],
                        'upper': color_info['upper'],
                        'bgr_color': bgr_color,
                        'value_multiplier': multiplier
                    }
                    
                    mean_hsv = color_info['mean_hsv']
                    print(f"   ✅ {chip_type} captured!")
                    print(f"      Mean HSV: H={mean_hsv[0]:.1f}, S={mean_hsv[1]:.1f}, V={mean_hsv[2]:.1f}")
                    print(f"      Range: {color_info['lower']} - {color_info['upper']}")
                    time.sleep(0.5)
                    break
                elif key == ord('q'):
                    print("   ⚠️  Calibration cancelled - using default ranges")
                    cv2.destroyWindow("Calibration")
                    return None
        
        cv2.destroyWindow("Calibration")
        
        print("\n✅ Calibration complete!")
        print("="*60 + "\n")
        
        return color_ranges
    
    def draw_detections(self, frame, detections):
        """Draw detections on frame"""
        output = frame.copy()
        
        for det in detections:
            x, y, w, h = det['bbox']
            chip_type = det['chip_type']
            value = det['value']
            is_fake = det['is_fake']
            color = det['color']
            digits = det['digits']
            
            # Choose color (red for fake)
            draw_color = (0, 0, 255) if is_fake else color
            
            # Draw bounding box
            cv2.rectangle(output, (x, y), (x+w, y+h), draw_color, 2)
            
            # Draw chip type
            label = f"{chip_type}"
            if is_fake:
                label += " [FAKE]"
            
            cv2.putText(output, label, (x, y-25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, draw_color, 2)
            
            # Draw digits
            digit_str = f"{digits[0]}{digits[1]}{digits[2]}"
            cv2.putText(output, digit_str, (x, y-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, draw_color, 1)
            
            # Draw value
            if not is_fake:
                cv2.putText(output, f"{value} CR", (x, y+h+20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return output
    
    def draw_stats(self, frame):
        """Draw statistics panel"""
        h, w = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        
        # Draw text
        y_offset = 40
        cv2.putText(frame, f"Total Value: {self.total_value} CR", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        y_offset += 30
        cv2.putText(frame, f"Real Chips: {self.real_count}", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)
        
        y_offset += 30
        cv2.putText(frame, f"Fake Chips: {self.fake_count}", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # FPS
        if self.fps_queue:
            fps = sum(self.fps_queue) / len(self.fps_queue)
            y_offset += 30
            cv2.putText(frame, f"FPS: {fps:.1f}", (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Main processing loop"""
        paused = False
        
        print("🎥 Starting camera feed...\n")
        
        while True:
            frame_start = time.time()
            
            # Capture frame
            if self.camera:
                success, frame = self.camera.read_frame()
                if not success or frame is None:
                    print("❌ Failed to capture frame")
                    break
            else:
                # Demo mode - create blank frame
                frame = np.zeros((720, 1280, 3), dtype=np.uint8)
                cv2.putText(frame, "DEMO MODE - Camera not available", (300, 360),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            
            if not paused and self.camera:
                # Detect chips
                detections = self.detector.detect_chips(frame)
                
                # Update statistics
                for det in detections:
                    if det['is_fake']:
                        self.fake_count += 1
                    else:
                        self.real_count += 1
                        self.total_value += det['value']
                
                # Draw detections
                frame = self.draw_detections(frame, detections)
            
            # Draw stats
            frame = self.draw_stats(frame)
            
            # Show frame
            cv2.imshow("Intergalactic Riksbanken Chip Authenticator", frame)
            
            # Calculate FPS
            frame_time = time.time() - frame_start
            if frame_time > 0:
                self.fps_queue.append(1.0 / frame_time)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n👋 Shutting down...")
                break
            elif key == ord('r'):
                print("🔄 Resetting statistics...")
                self.total_value = 0
                self.real_count = 0
                self.fake_count = 0
            elif key == ord(' '):
                paused = not paused
                print(f"{'⏸️  Paused' if paused else '▶️  Resumed'}")
        
        # Cleanup
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        
        print(f"\n📊 Final Statistics:")
        print(f"   Total Value: {self.total_value} CR")
        print(f"   Real Chips: {self.real_count}")
        print(f"   Fake Chips: {self.fake_count}")
        print("\n✅ System shutdown complete\n")


def main():
    """Main entry point"""
    # Ask user for camera type
    print("\n" + "="*60)
    print("CAMERA SELECTION")
    print("="*60)
    print("1. Webcam (default)")
    print("2. Basler camera")
    print("="*60)
    
    choice = input("\nSelect camera type (1/2) [1]: ").strip()
    
    if choice == "2":
        camera_type = "BASLER"
    else:
        camera_type = "WEBCAM"
    
    # Initialize and run system
    system = CameraChipSystem(camera_type=camera_type, webcam_index=0)
    system.run()


if __name__ == "__main__":
    main()
