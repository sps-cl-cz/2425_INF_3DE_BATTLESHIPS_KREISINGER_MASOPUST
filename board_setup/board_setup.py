import random
"""
board_setup.py

This module contains the BoardSetup class responsible for:
 - Initializing and resetting a 2D board (0 = water, 1..7 = ship ID).
 - Placing ships according to a dict {ship_id: count}.
 - Providing board statistics and individual tile lookups.
"""

class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        """
        Initializes BoardSetup.
        :param rows: Number of rows in the board.
        :param cols: Number of columns in the board.
        :param ships_dict: Dictionary mapping ship_id -> count.
                           e.g. {1: 2, 2: 1, 3: 1, ...}
        """
        # Tady si uložíme počet řádků, sloupců a lodí
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.total_blocks = rows * cols
        # Tady vytvoříme 2D pole pro board: 0 = voda, 1..7 = ID lodě (viz examples)
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_board(self) -> list[list[int]]:
        """
        Returns the current 2D board state.
        0 = water, 1..7 = specific ship ID.
        """
        return self.board
        raise NotImplementedError("get_board() is not implemented yet.")

    def get_tile(self, x: int, y: int) -> int:
        """
        Returns the value at board coordinate (x, y).
        0 = water, or 1..7 = ship ID.
        
        Raises an IndexError if the coordinates are out of bounds.
        Note: x is column, y is row.
        """
        if (x < 0 or x >= self.cols) or (y < 0 or y >= self.rows):
            raise IndexError("Coordinates out of bounds.")  
        return self.board[y][x]
        raise NotImplementedError("get_tile() is not implemented yet.")

    def place_ships(self) -> None:
        """
        Places ships onto the board according to self.ships_dict.

        - Ensures no overlap.
        - Stays within board bounds.
        - Ships cannot be placed with touching sides (diagonals are OK).
        - If it's impossible, raises ValueError.
        """
        shapes = {
            1: [(0, 0), (0, 1)],  # 2x1 loď
            2: [(0, 0), (0, 1), (0, 2)],  # 3x1 loď
            3: [(0, 0), (0, 1), (0, 2), (0, 3)],  # 4x1 loď
            4: [(0, 0), (0, 1), (0, 2), (1, 1)],  # Tvar "T"
            5: [(0, 0), (1, 0), (2, 0), (2, 1)],  # Tvar "L"
            6: [(0, 0), (0, 1), (1, 1), (1, 2)],  # Jiný "T" tvar
            7: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)]  # Delší Tvar
        }

        def rotate(shape):
            """Rotates the shape 90 degrees clockwise."""
            return [(dy, -dx) for dx, dy in shape]

        def mirror(shape):
            """Mirrors the shape horizontally."""
            return [(dx, -dy) for dx, dy in shape]

        def can_place_ship(x, y, ship_shape):
            for dx, dy in ship_shape:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.cols and 0 <= ny < self.rows):
                    return False
                if self.board[ny][nx] != 0:
                    return False
                # Check adjacent tiles
                for adj_x, adj_y in [(nx-1, ny), (nx+1, ny), (nx, ny-1), (nx, ny+1)]:
                    if 0 <= adj_x < self.cols and 0 <= adj_y < self.rows:
                        if self.board[adj_y][adj_x] != 0:
                            return False
            return True

        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                attempts = 2000

                while not placed and attempts > 0:
                    x = random.randint(0, self.cols - 1)
                    y = random.randint(0, self.rows - 1)
                    ship_shape = shapes.get(ship_id, [(0, 0)])

                    # Try all combinations of rotations and mirrors
                    for _ in range(2):  # Try original and mirrored shape
                        for _ in range(4):  # Try all 4 rotations
                            if can_place_ship(x, y, ship_shape):
                                for dx, dy in ship_shape:
                                    self.board[y + dy][x + dx] = ship_id
                                placed = True
                                break
                            ship_shape = rotate(ship_shape)
                        if placed:
                            break
                        ship_shape = mirror(ship_shape)

                    attempts -= 1

                if not placed:
                    raise ValueError(f"Nepodařilo se umístit loď {ship_id}")
                
        

    def reset_board(self) -> None:
        """
        Resets the board back to all 0 (water).
        """
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        #raise NotImplementedError("reset_board() is not implemented yet.")

    def board_stats(self) -> dict:
        """
        Returns a dict with simple stats about the board:
            {
              "empty_spaces": <int>
              "occupied_spaces": <int>
            }
        """
        return {
            "empty_spaces": sum(row.count(0) for row in self.board),
            "occupied_spaces": self.total_blocks - sum(row.count(0) for row in self.board)
        }
        # Tady spočítáme a vrátíme statistiky boardu
        raise NotImplementedError("board_stats() is not implemented yet.")