Overview
    This project is an attempt to create an old-school JRPG (Japanese Role-Playing Game) with a combination of real-time exploration and a turn-based combat system. The game initiates the turn-based combat mode when a collision occurs between the player and an enemy. More information about Classes, methods and functions you'll find in code comments.

How to Run
    To run the game, execute the main.py file. Additionally, the tests for the game can be executed using the pytest_style.py file.

Controls
    To move your character use either 'WASD' or arrow buttons. 
    To use healing potion press 'space' button.
    While in combat, use LMB to perform a light attack and RMB to execute a heavy attack (requires maximum energy) 

File Structure
    The game is organized into several Python files, each responsible for specific functionalities:

    1) battle.py: Displays the battle interface and contains the logic for turn-based combat.

    2) entity.py: Manages movement and collision logic, shared between the Player and Enemy classes.

    3) enemy.py: Loads animation sprites for enemies and implements chase logic.

    4) player.py: Loads animation sprites for the player and handles input logic.

    5) level.py: The Level class loads the level map from a CSV file using the import_csv_layout function from support.py. This class is also responsible for displaying the map and switching between battle and exploration modes.

    6) import_graphics.py: A support file used for sprite scaling.

    7) menu.py: Displays the menu immediately after running main.py.

    8) tile.py: Contains logic related to tiles.

    9) ui.py: Manages the user interface elements.

    10) support.py: A support file with functions used across various other classes.

    11) settings.py: Contains constant values for the game that can be modified.

Running the Game
    Upon running main.py, a menu will be displayed, allowing you to navigate through the game. The game seamlessly switches between exploration and battle modes based on player interactions.

Testing
    To ensure the robustness of the game, a set of tests is available in the pytest_game.py file. Run these tests using a testing framework like pytest to verify the correctness of the implemented features.