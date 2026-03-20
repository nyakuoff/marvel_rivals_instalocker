"""
Game Indicator Capture Tool

Replaces game_indicator.PNG with a small crop of a static UI element
that is ONLY visible on the hero selection screen (e.g. the CONFIRM button).

Usage:
    python capture_indicator.py

Steps:
    1. Run this script
    2. Switch to Marvel Rivals and open the hero selection screen
    3. Script counts down and takes a screenshot
    4. Click and drag a rectangle around a small, static element
       (the yellow CONFIRM button works best)
    5. Release — the crop is saved as images/game_indicator.PNG
"""

import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import time
import os
from instalocker_helpers import MONITOR_OFFSET_X, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT

OUTPUT_PATH = "images/game_indicator.PNG"
COUNTDOWN = 5


class IndicatorCapture:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Capture Game Indicator")
        self.screenshot = None
        self.screenshot_tk = None
        self.canvas = None
        self.scale = 1.0
        self.start_x = self.start_y = 0
        self.rect_id = None

    def countdown_and_screenshot(self):
        self.root.withdraw()
        print("\n  Switch to Marvel Rivals — open the hero selection screen")
        print("  Screenshot in:", end="", flush=True)
        for i in range(COUNTDOWN, 0, -1):
            print(f" {i}", end="", flush=True)
            time.sleep(1)
        print(" 📸")
        region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
        self.screenshot = pyautogui.screenshot(region=region)
        self.root.deiconify()

    def build_window(self):
        screen_w = self.root.winfo_screenwidth() // 2
        screen_h = self.root.winfo_screenheight() - 80
        img_w, img_h = self.screenshot.size
        self.scale = min(screen_w / img_w, screen_h / img_h, 1.0)
        disp_w = int(img_w * self.scale)
        disp_h = int(img_h * self.scale)

        self.root.geometry(f"{disp_w}x{disp_h + 40}+0+0")
        self.root.configure(bg="#1e1e1e")

        tk.Label(
            self.root,
            text="Click and drag to select the element to use as the game indicator  (CONFIRM button recommended)",
            font=("Arial", 10), bg="#2d3a4a", fg="white", pady=6
        ).pack(fill="x")

        display_img = self.screenshot.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
        self.screenshot_tk = ImageTk.PhotoImage(display_img)

        self.canvas = tk.Canvas(self.root, width=disp_w, height=disp_h,
                                bg="black", cursor="crosshair", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.screenshot_tk)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)

    def on_drag(self, event):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="yellow", width=2
        )

    def on_release(self, event):
        x1 = int(min(self.start_x, event.x) / self.scale)
        y1 = int(min(self.start_y, event.y) / self.scale)
        x2 = int(max(self.start_x, event.x) / self.scale)
        y2 = int(max(self.start_y, event.y) / self.scale)

        if (x2 - x1) < 10 or (y2 - y1) < 10:
            print("  Selection too small — try again")
            return

        crop = self.screenshot.crop((x1, y1, x2, y2))
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        crop.save(OUTPUT_PATH)
        print(f"\n  ✅ Saved indicator ({crop.size[0]}x{crop.size[1]}px) -> {OUTPUT_PATH}")
        print("  The instalocker will now wait for this element before locking.")
        self.root.destroy()

    def run(self):
        self.countdown_and_screenshot()
        self.build_window()
        self.root.mainloop()


if __name__ == "__main__":
    tool = IndicatorCapture()
    tool.run()
