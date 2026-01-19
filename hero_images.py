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
    },
    "strategist": {
        "Jeff the Land Shark": "images/strat_jeff.png",
        "Adam Warlock": "images/strat_adam.PNG",
        "Loki": "images/strat_loki.PNG",
        "Cloak & Dagger": "images/strat_cloak.PNG",
        "Luna Snow": "images/strat_luna.PNG",
        "Rocket Raccoon": "images/strat_raccoon.PNG",
        "Mantis": "images/strat_mantis.PNG",
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
    },
}

# Screen coordinates for role selection buttons (for 1920x1080 resolution)
duelist_button_coords = (1775, 364)
strategist_button_coords = (1817, 442)  # Renamed from strat_button_coords
vanguard_button_coords = (1733, 281)
lock_button_coords = (1660, 725)

# Game indicator image for detecting hero selection screen
game_indicator_path = "images/game_indicator.PNG"