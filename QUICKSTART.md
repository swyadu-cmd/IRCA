# 🎯 INTERGALACTIC RIKSBANKEN CHIP AUTHENTICATOR - QUICK START

## Three Modes Available

### 🚀 Launcher (All Modes)
```bash
python launcher.py
```
Select: 1=Simulator, 2=Camera, 3=Game

### 🎬 Simulator Mode
```bash
python main.py
```
Conveyor belt with automatic chip spawning

### 📸 Camera Mode
```bash
python camera_main.py
```
Real camera with calibration

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
- **R** - Reset stats | **Q** - Quit

### Camera (`camera_main.py`)
- **SPACE** - Capture/Pause | **R** - Reset
- **Q** - Quit

### Game (`game.py`)
- **1/2/3** - Spawn Gold/Silver/Bronze
- **C** - Clear all | **P** - Pause
- **R** - Reset | **Q** - Quit

## Requirements

- Python 3.8+
- OpenCV
- NumPy

Install: `pip install -r requirements.txt`

---

**All files are now in `chip_system/` folder - clean and organized!**
