# Changelog

**Authors**: Group 8 - Suneela, Sara, and Abhishek

## [1.0.0] - 2025-12-14

### Added
- **Intergalactic Riksbanken Chip Authenticator**: Complete authentication system
- **Simulator Mode**: Conveyor belt simulator with realistic chip physics
- **Camera Mode**: Real-time camera-based chip authentication system
- **Calibration System**: Interactive color calibration for Gold/Silver/Bronze chips
- **Value Calculation**: Automatic value computation based on chip type and digits
- **Fake Detection**: Identification of fake chips
- **Real-time Statistics**: Live tracking of total value, real/fake counts
- **Multiple Camera Support**: Webcam and Basler camera compatibility
- **Interactive Controls**: Keyboard shortcuts for spawning, pausing, resetting

### Features
- Green conveyor belt simulation (50% screen width, centered)
- Chips move perpendicular to belt direction
- HSV color-based detection
- Centroid tracking system
- FPS monitoring
- PNG image overlay with alpha blending
- Green background removal

### Value Calculation Rules
- **Gold**: Concatenate 3 digits × 10 (e.g., 752 → 7520 CR)
- **Silver**: Concatenate 3 digits as-is (e.g., 913 → 913 CR)
- **Bronze**: Multiply all 3 digits (e.g., 7×3×3 → 63 CR)

### Technical Stack
- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- HSV color space processing
- Alpha channel compositing
