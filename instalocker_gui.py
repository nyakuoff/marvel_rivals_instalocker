"""
Marvel Rivals Instalocker - Main GUI Application

A computer vision-based tool that automatically selects heroes in Marvel Rivals.
Features a clean GUI interface with visual hero selection organized by role.

Author: Marvel Rivals Community
Version: 1.0.0
"""

import tkinter as tk
from instalocker_helpers import select_category, update_hero_buttons_gui

def create_main_window():
    """Create and configure the main application window."""
    root = tk.Tk()
    root.title("🦸‍♀️ Marvel Rivals Instalocker 🦸‍♂️")
    root.geometry("600x500")
    root.resizable(True, True)
    
    # Set window icon if available
    try:
        root.iconbitmap("images/icon.ico")
    except:
        pass  # Icon file not found, continue without it
    
    return root

def create_ui_elements(root):
    """Create and arrange all UI elements."""
    # Title label
    title_label = tk.Label(
        root, 
        text="🚀 Marvel Rivals Instalocker", 
        font=("Arial", 16, "bold"),
        fg="#1E3A8A"
    )
    title_label.pack(pady=10)
    
    # Instructions label
    instructions = tk.Label(
        root,
        text="1. Select hero category  2. Choose your hero  3. Launch Marvel Rivals!",
        font=("Arial", 10),
        fg="#374151"
    )
    instructions.pack(pady=5)
    
    # Category selection frame
    frame_categories = tk.Frame(root)
    frame_categories.pack(pady=20)
    
    # Hero selection frame
    frame_heroes = tk.Frame(root)
    frame_heroes.pack(pady=20, fill="both", expand=True)
    
    return frame_categories, frame_heroes

def create_category_buttons(frame_categories, frame_heroes, root):
    """Create the hero category selection buttons."""
    
    button_duelist = tk.Button(
        frame_categories,
        text="🔥 Duelist",
        command=lambda: select_category("duelist", frame_heroes, root),
        bg="#EF4444",
        fg="white", 
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        relief="raised",
        borderwidth=2
    )
    
    button_strategist = tk.Button(
        frame_categories,
        text="🧠 Strategist", 
        command=lambda: select_category("strategist", frame_heroes, root),
        bg="#3B82F6",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        relief="raised",
        borderwidth=2
    )
    
    button_vanguard = tk.Button(
        frame_categories,
        text="🛡️ Vanguard",
        command=lambda: select_category("vanguard", frame_heroes, root),
        bg="#10B981",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        relief="raised",
        borderwidth=2
    )
    
    # Pack buttons with spacing
    button_duelist.pack(side=tk.LEFT, padx=10)
    button_strategist.pack(side=tk.LEFT, padx=10)
    button_vanguard.pack(side=tk.LEFT, padx=10)

def main():
    """Main application entry point."""
    # Create main window
    root = create_main_window()
    
    # Create UI elements
    frame_categories, frame_heroes = create_ui_elements(root)
    
    # Create category buttons
    create_category_buttons(frame_categories, frame_heroes, root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()