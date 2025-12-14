"""
Intergalactic Riksbanken Chip Authenticator - Main Launcher
Select from simulator, camera, or interactive game modes
"""

import sys
import os

def print_banner():
    """Print application banner"""
    print("\n" + "="*60)
    print("🎮 INTERGALACTIC RIKSBANKEN CHIP AUTHENTICATOR")
    print("="*60)
    print("\nSelect Mode:")
    print("  1. Simulator Mode - Conveyor belt simulation")
    print("  2. Camera Mode - Real-time camera detection")
    print("  3. Interactive Game - Manual chip spawning & testing")
    print("  Q. Quit")
    print("="*60)

def run_simulator():
    """Run conveyor belt simulator"""
    print("\n🎬 Starting Simulator Mode...")
    from main import ConveyorSimulator
    sim = ConveyorSimulator(width=1280, height=720, conveyor_speed=3)
    sim.run()

def run_camera():
    """Run camera detection system"""
    print("\n📸 Starting Camera Mode...")
    import camera_main
    camera_main.main()

def run_game():
    """Run interactive game mode"""
    print("\n🎮 Starting Interactive Game Mode...")
    import game
    game.main()

def main():
    """Main launcher"""
    while True:
        print_banner()
        choice = input("\nEnter your choice (1/2/3/Q): ").strip().upper()
        
        if choice == '1':
            try:
                run_simulator()
            except KeyboardInterrupt:
                print("\n\n↩️  Returning to main menu...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")
        
        elif choice == '2':
            try:
                run_camera()
            except KeyboardInterrupt:
                print("\n\n↩️  Returning to main menu...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")
        
        elif choice == '3':
            try:
                run_game()
            except KeyboardInterrupt:
                print("\n\n↩️  Returning to main menu...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")
        
        elif choice == 'Q':
            print("\n👋 Thank you for using Intergalactic Riksbanken Chip Authenticator!")
            print("="*60 + "\n")
            break
        
        else:
            print("\n⚠️  Invalid choice. Please select 1, 2, 3, or Q.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
