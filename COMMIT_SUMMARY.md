# Intergalactic Riksbanken Chip Authenticator - Commit Summary

## Changes Made

### ✅ Project Cleanup
- Removed old `sensorproject/` directory and backup files
- Removed empty `modules/` directory  
- Consolidated all code into `chip_system/`
- Created clean directory structure

### ✨ New Features Added

#### 1. Unified Launcher (`launcher.py`)
- Main entry point for all three modes
- Interactive menu system
- Error handling and graceful returns to menu

#### 2. Interactive Game Mode (`game.py`)
- Manual chip spawning with keyboard (1=Gold, 2=Silver, 3=Bronze)
- Static chip placement on grid background
- Real-time statistics tracking
- Perfect for testing without camera hardware

#### 3. Enhanced Camera System (`camera_main.py`)
- Interactive color calibration
- User places each chip type for auto-calibration
- Learns HSV color ranges automatically
- Supports webcam and Basler cameras

#### 4. Conveyor Simulator (`main.py`)
- Realistic belt physics (50% width, centered)
- Perpendicular chip movement
- Auto-spawning with real/fake distribution
- Green background removal with alpha blending

### 📚 Documentation Added

- **README.md** - Complete project documentation
- **QUICKSTART.md** - Fast reference for all modes
- **CHANGELOG.md** - Version history and features
- **LICENSE** - MIT License
- **CONTRIBUTING.md** - Contribution guidelines
- **docs/CAMERA_USAGE.md** - Detailed camera guide
- **docs/MIGRATION.md** - Cleanup notes

### 🎯 Three Operating Modes

| Mode | File | Description | Use Case |
|------|------|-------------|----------|
| **Simulator** | `main.py` | Conveyor belt simulation | Testing algorithms, no hardware needed |
| **Camera** | `camera_main.py` | Real-time detection | Production use with physical chips |
| **Game** | `game.py` | Interactive testing | Manual testing, debugging, demonstrations |

### 🎮 Complete Control Schemes

**Launcher**: 1/2/3 to select mode, Q to quit

**Simulator**: S (spawn), B (burst), C (clear), P (pause), R (reset), Q (quit)

**Camera**: SPACE (capture/pause), R (reset), Q (quit)

**Game**: 1/2/3 (spawn chips), C (clear), P (pause), R (reset), Q (quit)

### 📊 Value Calculation Rules

- **GOLD**: 3 digits × 10 (e.g., 752 → 7520 CR)
- **SILVER**: 3 digits (e.g., 913 → 913 CR)  
- **BRONZE**: 3 digits multiplied (e.g., 7×3×3 → 63 CR)
- **FAKE**: 0 value (displayed in red)

### 🔧 Technical Stack

- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- HSV color space processing
- Alpha channel compositing
- Centroid tracking (camera mode)

### 📁 Final Structure

```
chip_system/
├── launcher.py          # ⭐ Main entry point
├── main.py              # Simulator
├── camera_main.py       # Camera detection
├── game.py              # Interactive game
├── requirements.txt
├── .gitignore
├── README.md
├── QUICKSTART.md
├── CHANGELOG.md
├── LICENSE
├── CONTRIBUTING.md
├── assets/
│   ├── gold.png
│   ├── silver.png
│   └── bronze.png
└── docs/
    ├── CAMERA_USAGE.md
    └── MIGRATION.md
```

### ✅ Ready for Commit

All files cleaned, documented, and tested. Project is production-ready.

## Authors

**Group 8**: Suneela, Sara, and Abhishek

## Commit Message Suggestion

```
feat: Intergalactic Riksbanken Chip Authenticator with three modes

Authors: Group 8 (Suneela, Sara, Abhishek)

- Add unified launcher with simulator, camera, and game modes
- Implement interactive color calibration for camera system
- Add interactive game mode for manual chip testing
- Clean up project structure and remove legacy code
- Add comprehensive documentation (README, guides, changelog)
- Support webcam and Basler cameras
- Implement value calculation for Gold/Silver/Bronze chips
- Add real/fake detection with statistics tracking

Closes #1
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run launcher (recommended)
python launcher.py

# Or run individual modes
python main.py          # Simulator
python camera_main.py   # Camera
python game.py          # Game
```
