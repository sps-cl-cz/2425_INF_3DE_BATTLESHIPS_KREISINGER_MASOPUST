import random

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.shots_fired = set()
        self.missed_shots = set()
        self.hit_queue = []
        self.current_hits = []  # Ukládá souřadnice aktuálně zasažené lodi

    def get_next_attack(self) -> tuple[int, int]:
        if self.hit_queue:
            return self.hit_queue.pop(0)
        return self.get_random_shot()

    def get_random_shot(self):
        available_shots = [(x, y) for x in range(self.cols) for y in range(self.rows)
                           if (x, y) not in self.shots_fired and (x, y) not in self.missed_shots]
        return random.choice(available_shots) if available_shots else None

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        self.shots_fired.add((x, y))
        self.enemy_board[y][x] = 'H' if is_hit else 'M'
        
        if not is_hit:
            self.missed_shots.add((x, y))
            return
        
        self.current_hits.append((x, y))
        
        if is_sunk:
            self.identify_sunk_ship()
            self.hit_queue.clear()
            self.current_hits.clear()
        else:
            self.hit_queue.extend(self.get_target_cells())

    def get_adjacent_cells(self, x, y):
        candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [(cx, cy) for cx, cy in candidates 
                if 0 <= cx < self.cols and 0 <= cy < self.rows and (cx, cy) not in self.shots_fired]

    def get_target_cells(self):
        """ Analyzuje tvar zásahů a pokusí se určit další pravděpodobné cíle """
        if len(self.current_hits) == 1:
            return self.get_adjacent_cells(*self.current_hits[0])
        
        # Rozpoznání směru lodi (horizontální / vertikální)
        xs, ys = zip(*self.current_hits)
        if len(set(xs)) == 1:
            # Vertikální loď - rozšiřujeme nahoru/dolů
            min_y, max_y = min(ys), max(ys)
            targets = [(xs[0], min_y - 1), (xs[0], max_y + 1)]
        else:
            # Horizontální loď - rozšiřujeme vlevo/vpravo
            min_x, max_x = min(xs), max(xs)
            targets = [(min_x - 1, ys[0]), (max_x + 1, ys[0])]
        
        return [(cx, cy) for cx, cy in targets
                if 0 <= cx < self.cols and 0 <= cy < self.rows and (cx, cy) not in self.shots_fired]
    
    def identify_sunk_ship(self):
        """ Při potopení lodi zjistí její délku a eliminuje ji z dostupných lodí. """
        ship_size = len(self.current_hits)
        if ship_size in self.ships_dict and self.ships_dict[ship_size] > 0:
            self.ships_dict[ship_size] -= 1
            if self.ships_dict[ship_size] == 0:
                del self.ships_dict[ship_size]  # Odstraníme typ lodi, pokud už žádné nezbyly
    
    def get_enemy_board(self) -> list[list[str]]:
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        return self.ships_dict

    def all_ships_sunk(self) -> bool:
        return all(count == 0 for count in self.ships_dict.values())
