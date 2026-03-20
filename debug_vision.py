"""
Vision Debug Tool for Marvel Rivals Instalocker

Saves a screenshot of what the app actually captures, then draws a red box
around the best match for a given hero image, so you can see why detection fails.

Usage:
    python debug_vision.py [hero_name] [category]

Examples:
    python debug_vision.py "Spider-Man" duelist
    python debug_vision.py "Moon Knight" duelist
"""

import sys
import cv2
import numpy as np
import pyautogui
from instalocker_helpers import MONITOR_OFFSET_X, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT, DETECTION_CONFIDENCE
from hero_images import hero_image_paths

def debug(hero_name: str, category: str):
    region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
    print(f"Capturing region: {region}")

    screen = pyautogui.screenshot(region=region)
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    # Save raw screenshot so you can inspect what the app sees
    screen_path = "debug_screenshot.png"
    cv2.imwrite(screen_path, screen_np)
    print(f"Saved screenshot -> {screen_path}")

    hero_img_path = hero_image_paths.get(category, {}).get(hero_name)
    if not hero_img_path:
        print(f"Hero '{hero_name}' not found in category '{category}'")
        return

    template = cv2.imread(hero_img_path)
    if template is None:
        print(f"Could not load template: {hero_img_path}")
        return

    th, tw = template.shape[:2]
    print(f"Template size: {tw}x{th}  |  Screenshot size: {screen_np.shape[1]}x{screen_np.shape[0]}")

    result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"Best match confidence: {max_val:.4f}  (threshold: {DETECTION_CONFIDENCE})")
    print(f"Best match location (relative to region): {max_loc}")

    # Draw box around best match on screenshot
    top_left = max_loc
    bottom_right = (top_left[0] + tw, top_left[1] + th)
    color = (0, 255, 0) if max_val >= DETECTION_CONFIDENCE else (0, 0, 255)
    cv2.rectangle(screen_np, top_left, bottom_right, color, 3)
    label = f"{hero_name} ({max_val:.2f})"
    cv2.putText(screen_np, label, (top_left[0], top_left[1] - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    annotated_path = "debug_annotated.png"
    cv2.imwrite(annotated_path, screen_np)
    print(f"Saved annotated screenshot -> {annotated_path}")
    print()
    if max_val >= DETECTION_CONFIDENCE:
        print("PASS: hero would be detected")
    else:
        print("FAIL: confidence too low")
        print("  -> Open debug_screenshot.png and check:")
        print("     1. Is the game visible in the screenshot?")
        print("     2. Is the hero selection wheel visible?")
        print("  -> Open debug_annotated.png to see where the best (wrong) match is.")
        print("  -> If the screenshot looks correct, the template image needs to be")
        print("     re-captured from your current game version.")

if __name__ == "__main__":
    hero = sys.argv[1] if len(sys.argv) > 1 else "Spider-Man"
    cat  = sys.argv[2] if len(sys.argv) > 2 else "duelist"
    debug(hero, cat)
