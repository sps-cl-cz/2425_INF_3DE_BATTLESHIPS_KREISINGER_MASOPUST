import random
from itertools import product

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int], shapes=None):
        if shapes is None:
            shapes = {
                1: [(0, 0), (0, 1)],
                2: [(0, 0), (0, 1), (0, 2)],
                3: [(0, 0), (0, 1), (0, 2), (0, 3)],
                4: [(0, 0), (0, 1), (0, 2), (1, 1)],
                5: [(0, 0), (1, 0), (2, 0), (2, 1)],
                6: [(0, 0), (0, 1), (1, 1), (1, 2)],
                7: [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2)]
            }
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict.copy()
        self.shapes = {size: self.generate_rotations(shape) for size, shape in shapes.items()}
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.shots_fired = set()
        self.missed_shots = set()
        self.hit_queue = []
        self.current_hits = []
        self.available_shots = {(x, y) for x in range(cols) for y in range(rows)}
    
    def generate_rotations(self, shape):
        rotations = set()
        for flip_x, flip_y, swap in product([1, -1], [1, -1], [False, True]):
            rotated = [(x * flip_x, y * flip_y) for x, y in shape]
            if swap:
                rotated = [(y, x) for x, y in rotated]
            min_x = min(x for x, y in rotated)
            min_y = min(y for x, y in rotated)
            normalized = [(x - min_x, y - min_y) for x, y in rotated]
            rotations.add(tuple(normalized))
        return list(rotations)
    
    def get_next_attack(self) -> tuple[int, int]:
        if self.hit_queue:
            return self.hit_queue.pop(0)
        return self.get_random_shot()
    
    def get_random_shot(self):
        if not self.available_shots:
            return None
        return random.choice(tuple(self.available_shots))
    
    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        self.shots_fired.add((x, y))
        self.available_shots.discard((x, y))
        self.enemy_board[y][x] = 'H' if is_hit else 'M'
        
        if not is_hit:
            self.missed_shots.add((x, y))
            return
        
        self.current_hits.append((x, y))
        
        if is_sunk:
            self.identify_sunk_ship()
            self.mark_surrounding_cells()
            self.hit_queue.clear()
            self.current_hits.clear()
        else:
            self.hit_queue.extend(self.get_target_cells())
    
    def get_adjacent_cells(self, x, y):
        candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [(cx, cy) for cx, cy in candidates 
                if 0 <= cx < self.cols and 0 <= cy < self.rows and (cx, cy) in self.available_shots]
    
    def get_target_cells(self):
        if len(self.current_hits) == 1:
            return self.get_adjacent_cells(*self.current_hits[0])
        
        xs, ys = zip(*self.current_hits)
        if len(set(xs)) == 1:
            min_y, max_y = min(ys), max(ys)
            targets = [(xs[0], min_y - 1), (xs[0], max_y + 1)]
        else:
            min_x, max_x = min(xs), max(xs)
            targets = [(min_x - 1, ys[0]), (max_x + 1, ys[0])]
        
        return [(cx, cy) for cx, cy in targets if (cx, cy) in self.available_shots]
    
    def identify_sunk_ship(self):
        ship_size = len(self.current_hits)
        found = False
        
        for size, variations in self.shapes.items():
            if self.ships_dict.get(size, 0) > 0:
                for variant in variations:
                    transformed_hits = [(x - min(x for x, y in self.current_hits), 
                                         y - min(y for x, y in self.current_hits)) 
                                        for x, y in self.current_hits]
                    if sorted(transformed_hits) == sorted(variant):
                        self.ships_dict[size] -= 1
                        found = True
                        break
            if found:
                break
        
        if not found:
            raise ValueError(f"Chyba: Pokus o potopení neexistující lodi velikosti {ship_size}")
    
    def mark_surrounding_cells(self):
        for x, y in self.current_hits:
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for nx, ny in neighbors:
                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    self.available_shots.discard((nx, ny))
                    self.enemy_board[ny][nx] = 'M'
    
    def get_enemy_board(self) -> list[list[str]]:
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        return self.ships_dict
    
    def all_ships_sunk(self) -> bool:
        return all(count == 0 for count in self.ships_dict.values())
