import pico2d
from pico2d import load_image
import game_framework
import game_world
import sys

from tennis_court import COURT_CENTER_X, COURT_CENTER_Y


class Ball:
    image = None
    shadow_image = None

    def __init__(self, x, y, z, speed_x, speed_y, speed_z):
        self.x, self.y, self.z = x, y, z
        self.shadow_y = self.y
        self.move_speed_x, self.move_speed_y, self.move_speed_z = speed_x, speed_y, speed_z

        self.pps_speed_x, self.pps_speed_y, self.pps_speed_z = \
            kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y), kmph_to_pps(self.move_speed_z)

        self.w_meter, self.h_meter = 0.4, 0.4
        self.width, self.height = 0, 0

        self.bound_count = 0

        game_world.add_collision_pair('ball:net', self, None)

        if Ball.image == None:
            Ball.image = load_image('./../resources/tennis_ball.png')

        if Ball.shadow_image == None:
            Ball.shadow_image = load_image('./../resources/ball_shadow.png')

    def hit_ball(self, power_x, power_y, power_z):
        self.move_speed_x, self.move_speed_y, self.move_speed_z = power_x, power_y, power_z

    def update(self):
        pixel_per_meter = game_framework.PIXEL_PER_METER
        self.width, self.height = self.w_meter * pixel_per_meter, self.h_meter * pixel_per_meter

        self.move()
        self.gravity()
        if self.z < 0.0:
            self.bounding()

        if (self.x > game_framework.CANVAS_W or self.x < 0.0) or (self.y > game_framework.CANVAS_H or self.y < 0.0):
            game_world.remove_object(self)

    def gravity(self):
        if abs(self.move_speed_z) > sys.float_info.epsilon:
            self.move_speed_z -= kmph_to_pps(9.8 * game_framework.frame_time)

    def move(self):
        self.pps_speed_x, self.pps_speed_y, self.pps_speed_z = \
            kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y), kmph_to_pps(self.move_speed_z)

        self.x += self.pps_speed_x * game_framework.frame_time
        self.z += self.pps_speed_z * game_framework.frame_time
        self.shadow_y += self.pps_speed_y * game_framework.frame_time
        self.y += self.pps_speed_y * game_framework.frame_time + self.pps_speed_z * game_framework.frame_time

    def bounding(self):
        bound_coefficient = 1.5
        cant_bound_speed = 2.0

        self.bound_count += 1
        self.z = 0.0
        self.move_speed_z = abs(self.move_speed_z / bound_coefficient)
        if abs(self.move_speed_z) < cant_bound_speed: self.move_speed_z = 0.0
        self.move_speed_y = self.move_speed_y / bound_coefficient
        if abs(self.move_speed_y) < cant_bound_speed: self.move_speed_y = 0.0
        self.move_speed_x = self.move_speed_x / bound_coefficient
        if abs(self.move_speed_x) < cant_bound_speed: self.move_speed_x = 0.0

    def render(self):
        Ball.shadow_image.clip_composite_draw(0, 0, 128, 30,
                                              0, '', self.x, self.shadow_y,
                                              self.width, self.height)
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       self.width, self.height)
        # 디버그용
        pico2d.draw_rectangle(*self.get_bounding_box())

    def get_bounding_box(self):
        half_w, half_h = self.width // 2, self.height // 2
        return self.x - half_w, self.shadow_y - half_h, self.x + half_w, self.shadow_y + half_h

    def get_z(self):
        return self.z

    def handle_collision(self, groub, other):
        if groub == 'tennis_player:ball':
            pass
        if groub == 'tennis_player:serve_ball':
            game_world.remove_object(self)
        if groub == 'ball:net':
            pass


def kmph_to_pps(kmph_speed):
    mps = (kmph_speed * 1000.0 / 60.0) / 60.0
    return mps * game_framework.PIXEL_PER_METER


def pps_to_kmph(pps_speed):
    mps = pps_speed / game_framework.PIXEL_PER_METER
    mpm = mps * 60.0
    mph = mpm * 60.0
    return mph / 1000.0
