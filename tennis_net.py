import pico2d

import game_framework
import game_world

class TennisNet:
    def __init__(self):
        self.x, self.y, self.z = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2 - 35, 25
        self.width, self.height = 400, 40

    def get_bb(self):
        return self.x - self.width // 2, self.y - self.height // 2, self.x + self.width // 2, self.y + self.height // 2

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bb())

    def handle_collision(self, groub, other):
        if groub == 'ball:net':
            other.y -= 1.0
            move_powers = other.move_speed_x / 1.5, -other.move_speed_y / 1.3, -abs(other.move_speed_z / 10.0)
            print(move_powers)
            other.hit_ball(*move_powers)