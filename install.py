#!/usr/bin/env python3
"""
Smart Notes Installation Script
Automated setup for Smart Notes application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("         Smart Notes Installation Script")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_tkinter():
    """Check if tkinter is available"""
    print("Checking tkinter availability...")
    try:
        import tkinter
        print("✅ tkinter is available")
        return True
    except ImportError:
        print("❌ Error: tkinter is not available")
        print("   Please install tkinter:")

        system = platform.system().lower()
        if system == "linux":
            print("   Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   CentOS/RHEL: sudo yum install tkinter")
            print("   Arch: sudo pacman -S tk")
        elif system == "darwin":
            print("   macOS: tkinter should be included with Python")
            print("   If not, reinstall Python from python.org")
        elif system == "windows":
            print("   Windows: tkinter should be included with Python")
            print("   If not, reinstall Python from python.org")

        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")

    try:
        # Check if requirements.txt exists
        if not Path("requirements.txt").exists():
            print("❌ Error: requirements.txt not found")
            return False

        # Install dependencies
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Linux/Windows)"""
    print("Creating desktop shortcut...")

    try:
        system = platform.system().lower()
        current_dir = Path.cwd().absolute()
        script_path = current_dir / "smartnotes.py"

        if system == "linux":
            # Create .desktop file
            desktop_dir = Path.home() / "Desktop"
            if not desktop_dir.exists():
                desktop_dir = Path.home() / ".local" / "share" / "applications"
                desktop_dir.mkdir(parents=True, exist_ok=True)

            desktop_file = desktop_dir / "smart-notes.desktop"

            desktop_content = f"""[Desktop Entry]
Name=Smart Notes
Comment=Modern note-taking app with AI assistance
Exec={sys.executable} "{script_path}"
Icon=text-editor
Terminal=false
Type=Application
Categories=Office;TextEditor;
"""

            with open(desktop_file, 'w') as f:
                f.write(desktop_content)

            # Make executable
            os.chmod(desktop_file, 0o755)
            print(f"✅ Desktop shortcut created: {desktop_file}")

        elif system == "windows":
            # Create batch file for easy launching
            batch_file = current_dir / "Smart Notes.bat"

            batch_content = f"""@echo off
cd /d "{current_dir}"
"{sys.executable}" smartnotes.py
pause
"""

            with open(batch_file, 'w') as f:
                f.write(batch_content)

            print(f"✅ Launcher created: {batch_file}")
            print("   You can copy this to your Desktop for easy access")

        elif system == "darwin":
            print("ℹ️  macOS: You can create an alias or use Automator to create an app")
            print(f"   Script location: {script_path}")

        return True

    except Exception as e:
        print(f"⚠️  Warning: Could not create shortcut: {e}")
        return False

def test_installation():
    """Test if the application can start"""
    print("Testing installation...")

    try:
        # Try to import the main modules
        sys.path.insert(0, str(Path.cwd()))

        # Test basic imports
        import json
        import datetime
        import tkinter as tk

        print("✅ Core modules imported successfully")

        # Test if Google AI is available (optional)
        try:
            import google.generativeai as genai
            print("✅ Google Generative AI available")
        except ImportError:
            print("⚠️  Google Generative AI not available (install with: pip install google-generativeai)")

        return True

    except Exception as e:
        print(f"❌ Error testing installation: {e}")
        return False

def print_completion_message():
    """Print installation completion message"""
    print()
    print("=" * 60)
    print("         Installation Complete!")
    print("=" * 60)
    print()
    print("🎉 Smart Notes has been installed successfully!")
    print()
    print("To run Smart Notes:")
    print(f"   python {Path.cwd() / 'smartnotes.py'}")
    print()
    print("First-time setup:")
    print("1. Launch Smart Notes")
    print("2. Click 'Assign API' to configure Google Gemini (optional)")
    print("3. Start creating notes!")
    print()
    print("For help and documentation:")
    print("   - Click 'Tutorial' in the app")
    print("   - Read README.md")
    print("   - Visit our GitHub repository")
    print()

def main():
    """Main installation function"""
    print_header()

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    if not check_tkinter():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed: Could not install dependencies")
        sys.exit(1)

    # Create shortcuts
    create_desktop_shortcut()

    # Test installation
    if not test_installation():
        print("⚠️  Installation completed with warnings")

    # Print completion message
    print_completion_message()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)
