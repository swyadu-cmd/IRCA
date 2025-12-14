# Intergalactic Riksbanken Chip Authenticator
## Project Summary

**Authors**: Group 8  
- **Suneela**
- **Sara**
- **Abhishek**

**Course**: STB600 Final Project 2025  
**Date**: December 14, 2025

---

## ✅ Project Complete!

### 🎯 Deliverables

1. **✅ Source Code** - All three operating modes implemented
2. **✅ Documentation** - Complete technical design document
3. **✅ Screenshots** - 7 demonstration images captured
4. **✅ User Guides** - Quick start and detailed usage instructions
5. **✅ Design Report** - 30-page comprehensive project document

---

## 📁 Project Structure

```
chip_system/                         # Main project directory
├── launcher.py                      # ⭐ Main entry point (all modes)
├── main.py                          # Conveyor belt simulator
├── camera_main.py                   # Real-time camera detection
├── game.py                          # Interactive manual testing
├── capture_screenshots.py           # Documentation utility
│
├── assets/                          # Chip template images
│   ├── gold.png                     # Gold chip with green background
│   ├── silver.png                   # Silver chip
│   └── bronze.png                   # Bronze chip
│
├── docs/                            # Documentation folder
│   ├── images/                      # 📸 Project screenshots
│   │   ├── 01_empty_conveyor.png
│   │   ├── 02_multiple_chips.png
│   │   ├── 03_gold_chip.png
│   │   ├── 04_silver_chip.png
│   │   ├── 05_bronze_chip.png
│   │   ├── 06_fake_chip.png
│   │   └── 07_full_simulation.png
│   ├── SCREENSHOTS.md               # Screenshot documentation
│   ├── CAMERA_USAGE.md              # Camera system guide
│   └── MIGRATION.md                 # Cleanup notes
│
├── README.md                        # Main documentation
├── DESIGN_DOCUMENT.md               # 📄 Complete technical report
├── QUICKSTART.md                    # Fast reference guide
├── CHANGELOG.md                     # Version history
├── COMMIT_SUMMARY.md                # Git commit preparation
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # MIT License
├── requirements.txt                 # Python dependencies
└── .gitignore                       # Git ignore rules
```

---

## 🚀 Three Operating Modes

### 1. Simulator Mode (`python main.py`)
- Conveyor belt with automatic chip spawning
- 60 FPS real-time simulation
- Perfect for algorithm testing

### 2. Camera Mode (`python camera_main.py`)
- Interactive color calibration
- Real-time chip detection
- Supports webcam and Basler cameras
- 30+ FPS processing

### 3. Interactive Game (`python game.py`)
- Manual chip spawning (keys 1/2/3)
- Static display for testing
- Grid background for placement
- Instant value feedback

### Unified Launcher (`python launcher.py`)
- Single entry point for all modes
- Interactive menu system
- Error handling and recovery

---

## 📊 System Capabilities

### Chip Authentication
- **Gold Chips**: Yellow, value = digits × 10
- **Silver Chips**: Gray, value = digits
- **Bronze Chips**: Orange, value = digits multiplied
- **Fake Chips**: Red, zero value

### Technical Features
- ✅ HSV color space detection
- ✅ Alpha channel transparency
- ✅ Real-time statistics tracking
- ✅ 60 FPS simulator, 30+ FPS camera
- ✅ Green background removal
- ✅ Automatic value calculation

---

## 📸 Screenshots Captured

All screenshots are located in `docs/images/`:

1. **01_empty_conveyor.png** - Initial state with green belt
2. **02_multiple_chips.png** - Multiple chips in motion
3. **03_gold_chip.png** - Gold chip detection
4. **04_silver_chip.png** - Silver chip detection
5. **05_bronze_chip.png** - Bronze chip detection
6. **06_fake_chip.png** - Fake chip identification
7. **07_full_simulation.png** - Complete system view

View all screenshots with descriptions in [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md)

---

## 📚 Documentation Files

### User Documentation
- **README.md** (140 lines) - Complete project overview
- **QUICKSTART.md** (50 lines) - Fast reference
- **docs/SCREENSHOTS.md** (100 lines) - Visual demonstrations

### Technical Documentation
- **DESIGN_DOCUMENT.md** (700+ lines) - Complete technical design & project report
  - Executive summary
  - System architecture
  - Algorithm descriptions
  - Performance analysis
  - Code structure
  - Future enhancements

### Development Documentation
- **docs/CAMERA_USAGE.md** (200+ lines) - Camera system guide
- **CONTRIBUTING.md** (80 lines) - Contribution guidelines
- **CHANGELOG.md** (40 lines) - Version history
- **COMMIT_SUMMARY.md** (150 lines) - Git preparation

---

## 🔧 Technical Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.8+ |
| Vision | OpenCV | 4.8.0+ |
| Computing | NumPy | 1.24.0+ |
| Color Space | HSV | OpenCV |
| Camera | Webcam/Basler | Any |

---

## 🎯 Key Achievements

✅ **Multi-Mode System**: Simulator, Camera, Game modes  
✅ **Real-Time Processing**: 30-60 FPS performance  
✅ **Adaptive Calibration**: Interactive color learning  
✅ **Complete Documentation**: 30+ page technical report  
✅ **Visual Demonstrations**: 7 professional screenshots  
✅ **Clean Architecture**: Modular, extensible design  
✅ **User-Friendly**: Intuitive controls and feedback  

---

## 📖 How to Run

### Quick Start
```bash
# Navigate to project
cd chip_system

# Install dependencies
pip install -r requirements.txt

# Run launcher (recommended)
python launcher.py

# Select mode:
# 1 - Simulator
# 2 - Camera (with calibration)
# 3 - Interactive Game
```

### Individual Modes
```bash
# Simulator only
python main.py

# Camera only
python camera_main.py

# Game only
python game.py
```

---

## 🎓 Project Report

The complete technical design document is available in:
📄 **[DESIGN_DOCUMENT.md](DESIGN_DOCUMENT.md)**

Includes:
- System architecture diagrams
- Algorithm explanations with formulas
- Performance benchmarks
- Code structure analysis
- Testing & validation results
- Future enhancement roadmap

---

## 👥 Group 8 Members

| Name | Role | Contributions |
|------|------|---------------|
| **Suneela** | Team Member | System development |
| **Sara** | Team Member | System development |
| **Abhishek** | Team Member | System development |

---

## 📝 License

MIT License - Copyright (c) 2025 Group 8 (Suneela, Sara, Abhishek)

---

## 🌟 Project Status: COMPLETE ✅

All deliverables completed:
- ✅ Working software (3 modes)
- ✅ Technical documentation
- ✅ Project screenshots
- ✅ User guides
- ✅ Design report
- ✅ Source code organization
- ✅ Ready for submission

---

**Intergalactic Riksbanken Chip Authenticator**  
*Authenticating the future, one chip at a time* 🚀

**STB600 Final Project 2025**  
**Group 8**: Suneela, Sara, Abhishek
