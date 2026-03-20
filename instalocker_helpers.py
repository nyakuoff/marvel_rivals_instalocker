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
)
import pyautogui
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

# Configuration
HERO_BUTTON_SIZE = (100, 100)
HERO_DISPLAY_SIZE = (200, 200)
MAX_COLUMNS = 4
DETECTION_CONFIDENCE = 0.65
CLICK_DELAY = 0.1

# Multi-monitor support
# MONITOR_OFFSET_X is the X pixel offset of the monitor the game runs on.
# Detected via xrandr: DP-0 (primary) is at x=1920, HDMI-0 (left) is at x=0.
MONITOR_OFFSET_X = 1920
GAME_MONITOR_WIDTH = 1920
GAME_MONITOR_HEIGHT = 1080

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

            # Create hero button with improved styling
            hero_button = tk.Button(
                frame_heroes,
                image=hero_img_tk,
                command=lambda h=hero: select_hero(h, selected_category, root),
                relief="raised",
                borderwidth=2,
                bg="#F3F4F6",
                activebackground="#E5E7EB"
            )
            hero_button.image = hero_img_tk  # Prevent garbage collection
            hero_button.grid(row=row, column=col, padx=5, pady=5)
            
            # Add tooltip with hero name
            create_tooltip(hero_button, hero)

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
    print(f"Selected category: {category}")
    update_hero_buttons_gui(category, frame_heroes, root)


def select_hero(hero_name: str, selected_category: str, root: tk.Tk) -> None:
    """
    Select a hero and initiate the locking process.
    
    Args:
        hero_name: Name of the hero to select
        selected_category: The category the hero belongs to
        root: The main window
    """
    global locked_hero
    locked_hero = hero_name
    
    print(f"Selected hero: {hero_name} ({selected_category})")
    
    display_locked_hero_message(root, hero_name)
    display_hero_image(hero_name, selected_category, root)
    
    # Start monitoring for game in a separate thread to avoid blocking GUI
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
        else:
            root.hero_label = tk.Label(root, image=hero_img_tk, bg="#F9FAFB")
            root.hero_label.image = hero_img_tk
            root.hero_label.pack(pady=10)
            
    except Exception as e:
        print(f"Error displaying hero image: {e}")


def display_locked_hero_message(root: tk.Tk, hero_name: str) -> None:
    """Display the locked hero message in the GUI."""
    message = f"🎯 Ready to lock: {hero_name}"
    
    if hasattr(root, "locked_hero_label"):
        root.locked_hero_label.config(text=message)
    else:
        root.locked_hero_label = tk.Label(
            root, 
            text=message, 
            font=("Arial", 14, "bold"),
            fg="#059669",
            bg="#F9FAFB"
        )
        root.locked_hero_label.pack(pady=10)


def start_game_monitoring(hero_name: str, selected_category: str) -> None:
    """
    Start monitoring for the game and auto-lock hero when detected.
    This runs in the background to avoid freezing the GUI.
    """
    import threading
    
    def monitor():
        print(f"🔍 Monitoring for game start... Will auto-lock {hero_name}")

        # Poll until the hero selection screen is detected
        while not detect_hero_selection_screen():
            time.sleep(1)

        print(f"✅ Hero selection screen detected — locking {hero_name}")
        time.sleep(0.5)  # Brief pause for screen to fully load
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
            
        region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
        screen = pyautogui.screenshot(region=region)
        screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        indicator = cv2.imread(game_indicator_path)

        # Use template matching to find the indicator
        result = cv2.matchTemplate(screen_np, indicator, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
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
            
            # Click lock button multiple times to ensure it registers
            for _ in range(3):
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
        # Take screenshot of game monitor only
        region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
        screen = pyautogui.screenshot(region=region)
        screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        
        # Load hero template
        hero_template = cv2.imread(hero_img_path)
        if hero_template is None:
            print(f"Failed to load template: {hero_img_path}")
            return None
            
        # Perform template matching
        result = cv2.matchTemplate(screen_np, hero_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > DETECTION_CONFIDENCE:
            # Calculate center of matched region
            # Add MONITOR_OFFSET_X because coordinates are relative to the region screenshot
            template_height, template_width = hero_template.shape[:2]
            center_x = MONITOR_OFFSET_X + max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            return (center_x, center_y)
        else:
            print(f"Hero detection confidence too low: {max_val}")
            return None
            
    except Exception as e:
        print(f"Error in template matching: {e}")
        return None


# Disable pyautogui failsafe for smoother operation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05  # Small pause between actions