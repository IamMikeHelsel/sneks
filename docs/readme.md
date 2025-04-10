# Modern Python Snake Game

## Description

A classic Snake game implemented in Python with a highly performant, modern and beautiful graphical user interface (GUI). The project follows Test-Driven Development (TDD) principles using `pytest` for testing and `pytest-cov` for monitoring code coverage.

## Features

* Classic Snake gameplay: Control the snake to eat food and grow longer.
* **Modern UI System**: Beautiful visuals with smooth animations, particle effects, and transitions.
* **Multiple Game Screens**: Professional menu screen and in-game interface.
* **Enhanced Visual Elements**: Anti-aliased shapes, gradients, and shadows for visual appeal.
* **Interactive UI Components**: Animated buttons with visual feedback and hover effects.
* **Pause Functionality**: Clean pause menu with resume and main menu options.
* Score Tracking: Animated score display with visual feedback when points are earned.
* Game Over Detection: The game ends if the snake hits the boundaries or itself.
* Keyboard Controls: Intuitive controls for snake movement.

## Technology Stack

* **Language:** Python 3.x
* **GUI Framework:** Pygame
* **UI Architecture:** Component-based modular system with:
  * Screen management system
  * Particle effect engine
  * Animation framework
  * Interactive UI components
* **Rendering:** Hardware-accelerated graphics with optimized pre-rendering
* **Testing:** `pytest`
* **Code Coverage:** `pytest-cov`

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: Ensure `requirements.txt` lists all necessary packages, including the GUI library, pytest, and pytest-cov).*


## How to Run the Game

Execute the main Python script to start the game:

```bash
python main.py
```

### Testing the New UI

The enhanced UI system includes several features you can test:

1. **Main Menu**: When you start the game, you'll see a modern menu screen with:
   * Animated background and particle effects
   * Interactive buttons with hover and click animations
   * Stylish title with subtle animations

2. **Game Interface**: During gameplay, test these enhanced features:
   * Smooth, rounded snake segments with gradient effects
   * Pulsing food animation with glow effects
   * Animated score counter that increases with visual feedback
   * Press P or ESC to open the pause menu

3. **Pause Menu**: The pause system allows you to:
   * Temporarily stop the game with a stylish overlay
   * Resume gameplay by clicking the Resume button
   * Return to the main menu with the Main Menu button

4. **Game Over Screen**: When the game ends:
   * A smooth fade overlay appears
   * Try the Restart button to begin a new game immediately
   * Return to the main menu via the Main Menu button

## How to Run Tests

Tests are written using `pytest` and ensure the core game logic functions correctly.

1. **Run all tests:**

    ```bash
    pytest
    ```

2. **Run tests with coverage report:**

    ```bash
    pytest --cov=src --cov-report=html
    ```

    *(Note: Replace `src` with the actual source directory name. This command generates an HTML coverage report in the `htmlcov` directory.)*

## Future Development Ideas

Here are some ideas for future enhancements to the Snake game:

1. **Game Modes**
   * Survival mode with increasing difficulty
   * Time attack mode
   * Maze mode with obstacles
   * Mission-based levels with specific goals

2. **Enhanced Features**
   * High score system with persistent storage
   * Customizable game settings (speed, grid size, etc.)
   * Power-ups and special food items
   * Additional visual themes/skins
   * Sound effects and background music

3. **Technical Improvements**
   * Optimizations for better performance on low-end devices
   * Support for gamepad/controller input
   * AI opponent or demo mode
   * Online multiplayer functionality
   * Mobile-friendly touch controls

## Distribution Options

Consider these options for distributing your Snake game:

1. **Desktop Application**
   * Package as standalone executable using PyInstaller
     ```bash
     pip install pyinstaller
     pyinstaller --onefile --windowed main.py
     ```
   * Create platform-specific installers using tools like Inno Setup (Windows) or AppImage (Linux)
   * Distribute via GitHub Releases with version tracking

2. **Web Distribution**
   * Convert to web application using Pygbag or Pyodide
   * Host on GitHub Pages or similar free hosting services
   * Share on game portals like itch.io or Game Jolt

3. **Package Distribution**
   * Publish to PyPI (Python Package Index)
     ```bash
     pip install setuptools wheel twine
     python setup.py sdist bdist_wheel
     twine upload dist/*
     ```
   * This allows users to install with `pip install snake-game`

4. **Alternative Platforms**
   * Package in Docker container for consistent deployment
   * Create Android/iOS versions using Pygame subset for mobile or Kivy
   * Consider game engine exports (e.g., via Godot with Python integration)
