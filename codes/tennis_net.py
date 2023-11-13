import pico2d

import game_framework
import game_world

class Wall:
    def __init__(self):
        self.x, self.y, self.z = 0, game_framework.CANVAS_H - 100, 100
        self.width, self.height = game_framework.CANVAS_W, 100

    def get_bounding_box(self):
        return self.x, self.y - self.height // 2, self.width, self.y + self.height // 2

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bounding_box())

    def handle_collision(self, groub, other):
        if groub == 'ball:wall':
            push_out_object_y = -1.0

            bound_coefficient = 1.5
            other.y -= push_out_object_y
            after_bounding_speeds = (other.move_speed_x / bound_coefficient,
                                     -other.move_speed_y / bound_coefficient, bound_coefficient)
            other.hit_ball(*after_bounding_speeds)


class TennisNet:
    def __init__(self):
        self.x, self.y, self.z = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2 - 35, 0
        self.width, self.height = 600, 40

    def get_bounding_box(self):
        half_width, half_height = self.width // 2, self.height // 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z, self.z + self.height

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bounding_box())

    def handle_collision(self, groub, other):
        if groub == 'ball:net':
            ball_move_dir_y = other.move_speed_y / abs(other.move_speed_y)
            push_out_object_y = self.height + other.height

            bound_coefficient = 1.5
            other.y += push_out_object_y if ball_move_dir_y < 0 else -push_out_object_y
            other.shadow_y += push_out_object_y if ball_move_dir_y < 0 else -push_out_object_y
            after_bounding_speeds = (other.move_speed_x / bound_coefficient,
                                     -other.move_speed_y / bound_coefficient, bound_coefficient)
            other.hit_ball(*after_bounding_speeds)
