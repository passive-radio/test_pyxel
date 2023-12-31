import pyxel
from pyxelunicode import PyxelUnicode

from state import *
from object import *

# World Class
class World:
    def __init__(self, fps: int):
        self.state = None
        self.enemies = []
        self.items = []
        self.level = Level()
        self.fps = fps
        self.delta_time = 1 / self.fps

    def set_state(self, state):
        if self.state:
            self.state.exit()
        self.state = state
        self.state.world = self
        self.state.fps = self.fps
        self.state.enter()

    def update(self):
        if self.state:
            self.state.update()

    def render(self):
        if self.state:
            self.state.render()
        # pyxel.show()

# Pyxel App Class
class App:
    def __init__(self, fps: int = 60):
        self.fps = fps
        screen_size = (1920, 1080)
        pyxel.init(screen_size[0], screen_size[1], title="RPG Game", fps=fps)
        pyxel.mouse(True)
        
        self.font_path = "asset/font/notosans_jp_bold.ttf"
        self.pyuni = PyxelUnicode(font_path=self.font_path, original_size=32, multipler=10)
        
        pyxel.load('asset/img/map.pyxres', image=True)
        pyxel.image(0).load(0, 0, "asset/img/player.png")
        pyxel.image(2).load(0, 0, "asset/img/enemy0.png")
        # pyxel.image(1).load(0, 0, "asset/img/map01.png")
        
        player = Player(960, 540, 0, "Player")  # start in the middle of the screen
        enemies = []
        for i in range(9):
            enemies.append(Enemy((i+1)*100, (i+1)*100, id=100+i, name=f'Enemy{i}'))
        item = Item(500, 500, "potion", 200)
        
        self.world = World(self.fps)
        self.world.screen_size = screen_size
        self.world.game_objects = [player, item]
        self.world.game_objects += [enemy for enemy in enemies]
        self.world.set_state(MainMenuState(fps=self.fps, writer = self.pyuni))
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.world.update()

    def draw(self):
        pyxel.cls(0)
        self.world.render()

# Run the Game
if __name__ == "__main__":
    App()
