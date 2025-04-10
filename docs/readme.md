# Python Snake Game

## Description

A classic Snake game implemented in Python with a modern graphical user interface (GUI). The project follows Test-Driven Development (TDD) principles using `pytest` for testing and `pytest-cov` for monitoring code coverage.

## Features

* Classic Snake gameplay: Control the snake to eat food and grow longer.
* Modern GUI: A visually appealing and user-friendly interface.
* Score Tracking: Keep track of your score as you eat food.
* Game Over Detection: The game ends if the snake hits the boundaries or itself.
* Keyboard Controls: Intuitive controls for snake movement.

## Technology Stack

* **Language:** Python 3.x
* **GUI:** Pygame
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

*(Note: Replace `main.py` with the actual entry point script name if different).*

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
