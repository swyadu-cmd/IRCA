# Basler Camera Support

## Overview
The chip authenticator now supports both **standard webcams** (via OpenCV) and **Basler industrial cameras** (via pypylon).

## Changes Made

### 1. Updated `sensorproject/camera_setup.py`
The `CameraManager` class now supports dual camera backends:

**New Parameters:**
```python
CameraManager(
    camera_type="WEBCAM",  # or "BASLER"
    camera_index=0,         # for webcam
    width=1280,
    height=720
)
```

**Key Changes:**
- Added `camera_type` parameter to constructor
- Implemented separate methods for each camera type:
  - `_open_webcam()` / `_open_basler()`
  - `_read_webcam()` / `_read_basler()`
  - `_get_webcam_properties()` / `_get_basler_properties()`
  - `_set_webcam_property()` / `_set_basler_property()`
- Added pypylon import with graceful fallback
- Basler-specific features:
  - Automatic first device detection
  - Configurable width/height
  - RGB8 pixel format
  - LatestImageOnly grab strategy
  - Automatic BGR8 conversion for OpenCV compatibility

### 2. Updated `chip_system/camera_main.py`

**New Features:**
- Checks for pypylon availability at startup
- Camera selection menu shows Basler availability status:
  - `2. Basler camera ✓` (if pypylon installed)
  - `2. Basler camera ✗ (pypylon not installed)` (if missing)
- Automatic fallback to webcam if Basler selected but pypylon missing
- Explicit `camera.open()` call for proper initialization
- Passes `camera_type` parameter to CameraManager

## Installation

### For Webcam Only (No Changes Needed)
```bash
# Already installed with requirements.txt
pip install opencv-python
```

### For Basler Camera Support
```bash
# Install Basler pypylon SDK
pip install pypylon
```

## Usage

### Running with Webcam (Default)
```bash
cd chip_system
python main.py --camera
# Select option 1 at the prompt
```

### Running with Basler Camera
```bash
cd chip_system
python main.py --camera
# Select option 2 at the prompt
```

The system will automatically:
1. Check if pypylon is installed
2. Connect to the first available Basler camera
3. Configure resolution to 1280x720
4. Start grabbing frames in BGR format

## Troubleshooting

### "pypylon not installed" Error
```bash
pip install pypylon
```

### Basler Camera Not Detected
1. Ensure Basler camera is connected via USB3 or GigE
2. Install Basler Pylon Software Suite from: https://www.baslerweb.com/
3. Test camera with Pylon Viewer application first
4. Check camera permissions/drivers

### Camera Opens But No Frames
- For Basler: Check that `PixelFormat` supports RGB8
- For Webcam: Check camera isn't in use by another application

## API Compatibility

Both camera types expose the same interface:
```python
# Initialize
camera = CameraManager(camera_type="BASLER", width=1280, height=720)

# Open connection
success = camera.open()

# Read frames
success, frame = camera.read()  # Returns BGR numpy array

# Get properties
props = camera.get_properties()

# Set properties
camera.set_property('exposure', 10000)  # For Basler
camera.set_property('brightness', 128)   # For webcam

# Release
camera.release()
```

## Performance Notes

### Basler Cameras
- **Pros:** Higher frame rates, better image quality, industrial-grade reliability
- **Cons:** Requires pypylon, more expensive hardware
- **Typical FPS:** 30-100+ depending on model

### Webcams
- **Pros:** No additional software, cheaper, widely available
- **Cons:** Lower frame rates, consumer-grade quality
- **Typical FPS:** 15-30

## File Locations

```
Sensor_Project/
├── chip_system/
│   ├── camera_main.py          # Updated with Basler support
│   └── main.py                 # Entry point with --camera flag
└── sensorproject/
    └── camera_setup.py         # Updated CameraManager class
```

## Git Commit Summary

**Commit 1:** Integrated camera system with main authenticator
- Added `--camera` flag to main.py
- Fixed CameraManager API compatibility

**Commit 2:** Added Basler camera support
- Extended CameraManager for dual backends
- Added pypylon detection and graceful fallback
- Updated camera selection menu

## Next Steps

To test Basler camera support:
1. Connect Basler camera
2. Install pypylon: `pip install pypylon`
3. Run: `python main.py --camera`
4. Select option 2
5. System should display camera model and serial number on connection
