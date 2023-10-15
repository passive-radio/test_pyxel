import pyxel

from object import *

class PlayerControlSystem:
    @staticmethod
    def execute(game_objects, delta_time):
        for game_object in game_objects:
            player_control = game_object.get_component(PlayerControlComponent)
            animation = game_object.get_component(AnimationComponent)
            if player_control:
                dx, dy = 0, 0
                
                if pyxel.btn(pyxel.KEY_UP):
                    dy = -player_control.speed * delta_time
                if pyxel.btn(pyxel.KEY_DOWN):
                    dy = player_control.speed * delta_time
                if pyxel.btn(pyxel.KEY_LEFT):
                    dx = -player_control.speed * delta_time
                if pyxel.btn(pyxel.KEY_RIGHT):
                    dx = player_control.speed * delta_time
                
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
                pyxel.blt(game_object.x, game_object.y, 0, animation.frames[animation.current_frame] * 32, 0, 32, 32, 11)
            # You can add further rendering logic for other game objects if needed.
            
class StaticRenderSystem:
    @staticmethod
    def execute(game_obects):
        for object in game_obects:
            if type(object) == Level:
                for y in range(0, pyxel.height, 32):
                    for x in range(0, pyxel.width, 32):
                        tile = int(object.tiles[y//32][x//32])
                        pyxel.blt(x, y, 1, 0, tile*32, 32, 32, 7)