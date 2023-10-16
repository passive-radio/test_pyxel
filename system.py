import pyxel
from pyxelunicode import PyxelUnicode

from object import *

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
                if game_object.collide_object is not None:
                    print(game_object.collide_object)
                    font_path = "asset/font/notosans_jp.ttf"
                    writer = PyxelUnicode(font_path=font_path, original_size=32, multipler=8)
                    writer.text(0, 0, 'Hi!', 0, None)

            
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
                font_path = "asset/font/notosans_jp.ttf"
                writer = PyxelUnicode(font_path=font_path, original_size=object.font_size, multipler=8)
                writer.text(object.x+object.padding_left, object.y+object.padding_top, object.content, object.font_colkey, None)

class CollisionSystem:
    @staticmethod
    def execute(game_objects, delta_time):
        collide_objects = []
        for i, object in enumerate(game_objects):
            if object.get_component(CollisionComponent):
                collide_objects.append(object)
                
        for i, object in enumerate(collide_objects):
            others = collide_objects.copy()
            others.pop(i)
            for other in others:
                if (other.x < object.x + object.w <= other.x + other.w and \
                other.y < object.y + object.h <= other.y + other.h) or \
                (other.x < object.x + object.w <= other.x + other.w and \
                other.y < object.y <= other.y + other.h) or \
                (other.x < object.x <= other.x + other.w and \
                other.y < object.y + object.h <= other.y + other.h) or \
                (other.x < object.x <= other.x + other.w and \
                other.y < object.y <= other.y + other.h):
                    object.x = object.prev_x
                    object.y = object.prev_y
                    object.collide_object = other
                    other.collide_object = object
                else:
                    pass

class InteractSystem:
    @staticmethod
    def execute(game_objects, delta_time):
        pass