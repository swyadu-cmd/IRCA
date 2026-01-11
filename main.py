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
        self.reference_templates = self.chip_templates.copy()  # Store clean references
        self.fake_threshold = 0.05  # 5% difference threshold
        
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
        
        # Test mode tracking
        self.test_mode = False
        self.test_real_count = 0
        self.test_fake_count = 0
        self.test_real_spawned = 0
        self.test_fake_spawned = 0
        self.test_real_detected = 0
        self.test_fake_detected = 0
        self.test_chips_spawned = []  # Track each spawned chip's ground truth
        
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
    
    def calculate_image_difference(self, img1, img2):
        """
        Calculate percentage difference between two images.
        Returns value between 0.0 (identical) and 1.0 (completely different)
        """
        # Ensure same size
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Convert to grayscale if needed (ignore alpha channel)
        if len(img1.shape) == 3 and img1.shape[2] == 4:
            img1_gray = cv2.cvtColor(img1[:, :, :3], cv2.COLOR_BGR2GRAY)
        else:
            img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            
        if len(img2.shape) == 3 and img2.shape[2] == 4:
            img2_gray = cv2.cvtColor(img2[:, :, :3], cv2.COLOR_BGR2GRAY)
        else:
            img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference
        diff = cv2.absdiff(img1_gray, img2_gray)
        
        # Calculate percentage of different pixels
        non_zero = np.count_nonzero(diff > 10)  # Threshold to ignore minor variations
        total_pixels = diff.size
        difference_percent = non_zero / total_pixels
        
        return difference_percent
    
    def apply_fake_alterations(self, template, chip_type):
        """
        Apply random alterations to template to create a fake chip.
        Returns altered template and whether it's fake based on 5% threshold.
        """
        altered = template.copy()
        
        # Randomly decide to alter (30% chance of creating a fake)
        if random.random() > 0.3:
            return altered, False  # Not altered, authentic
        
        # Apply various alterations
        alteration_type = random.choice(['noise', 'blur', 'color', 'rotate', 'crop'])
        
        if alteration_type == 'noise':
            # Add noise
            noise = np.random.randint(-30, 30, altered.shape, dtype=np.int16)
            altered = np.clip(altered.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        elif alteration_type == 'blur':
            # Add blur
            altered[:, :, :3] = cv2.GaussianBlur(altered[:, :, :3], (15, 15), 0)
        
        elif alteration_type == 'color':
            # Change color slightly
            hsv = cv2.cvtColor(altered[:, :, :3], cv2.COLOR_BGR2HSV)
            hsv[:, :, 0] = (hsv[:, :, 0] + random.randint(10, 30)) % 180  # Hue shift
            altered[:, :, :3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        elif alteration_type == 'rotate':
            # Rotate slightly
            h, w = altered.shape[:2]
            center = (w // 2, h // 2)
            angle = random.uniform(-15, 15)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            altered = cv2.warpAffine(altered, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        
        elif alteration_type == 'crop':
            # Add black patches
            h, w = altered.shape[:2]
            for _ in range(random.randint(2, 5)):
                x1 = random.randint(0, w - 20)
                y1 = random.randint(0, h - 20)
                x2 = x1 + random.randint(10, 30)
                y2 = y1 + random.randint(10, 30)
                altered[y1:y2, x1:x2] = 0
        
        # Check if alteration exceeds 5% threshold
        diff = self.calculate_image_difference(template, altered)
        is_fake = diff > self.fake_threshold
        
        return altered, is_fake
    
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
    
    def spawn_chip(self, force_authentic=None, chip_type_override=None):
        """Spawn a new chip with fake detection based on 5% difference threshold
        
        Args:
            force_authentic: If True, force real chip. If False, force fake chip. If None, random.
            chip_type_override: Force specific chip type ('GOLD', 'SILVER', 'BRONZE')
        """
        if chip_type_override:
            chip_type = chip_type_override
        else:
            chip_type = random.choices(['GOLD', 'SILVER', 'BRONZE'], weights=[0.15, 0.35, 0.50])[0]
        
        if chip_type not in self.chip_templates:
            return
        
        # Get reference template and apply potential alterations
        reference_template = self.reference_templates[chip_type]
        
        # Override fake/real if specified
        if force_authentic is not None:
            if force_authentic:
                # Force real chip - no alterations
                altered_template = reference_template.copy()
                is_fake = False
            else:
                # Force fake chip - apply heavy alterations
                altered_template, is_fake = self.apply_fake_alterations(reference_template, chip_type)
                # Ensure it's actually fake by reapplying if needed
                attempts = 0
                while not is_fake and attempts < 5:
                    altered_template, is_fake = self.apply_fake_alterations(reference_template, chip_type)
                    attempts += 1
        else:
            altered_template, is_fake = self.apply_fake_alterations(reference_template, chip_type)
        
        h, w = altered_template.shape[:2]
        
        # Calculate value based on authenticity
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
        
        # Calculate actual difference percentage for display
        diff_percent = self.calculate_image_difference(reference_template, altered_template)
        
        chip = {
            'id': self.next_chip_id, 'type': chip_type, 'x': x, 'y': y,
            'width': w, 'height': h, 'template': altered_template,
            'value': value, 'authentic': authentic,
            'velocity_y': self.conveyor_speed, 'counted': False,
            'difference': diff_percent  # Store difference for display
        }
        
        self.chips.append(chip)
        self.next_chip_id += 1
        fake_status = 'FAKE' if is_fake else 'REAL'
        
        # Track in test mode
        if self.test_mode:
            self.test_chips_spawned.append({
                'id': chip['id'],
                'authentic': authentic,
                'counted': False
            })
            if authentic:
                self.test_real_spawned += 1
            else:
                self.test_fake_spawned += 1
        
        print(f"✨ Spawned {chip_type} #{chip['id']} - {fake_status} - {value} CR (Diff: {diff_percent*100:.1f}%)")
    
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
                
                # Update test mode detection counts
                if self.test_mode:
                    for test_chip in self.test_chips_spawned:
                        if test_chip['id'] == chip['id'] and not test_chip['counted']:
                            test_chip['counted'] = True
                            if chip['authentic']:
                                self.test_real_detected += 1
                            else:
                                self.test_fake_detected += 1
                            break
            
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
        
        # Adjust overlay height based on test mode
        overlay_height = 320 if self.test_mode else 220
        cv2.rectangle(overlay, (10, 10), (450, overlay_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        title = "TEST MODE" if self.test_mode else "CHIP CONVEYOR SYSTEM"
        title_color = (0, 255, 255) if not self.test_mode else (255, 100, 255)
        cv2.putText(frame, title, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, title_color, 2)
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
        
        # Test mode stats
        if self.test_mode:
            y += 40
            cv2.putText(frame, "TEST VALIDATION:", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 255), 2)
            y += 25
            real_accuracy = f"{self.test_real_detected}/{self.test_real_spawned}" if self.test_real_spawned > 0 else "0/0"
            cv2.putText(frame, f"Real detected: {real_accuracy}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y += 20
            fake_accuracy = f"{self.test_fake_detected}/{self.test_fake_spawned}" if self.test_fake_spawned > 0 else "0/0"
            cv2.putText(frame, f"Fake detected: {fake_accuracy}", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            y += 25
            total_spawned = self.test_real_spawned + self.test_fake_spawned
            total_detected = self.test_real_detected + self.test_fake_detected
            if total_spawned > 0:
                accuracy = (total_detected / total_spawned) * 100
                accuracy_color = (0, 255, 0) if accuracy >= 90 else (0, 255, 255) if accuracy >= 70 else (0, 0, 255)
                cv2.putText(frame, f"Accuracy: {accuracy:.1f}%", (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, accuracy_color, 2)
        
        instructions = ["Controls:", "S - Spawn | B - Burst (5) | T - Test Mode", "C - Clear | P - Pause | R - Reset | Q - Quit"]
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
                
                # Show difference percentage and status
                diff_pct = chip.get('difference', 0) * 100
                status_text = f"FAKE ({diff_pct:.1f}%)" if not chip['authentic'] else f"REAL ({diff_pct:.1f}%)"
                cv2.putText(frame, status_text, (x, y + chip['height'] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        self.draw_ui(frame)
        return frame
    
    def spawn_test_batch(self, num_real, num_fake):
        """Spawn a specific number of real and fake chips for testing
        
        Args:
            num_real: Number of real chips to spawn
            num_fake: Number of fake chips to spawn
        """
        print(f"\n🧪 TEST BATCH: Spawning {num_real} real + {num_fake} fake chips...")
        
        # Enable test mode
        self.test_mode = True
        self.test_real_spawned = 0
        self.test_fake_spawned = 0
        self.test_real_detected = 0
        self.test_fake_detected = 0
        self.test_chips_spawned.clear()
        
        # Spawn real chips
        for _ in range(num_real):
            self.spawn_chip(force_authentic=True)
        
        # Spawn fake chips
        for _ in range(num_fake):
            self.spawn_chip(force_authentic=False)
        
        print(f"✅ Test batch ready: {num_real} real, {num_fake} fake")
        print(f"   System will validate detection accuracy.")
    
    def print_test_results(self):
        """Print test mode results"""
        if not self.test_mode:
            return
        
        print("\n" + "="*60)
        print("🧪 TEST RESULTS")
        print("="*60)
        
        total_spawned = self.test_real_spawned + self.test_fake_spawned
        total_detected = self.test_real_detected + self.test_fake_detected
        
        print(f"\nChips Spawned: {total_spawned}")
        print(f"  Real:  {self.test_real_spawned}")
        print(f"  Fake:  {self.test_fake_spawned}")
        
        print(f"\nChips Detected: {total_detected}")
        print(f"  Real detected:  {self.test_real_detected}/{self.test_real_spawned}")
        print(f"  Fake detected:  {self.test_fake_detected}/{self.test_fake_spawned}")
        
        if total_spawned > 0:
            accuracy = (total_detected / total_spawned) * 100
            print(f"\nOverall Accuracy: {accuracy:.1f}%")
            
            if self.test_real_spawned > 0:
                real_accuracy = (self.test_real_detected / self.test_real_spawned) * 100
                print(f"Real Chip Accuracy: {real_accuracy:.1f}%")
            
            if self.test_fake_spawned > 0:
                fake_accuracy = (self.test_fake_detected / self.test_fake_spawned) * 100
                print(f"Fake Chip Accuracy: {fake_accuracy:.1f}%")
            
            # Pass/Fail verdict
            if accuracy >= 90:
                print("\n✅ TEST PASSED (≥90% accuracy)")
            elif accuracy >= 70:
                print("\n⚠️  TEST MARGINAL (70-89% accuracy)")
            else:
                print("\n❌ TEST FAILED (<70% accuracy)")
        
        print("="*60)
    
    def run(self):
        """Main simulation loop"""
        print("\n🎬 Starting Intergalactic Riksbanken Chip Authenticator...")
        print("Controls: S-Spawn | B-Burst(5) | T-Test | C-Clear | P-Pause | R-Reset | Q-Quit\n")
        
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
            elif key == ord('t') or key == ord('T'):
                # Test mode - prompt for numbers
                print("\n" + "="*60)
                print("🧪 TEST MODE")
                print("="*60)
                paused = True
                try:
                    num_real = int(input("Enter number of REAL chips to spawn: "))
                    num_fake = int(input("Enter number of FAKE chips to spawn: "))
                    if num_real >= 0 and num_fake >= 0:
                        self.spawn_test_batch(num_real, num_fake)
                        print("\nPress P to resume and watch the test...")
                    else:
                        print("❌ Invalid numbers. Must be non-negative.")
                        paused = False
                except ValueError:
                    print("❌ Invalid input. Please enter numbers.")
                    paused = False
            elif key == ord('r') or key == ord('R'):
                # Print test results if in test mode
                if self.test_mode:
                    self.print_test_results()
                
                # Reset everything
                self.total_value = self.total_real = self.total_fake = 0
                self.session_chips.clear()
                self.test_mode = False
                self.test_real_spawned = 0
                self.test_fake_spawned = 0
                self.test_real_detected = 0
                self.test_fake_detected = 0
                self.test_chips_spawned.clear()
                print("🔄 Reset!")
        
        cv2.destroyAllWindows()
        
        # Print test results if in test mode
        if self.test_mode:
            self.print_test_results()
        
        print(f"\n{'='*60}\nSESSION COMPLETE\n{'='*60}")
        print(f"Total Chips: {len(self.session_chips)} | Real: {self.total_real} | Fake: {self.total_fake}")
        print(f"Total Value: {self.total_value} CR")
        if self.total_real > 0: print(f"Average: {self.total_value / self.total_real:.1f} CR")
        print("="*60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Chip Authenticator')
    parser.add_argument('--camera', action='store_true', help='Use camera mode')
    args = parser.parse_args()
    
    if args.camera:
        # Launch camera mode
        import camera_main
        camera_main.main()
    else:
        # Launch simulation mode
        print("="*60)
        print("🎬 CHIP CONVEYOR SIMULATOR")
        print("="*60)
        print("\nValue Calculation Rules:")
        print("  GOLD:   3 digits × 10  (e.g., 752 → 7520 CR)")
        print("  SILVER: 3 digits       (e.g., 756 → 756 CR)")
        print("  BRONZE: 2 digits × ×   (e.g., 2×4 → 8 CR)")
        print("="*60 + "\n")
        
        ConveyorSimulator(width=1280, height=720, conveyor_speed=3).run()
