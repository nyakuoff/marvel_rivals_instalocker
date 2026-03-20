"""
Coordinate Finder Utility for Marvel Rivals Instalocker

Usage:
  1. Run this script: python find_coords.py
  2. Alt-tab into Marvel Rivals and navigate to the hero selection screen
  3. Hover over each button and press SPACE to capture its coordinates
  4. Press ESC when done — the script prints ready-to-paste code

Captures (in order): Duelist, Strategist, Vanguard, Lock button
"""

import pyautogui
from pynput import keyboard

BUTTONS = [
    ("duelist_button_coords",     "Hover over the DUELIST role button"),
    ("strategist_button_coords",  "Hover over the STRATEGIST role button"),
    ("vanguard_button_coords",    "Hover over the VANGUARD role button"),
    ("lock_button_coords",        "Hover over the LOCK / CONFIRM button"),
]

def wait_for_keypress():
    """Block until SPACE or ESC is pressed. Returns 'space' or 'esc'."""
    result = []

    def on_press(key):
        if key == keyboard.Key.space:
            result.append("space")
            return False  # stop listener
        if key == keyboard.Key.esc:
            result.append("esc")
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    return result[0] if result else "esc"

def main():
    print("=" * 55)
    print("  Marvel Rivals Coordinate Finder")
    print("=" * 55)
    print("Alt-tab into Marvel Rivals, then follow the prompts.")
    print("Press SPACE to capture  |  ESC to quit early\n")

    captured = {}

    for var_name, instruction in BUTTONS:
        print(f"  -> {instruction}")
        print("     Press SPACE to capture (ESC to quit) ...", end="", flush=True)

        key = wait_for_keypress()
        if key == "esc":
            print("\nAborted.")
            return

        x, y = pyautogui.position()
        captured[var_name] = (x, y)
        print(f"  captured: ({x}, {y})")

    print("\n" + "=" * 55)
    print("  Paste these into hero_images.py:")
    print("=" * 55)
    for var_name, coords in captured.items():
        print(f"{var_name} = {coords}")

if __name__ == "__main__":
    main()
