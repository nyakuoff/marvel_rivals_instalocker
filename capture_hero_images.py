"""
Hero Image Capture Tool for Marvel Rivals Instalocker

Walks you through capturing hero portraits category by category.
Within each category, you can take multiple screenshots to handle scrolling.

Usage:
    python capture_hero_images.py
"""

import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import time
import os
from instalocker_helpers import MONITOR_OFFSET_X, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT
from hero_images import hero_image_paths

CROP_SIZE = 80  # pixels to crop around each click (square)
COUNTDOWN = 5

CATEGORY_INSTRUCTIONS = {
    "duelist":    "Switch to Marvel Rivals → click the 🔥 DUELIST tab",
    "strategist": "Switch to Marvel Rivals → click the 🧠 STRATEGIST tab",
    "vanguard":   "Switch to Marvel Rivals → click the 🛡️ VANGUARD tab",
}


class ImageCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hero Image Capture Tool")
        self.screenshot = None
        self.screenshot_tk = None
        self.canvas = None
        self.scale = 1.0
        self.disp_w = 0
        self.disp_h = 0

        self.categories = list(hero_image_paths.keys())
        self.todo_by_category = {
            cat: list(heroes.items())
            for cat, heroes in hero_image_paths.items()
        }
        self.done = []
        self.skipped = []
        self.current_category_index = 0
        self.current_hero = None
        self.current_path = None

    # ------------------------------------------------------------------
    # Screenshot helpers
    # ------------------------------------------------------------------

    def countdown_and_screenshot(self, instruction: str):
        self.root.withdraw()
        print(f"\n  ➡  {instruction}")
        print("     Screenshot in:", end="", flush=True)
        for i in range(COUNTDOWN, 0, -1):
            print(f" {i}", end="", flush=True)
            time.sleep(1)
        print(" 📸")
        region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
        self.screenshot = pyautogui.screenshot(region=region)
        self.root.deiconify()
        self._refresh_canvas()

    def _refresh_canvas(self):
        if self.canvas is None:
            return
        display_img = self.screenshot.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        self.screenshot_tk = ImageTk.PhotoImage(display_img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.screenshot_tk)

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _build_window(self):
        screen_w = self.root.winfo_screenwidth() // 2
        screen_h = self.root.winfo_screenheight() - 120
        img_w, img_h = self.screenshot.size
        self.scale = min(screen_w / img_w, screen_h / img_h, 1.0)
        self.disp_w = int(img_w * self.scale)
        self.disp_h = int(img_h * self.scale)

        self.root.geometry(f"{self.disp_w}x{self.disp_h + 90}+0+0")
        self.root.configure(bg="#1e1e1e")

        self.category_label = tk.Label(
            self.root, text="", font=("Arial", 11, "bold"),
            bg="#2d3a4a", fg="#7ec8e3", pady=4
        )
        self.category_label.pack(fill="x")

        self.status_label = tk.Label(
            self.root, text="", font=("Arial", 12, "bold"),
            bg="#1e1e1e", fg="white", pady=4
        )
        self.status_label.pack(fill="x")

        display_img = self.screenshot.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        self.screenshot_tk = ImageTk.PhotoImage(display_img)
        self.canvas = tk.Canvas(
            self.root, width=self.disp_w, height=self.disp_h,
            bg="black", cursor="crosshair", highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.screenshot_tk)
        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=4)

        tk.Button(
            btn_frame, text="⏭  Skip hero", command=self.skip_hero,
            bg="#444", fg="white", font=("Arial", 10), padx=8
        ).pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="📸  Scroll & retake screenshot", command=self.scroll_retake,
            bg="#1a5276", fg="white", font=("Arial", 10, "bold"), padx=8
        ).pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="➡  Next category (switch tab first)", command=self.next_category_manual,
            bg="#1e8449", fg="white", font=("Arial", 10, "bold"), padx=8
        ).pack(side="left", padx=6)

    # ------------------------------------------------------------------
    # Category flow
    # ------------------------------------------------------------------

    def start_category(self):
        if self.current_category_index >= len(self.categories):
            self.finish()
            return
        cat = self.categories[self.current_category_index]
        instruction = CATEGORY_INSTRUCTIONS.get(cat, f"Switch to the {cat.upper()} tab in Marvel Rivals")
        self.countdown_and_screenshot(instruction)
        self.category_label.config(
            text=f"Category: {cat.upper()}  —  {len(self.todo_by_category[cat])} heroes remaining"
        )
        self.prompt_next()

    def prompt_next(self):
        cat = self.categories[self.current_category_index]
        todo = self.todo_by_category[cat]

        if not todo:
            self.category_label.config(text=f"Category: {cat.upper()}  —  ✅ complete!")
            next_idx = self.current_category_index + 1
            if next_idx < len(self.categories):
                next_cat = self.categories[next_idx].upper()
                self.status_label.config(
                    text=f"✅ {cat.upper()} done!  Switch to {next_cat} tab in-game, then click 'Next category'"
                )
            else:
                self.finish()
            return

        self.current_hero, self.current_path = todo[0]
        self.category_label.config(
            text=f"Category: {cat.upper()}  —  {len(todo)} heroes remaining"
        )
        self.status_label.config(text=f"Click the portrait of:  {self.current_hero}")
        self.root.title(f"Capture: {self.current_hero} ({cat})")

    # ------------------------------------------------------------------
    # User actions
    # ------------------------------------------------------------------

    def on_click(self, event):
        cat = self.categories[self.current_category_index]
        if not self.todo_by_category[cat]:
            return

        real_x = int(event.x / self.scale)
        real_y = int(event.y / self.scale)
        half = CROP_SIZE // 2

        left   = max(real_x - half, 0)
        top    = max(real_y - half, 0)
        right  = min(real_x + half, self.screenshot.width)
        bottom = min(real_y + half, self.screenshot.height)

        crop = self.screenshot.crop((left, top, right, bottom))
        save_dir = os.path.dirname(self.current_path)
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
        crop.save(self.current_path)
        print(f"  ✅ {self.current_hero} ({cat}) -> {self.current_path}")

        hs = half * self.scale
        self.canvas.create_rectangle(
            event.x - hs, event.y - hs, event.x + hs, event.y + hs,
            outline="lime", width=2
        )
        self.canvas.create_text(
            event.x, event.y - hs - 8,
            text=self.current_hero, fill="lime", font=("Arial", 9, "bold")
        )

        self.done.append(self.todo_by_category[cat].pop(0))
        self.prompt_next()

    def skip_hero(self):
        cat = self.categories[self.current_category_index]
        if not self.todo_by_category[cat]:
            return
        hero, _ = self.todo_by_category[cat][0]
        print(f"  ⏭  Skipped {hero} ({cat})")
        self.skipped.append(self.todo_by_category[cat].pop(0))
        self.prompt_next()

    def scroll_retake(self):
        cat = self.categories[self.current_category_index]
        instruction = (
            f"Scroll the hero wheel in Marvel Rivals "
            f"({cat.upper()} tab still selected), then switch back"
        )
        self.countdown_and_screenshot(instruction)
        self.prompt_next()

    def next_category_manual(self):
        self.current_category_index += 1
        if self.current_category_index >= len(self.categories):
            self.finish()
            return
        self.start_category()

    # ------------------------------------------------------------------
    # Finish
    # ------------------------------------------------------------------

    def finish(self):
        print(f"\n{'='*50}")
        print(f"  Done!  Captured: {len(self.done)}  |  Skipped: {len(self.skipped)}")
        remaining = sum(len(v) for v in self.todo_by_category.values())
        if remaining:
            print(f"  Still uncaptured: {remaining}")
            for cat, heroes in self.todo_by_category.items():
                for hero, _ in heroes:
                    print(f"    - {hero} ({cat})")
        print("\n  Re-run instalocker_gui.py — detection should now work.")
        try:
            self.root.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        total = sum(len(v) for v in self.todo_by_category.values())
        print(f"Heroes to capture: {total}")
        print("\nFlow:")
        print("  1. For each category the tool auto-screenshots (5s countdown)")
        print("  2. Click each hero portrait on the wheel as prompted")
        print("  3. If some heroes are off-screen, scroll the wheel in-game then click")
        print("     '📸 Scroll & retake screenshot'")
        print("  4. When all visible heroes are done, switch to the next tab in-game")
        print("     then click '➡ Next category'\n")

        region = (MONITOR_OFFSET_X, 0, GAME_MONITOR_WIDTH, GAME_MONITOR_HEIGHT)
        self.screenshot = pyautogui.screenshot(region=region)

        self.root.withdraw()
        self.root.update()
        self._build_window()
        self.root.deiconify()
        self.root.update()

        self.start_category()
        self.root.mainloop()


if __name__ == "__main__":
    tool = ImageCaptureTool()
    tool.run()
