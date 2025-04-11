"""
Build script to create a single executable file for the Sneks game.
This uses PyInstaller to bundle everything into one .exe file.
"""
import PyInstaller.__main__
import os
import shutil

# Clean previous build files if they exist
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Create the executable with PyInstaller
PyInstaller.__main__.run([
    'main.py',                          # Your script
    '--name=Sneks',                     # Name of the executable
    '--onefile',                        # Create a single file
    '--windowed',                       # Use the windowed subsystem (no console)
    '--add-data=assets;assets',         # Include assets folder
    '--icon=assets/logo.png',           # Use the logo as icon
    '--clean',                          # Clean PyInstaller cache
    '--noconfirm',                      # Replace output without confirmation
])

print("\nBuild complete! Look for the executable in the 'dist' folder.")
