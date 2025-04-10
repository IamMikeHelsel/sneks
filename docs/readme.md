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
