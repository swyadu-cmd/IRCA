# 🎯 INTERGALACTIC RIKSBANKEN CHIP AUTHENTICATOR - QUICK START

## Three Modes Available

### 🚀 Launcher (All Modes)
```bash
python launcher.py
```
Select: 1=Simulator, 2=Camera, 3=Game

### 🎬 Simulator Mode (Default)
```bash
python main.py
```
Conveyor belt with automatic chip spawning

**With Setup Mode:**
```bash
python main.py --setup
```
Interactive setup for conveyor boundary and scan line position

### 📸 Camera Mode (NEW!)
```bash
python main.py --camera
```
Real camera with chip detection and calibration
- Supports **Webcam** (standard OpenCV)
- Supports **Basler** industrial cameras (requires pypylon)
- Interactive calibration for each chip type

**Alternative:** Direct launch with `python camera_main.py`

### 🎮 Interactive Game
```bash
python game.py
```
Manual chip spawning and testing

## What It Does

✅ Green conveyor belt (50% width, centered)
✅ Chips move straight down
✅ Auto-detects Gold, Silver, Bronze chips
✅ Calculates values (Gold×10, Silver direct, Bronze××)
✅ Tracks real vs fake chips
✅ Real-time statistics

## Controls

### Simulator (`main.py`)
- **S** - Spawn chip | **B** - Burst (5 chips)
- **C** - Clear all | **P** - Pause/Resume
- **T** - Test Mode | **R** - Reset stats | **Q** - Quit

### Setup Mode (`--setup` flag)
**Boundary Setup Options:**
1. **Manual Click** - Click left and right edges on screen
2. **Auto-detect** - Automatically find green conveyor belt
3. **Manual Input** - Enter X coordinate and width
4. **Use Defaults** - 50% width, centered

**Scan Line Setup:**
1. **Click Position** - Click to set scan line Y position
2. **Manual Input** - Enter Y coordinate
3. **Use Default** - Middle of screen

### Camera (`main.py --camera`)
- **Camera Selection** - Choose Webcam (1) or Basler (2)
- **Calibration** - Place each chip type in center, press SPACE to capture
- **SPACE** - Pause/Resume detection
- **R** - Reset statistics
- **Q** - Quit

### Game (`game.py`)
- **1/2/3** - Spawn Gold/Silver/Bronze
- **C** - Clear all | **P** - Pause
- **R** - Reset | **Q** - Quit

## Requirements

### Basic (Simulator & Game)
- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy

```bash
pip install -r requirements.txt
```

### Camera Mode - Webcam
- Same as basic requirements
- Any USB/built-in webcam

### Camera Mode - Basler (Optional)
- All basic requirements
- Basler camera hardware
- Pypylon SDK

```bash
pip install pypylon
```

📖 **See [BASLER_CAMERA_SETUP.md](BASLER_CAMERA_SETUP.md) for detailed camera setup**

---

**All files are now in `chip_system/` folder - clean and organized!**
