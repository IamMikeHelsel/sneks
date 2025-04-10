# Development Steps / Task List

This is a detailed breakdown of potential steps following TDD principles:

## Phase 1: Project Setup & Core Dependencies

1. Initialize Git repository (`git init`).
2. Create project structure (e.g., `src/`, `tests/`, `docs/`).
3. Set up Python virtual environment (`python -m venv venv`).
4. Activate virtual environment.
5. Install `pytest` (`pip install pytest`).
6. Install `pytest-cov` (`pip install pytest-cov`).
7. Install `pygame` (`pip install pygame`).
8. Create `requirements.txt` (`pip freeze > requirements.txt`).
9. Configure `pytest` (e.g., `pytest.ini` if needed).
10. Create initial empty source files (e.g., `src/main.py`, `src/game.py`, `src/snake.py`, `src/food.py`, `src/config.py`).
11. Create initial empty test files (e.g., `tests/test_snake.py`, `tests/test_food.py`, `tests/test_game.py`).
12. Write a simple dummy test to ensure `pytest` runs.
13. Run `pytest` to confirm setup.
14. Run `pytest --cov=src` to confirm coverage setup.

### Phase 2: Core Game Logic (TDD)

* **Configuration:**
    1. Define constants (screen width, height, grid size, colors, speed) in `src/config.py`.
    2. Write tests to verify config values can be loaded/accessed (if applicable, might be simple constants).
* **Snake Logic (`src/snake.py`, `tests/test_snake.py`):**
    1. Write test for Snake initialization (position, initial body).
    2. Define `Snake` class.
    3. Implement `Snake.__init__`.
    4. Write test for Snake moving up.
    5. Implement `Snake.move()` logic for 'UP'.
    6. Write test for Snake moving down.
    7. Implement `Snake.move()` logic for 'DOWN'.
    8. Write test for Snake moving left.
    9. Implement `Snake.move()` logic for 'LEFT'.
    10. Write test for Snake moving right.
    11. Implement `Snake.move()` logic for 'RIGHT'.
    12. Write test for changing direction up.
    13. Implement `Snake.change_direction()` for 'UP'.
    14. Write test for changing direction down.
    15. Implement `Snake.change_direction()` for 'DOWN'.
    16. Write test for changing direction left.
    17. Implement `Snake.change_direction()` for 'LEFT'.
    18. Write test for changing direction right.
    19. Implement `Snake.change_direction()` for 'RIGHT'.
    20. Write test to prevent reversing direction (e.g., can't go left if moving right).
    21. Add direction reversal prevention logic to `Snake.change_direction()`.
    22. Write test for snake growth.
    23. Implement `Snake.grow()` method.
    24. Write test for checking collision with self (simple case).
    25. Implement `Snake.check_self_collision()` method.
    26. Write test for checking collision with self (complex case).
    27. Refine `Snake.check_self_collision()`.
    28. Write test for getting snake head position.
    29. Implement property/method for `Snake.get_head_position()`.
    30. Write test for getting snake body segments.
    31. Implement property/method for `Snake.get_body()`.
* **Food Logic (`src/food.py`, `tests/test_food.py`):**
    1. Write test for Food initialization (position).
    2. Define `Food` class.
    3. Implement `Food.__init__`.
    4. Write test for randomizing food position within bounds.
    5. Implement `Food.randomize_position(max_x, max_y)`.
    6. Write test to ensure new food position avoids snake body.
    7. Modify `Food.randomize_position(max_x, max_y, snake_body)`.
    8. Write test for getting food position.
    9. Implement property/method for `Food.get_position()`.
* **Game Logic (`src/game.py`, `tests/test_game.py`):**
    1. Write test for Game initialization (creates Snake, Food, sets initial state).
    2. Define `Game` class.
    3. Implement `Game.__init__(width, height)`.
    4. Write test for updating game state (move snake).
    5. Implement `Game.update()`.
    6. Write test for snake eating food (score increases, snake grows, food moves).
    7. Add food eating logic to `Game.update()`.
    8. Write test for checking wall collision (top).
    9. Add wall collision logic to `Game.update()` or a dedicated method.
    10. Write test for checking wall collision (bottom).
    11. Refine wall collision logic.
    12. Write test for checking wall collision (left).
    13. Refine wall collision logic.
    14. Write test for checking wall collision (right).
    15. Refine wall collision logic.
    16. Write test for checking snake self-collision in Game update.
    17. Add self-collision check to `Game.update()`.
    18. Write test for game over state transition (wall collision).
    19. Implement game state management (`is_game_over`).
    20. Write test for game over state transition (self-collision).
    21. Refine game state management.
    22. Write test for getting current score.
    23. Implement `Game.get_score()`.
    24. Write test for handling direction change input.
    25. Implement `Game.handle_input(direction)`.
    26. Write test for resetting the game.
    27. Implement `Game.reset()`.
    28. Review test coverage (`pytest --cov=src`).
    29. Add tests for any uncovered logic branches.

**Phase 3: Pygame GUI Implementation (`src/main.py`, potentially `src/graphics.py`)**

1. Create basic Pygame window initialization in `src/main.py`.
2. Implement the main game loop structure (event handling, update, draw).
3. Add basic event handling (QUIT event).
4. Create a function/class to draw the game background/grid.
5. Call drawing function in the main loop.
6. Create a function/class to draw the Snake (using `Game` object state).
7. Call snake drawing function in the main loop.
8. Create a function/class to draw the Food (using `Game` object state).
9. Call food drawing function in the main loop.
10. Implement keyboard event handling (Arrow keys).
11. Connect keyboard events to `Game.handle_input()`.
12. Integrate `Game.update()` into the main loop.
13. Add game clock (`pygame.time.Clock`) to control frame rate/game speed.
14. Create a function to draw the score on the screen.
15. Call score drawing function in the main loop.
16. Implement drawing the "Game Over" message when `Game.is_game_over` is true.
17. Add logic to pause the game update loop when game is over.
18. Add event handling (e.g., pressing Enter/Space) to reset the game using `Game.reset()` when game is over.
19. Refine colors and visual appearance.
20. Add window title.
21. Consider adding simple sound effects (optional).

## Phase 4: Integration, Refinement & Documentation

1. Perform end-to-end testing by playing the game.
2. Debug any issues found during gameplay.
3. Adjust game speed (`tick` rate or movement delay) for playability.
4. Refactor code for clarity and efficiency (e.g., separate graphics concerns).
5. Add comments and docstrings to code.
6. Ensure README is up-to-date with final instructions.
7. Run final tests and check coverage (`pytest --cov=src`).
8. Add any missing tests.
9. Finalize `requirements.txt`.
10. Consider error handling (e.g., Pygame initialization errors).

## Contributing

[Optional: Add guidelines for contributing if the project is open source.]

## License

[Optional: Specify the license under which the project is distributed, e.g., MIT License.]
