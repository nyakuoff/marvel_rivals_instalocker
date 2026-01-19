# 🚀 Marvel Rivals Instalocker

**Instantly lock your favorite heroes in Marvel Rivals with computer vision and automation!**

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎯 **Instant Hero Selection** - Automatically detects and clicks your chosen hero
- 🖼️ **Visual Recognition** - Uses computer vision to identify heroes on screen
- 🎮 **Easy GUI Interface** - Simple point-and-click hero selection
- ⚡ **Lightning Fast** - Faster than human reaction time
- 🛡️ **Three Role Categories** - Supports Duelist, Strategist, and Vanguard heroes
- 🔄 **Smart Detection** - Waits for game lobby before attempting to lock

## 🎯 Supported Heroes

### 🔥 **Duelists** (17 Heroes)
- Hawkeye, Black Panther, Black Widow, Iron Man, Iron Fist
- Magik, Moon Knight, Namor, Psylocke, Scarlet Witch
- Squirrel Girl, Star-Lord, Storm, The Punisher, Hela
- Winter Soldier, Wolverine

### 🧠 **Strategists** (7 Heroes)  
- Jeff the Land Shark, Adam Warlock, Loki, Cloak & Dagger
- Luna Snow, Rocket Raccoon, Mantis

### 🛡️ **Vanguards** (9 Heroes)
- Captain America, Doctor Strange, Groot, Hulk
- Magneto, Peni Parker, Thor, Venom

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Windows OS (for optimal compatibility)
- Marvel Rivals installed

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Marvel-Rivals-Instalocker.git
   cd Marvel-Rivals-Instalocker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python instalocker_gui.py
   ```

## 🎮 How to Use

1. **Launch Marvel Rivals** and queue for a match
2. **Run the instalocker** using `python instalocker_gui.py`
3. **Select hero category** (Duelist/Strategist/Vanguard)
4. **Click your desired hero** from the visual grid
5. **Wait for match** - the tool will auto-detect the hero select screen
6. **Watch the magic** ✨ - Your hero will be locked instantly!

## 🛠️ How It Works

The instalocker uses advanced computer vision techniques:

1. **Screen Monitoring** - Continuously scans for the hero selection screen
2. **Template Matching** - Uses OpenCV to locate hero portraits
3. **Precise Clicking** - PyAutoGUI handles exact coordinate clicking
4. **Smart Timing** - Only activates when the selection screen is detected

## 📁 Project Structure

```
Marvel-Rivals-Instalocker/
├── 📄 instalocker_gui.py      # Main GUI application
├── 🛠️ instalocker_helpers.py  # Core automation logic
├── 🎨 hero_images.py          # Hero image path mappings
├── 📁 images/                 # Hero portrait images
│   ├── duelist_*.png         # Duelist hero images
│   ├── strat_*.png          # Strategist hero images
│   └── vanguard_*.png       # Vanguard hero images
├── 📄 requirements.txt        # Python dependencies
└── 📄 README.md              # Project documentation
```

## ⚙️ Configuration

### Adding New Heroes
1. Add hero portrait image to `/images/` folder
2. Update `hero_images.py` with the new hero entry
3. Follow the naming convention: `category_heroname.png`

### Adjusting Detection Settings
- Modify confidence thresholds in `instalocker_helpers.py`
- Customize click timing and positioning
- Adjust screen scanning intervals

## 🎯 Technical Details

- **Computer Vision**: OpenCV for template matching
- **GUI Framework**: Tkinter for cross-platform compatibility  
- **Automation**: PyAutoGUI for mouse/keyboard control
- **Image Processing**: PIL/Pillow for image manipulation
- **Hotkeys**: Keyboard library for global key detection

## ⚠️ Important Notes

- **Use Responsibly**: This tool is for personal use and learning purposes
- **Fair Play**: Respect other players and game rules
- **Screen Resolution**: Optimized for 1920x1080, may need adjustments for other resolutions
- **Anticheat**: Use at your own discretion regarding game policies

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a Pull Request

### Todo List
- [ ] Support for different screen resolutions
- [ ] Add sound notifications
- [ ] Implement role queue detection
- [ ] Create hero priority lists
- [ ] Add statistics tracking

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Disclaimer

This tool is created for educational purposes and personal use. The developers are not responsible for any consequences of using this software. Please use responsibly and in accordance with Marvel Rivals' Terms of Service.

## 🙏 Acknowledgments

- **NetEase Games** for creating Marvel Rivals
- **Marvel** for the amazing hero universe
- **OpenCV Community** for computer vision tools
- **Python Community** for excellent libraries

---

**⭐ If this project helped you, please give it a star! ⭐**

*Made with ❤️ for the Marvel Rivals community*