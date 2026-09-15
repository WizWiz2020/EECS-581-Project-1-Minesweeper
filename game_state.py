"""
Game state and victory logic for Minesweeper.
"""

PLAYING = "Playing"
VICTORY = "Victory"
LOSS = "Game Over: Loss"

game_status = PLAYING


def check_victory(grid):
    """
    Check whether all non-mine cells have been revealed.
    """
    global game_status

    for row in grid:
        for cell in row:
            if not cell.is_mine and not cell.is_revealed:
                return False

    game_status = VICTORY
    return True


def set_game_over():
    """
    Set the game state to loss.
    """
    global game_status
    game_status = LOSS


def reset_game_status():
    """
    Reset the game state for a new game.
    """
    global game_status
    game_status = PLAYING


def get_game_status():
    """
    Return the current game status.
    """
    return game_status
