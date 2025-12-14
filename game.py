"""
Intergalactic Riksbanken Chip Authenticator - Interactive Game
Manually spawn and authenticate chips with keyboard controls
"""

import cv2
import numpy as np
import time
import random
from collections import deque


class ChipGame:
    """Interactive game for manual chip testing"""
    
    def __init__(self, width=1280, height=720):
        """Initialize game"""
        self.width = width
        self.height = height
        
        # Load chip templates
        self.templates = {}
        self.load_chip_templates()
        
        # Game state
        self.chips = []
        self.next_chip_id = 0
        self.paused = False
        
        # Statistics
        self.total_value = 0
        self.real_count = 0
        self.fake_count = 0
        
        # FPS
        self.fps_queue = deque(maxlen=30)
        
        print("\n🎮 INTERGALACTIC RIKSBANKEN CHIP AUTHENTICATOR")
        print("         Interactive Game Mode")
        print("="*60)
        print("Controls:")
        print("  1 - Spawn GOLD chip")
        print("  2 - Spawn SILVER chip")
        print("  3 - Spawn BRONZE chip")
        print("  C - Clear all chips")
        print("  P - Pause/Resume")
        print("  R - Reset statistics")
        print("  Q - Quit")
        print("="*60 + "\n")
    
    def load_chip_templates(self):
        """Load chip template images"""
        chip_types = ['GOLD', 'SILVER', 'BRONZE']
        
        for chip_type in chip_types:
            filename = f"assets/{chip_type.lower()}.png"
            img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            
            if img is None:
                print(f"⚠️  Warning: Could not load {filename}")
                # Create placeholder
                img = np.ones((100, 200, 4), dtype=np.uint8) * 255
            
            # Remove green background
            if img.shape[2] == 4:
                rgb_img = img[:, :, :3]
            else:
                rgb_img = img
            
            hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
            
            # Green mask
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Create alpha channel
            alpha = np.where(green_mask == 255, 0, 255).astype(np.uint8)
            
            # Combine with RGB
            if img.shape[2] == 4:
                rgba = img.copy()
                rgba[:, :, 3] = alpha
            else:
                rgba = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2BGRA)
                rgba[:, :, 3] = alpha
            
            self.templates[chip_type] = rgba
            print(f"✓ {chip_type}: {rgba.shape}")
    
    def spawn_chip(self, chip_type):
        """Spawn a chip at mouse position or center"""
        template = self.templates[chip_type]
        h, w = template.shape[:2]
        
        # Random position
        x = random.randint(50, self.width - w - 50)
        y = random.randint(50, self.height - h - 50)
        
        # Generate random digits
        digits = (random.randint(1, 9), random.randint(0, 9), random.randint(0, 9))
        
        # Calculate value
        if chip_type == 'GOLD':
            value = int(f"{digits[0]}{digits[1]}{digits[2]}") * 10
        elif chip_type == 'SILVER':
            value = int(f"{digits[0]}{digits[1]}{digits[2]}")
        else:  # BRONZE
            value = digits[0] * digits[1] * digits[2]
        
        # Random fake (20% chance)
        is_fake = random.random() < 0.2
        if is_fake:
            value = 0
        
        chip = {
            'id': self.next_chip_id,
            'chip_type': chip_type,
            'x': x,
            'y': y,
            'digits': digits,
            'value': value,
            'is_fake': is_fake,
            'template': template
        }
        
        self.chips.append(chip)
        self.next_chip_id += 1
        
        # Update stats
        if is_fake:
            self.fake_count += 1
        else:
            self.real_count += 1
            self.total_value += value
        
        status = "FAKE" if is_fake else "REAL"
        print(f"✨ Spawned {chip_type} #{chip['id']} - {status} - {value} CR")
    
    def overlay_image(self, background, overlay, x, y):
        """Overlay image with alpha blending"""
        h, w = overlay.shape[:2]
        
        # Check bounds
        if x + w > background.shape[1] or y + h > background.shape[0]:
            return background
        if x < 0 or y < 0:
            return background
        
        # Extract alpha channel
        alpha = overlay[:, :, 3] / 255.0
        alpha_3ch = np.stack([alpha] * 3, axis=-1)
        
        # Blend
        roi = background[y:y+h, x:x+w]
        foreground = overlay[:, :, :3]
        
        blended = (alpha_3ch * foreground + (1 - alpha_3ch) * roi).astype(np.uint8)
        background[y:y+h, x:x+w] = blended
        
        return background
    
    def draw_chip_info(self, frame, chip):
        """Draw chip information"""
        x, y = chip['x'], chip['y']
        chip_type = chip['chip_type']
        digits = chip['digits']
        value = chip['value']
        is_fake = chip['is_fake']
        
        # Color
        if is_fake:
            color = (0, 0, 255)  # Red
        elif chip_type == 'GOLD':
            color = (0, 215, 255)  # Yellow
        elif chip_type == 'SILVER':
            color = (200, 200, 200)  # Gray
        else:
            color = (0, 100, 200)  # Orange
        
        # Label
        label = f"{chip_type}"
        if is_fake:
            label += " [FAKE]"
        
        cv2.putText(frame, label, (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Digits
        digit_str = f"{digits[0]}{digits[1]}{digits[2]}"
        cv2.putText(frame, digit_str, (x, y-25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        # Value
        if not is_fake:
            h = chip['template'].shape[0]
            cv2.putText(frame, f"{value} CR", (x, y+h+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    def draw_stats(self, frame):
        """Draw statistics panel"""
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        
        # Stats
        y_offset = 40
        cv2.putText(frame, f"Total Value: {self.total_value} CR", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        y_offset += 30
        cv2.putText(frame, f"Real Chips: {self.real_count}", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)
        
        y_offset += 30
        cv2.putText(frame, f"Fake Chips: {self.fake_count}", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        y_offset += 30
        cv2.putText(frame, f"Total Chips: {len(self.chips)}", (20, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # FPS
        if self.fps_queue:
            fps = sum(self.fps_queue) / len(self.fps_queue)
            cv2.putText(frame, f"FPS: {fps:.1f}", (self.width - 150, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def render_frame(self):
        """Render current frame"""
        # Create background
        frame = np.ones((self.height, self.width, 3), dtype=np.uint8) * 50
        
        # Draw grid
        for x in range(0, self.width, 100):
            cv2.line(frame, (x, 0), (x, self.height), (70, 70, 70), 1)
        for y in range(0, self.height, 100):
            cv2.line(frame, (0, y), (self.width, y), (70, 70, 70), 1)
        
        # Draw chips
        for chip in self.chips:
            frame = self.overlay_image(frame, chip['template'], chip['x'], chip['y'])
            self.draw_chip_info(frame, chip)
        
        # Draw stats
        frame = self.draw_stats(frame)
        
        return frame
    
    def run(self):
        """Main game loop"""
        print("🎮 Game started!\n")
        
        while True:
            frame_start = time.time()
            
            # Render
            frame = self.render_frame()
            
            # Display
            cv2.imshow("Intergalactic Riksbanken Chip Authenticator - Game", frame)
            
            # Calculate FPS
            frame_time = time.time() - frame_start
            if frame_time > 0:
                self.fps_queue.append(1.0 / frame_time)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('1'):
                self.spawn_chip('GOLD')
            elif key == ord('2'):
                self.spawn_chip('SILVER')
            elif key == ord('3'):
                self.spawn_chip('BRONZE')
            elif key == ord('c'):
                print("🗑️  Clearing all chips...")
                self.chips.clear()
            elif key == ord('p'):
                self.paused = not self.paused
                print(f"{'⏸️  Paused' if self.paused else '▶️  Resumed'}")
            elif key == ord('r'):
                print("🔄 Resetting statistics...")
                self.total_value = 0
                self.real_count = 0
                self.fake_count = 0
                self.chips.clear()
        
        cv2.destroyAllWindows()
        
        print(f"\n📊 Final Statistics:")
        print(f"   Total Value: {self.total_value} CR")
        print(f"   Real Chips: {self.real_count}")
        print(f"   Fake Chips: {self.fake_count}")
        print("\n✅ Game ended\n")


def main():
    """Entry point"""
    game = ChipGame(width=1280, height=720)
    game.run()


if __name__ == "__main__":
    main()
