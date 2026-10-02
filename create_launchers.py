#!/usr/bin/env python3
"""
Create Windows batch file launchers for Color Separation & Ink Analysis

This script creates RUN_DESKTOP.bat and RUN_WEB.bat files
if you prefer not to create them manually.

Usage:
    python create_launchers.py
"""

import os
from pathlib import Path

def create_batch_files():
    """Create Windows batch launcher files"""
    
    # Get current directory
    current_dir = Path.cwd()
    
    # Create RUN_DESKTOP.bat
    desktop_bat = current_dir / "RUN_DESKTOP.bat"
    with open(desktop_bat, 'w') as f:
        f.write('@echo off\n')
        f.write('REM Color Separation & Ink Analysis - Desktop Application\n')
        f.write('python ColorAnalysisApp.py\n')
        f.write('pause\n')
    
    print(f"✓ Created: RUN_DESKTOP.bat")
    print(f"  Location: {desktop_bat}")
    
    # Create RUN_WEB.bat
    web_bat = current_dir / "RUN_WEB.bat"
    with open(web_bat, 'w') as f:
        f.write('@echo off\n')
        f.write('REM Color Separation & Ink Analysis - Web Application\n')
        f.write('streamlit run color_separation_app.py\n')
        f.write('pause\n')
    
    print(f"✓ Created: RUN_WEB.bat")
    print(f"  Location: {web_bat}")
    
    print("\n✅ Done! You can now double-click either .bat file to run the app.")
    print("\nUsage:")
    print("  RUN_DESKTOP.bat  - Launch desktop application")
    print("  RUN_WEB.bat      - Launch web application (browser-based)")

if __name__ == '__main__':
    try:
        create_batch_files()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nIf this doesn't work, create the files manually:")
        print("1. Open Notepad")
        print("2. Type: @echo off")
        print("3. Type: python ColorAnalysisApp.py")
        print("4. Type: pause")
        print("5. Save as: RUN_DESKTOP.bat (All Files type)")
        print("\nRepeat for RUN_WEB.bat with:")
        print("  @echo off")
        print("  streamlit run color_separation_app.py")
        print("  pause")
