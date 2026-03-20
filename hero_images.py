"""
Hero image path mappings for Marvel Rivals Instalocker.

This module contains the file paths for all hero portrait images organized by role category.
All hero images should be 100x100 pixels for optimal display in the GUI.
"""

hero_image_paths = {
    "duelist": {
        "Hawkeye": "images/duelist_hawkeye.PNG",
        "Black Panther": "images/duelist_BlackPanther.PNG", 
        "Black Widow": "images/duelist_blackwidow.PNG",
        "Iron Man": "images/duelist_ironman.PNG",
        "Iron Fist": "images/duelist_ironfist.PNG",
        "Magik": "images/duelist_magik.PNG",
        "Moon Knight": "images/duelist_moon.PNG",
        "Namor": "images/duelist_namor.PNG",
        "Psylocke": "images/duelist_psylocke.PNG",
        "Scarlet Witch": "images/duelist_scarlet.PNG",
        "Spider-Man": "images/duelist_SpiderMan.PNG",
        "Squirrel Girl": "images/duelist_Squirrel.PNG",
        "Star-Lord": "images/duelist_Starlord.PNG",
        "Storm": "images/duelist_storm.PNG",
        "The Punisher": "images/duelist_thepunisher.PNG",
        "Hela": "images/duelist_hela.PNG",
        "Winter Soldier": "images/duelist_wintersoldier.PNG",
        "Wolverine": "images/duelist_wolverine.PNG",
        "Phoenix": "images/duelist_phoenix.PNG",
        "Daredevil": "images/duelist_daredevil.PNG",
        "Blade": "images/duelist_blade.PNG",
        "Human Torch": "images/duelist_humantorch.PNG",
        "Mr. Fantastic": "images/duelist_mrfantastic.PNG",
        "Deadpool": "images/duelist_deadpool.PNG",
        "Elsa Bloodstone": "images/duelist_elsa.PNG",
    },
    "strategist": {
        "Jeff the Land Shark": "images/strat_jeff.png",
        "Adam Warlock": "images/strat_adam.PNG",
        "Loki": "images/strat_loki.PNG",
        "Cloak & Dagger": "images/strat_cloak.PNG",
        "Luna Snow": "images/strat_luna.PNG",
        "Rocket Raccoon": "images/strat_raccoon.PNG",
        "Mantis": "images/strat_mantis.PNG",
        "Invisible Woman": "images/strat_invisiblewoman.PNG",
        "Gambit": "images/strat_gambit.PNG",
        "Deadpool": "images/strat_deadpool.PNG",
        "Ultron": "images/strat_ultron.PNG",
        "White Fox": "images/strat_whitefox.PNG",
    },
    "vanguard": {
        "Thor": "images/vanguard_thor.PNG",
        "Venom": "images/vanguard_venom.PNG",
        "Captain America": "images/vanguard_CaptainAmerica.PNG",
        "Doctor Strange": "images/vanguard_DoctorStrange.PNG",
        "Groot": "images/vanguard_groot.PNG",
        "Hulk": "images/vanguard_hulk.PNG",
        "Magneto": "images/vanguard_magento.PNG",
        "Peni Parker": "images/vanguard_PeniParker.PNG",
        "Rogue": "images/vanguard_rogue.PNG",
        "Emma Frost": "images/vanguard_emmafrost.PNG",
        "Deadpool": "images/vanguard_deadpool.PNG",
        "The Thing": "images/vanguard_thing.PNG",
        "Angela": "images/vanguard_angela.PNG",
    },
}

# Screen coordinates for role selection buttons (for 1920x1080 resolution)
duelist_button_coords = (3650, 285)
strategist_button_coords = (3700, 360)
vanguard_button_coords = (3600, 225)
lock_button_coords = (3600, 725)

# Coordinate anywhere on the hero wheel (used for scrolling).
# Capture with: python find_coords.py  (it will prompt for "wheel scroll point")
wheel_scroll_coords = (3500, 335)

# How many scroll clicks down each hero requires before it becomes visible.
# 0 = visible immediately. Increase for heroes lower in the wheel.
# Run the instalocker and check which heroes fail, then increment their value until they work.
hero_scroll_steps = {
    # --- Duelist ---
    "Hawkeye": 0,
    "Black Panther": 0,
    "Black Widow": 0,
    "Iron Man": 0,
    "Iron Fist": 0,
    "Magik": 0,
    "Moon Knight": 0,
    "Namor": 0,
    "Psylocke": 0,
    "Scarlet Witch": 0,
    "Spider-Man": 0,
    "Squirrel Girl": 0,
    "Star-Lord": 0,
    "Storm": 0,
    "The Punisher": 0,
    "Hela": 0,
    "Winter Soldier": 0,
    "Wolverine": 0,
    "Phoenix": 1,
    "Daredevil": 2,
    "Blade": 2,
    "Human Torch": 1,
    "Mr. Fantastic": 1,
    "Deadpool": 2,
    "Elsa Bloodstone": 4,
    # --- Strategist ---
    "Jeff the Land Shark": 0,
    "Adam Warlock": 0,
    "Loki": 0,
    "Cloak & Dagger": 0,
    "Luna Snow": 0,
    "Rocket Raccoon": 0,
    "Mantis": 0,
    "Invisible Woman": 0,
    "Gambit": 0,
    "Ultron": 0,
    "White Fox": 0,
    # --- Vanguard ---
    "Thor": 0,
    "Venom": 0,
    "Captain America": 0,
    "Doctor Strange": 0,
    "Groot": 0,
    "Hulk": 0,
    "Magneto": 0,
    "Peni Parker": 0,
    "Rogue": 0,
    "Emma Frost": 0,
    "The Thing": 0,
    "Angela": 0,
}

# Game indicator image for detecting hero selection screen
game_indicator_path = "images/game_indicator.PNG"