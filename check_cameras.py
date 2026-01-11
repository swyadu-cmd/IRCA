"""
Camera Detection Diagnostic Tool
Checks for available webcams and Basler cameras
"""

import cv2
import sys
import os

print("\n" + "="*60)
print("🔍 CAMERA DETECTION DIAGNOSTIC")
print("="*60)

# Check pypylon availability
print("\n1. Checking Basler Support...")
try:
    from pypylon import pylon
    print("   ✅ pypylon installed")
    
    # Try to enumerate Basler cameras
    try:
        factory = pylon.TlFactory.GetInstance()
        devices = factory.EnumerateDevices()
        
        if len(devices) == 0:
            print("   ⚠️  No Basler cameras detected")
            print("\n   Possible reasons:")
            print("   - No Basler camera connected")
            print("   - Camera USB cable not plugged in")
            print("   - Pylon drivers not installed (download from baslerweb.com)")
            print("   - Camera in use by another application")
            print("   - Insufficient USB power or faulty cable")
        else:
            print(f"   ✅ Found {len(devices)} Basler camera(s):")
            for i, dev in enumerate(devices):
                print(f"      {i+1}. {dev.GetModelName()} (SN: {dev.GetSerialNumber()})")
    except Exception as e:
        print(f"   ❌ Error enumerating Basler cameras: {e}")
        
except ImportError:
    print("   ❌ pypylon not installed")
    print("   Install with: pip install pypylon")

# Check webcams
print("\n2. Checking Webcams...")
found_webcam = False
for i in range(5):  # Check first 5 indices
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            h, w = frame.shape[:2]
            print(f"   ✅ Webcam {i}: {w}x{h}")
            found_webcam = True
        cap.release()

if not found_webcam:
    print("   ⚠️  No webcams detected")
    print("   - Check if webcam is connected")
    print("   - Try closing other apps using the camera")

# Check sensorproject module
print("\n3. Checking Camera Setup Module...")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from sensorproject.camera_setup import CameraManager, BASLER_AVAILABLE
    print(f"   ✅ CameraManager imported successfully")
    print(f"   Basler support in module: {BASLER_AVAILABLE}")
except ImportError as e:
    print(f"   ❌ Failed to import CameraManager: {e}")

print("\n" + "="*60)
print("RECOMMENDATIONS:")
print("="*60)

# Give recommendations based on findings
try:
    from pypylon import pylon
    devices = pylon.TlFactory.GetInstance().EnumerateDevices()
    
    if len(devices) == 0:
        print("\n📌 For Basler Camera:")
        print("   1. Connect Basler camera via USB 3.0 or GigE")
        print("   2. Install Basler Pylon Software Suite:")
        print("      https://www.baslerweb.com/en/downloads/software-downloads/")
        print("   3. Test camera with Pylon Viewer application")
        print("   4. Then re-run this diagnostic")
        print("\n📌 To use Webcam instead:")
        print("   Run: python main.py --camera")
        print("   Select option 1 (Webcam)")
    else:
        print("\n✅ Basler camera ready!")
        print("   Run: python main.py --camera")
        print("   Select option 2 (Basler)")
except:
    pass

print("="*60 + "\n")
