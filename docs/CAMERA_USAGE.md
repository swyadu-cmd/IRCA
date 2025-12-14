# Camera System Usage Guide

## Overview

The camera system integrates real camera input with chip detection, tracking, and value calculation.

## System Architecture

```
Camera Input → Color Detection → Digit Extraction → Value Calculation → Tracking → Display
```

## Getting Started

### 1. Choose Your Mode

**Simulator Mode** - No camera required, uses simulated conveyor belt
```bash
python main.py
```

**Camera Mode** - Uses real camera for detection
```bash
python camera_main.py
```

### 2. Camera Selection

When running camera mode, you'll be prompted:
```
1. Webcam (default)
2. Basler camera
```

- Select **1** for standard USB webcams
- Select **2** for Basler professional cameras

### 3. Detection Process

The system automatically:
1. **Captures** frames from camera
2. **Converts** to HSV color space
3. **Detects** Gold, Silver, Bronze chips by color
4. **Extracts** 3-digit numbers from each chip
5. **Calculates** values based on chip type
6. **Identifies** fake chips (shape/color anomalies)
7. **Tracks** chips across frames
8. **Displays** results in real-time

## Color Detection Ranges

### Gold Chips
- **HSV Range**: H=20-35, S=100-255, V=100-255
- **Display Color**: Yellow
- **Value Rule**: Concatenate 3 digits × 10

### Silver Chips
- **HSV Range**: H=0-180, S=0-50, V=100-255
- **Display Color**: Gray
- **Value Rule**: Concatenate 3 digits as-is

### Bronze Chips
- **HSV Range**: H=5-25, S=50-255, V=50-200
- **Display Color**: Orange
- **Value Rule**: Multiply all 3 digits

## Lighting Recommendations

For best detection results:

1. **Uniform Lighting**: Avoid shadows and reflections
2. **White/Green Background**: Provides good contrast
3. **Avoid Extreme Brightness**: May wash out colors
4. **Avoid Extreme Darkness**: May lose color information

## Calibration Tips

If detection is poor:

1. **Adjust Color Ranges**: Edit HSV ranges in `camera_main.py`
   ```python
   'GOLD': {
       'lower': np.array([20, 100, 100]),  # Adjust these
       'upper': np.array([35, 255, 255]),  # Adjust these
   }
   ```

2. **Adjust Area Thresholds**: Change min/max area
   ```python
   self.min_area = 2000  # Minimum chip size
   self.max_area = 50000  # Maximum chip size
   ```

3. **Check Camera Resolution**: Ensure camera is set to 1280x720 or higher

## Integration with Existing System

To use the full detection pipeline from `sensorproject/`:

1. **Ensure dependencies are installed**:
   ```bash
   pip install pypylon  # For Basler cameras
   pip install pytesseract  # For OCR
   ```

2. **Run the full system**:
   ```bash
   python camera_main.py
   ```

3. **The system uses**:
   - `camera_setup.py` - Camera management
   - `centroid_tracker.py` - Object tracking
   - Color detection from `camera_main.py`

## Troubleshooting

### Camera Not Found
```
ERROR: Could not open webcam at index 0
```
**Solution**: Try different indices (1, 2, etc.)

### No Chips Detected
**Possible Causes**:
- Poor lighting
- Colors outside HSV range
- Chips too small/large

**Solution**: Adjust HSV ranges and area thresholds

### Low FPS
**Possible Causes**:
- High resolution
- Slow processing

**Solution**: 
- Reduce camera resolution
- Process every Nth frame

### Fake Detection Not Working
**Note**: Current version uses random 20% fake rate for demo.

**To implement real fake detection**:
- Add shape analysis (circularity check)
- Add color consistency check
- Add digit OCR validation

## Advanced Features

### Add OCR for Real Digit Recognition

Replace the random digit generation with actual OCR:

```python
import pytesseract

def extract_digits(self, roi):
    # Preprocess
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # OCR
    text = pytesseract.image_to_string(thresh, config='--psm 7 digits')
    digits = ''.join(filter(str.isdigit, text))
    
    if len(digits) >= 3:
        return (int(digits[0]), int(digits[1]), int(digits[2]))
    return (0, 0, 0)
```

### Save Detection Results

Add logging to save detections:

```python
import json
from datetime import datetime

def save_detection(self, chip_info):
    with open('detections.json', 'a') as f:
        chip_info['timestamp'] = datetime.now().isoformat()
        json.dump(chip_info, f)
        f.write('\n')
```

## Performance Optimization

### 1. Skip Frames
Process every Nth frame:
```python
frame_count = 0
if frame_count % 3 == 0:  # Process every 3rd frame
    detections = self.detector.detect_chips(frame)
frame_count += 1
```

### 2. Region of Interest
Only process conveyor belt area:
```python
roi = frame[100:620, 320:960]  # Focus on belt region
detections = self.detector.detect_chips(roi)
```

### 3. Multi-threading
Separate capture and processing threads for better performance.

## Next Steps

1. ✅ Camera system integrated
2. ✅ Color detection working
3. ⚠️ Add real OCR for digit recognition
4. ⚠️ Implement proper fake detection
5. ⚠️ Add calibration UI
6. ⚠️ Add export/logging features

## Support

For issues or questions:
- Check HSV color ranges match your lighting
- Verify camera is working: `python -c "import cv2; cv2.VideoCapture(0).read()"`
- Ensure all dependencies are installed
