from itertools import product
 
# Definované tvary lodí (y, x)
SHAPES = {
    1: [(0, 0), (0, 1)],
    2: [(0, 0), (0, 1), (0, 2)],
    3: [(0, 0), (0, 1), (0, 2), (0, 3)],
    4: [(0, 0), (0, 1), (0, 2), (1, 1)],
    5: [(0, 0), (1, 0), (2, 0), (2, 1)],  
    6: [(0, 0), (0, 1), (1, 1), (1, 2)],
    7: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)]  
}
 
def generate_variants(shape):
    """
    Generates all unique rotations and reflections of a given shape.
    """
    variants = set()
 
    for flip_y in [1, -1]:  
        for flip_x in [1, -1]:  
            for rotate in range(4):  
                rotated = [(y * flip_y, x * flip_x) for y, x in shape]
                rotated = [(y, x) for y, x in rotated]  
                min_y = min(y for y, x in rotated)
                min_x = min(x for y, x in rotated)
                normalized = tuple(sorted((y - min_y, x - min_x) for y, x in rotated))
                variants.add(normalized)
 
                shape = [(x, -y) for y, x in shape]  
 
    return variants
 
# Vytvoření všech variant pro každý tvar lodě
SHAPE_VARIANTS = {key: generate_variants(value) for key, value in SHAPES.items()}
 
class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        """
        Initializes the Strategy.
 
        :param rows: Number of rows in the enemy board.
        :param cols: Number of columns in the enemy board.
        :param ships_dict: Dictionary mapping ship_id -> count for enemy ships.
                           e.g. {1: 2, 2: 1, 3: 1, ...}
 
        The enemy board is initially unknown.
        """
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
       
        # Tady vytvoříme 2D seznam otazníků '?', znamenající "neznámé pole"
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
 
    def get_next_attack(self) -> tuple[int, int]:
        """
        Returns the next (x, y) coordinates to attack.
        x = column, y = row.
        Must be within [0 .. cols-1], [0 .. rows-1].
        Assume we will never call this function if all ships are sunk.
        """
        for y, x in product(range(self.rows), range(self.cols)):
            if self.enemy_board[y][x] == '?':  # Neznámá pole
                return x, y
 
        raise RuntimeError("No available attack positions found!")
 
    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        """
        Called by the main simulation AFTER each shot, informing of the result:
        - is_hit: True if it's a hit
        - is_sunk: True if this shot sank a ship
 
        If is_sunk == True, we should decrement the count of one ship in ships_dict (you need to find out which ID).
        You should update the enemy board appropriately too.
        """
        if is_hit:
            self.enemy_board[y][x] = 'H'  
        else:
            self.enemy_board[y][x] = 'M'  
 
        if is_sunk:
            # Pokusíme se najít, která loď byla právě potopena
            for ship_id, count in self.ships_dict.items():
                if count > 0:
                    self.ships_dict[ship_id] -= 1
                    break  
 
            # Označíme potopenou loď (S) pro lepší přehlednost
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.enemy_board[row][col] == 'H':
                        self.enemy_board[row][col] = 'S'
 
    def get_enemy_board(self) -> list[list[str]]:
        """
        Returns the current 2D state (knowledge) of the enemy board.
        '?' = unknown, 'H' = hit, 'M' = miss.
        You may optionally use 'S' for sunk ships (not required).
        You may optionally use 'X' for tiles that are impossible to contain a ship (not required).
        """
        return self.enemy_board
 
    def get_remaining_ships(self) -> dict[int, int]:
        """
        Returns the dictionary of ship_id -> count for ships we believe remain afloat.
        """
        return self.ships_dict
 
    def all_ships_sunk(self) -> bool:
        """
        Returns True if all enemy ships are sunk (ships_dict counts are all zero).
        """
        return all(count == 0 for count in self.ships_dict.values())
 
 
