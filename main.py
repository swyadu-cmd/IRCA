"""
Main Conveyor Belt Chip Simulator
Simulates chips (Gold, Silver, Bronze) moving on a green conveyor belt
"""

import cv2
import numpy as np
import random
import os


class ConveyorSimulator:
    """Simulates chips on a green conveyor belt"""
    
    def __init__(self, width=1280, height=720, conveyor_speed=3):
        """Initialize simulator"""
        self.width = width
        self.height = height
        self.conveyor_speed = conveyor_speed
        
        # Conveyor belt is 50% of screen width, centered
        self.belt_width = width // 2
        self.belt_x = (width - self.belt_width) // 2
        
        # Load chip templates
        self.chip_templates = self.load_chip_templates()
        
        # Active chips on belt
        self.chips = []
        self.next_chip_id = 0
        
        # Spawning control
        self.frame_count = 0
        self.spawn_interval = random.randint(30, 60)
        
        # Statistics
        self.total_value = 0
        self.total_real = 0
        self.total_fake = 0
        self.session_chips = []
        
        print("🎬 Intergalactic Riksbanken Chip Authenticator initialized")
        print(f"   Resolution: {width}x{height}")
        print(f"   Belt width: {self.belt_width}px (50% of screen)")
        
    def load_chip_templates(self):
        """Load chip templates from PNG files"""
        templates = {}
        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        
        for chip_type in ['GOLD', 'SILVER', 'BRONZE']:
            filename = f"{chip_type.lower()}.png"
            filepath = os.path.join(assets_dir, filename)
            
            if os.path.exists(filepath):
                img = cv2.imread(filepath)
                if img is not None:
                    img_clean = self.remove_green_background(img)
                    scale = 0.3
                    h, w = img_clean.shape[:2]
                    img_clean = cv2.resize(img_clean, (int(w * scale), int(h * scale)))
                    templates[chip_type] = img_clean
                    print(f"   ✓ {chip_type}: {img_clean.shape}")
        
        return templates
    
    def remove_green_background(self, img):
        """Remove green screen background"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.bitwise_not(green_mask)
        b, g, r = cv2.split(img)
        return cv2.merge([b, g, r, mask])
    
    def create_green_conveyor_background(self):
        """Create green conveyor belt background"""
        background = np.ones((self.height, self.width, 3), dtype=np.uint8) * 50
        green_color = (60, 180, 75)
        belt_area = np.ones((self.height, self.belt_width, 3), dtype=np.uint8)
        belt_area[:] = green_color
        
        belt_y_offset = (self.frame_count * self.conveyor_speed) % 100
        for i in range(-1, self.height // 100 + 2):
            y = i * 100 + belt_y_offset
            if 0 <= y < self.height:
                cv2.line(belt_area, (0, int(y)), (self.belt_width, int(y)), (40, 140, 55), 2)
        
        noise = np.random.randint(-10, 10, belt_area.shape, dtype=np.int16)
        belt_area = np.clip(belt_area.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        background[:, self.belt_x:self.belt_x + self.belt_width] = belt_area
        
        cv2.line(background, (self.belt_x, 0), (self.belt_x, self.height), (200, 200, 200), 3)
        cv2.line(background, (self.belt_x + self.belt_width, 0), (self.belt_x + self.belt_width, self.height), (200, 200, 200), 3)
        
        return background
    
    def spawn_chip(self):
        """Spawn a new chip"""
        chip_type = random.choices(['GOLD', 'SILVER', 'BRONZE'], weights=[0.15, 0.35, 0.50])[0]
        
        if chip_type not in self.chip_templates:
            return
        
        template = self.chip_templates[chip_type]
        h, w = template.shape[:2]
        is_fake = random.random() < 0.2
        
        if is_fake:
            value = 0
            authentic = False
        else:
            authentic = True
            if chip_type == 'GOLD':
                digits = [random.randint(1, 9) for _ in range(3)]
                value = (digits[0] * 100 + digits[1] * 10 + digits[2]) * 10
            elif chip_type == 'SILVER':
                digits = [random.randint(1, 9) for _ in range(3)]
                value = digits[0] * 100 + digits[1] * 10 + digits[2]
            else:
                digits = [random.randint(1, 9) for _ in range(2)]
                value = digits[0] * digits[1]
        
        x = random.randint(self.belt_x + 10, self.belt_x + self.belt_width - w - 10)
        y = -h - 10
        
        chip = {
            'id': self.next_chip_id, 'type': chip_type, 'x': x, 'y': y,
            'width': w, 'height': h, 'template': template,
            'value': value, 'authentic': authentic,
            'velocity_y': self.conveyor_speed, 'counted': False
        }
        
        self.chips.append(chip)
        self.next_chip_id += 1
        print(f"✨ Spawned {chip_type} #{chip['id']} - {'REAL' if authentic else 'FAKE'} - {value} CR")
    
    def update_chips(self):
        """Update chip positions"""
        chips_to_remove = []
        for i, chip in enumerate(self.chips):
            chip['y'] += chip['velocity_y']
            
            if chip['y'] > self.height // 2 and not chip['counted']:
                chip['counted'] = True
                if chip['authentic']:
                    self.total_real += 1
                    self.total_value += chip['value']
                else:
                    self.total_fake += 1
                self.session_chips.append({'type': chip['type'], 'value': chip['value'], 'authentic': chip['authentic']})
            
            if chip['y'] > self.height + 50:
                chips_to_remove.append(i)
        
        for i in reversed(chips_to_remove):
            del self.chips[i]
    
    def overlay_image_alpha(self, background, overlay, x, y):
        """Overlay RGBA image on BGR background"""
        if overlay.shape[2] != 4:
            h, w = overlay.shape[:2]
            if 0 <= y < background.shape[0] and 0 <= x < background.shape[1]:
                y_end = min(y + h, background.shape[0])
                x_end = min(x + w, background.shape[1])
                background[y:y_end, x:x_end] = overlay[:y_end-y, :x_end-x, :3]
            return
        
        h, w = overlay.shape[:2]
        if y + h > background.shape[0]: h = background.shape[0] - y; overlay = overlay[:h, :, :]
        if x + w > background.shape[1]: w = background.shape[1] - x; overlay = overlay[:, :w, :]
        if y < 0: overlay = overlay[-y:, :, :]; h += y; y = 0
        if x < 0: overlay = overlay[:, -x:, :]; w += x; x = 0
        if h <= 0 or w <= 0: return
        
        alpha = np.expand_dims(overlay[:, :, 3] / 255.0, axis=2)
        foreground = overlay[:, :, :3]
        background_section = background[y:y+h, x:x+w]
        blended = (alpha * foreground + (1 - alpha) * background_section).astype(np.uint8)
        background[y:y+h, x:x+w] = blended
    
    def draw_ui(self, frame):
        """Draw UI overlay"""
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 220), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, "CHIP CONVEYOR SYSTEM", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        y = 75
        cv2.putText(frame, f"On Belt: {len(self.chips)} chips", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 30
        cv2.putText(frame, f"Total Value: {self.total_value} CR", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        y += 30
        cv2.putText(frame, f"Real Chips: {self.total_real}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y += 30
        cv2.putText(frame, f"Fake Chips: {self.total_fake}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        y += 30
        cv2.putText(frame, f"Scanned: {len(self.session_chips)}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        
        instructions = ["Controls:", "S - Spawn | B - Burst (5) | C - Clear", "P - Pause | R - Reset | Q - Quit"]
        y = frame.shape[0] - 80
        for instruction in instructions:
            cv2.putText(frame, instruction, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y += 25
    
    def render_frame(self):
        """Render current frame"""
        frame = self.create_green_conveyor_background()
        center_y = self.height // 2
        cv2.line(frame, (self.belt_x, center_y), (self.belt_x + self.belt_width, center_y), (255, 255, 0), 3)
        cv2.putText(frame, "SCAN LINE", (self.belt_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        for chip in self.chips:
            x, y = int(chip['x']), int(chip['y'])
            self.overlay_image_alpha(frame, chip['template'], x, y)
            color = (0, 255, 0) if chip['authentic'] else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + chip['width'], y + chip['height']), color, 2)
            
            if y > -20:
                cv2.putText(frame, f"{chip['type']} #{chip['id']}", (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(frame, f"{chip['value']} CR", (x, y + chip['height'] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.putText(frame, "REAL" if chip['authentic'] else "FAKE", (x, y + chip['height'] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        self.draw_ui(frame)
        return frame
    
    def run(self):
        """Main simulation loop"""
        print("\n🎬 Starting Intergalactic Riksbanken Chip Authenticator...")
        print("Controls: S-Spawn | B-Burst(5) | C-Clear | P-Pause | R-Reset | Q-Quit\n")
        
        paused = False
        while True:
            if not paused:
                self.frame_count += 1
                self.update_chips()
                if self.frame_count % self.spawn_interval == 0:
                    self.spawn_chip()
                    self.spawn_interval = random.randint(30, 60)
            
            frame = self.render_frame()
            cv2.imshow("Chip Conveyor Simulator", frame)
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('q') or key == ord('Q'): break
            elif key == ord('s') or key == ord('S'): self.spawn_chip()
            elif key == ord('b') or key == ord('B'):
                for _ in range(5): self.spawn_chip()
                print("💥 Burst spawned 5 chips!")
            elif key == ord('c') or key == ord('C'): self.chips.clear(); print("🧹 Cleared!")
            elif key == ord('p') or key == ord('P'):
                paused = not paused
                print(f"\n{'⏸️  PAUSED' if paused else '▶️  RESUMED'}")
                if paused: print(f"   Value: {self.total_value} CR | Real: {self.total_real} | Fake: {self.total_fake}")
            elif key == ord('r') or key == ord('R'):
                self.total_value = self.total_real = self.total_fake = 0
                self.session_chips.clear()
                print("🔄 Reset!")
        
        cv2.destroyAllWindows()
        print(f"\n{'='*60}\nSESSION COMPLETE\n{'='*60}")
        print(f"Total Chips: {len(self.session_chips)} | Real: {self.total_real} | Fake: {self.total_fake}")
        print(f"Total Value: {self.total_value} CR")
        if self.total_real > 0: print(f"Average: {self.total_value / self.total_real:.1f} CR")
        print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("🎬 CHIP CONVEYOR SIMULATOR")
    print("="*60)
    print("\nValue Calculation Rules:")
    print("  GOLD:   3 digits × 10  (e.g., 752 → 7520 CR)")
    print("  SILVER: 3 digits       (e.g., 756 → 756 CR)")
    print("  BRONZE: 2 digits × ×   (e.g., 2×4 → 8 CR)")
    print("="*60 + "\n")
    
    ConveyorSimulator(width=1280, height=720, conveyor_speed=3).run()
