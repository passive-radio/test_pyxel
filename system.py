import copy

import pyxel
from pyxelunicode import PyxelUnicode

from object import *
from utils import BDFRenderer

class PlayerControlSystem:
    @staticmethod
    def execute(game_objects, delta_time):
        for game_object in game_objects:
            player_control = game_object.get_component(PlayerControlComponent)
            animation = game_object.get_component(AnimationComponent)
            if player_control:
                game_object.prev_x = game_object.x
                game_object.prev_y = game_object.y
                dx, dy = 0, 0
                
                if pyxel.btn(pyxel.KEY_UP):
                    dy = -player_control.speed * delta_time
                    animation.direction = 3
                if pyxel.btn(pyxel.KEY_DOWN):
                    dy = player_control.speed * delta_time
                    animation.direction = 0
                if pyxel.btn(pyxel.KEY_LEFT):
                    dx = -player_control.speed * delta_time
                    animation.direction = 1
                if pyxel.btn(pyxel.KEY_RIGHT):
                    dx = player_control.speed * delta_time
                    animation.direction = 2
                
                if dx or dy and animation:  # If the player is moving and has an animation component
                    animation.tick_count += 1
                    if animation.tick_count > animation.ticks_per_frame:
                        animation.tick_count = 0
                        animation.current_frame = (animation.current_frame + 1) % len(animation.frames)
                
                game_object.x += dx
                game_object.y += dy
                
class RenderSystem:
    @staticmethod
    def execute(game_objects):
        for game_object in game_objects:
            animation = game_object.get_component(AnimationComponent)
            if isinstance(game_object, Player) and animation:
                pyxel.blt(game_object.x, game_object.y, 0, animation.frames[animation.current_frame] * 32, animation.direction * 32, 32, 32, 11)
            elif isinstance(game_object, Enemy):
                pyxel.blt(game_object.x, game_object.y, 2, 0, 0, 32, 32, 11)
            # You can add further rendering logic for other game objects if needed.
            if game_object.get_component(PlayerControlComponent):
                font_path = "asset/font/notosans_jp_bold.ttf"
                writer = PyxelUnicode(font_path=font_path, original_size=32, multipler=8)
                if game_object.collide_object is not None:
                    writer.text(0, 0, f'Hi! {game_object.collide_object[0].id}', 0, None)
                else:
                    writer.text(0,0, 'Away!', 0, None)
            
            
class StaticRenderSystem:
    @staticmethod
    def execute(game_obects):
        for object in game_obects:
            if object.get_component(MapComponent):
                for y in range(0, pyxel.height, 32):
                    for x in range(0, pyxel.width, 32):
                        tile = int(object.tiles[y//32][x//32])
                        pyxel.blt(x, y, 1, 0, tile*32, 32, 32, 7)
                        
            elif object.get_component(StaticUIComponent):
                pyxel.rect(object.x, object.y, object.w, object.h, object.colkey)
                font_path = "asset/font/notosans_jp_bold.ttf"
                writer = PyxelUnicode(font_path=font_path, original_size=object.font_size, multipler=8)
                writer.text(object.x+object.padding_left, object.y+object.padding_top, object.content, object.font_colkey, None)

class CollisionSystem:
    def __init__(self) -> None:
        pass
    def execute(self, game_objects, delta_time):
        candidates = []
        for i, object in enumerate(game_objects):
            if object.get_component(CollisionComponent):
                candidates.append(object)
                
        for j, object in enumerate(candidates):
            others = candidates.copy()
            others.pop(j)
            object.collide_object = []
            for k, other in enumerate(others):
                if self._is_close(object, other):
                    object.collide_object.append(other)
                if self._is_touched(object, other):
                    object.x = object.prev_x
                    object.y = object.prev_y
            if len(object.collide_object) < 1:
                object.collide_object = None
                
    def _is_close(self, object, other):
        return abs(object.x - other.x) < 34 and abs(object.y - other.y) < 34
    
    def _is_touched(self, object, other):
        return abs(object.x - other.x) < 33 and abs(object.y - other.y) < 33

    def _is_close_old(self, object, other):
        return (other.x < object.x + object.w <= other.x + other.w and \
                other.y < object.y + object.h <= other.y + other.h) or \
                (other.x < object.x + object.w <= other.x + other.w and \
                other.y < object.y <= other.y + other.h) or \
                (other.x < object.x <= other.x + other.w and \
                other.y < object.y + object.h <= other.y + other.h) or \
                (other.x < object.x <= other.x + other.w and \
                other.y < object.y <= other.y + other.h)
    
    def _is_far(self, object, other):
        return abs(object.x - other.x) > 44 or abs(object.y - other.y) > 44


class InteractionSystem():
    def __init__(self) -> None:
        self.active_interaction = None
        self.is_menu = False
        self.is_dialog = False
        self.is_menu_closable = False
        self.writer = BDFRenderer("asset/font/b24.bdf")
        font_path = "asset/font/notosans_jp_bold.ttf"
        self.writer_32px = PyxelUnicode(font_path=font_path, original_size=32, multipler=8)
        self.writer_24px = PyxelUnicode(font_path=font_path, original_size=24, multipler=8)
    def execute(self, game_objects, delta_time=None):
        self.player = [obj for obj in game_objects if isinstance(obj, Player)][0]
        interactables = [obj for obj in game_objects if isinstance(obj, Interactable)]
        
        if self.player.collide_object is not None:
            for obj in self.player.collide_object:
                if pyxel.btnp(pyxel.KEY_RETURN):
                    self.active_interaction = obj
                    self.is_menu = True
                    
        if self.is_menu == True and pyxel.btnr(pyxel.KEY_RETURN):
            self.is_menu_closable = True
        if self.is_menu == True:
            self._handle_interaction_menu(self.active_interaction)
        self._display_dialog_ui(self.active_interaction)
    
    def _handle_interaction_menu(self, obj):
        # Handle up and down arrows for selection
        if obj is not None:
            interactions = obj.get_component(Interactable).types
            if pyxel.btnp(pyxel.KEY_W) and obj.get_component(Interactable).selected_interaction_index > 0:
                obj.get_component(Interactable).selected_interaction_index -= 1
            elif pyxel.btnp(pyxel.KEY_S) and obj.get_component(Interactable).selected_interaction_index < len(interactions) - 1:
                obj.get_component(Interactable).selected_interaction_index += 1

            # Handle the Enter key for choosing an interaction
            
            if pyxel.btnp(pyxel.KEY_RETURN):
                chosen_interaction = interactions[obj.get_component(Interactable).selected_interaction_index]
                if chosen_interaction == "fight":
                    # Call the BattleState
                    # Assuming you have a method to change states.
                    # change_state(BattleState())
                    pass
                elif chosen_interaction == "talk":
                    self.is_dialog = True
                    self.is_menu = False
                    pass
                # Reset menu state
                if self.is_menu_closable:
                    self.is_menu = False
                    self.is_menu_closable = False
                obj.get_component(Interactable).selected_interaction_index = 0

            # Handle the Escape key to close the menu
            if pyxel.btnp(pyxel.KEY_DELETE):
                self.active_interaction = None
                self.is_dialog = False
                obj.get_component(Interactable).selected_interaction_index = 0
            
    def _display_dialog_ui(self, obj):
        if self.is_menu and obj is not None:
            pyxel.rect(500, 200, 400, 300, 8)
            pyxel.rect(500, 200, 400, 20, 2)
            idx = obj.get_component(Interactable).selected_interaction_index
            for idx, choice in enumerate(obj.get_component(Interactable).types):
                color = pyxel.COLOR_WHITE if idx == obj.get_component(Interactable).selected_interaction_index else pyxel.COLOR_GRAY
                font_path = "asset/font/notosans_jp_bold.ttf"
                writer = PyxelUnicode(font_path=font_path, original_size=32, multipler=8)
                writer.text(500+40, 200 + 40 + 50 * idx, choice, color, None)
        if self.is_dialog == True:
            pyxel.rect(500, 160, 600, 300, 9)
            self.writer_32px.text(540, 180, f"Hello, {self.player.name}!", 0, None)
            self.writer_24px.text(540, 230, f"{obj.get_component(Interactable).content}", 0, None)
        