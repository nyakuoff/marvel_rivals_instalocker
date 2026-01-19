#!/usr/bin/env python3
"""
Marvel Rivals Instalocker Setup Script

Run this script to automatically install all required dependencies
and verify that the instalocker is ready to use.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def verify_images():
    """Verify that hero images are present."""
    print("🖼️ Verifying hero images...")
    images_dir = Path("images")
    
    if not images_dir.exists():
        print("❌ Images directory not found!")
        return False
    
    image_files = list(images_dir.glob("*.png")) + list(images_dir.glob("*.PNG"))
    
    if len(image_files) < 30:  # Should have at least 30+ hero images
        print(f"⚠️ Warning: Only found {len(image_files)} image files. Expected 30+")
    else:
        print(f"✅ Found {len(image_files)} hero image files")
    
    return True

def verify_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def main():
    """Main setup function."""
    print("🚀 Marvel Rivals Instalocker Setup")
    print("=" * 40)
    
    # Check Python version
    if not verify_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Verify images
    if not verify_images():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Launch Marvel Rivals")
    print("2. Run: python instalocker_gui.py")
    print("3. Select your favorite hero!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)