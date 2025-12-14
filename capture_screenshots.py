"""
Screenshot Capture Utility
Captures screenshots from the simulator for documentation
"""

import cv2
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import ConveyorSimulator

def capture_screenshots():
    """Capture various screenshots from the simulator"""
    
    print("\n📸 Screenshot Capture Utility")
    print("="*60)
    print("Capturing screenshots for documentation...")
    print("="*60 + "\n")
    
    # Create simulator
    sim = ConveyorSimulator(width=1280, height=720, conveyor_speed=3)
    
    screenshots = []
    
    # Capture initial state
    print("1. Capturing empty conveyor...")
    sim.chips.clear()  # Make sure it's empty
    frame = sim.render_frame()
    screenshots.append(("01_empty_conveyor.png", frame.copy()))
    print("   ✓ Empty conveyor captured")
    
    # Screenshot 2: Multiple chips on conveyor
    print("2. Capturing with multiple chips...")
    sim.chips.clear()
    # Manually spawn multiple chips at different positions
    for i in range(6):
        sim.spawn_chip()
    
    # Position them nicely along the conveyor
    positions = [(320, 100), (450, 200), (600, 150), (380, 350), (700, 280), (520, 450)]
    for i, pos in enumerate(positions):
        if i < len(sim.chips):
            sim.chips[i]['x'] = pos[0]
            sim.chips[i]['y'] = pos[1]
    
    frame = sim.render_frame()
    screenshots.append(("02_multiple_chips.png", frame.copy()))
    print("   ✓ Multiple chips captured")
    
    # Screenshot 3-5: Individual chip types
    print("3. Capturing Gold chip...")
    sim.chips.clear()
    sim.spawn_chip()
    sim.chips[0]['type'] = 'GOLD'
    sim.chips[0]['chip_type'] = 'GOLD'
    sim.chips[0]['x'] = 400
    sim.chips[0]['y'] = 250
    frame = sim.render_frame()
    screenshots.append(("03_gold_chip.png", frame.copy()))
    print("   ✓ Gold chip captured")
    
    print("4. Capturing Silver chip...")
    sim.chips.clear()
    sim.spawn_chip()
    sim.chips[0]['type'] = 'SILVER'
    sim.chips[0]['chip_type'] = 'SILVER'
    sim.chips[0]['x'] = 500
    sim.chips[0]['y'] = 280
    frame = sim.render_frame()
    screenshots.append(("04_silver_chip.png", frame.copy()))
    print("   ✓ Silver chip captured")
    
    print("5. Capturing Bronze chip...")
    sim.chips.clear()
    sim.spawn_chip()
    sim.chips[0]['type'] = 'BRONZE'
    sim.chips[0]['chip_type'] = 'BRONZE'
    sim.chips[0]['x'] = 600
    sim.chips[0]['y'] = 320
    frame = sim.render_frame()
    screenshots.append(("05_bronze_chip.png", frame.copy()))
    print("   ✓ Bronze chip captured")
    
    print("6. Capturing fake chip...")
    sim.chips.clear()
    sim.spawn_chip()
    sim.chips[0]['authentic'] = False
    sim.chips[0]['value'] = 0
    sim.chips[0]['x'] = 450
    sim.chips[0]['y'] = 300
    frame = sim.render_frame()
    screenshots.append(("06_fake_chip.png", frame.copy()))
    print("   ✓ Fake chip captured")
    
    # Screenshot: Full simulation
    print("7. Creating full simulation scene...")
    sim.chips.clear()
    for _ in range(5):
        sim.spawn_chip()
    
    # Spread them out nicely
    positions = [(300, 150), (500, 300), (650, 450), (400, 550), (750, 200)]
    for i, pos in enumerate(positions):
        if i < len(sim.chips):
            sim.chips[i]['x'] = pos[0]
            sim.chips[i]['y'] = pos[1]
    
    frame = sim.render_frame()
    screenshots.append(("07_full_simulation.png", frame.copy()))
    print("   ✓ Full simulation captured")
    
    # Save all screenshots
    print("\n💾 Saving screenshots...")
    output_dir = "docs/images"
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, image in screenshots:
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, image)
        print(f"   ✓ Saved: {filename}")
    
    print(f"\n✅ Captured {len(screenshots)} screenshots")
    print(f"📁 Location: {output_dir}/")
    print("="*60 + "\n")

if __name__ == "__main__":
    capture_screenshots()
