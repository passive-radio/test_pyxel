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
            if system == RenderSystem or system == StaticRenderSystem:
                pass
            else:
                system.execute(self.world.game_objects, self.delta_time)

    def render(self):
        for system in self.systems:
            if system == RenderSystem or system == StaticRenderSystem:
                system.execute(self.world.game_objects)
            else:
                pass

    def exit(self):
        pass

# Sample States
class MainMenuState(State):
    def __init__(self, fps, writer: PyxelUnicode) -> None:
        super().__init__(fps, game_objects=[])
        self.writer = writer
        self.systems = [StaticRenderSystem]
        
    def enter(self):
        # Initialization code for the main menu
        self.start_button = ButtonUI("start", "START GAME", 0, 6, 32, center=True, h=60, w=240, margin_top=-40)
        self.exit_button = ButtonUI("exit", "EXIT GAME", 0, 6, 32, center=True, h=60, w=240, margin_top=40)

        self.world.game_objects.append(self.start_button)
        self.world.game_objects.append(self.exit_button)
        
        for object in self.world.game_objects:
            if object.get_component(StaticUIComponent):
                object._gen_style(self.world.screen_size)

    def update(self):
        # Check for mouse click within the button's coordinates
        
        for obj in self.world.game_objects:
            if obj.type == "start":
                if (obj.x <= pyxel.mouse_x <= obj.x + obj.w and
                    obj.y <= pyxel.mouse_y <= obj.y + obj.h and
                    pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                    pyxel.cls(0)
                    self.world.set_state(InGameState(self.world.fps, self.world.game_objects))
            
            # Check for mouse click within the EXIT button's coordinates
            if obj.type == "exit":
                if (obj.x <= pyxel.mouse_x <= obj.x + obj.w and
                    obj.y <= pyxel.mouse_y <= obj.y + obj.h and
                    pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
                    pyxel.quit()  # Exit the game
        
        return super().update()

    def render(self):
        return super().render()
    
    def exit(self):
        rm_list = []
        for i, obj in enumerate(self.world.game_objects):
            if obj.get_component(StaticUIComponent):
                rm_list.append(i)
        
        for i in reversed(rm_list):
            self.world.game_objects.pop(i)
        

class InGameState(State):
    def __init__(self, fps: int, game_objects) -> None:
        super().__init__(fps, game_objects)
        self.systems = [StaticRenderSystem, PlayerControlSystem, RenderSystem, CollisionSystem, InteractSystem]
        
    def enter(self):
        # Initialization code when game starts
        # This could include setting the player's starting position.
        self.level = Level()
        self.level.load_tile_map_from_csv('asset/map/map0.csv')
        self.world.game_objects.append(self.level)
        settings_button = ButtonUI(type="settings", content = "設定", right = 0, bottom = 0, h=60, w=120, font_size=32, font_colkey=0, colkey=7)
        self.world.game_objects.append(settings_button)
        
        for object in self.world.game_objects:
            if object.get_component(StaticUIComponent):
                object._gen_style(self.world.screen_size)
        
    def update(self):
        return super().update()

    def render(self):
        return super().render()
    