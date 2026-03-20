"""
Marvel Rivals Instalocker - Helper Functions

This module contains all the core functionality for the instalocker including:
- Hero selection and GUI management
- Computer vision-based hero detection
- Automated clicking and hero locking
- Screen monitoring and game state detection

Author: Marvel Rivals Community
Version: 1.0.0
"""

import tkinter as tk
from PIL import Image, ImageTk
from hero_images import (
    hero_image_paths,
    game_indicator_path,
    duelist_button_coords,
    strategist_button_coords,
    vanguard_button_coords,
    lock_button_coords,
    wheel_scroll_coords,
    hero_scroll_steps,
)
import pyautogui
import mss
import time
import cv2
import numpy as np
import keyboard
import os
from typing import Optional, Tuple

# Global state
locked_hero: Optional[str] = None
hero_images_cache = {}
current_category: Optional[str] = None
_cancel_event = __import__('threading').Event()

# Configuration
HERO_BUTTON_SIZE = (90, 90)
HERO_DISPLAY_SIZE = (56, 56)
MAX_COLUMNS = 4
DETECTION_CONFIDENCE = 0.65
CLICK_DELAY = 0.05

# Multi-monitor support
# MONITOR_OFFSET_X is the X pixel offset of the monitor the game runs on.
# Detected via xrandr: DP-0 (primary) is at x=1920, HDMI-0 (left) is at x=0.
MONITOR_OFFSET_X = 1920
GAME_MONITOR_WIDTH = 1920
GAME_MONITOR_HEIGHT = 1080

# Restrict hero template search to the wheel area (right portion) for faster detection.
# (x_offset, y_offset, width, height) relative to game monitor top-left.
HERO_WHEEL_REGION = (900, 0, 1020, 750)

# Restrict indicator search to where the CONFIRM button lives (faster polling).
INDICATOR_REGION = (1400, 620, 480, 220)

# Cache for CV2 grayscale templates — loaded from disk once, then reused.
cv_template_cache: dict = {}

def update_hero_buttons_gui(selected_category: str, frame_heroes: tk.Frame, root: tk.Tk) -> None:
    """
    Update the GUI to display hero buttons for the selected category.
    
    Args:
        selected_category: The hero category to display ("duelist", "strategist", "vanguard")
        frame_heroes: The tkinter frame to contain hero buttons
        root: The main tkinter window
    """
    global current_category
    current_category = selected_category

    # Clear existing hero buttons
    for widget in frame_heroes.winfo_children():
        widget.destroy()

    frame_heroes.configure(bg="#1a1d27")

    if selected_category not in hero_image_paths:
        print(f"Warning: Unknown category '{selected_category}'")
        return

    heroes = list(hero_image_paths[selected_category].keys())
    row, col = 0, 0

    for hero in heroes:
        try:
            # Load and cache hero image
            if hero not in hero_images_cache:
                hero_img_path = hero_image_paths[selected_category][hero]
                if not os.path.exists(hero_img_path):
                    print(f"Warning: Image not found for {hero}: {hero_img_path}")
                    continue

                hero_img = Image.open(hero_img_path)
                hero_img = hero_img.resize(HERO_BUTTON_SIZE, Image.Resampling.LANCZOS)
                hero_img_tk = ImageTk.PhotoImage(hero_img)
                hero_images_cache[hero] = hero_img_tk
            else:
                hero_img_tk = hero_images_cache[hero]

            # Container: image button + name label stacked
            cell = tk.Frame(frame_heroes, bg="#1a1d27", cursor="hand2")
            cell.grid(row=row, column=col, padx=5, pady=5)

            hero_button = tk.Button(
                cell,
                image=hero_img_tk,
                command=lambda h=hero: select_hero(h, selected_category, root),
                relief="flat",
                borderwidth=0,
                bg="#22263a",
                activebackground="#2d3348"
            )
            hero_button.image = hero_img_tk  # Prevent garbage collection
            hero_button.pack()

            short = hero if len(hero) <= 13 else hero[:12] + "…"
            tk.Label(
                cell, text=short,
                font=("Arial", 7), fg="#94a3b8", bg="#1a1d27",
                width=11
            ).pack()

            # Update grid position
            col += 1
            if col >= MAX_COLUMNS:
                col = 0
                row += 1

        except Exception as e:
            print(f"Error loading hero {hero}: {e}")
            continue


def create_tooltip(widget: tk.Widget, text: str) -> None:
    """Create a tooltip that shows hero name on hover."""
    def show_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=text, background="lightyellow", 
                        relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()
        widget.tooltip = tooltip

    def hide_tooltip(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)


def select_category(category: str, frame_heroes: tk.Frame, root: tk.Tk) -> None:
    """
    Select a hero category and update the GUI.
    
    Args:
        category: The category to select ("duelist", "strategist", "vanguard")
        frame_heroes: The frame containing hero buttons
        root: The main window
    """
    update_hero_buttons_gui(category, frame_heroes, root)


_gui_hero_callback = None  # Set by GUI to intercept hero clicks


def select_hero(hero_name: str, selected_category: str, root: tk.Tk) -> None:
    global locked_hero
    locked_hero = hero_name
    print(f"Selected hero: {hero_name} ({selected_category})")
    if _gui_hero_callback:
        _gui_hero_callback(hero_name, selected_category)
    else:
        # Fallback: start monitoring immediately (no GUI confirm button)
        display_locked_hero_message(root, hero_name)
        display_hero_image(hero_name, selected_category, root)
        start_game_monitoring(hero_name, selected_category)


def display_hero_image(hero_name: str, selected_category: str, root: tk.Tk) -> None:
    """Display the selected hero's image in the GUI."""
    try:
        hero_img_path = hero_image_paths[selected_category].get(hero_name)
        if not hero_img_path or not os.path.exists(hero_img_path):
            return
            
        # Load and resize image for display
        hero_img = Image.open(hero_img_path)
        hero_img = hero_img.resize(HERO_DISPLAY_SIZE, Image.Resampling.LANCZOS)
        hero_img_tk = ImageTk.PhotoImage(hero_img)

        # Update or create hero display label
        if hasattr(root, "hero_label"):
            root.hero_label.config(image=hero_img_tk)
            root.hero_label.image = hero_img_tk
            
    except Exception as e:
        print(f"Error displaying hero image: {e}")


def display_locked_hero_message(root: tk.Tk, hero_name: str) -> None:
    """Display the locked hero message in the GUI."""
    message = f"🎯  {hero_name}"

    if hasattr(root, "locked_hero_label"):
        root.locked_hero_label.config(text=message, fg="#10b981")


def cancel_monitoring() -> None:
    """Signal any running monitor thread to stop."""
    _cancel_event.set()
    print("🛑 Auto-lock cancelled")


def start_game_monitoring(hero_name: str, selected_category: str) -> None:
    """
    Start monitoring for the game and auto-lock hero when detected.
    This runs in the background to avoid freezing the GUI.
    """
    import threading
    
    def monitor():
        _cancel_event.clear()
        print(f"🔍 Monitoring for game start... Will auto-lock {hero_name}")

        # Poll as fast as possible — mss grabs are ~1ms so CPU use stays low.
        # A 10ms yield just prevents 100% core saturation.
        while not _cancel_event.is_set() and not detect_hero_selection_screen():
            time.sleep(0.01)

        if _cancel_event.is_set():
            return

        print(f"✅ Hero selection screen detected — locking {hero_name}")
        try:
            lock_hero_in_game(hero_name, selected_category)
        except Exception as e:
            print(f"Error during auto-lock: {e}")
    
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()


def detect_hero_selection_screen() -> bool:
    """
    Detect if the hero selection screen is currently active.
    Returns True if the game is ready for hero selection.
    """
    try:
        if not os.path.exists(game_indicator_path):
            print("Game indicator image not found")
            return True  # Assume ready if no indicator

        # Search only the small region where the CONFIRM button lives (much faster)
        rx, ry, rw, rh = INDICATOR_REGION
        monitor = {"top": ry, "left": MONITOR_OFFSET_X + rx, "width": rw, "height": rh}
        with mss.mss() as sct:
            screen_np = np.array(sct.grab(monitor))
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2GRAY)

        # Load and cache indicator template in grayscale
        if game_indicator_path not in cv_template_cache:
            t = cv2.imread(game_indicator_path, cv2.IMREAD_GRAYSCALE)
            cv_template_cache[game_indicator_path] = t
        indicator_gray = cv_template_cache[game_indicator_path]

        result = cv2.matchTemplate(screen_gray, indicator_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        return max_val > DETECTION_CONFIDENCE

    except Exception as e:
        print(f"Error detecting game screen: {e}")
        return False  # Assume not ready on error


def lock_hero_in_game(hero_name: str, selected_category: str) -> bool:
    """
    Perform the actual hero locking in the game.
    
    Args:
        hero_name: Name of hero to lock
        selected_category: Category of the hero
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"🎮 Attempting to lock {hero_name}...")
        
        # Wait a moment for screen to be ready
        time.sleep(CLICK_DELAY)
        
        # Click category button first
        if selected_category == "duelist":
            pyautogui.click(duelist_button_coords[0], duelist_button_coords[1])
        elif selected_category == "strategist":
            pyautogui.click(strategist_button_coords[0], strategist_button_coords[1])
        elif selected_category == "vanguard":
            pyautogui.click(vanguard_button_coords[0], vanguard_button_coords[1])
        else:
            print(f"Unknown category: {selected_category}")
            return False
            
        time.sleep(CLICK_DELAY)

        scroll_steps = hero_scroll_steps.get(hero_name, 0)
        if scroll_steps > 0:
            # Reset wheel to top, then scroll down to the hero's position.
            # One event per loop because on Linux pyautogui.scroll(N) fires only once.
            for _ in range(30):
                pyautogui.scroll(1, wheel_scroll_coords[0], wheel_scroll_coords[1])
                time.sleep(0.03)
            time.sleep(0.05)
            for _ in range(scroll_steps):
                pyautogui.scroll(-1, wheel_scroll_coords[0], wheel_scroll_coords[1])
                time.sleep(0.03)
            time.sleep(0.05)

        # Find and click the hero
        hero_img_path = hero_image_paths[selected_category].get(hero_name)
        if not hero_img_path or not os.path.exists(hero_img_path):
            print(f"Hero image not found: {hero_img_path}")
            return False
            
        hero_location = find_hero_on_screen(hero_img_path)
        if hero_location:
            # Click hero
            pyautogui.click(hero_location[0], hero_location[1])
            time.sleep(CLICK_DELAY)
            
            # Click lock button twice to ensure it registers
            for _ in range(2):
                pyautogui.click(lock_button_coords[0], lock_button_coords[1])
                time.sleep(CLICK_DELAY)
            
            print(f"✅ Successfully locked {hero_name}!")
            return True
        else:
            print(f"❌ Could not locate {hero_name} on screen")
            return False
            
    except Exception as e:
        print(f"❌ Error locking hero: {e}")
        return False


def find_hero_on_screen(hero_img_path: str) -> Optional[Tuple[int, int]]:
    """
    Find hero location on screen using template matching.

    Args:
        hero_img_path: Path to hero image file

    Returns:
        Tuple of (x, y) coordinates if found, None otherwise
    """
    try:
        # Screenshot only the hero wheel region (smaller area = faster match)
        rx, ry, rw, rh = HERO_WHEEL_REGION
        monitor = {"top": ry, "left": MONITOR_OFFSET_X + rx, "width": rw, "height": rh}
        with mss.mss() as sct:
            screen_np = np.array(sct.grab(monitor))
        screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2GRAY)

        # Load and cache hero template in grayscale (avoids disk reads on retry)
        if hero_img_path not in cv_template_cache:
            t = cv2.imread(hero_img_path, cv2.IMREAD_GRAYSCALE)
            cv_template_cache[hero_img_path] = t
        hero_template = cv_template_cache[hero_img_path]

        if hero_template is None:
            print(f"Failed to load template: {hero_img_path}")
            return None

        result = cv2.matchTemplate(screen_gray, hero_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > DETECTION_CONFIDENCE:
            template_height, template_width = hero_template.shape[:2]
            center_x = MONITOR_OFFSET_X + rx + max_loc[0] + template_width // 2
            center_y = ry + max_loc[1] + template_height // 2
            return (center_x, center_y)
        else:
            print(f"Hero detection confidence too low: {max_val:.2f}")
            return None

    except Exception as e:
        print(f"Error in template matching: {e}")
        return None


# Disable pyautogui failsafe for smoother operation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # No automatic inter-call delay — we add explicit sleeps only where needed