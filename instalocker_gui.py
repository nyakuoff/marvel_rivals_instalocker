"""
Marvel Rivals Instalocker - Main GUI Application
"""

import tkinter as tk
from tkinter import ttk
from instalocker_helpers import (
    select_category, cancel_monitoring,
    display_hero_image, display_locked_hero_message,
    start_game_monitoring,
)

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#0f1117"
BG_PANEL = "#1a1d27"
BG_CARD  = "#22263a"
ACCENT_D = "#ef4444"
ACCENT_S = "#3b82f6"
ACCENT_V = "#10b981"
FG       = "#e2e8f0"
FG_DIM   = "#64748b"


def _make_scrollable(parent):
    """Return (canvas, inner_frame). Pack your widgets into inner_frame."""
    canvas = tk.Canvas(parent, bg=BG_PANEL, highlightthickness=0)
    sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)

    inner = tk.Frame(canvas, bg=BG_PANEL)
    win = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfig(win, width=e.width))

    def _scroll(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _scroll_linux(e):
        canvas.yview_scroll(-1 if e.num == 4 else 1, "units")

    canvas.bind_all("<MouseWheel>", _scroll)
    canvas.bind_all("<Button-4>",   _scroll_linux)
    canvas.bind_all("<Button-5>",   _scroll_linux)

    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    return canvas, inner


def main():
    root = tk.Tk()
    root.title("Marvel Rivals Instalocker")
    root.geometry("520x640")
    root.configure(bg=BG)
    root.resizable(True, True)
    root.minsize(420, 480)

    try:
        root.iconbitmap("images/icon.ico")
    except Exception:
        pass

    # ── Header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(root, bg="#0d0f1a", pady=12)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Marvel Rivals Instalocker",
             font=("Arial", 17, "bold"), fg=FG, bg="#0d0f1a").pack()

    # ── Category tabs ─────────────────────────────────────────────────────────
    tabs = tk.Frame(root, bg=BG, pady=8)
    tabs.pack(anchor="center")

    def _switch(cat, color, btn):
        for w in tabs.winfo_children():
            w.config(bg=BG_CARD, fg=FG_DIM)
        btn.config(bg=color, fg="white")
        select_category(cat, frame_heroes, root)
        hero_canvas.yview_moveto(0)

    def _tab(label, cat, color):
        b = tk.Button(tabs, text=label,
                      font=("Arial", 10, "bold"),
                      bg=BG_CARD, fg=FG_DIM,
                      activebackground=color, activeforeground="white",
                      relief="flat", bd=0, padx=18, pady=8, cursor="hand2")
        b.config(command=lambda: _switch(cat, color, b))
        b.pack(side="left", padx=4)

    _tab("Duelist",    "duelist",    ACCENT_D)
    _tab("Vanguard",   "vanguard",   ACCENT_V)
    _tab("Strategist", "strategist", ACCENT_S)

    # State
    root._pending_hero = None
    root._pending_category = None

    # ── Scrollable hero grid ───────────────────────────────────────────────────
    grid_wrap = tk.Frame(root, bg=BG_PANEL)
    grid_wrap.pack(fill="both", expand=True, padx=12, pady=(4, 6))

    hero_canvas, frame_heroes = _make_scrollable(grid_wrap)
    root.hero_canvas = hero_canvas

    # ── Status / action bar ───────────────────────────────────────────────────
    bar = tk.Frame(root, bg="#0d0f1a", padx=14, pady=8)
    bar.pack(fill="x", side="bottom")

    root.hero_label = tk.Label(bar, bg="#0d0f1a", bd=0)
    root.hero_label.pack(side="left", padx=(0, 8))

    root.locked_hero_label = tk.Label(
        bar, text="Select a hero",
        font=("Arial", 11, "bold"), fg=FG_DIM, bg="#0d0f1a"
    )
    root.locked_hero_label.pack(side="left")

    # Confirm button — hidden until a hero is staged
    root.confirm_btn = tk.Button(
        bar, text="Lock in  ▶",
        font=("Arial", 10, "bold"),
        bg=ACCENT_V, fg="white",
        activebackground="#0d9e6e", activeforeground="white",
        relief="flat", bd=0, padx=14, pady=4, cursor="hand2",
    )

    esc_hint = tk.Label(bar, text="Esc = cancel",
                        font=("Arial", 8), fg=FG_DIM, bg="#0d0f1a")
    esc_hint.pack(side="right")

    # ── Hero selection callback (preview only) ────────────────────────────────
    def _on_hero_click(hero_name, category):
        cancel_monitoring()                          # stop any previous monitor
        root._pending_hero = hero_name
        root._pending_category = category
        display_hero_image(hero_name, category, root)
        root.locked_hero_label.config(
            text=f"{hero_name}", fg="#f59e0b"
        )
        root.confirm_btn.pack(side="left", padx=(10, 0))

    root.on_hero_click = _on_hero_click
    select_category.__globals__['_gui_hero_callback'] = _on_hero_click

    # ── Confirm callback ──────────────────────────────────────────────────────
    def _confirm(e=None):
        if not root._pending_hero:
            return
        hero, cat = root._pending_hero, root._pending_category
        root._pending_hero = None
        root.confirm_btn.pack_forget()
        root.locked_hero_label.config(text=f"🔍 Waiting for game...  {hero}", fg="#94a3b8")
        display_locked_hero_message(root, hero)
        start_game_monitoring(hero, cat)

    root.confirm_btn.config(command=_confirm)
    root.bind("<Return>", _confirm)

    # ── Cancel callback ───────────────────────────────────────────────────────
    def _cancel(e=None):
        root._pending_hero = None
        root.confirm_btn.pack_forget()
        cancel_monitoring()
        root.locked_hero_label.config(text="Cancelled — select a hero", fg="#ef4444")

    root.bind("<Escape>", _cancel)

    root.mainloop()


if __name__ == "__main__":
    main()