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

        - Must ensure no overlap.
        - Must stay within board bounds.
        - Cannot place ships with touching sides (diagonals are OK).
        - If it's impossible, raise ValueError.
        """
        # Tady by se měla provést logika umisťování lodí
        # find right bottom corner of the board
        rightBottom = [self.cols - 1, self.rows - 1]
        # find center of the board
        center = [self.cols // 2, self.rows // 2]
        for ship_id, count in self.ships_dict.items():  # Pro každý typ lodě (ID + počet lodí)
            for _ in range(count):  # Opakuj tolikrát, kolik jich máme umístit     
                method = random.randint(1, 1)
                ship = list()
                BoatCenter = [0, 0]
                print(type(BoatCenter))
                print(BoatCenter)
                wholeBoardChecked = False
                #create ship and place it on the board
                if (ship_id == 1):    
                    ship.append([BoatCenter])
                    ship.append([BoatCenter[0], BoatCenter[1] + 1])
                for _ in range(self.total_blocks):
                    for Shipblocks in range(len(ship)):
                        y, x = ship[Shipblocks]
                        if (method == 1):
                            if 0 <= x < self.cols and 0 <= y < self.rows and self.board[y][x] == 0:
                                self.board[y][x] = ship_id
                                

            
                
        raise NotImplementedError("place_ships() is not implemented yet.")

    def reset_board(self) -> None:
        """
        Resets the board back to all 0 (water).
        """
        raise NotImplementedError("reset_board() is not implemented yet.")

    def board_stats(self) -> dict:
        """
        Returns a dict with simple stats about the board:
            {
              "empty_spaces": <int>,
              "occupied_spaces": <int>
            }
        """
        # Tady spočítáme a vrátíme statistiky boardu
        raise NotImplementedError("board_stats() is not implemented yet.")

board = BoardSetup(10, 10, {1: 2, 2: 1, 3: 1, 4: 1})

board.place_ships()
print(board.get_board())