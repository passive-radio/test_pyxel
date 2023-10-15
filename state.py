import csv

import pyxel
from pyxelunicode import PyxelUnicode

from system import *

# State Machine Base
class State:
    def __init__(self, fps: int, game_objects) -> None:
        self.fps = 60
        self.delta_time = 1 / self.fps
        self.game_objects = game_objects
        
    def enter(self):
        pass

    def update(self):
        for system in self.systems:
            print(system)
            if system == RenderSystem or system == StaticRenderSystem:
                pass
            else:
                system.execute(self.game_objects, self.delta_time)

    def render(self):
        for system in self.systems:
            if system == RenderSystem or system == StaticRenderSystem:
                system.execute(self.game_objects)
            else:
                pass

    def exit(self):
        pass

# Sample States
class MainMenuState(State):
    def __init__(self, fps, writer: PyxelUnicode) -> None:
        super().__init__(fps, game_objects=[])
        self.writer = writer
        
    def enter(self):
        # Initialization code for the main menu
        self.start_button_x = 860
        self.start_button_y = 450
        self.start_button_width = 200
        self.start_button_height = 55
        
        # Initialization for the EXIT button
        self.exit_button_x = 860
        self.exit_button_y = 550  # Placed below the START button
        self.exit_button_width = 200
        self.exit_button_height = 55

    def update(self):
        # Check for mouse click within the button's coordinates
        if (self.start_button_x <= pyxel.mouse_x <= self.start_button_x + self.start_button_width and
            self.start_button_y <= pyxel.mouse_y <= self.start_button_y + self.start_button_height and
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            pyxel.cls(0)
            self.world.set_state(InGameState(self.world.fps, self.world.game_objects))
            
        # Check for mouse click within the EXIT button's coordinates
        if (self.exit_button_x <= pyxel.mouse_x <= self.exit_button_x + self.exit_button_width and
            self.exit_button_y <= pyxel.mouse_y <= self.exit_button_y + self.exit_button_height and
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            pyxel.quit()  # Exit the game

    def render(self):
        # Render main menu
        pyxel.rect(self.start_button_x, self.start_button_y, self.start_button_width, self.start_button_height, 9)
        # pyxel.text(self.start_button_x + 50, self.start_button_y + 15, "START GAME", 7)
        self.writer.text(self.start_button_x + 12, self.start_button_y + 4, "START GAME", 7)

        pyxel.rect(self.exit_button_x, self.exit_button_y, self.exit_button_width, self.exit_button_height, 8)
        # pyxel.text(self.exit_button_x + 65, self.exit_button_y + 15, "EXIT", 7)
        self.writer.text(self.exit_button_x + 30, self.exit_button_y + 4, "EXIT GAME", 7)
        

class InGameState(State):
    def __init__(self, fps: int, game_objects) -> None:
        super().__init__(fps, game_objects)
        self.systems = [StaticRenderSystem, PlayerControlSystem, RenderSystem]
        
    def enter(self):
        # Initialization code when game starts
        # This could include setting the player's starting position.
        self.level = Level()
        self.level.load_tile_map_from_csv('asset/map/map0.csv')
        self.world.game_objects.append(self.level)
        
    def update(self):
        return super().update()

    def render(self):
        return super().render()
    