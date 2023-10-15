import csv

# Base GameObject Class
class GameObject:
    def __init__(self):
        self.components = {}
        
    def add_component(self, component):
        self.components[type(component)] = component
        
    def get_component(self, component_type):
        return self.components.get(component_type)

# Character Class inheriting from GameObject
class Character(GameObject):
    def __init__(self, x, y, hp):
        super().__init__()
        self.x = x
        self.y = y
        self.hp = hp
        self.vx = 0
        self.vy = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class PlayerControlComponent:
    def __init__(self, speed: int = 200) -> None:
        self.speed = speed
        
class AnimationComponent:
    def __init__(self):
        self.current_frame = 0
        self.frames = [0, 1, 2, 1]  # cycling through frames for walking animation, for simplicity
        self.tick_count = 0
        self.ticks_per_frame = 10  # controls animation speed

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, hp=100)
        self.add_component(PlayerControlComponent())
        self.add_component(AnimationComponent())

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, hp=50)

class Item(GameObject):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.x = x
        self.y = y
        self.item_type = item_type
        
class MapComponent:
    def __init__(self) -> None:
        pass

class Level(GameObject):
    def __init__(self):
        super().__init__()
        self.tiles = [[]]  # 2D grid to represent the level tiles
        self.width = 0
        self.height = 0
        self.add_component(MapComponent())
        
    def load_from_file(self, filename):
        # Implement level loading logic
        pass
    
    def load_tile_map_from_csv(self, csv_filename):
        with open(csv_filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for y, row in enumerate(csv_reader):
                for x, tile in enumerate(row):
                    self.tiles[y].append(tile)
                self.tiles.append([])
                
        # For debug purposes, print out the contents of the CSV
        with open(csv_filename, newline='') as csvfile:
            csv_contents = csvfile.read()
            print(csv_contents)
