import csv
import pyxel
import unicodedata

# Base GameObject Class
class GameObject:
    def __init__(self):
        self.components = {}
        self.type = ""
        self.id = None
        
    def add_component(self, component):
        self.components[type(component)] = component
        
    def get_component(self, component_type):
        return self.components.get(component_type)
    
    def add_components(self, *args):
        for arg in args:
            self.components[type(arg)] = arg

# Character Class inheriting from GameObject
class Character(GameObject):
    def __init__(self, x, y, hp, id):
        super().__init__()
        self.x = x
        self.y = y
        self.hp = hp
        self.vx = 0
        self.vy = 0
        self.w = 32
        self.h = 32
        self.prev_x = x
        self.prev_y = y
        self.collide_object = None
        self.id = id

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
        self.direction = 0
        
class CollisionComponent:
    def __init__(self) -> None:
        pass

class Interactable:
    def __init__(self, types: list[str]) -> None:
        self.types = types
        self.selected_interaction_index = 0
        self.content = "I want to fight with you!"

class Player(Character):
    def __init__(self, x, y, id, name: str):
        super().__init__(x, y, hp=100, id=id)
        self.add_components(PlayerControlComponent(), CollisionComponent(), AnimationComponent(), Interactable(["fight", "talk"]))
        self.name = name

class Enemy(Character):
    def __init__(self, x, y, id, name: str = "Enemy"):
        super().__init__(x, y, hp=50, id=id)
        self.add_components(CollisionComponent(), Interactable(["fight", "talk"]))
        self.name = name

class Item(GameObject):
    def __init__(self, x, y, item_type, id):
        super().__init__()
        self.x = x
        self.y = y
        self.item_type = item_type
        self.collide_object = None
        self.id = id
        
class MapComponent:
    def __init__(self) -> None:
        pass

class StaticUIComponent:
    def __init__(self) -> None:
        pass
    
class StaticInGameUI(GameObject):
    def __init__(self):
        super().__init__()
        self.x = None
        self.y = None
        self.h = None
        self.w = None
        self.zindex = 0
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.padding_top = -10
        self.padding_left = 0
        self.center = False
    
class ButtonUI(StaticInGameUI):
    def __init__(self, type: str, content: str = "", font_colkey = 0, colkey = 8, font_size = None, top = None, 
                left = None, right = None, bottom = None, padding_top = None, padding_left = None, 
                center = False, h = None, w = None, zindex = 0, margin_top = 0, margin_left = 0):
        super().__init__()
        self.right = right
        self.bottom = bottom
        self.h = h
        self.w = w
        self.font_size = font_size
        self.zindex = zindex
        self.content = content
        self.colkey = colkey
        self.font_colkey = font_colkey
        self.center = center
        self.padding_top += (self.h - self.font_size)//2
        self.padding_left += (self.w - self.__get_content_width())//2
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.type = type
        
        self.add_component(StaticUIComponent())
    
    def _gen_style(self, window_size: tuple[int, int]):
        if self.left is not None:
            self.x = self.left
        if self.top is not None:
            self.y = self.top
        if self.right is not None:
            self.x = window_size[0] - self.w - self.right
        if self.bottom is not None:
            self.y = window_size[1] - self.h - self.bottom
        if self.center == True:
            self.x = (window_size[0] - self.w)//2
            self.y = (window_size[1] - self.h)//2
        self.y += self.margin_top
        self.x += self.margin_left
        
    def __get_content_width(self):
        count = 0
        for c in self.content:
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 1
            else:
                count += 0.5
        return count * self.font_size

class Level(GameObject):
    def __init__(self):
        super().__init__()
        self.tiles = [[]]  # 2D grid to represent the level tiles
        self.width = 0
        self.height = 0
        self.add_components(MapComponent())
        
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
            