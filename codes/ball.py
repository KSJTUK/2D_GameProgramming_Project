from pico2d import load_image, load_wav
import codes.game_framework as game_framework
import codes.game_world as game_world
import sys

from codes.tennis_court import COURT_CENTER_X, COURT_CENTER_Y, get_court_width, get_court_heights
import codes.tennis_referee as tennis_referee
import codes.tennis_game_ui as tennis_game_ui


class Ball:
    image = None
    shadow_image = None
    bounding_sound = None

    def __init__(self, x, y, z, speed_x, speed_y, speed_z):
        self.x, self.y, self.z = x, y, z
        self.shadow_y = self.y
        self.move_speed_x, self.move_speed_y, self.move_speed_z = speed_x, speed_y, speed_z

        self.pps_speed_x, self.pps_speed_y, self.pps_speed_z = \
            kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y), kmph_to_pps(self.move_speed_z)

        self.w_meter, self.h_meter = 0.4, 0.4
        self.width, self.height = 0, 0

        self.last_check_collision_groub = ''

        self.bound_count = 0

        if Ball.image == None:
            Ball.image = load_image(tennis_game_ui.resource_dir+'game_image/tennis_ball.png')

        if Ball.shadow_image == None:
            Ball.shadow_image = load_image(tennis_game_ui.resource_dir+'game_image/ball_shadow.png')

        if Ball.bounding_sound == None:
            Ball.bounding_sound = load_wav(tennis_game_ui.sound_dir+'ball_bounding.wav')
            Ball.bounding_sound.set_volume(32)

        if Ball.bounding_sound:
            Ball.bounding_sound.play()

    def hit_ball(self, power_x, power_y, power_z):
        self.bound_count = 0
        self.move_speed_x, self.move_speed_y, self.move_speed_z = power_x, power_y, power_z

    def update(self):
        pixel_per_meter = game_framework.PIXEL_PER_METER
        self.width, self.height = self.w_meter * pixel_per_meter, self.h_meter * pixel_per_meter

        self.move()
        self.gravity()
        if self.z < 0.0:
            self.bounding()

        if (self.x > game_framework.CANVAS_W or self.x < 0.0) or (self.y > game_framework.CANVAS_H or self.y < 0.0):
            tennis_referee.ball_in_over_court()
            tennis_referee.remove_ball(self)
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
        Ball.bounding_sound.play()
        bound_coefficient = 1.5
        cant_bound_speed = 2.0

        self.bound_count += 1
        self.shadow_y = self.y
        self.z = 0.0
        self.move_speed_z = abs(self.move_speed_z / bound_coefficient)
        if abs(self.move_speed_z) < cant_bound_speed: self.move_speed_z = 0.0
        self.move_speed_y = self.move_speed_y / bound_coefficient
        if abs(self.move_speed_y) < cant_bound_speed: self.move_speed_y = 0.0
        self.move_speed_x = self.move_speed_x / bound_coefficient
        if abs(self.move_speed_x) < cant_bound_speed: self.move_speed_x = 0.0

        if not self.is_in_court():
            tennis_referee.bound_over_court()

    def render(self):
        # 그림자는 크기가 y값에 따라 감소 하고 z값에 따라 증가함
        shadow_scale = 1.0 + self.z * game_framework.SCALE_PER_Z_PIXEL - self.y * game_framework.SCALE_PER_Y_PIXEL
        scale = 1.0 - self.z * game_framework.SCALE_PER_Z_PIXEL - self.y * game_framework.SCALE_PER_Y_PIXEL
        Ball.shadow_image.clip_composite_draw(0, 0, 128, 30,
                                              0, '', self.x, self.shadow_y,
                                              self.width * shadow_scale, self.height * shadow_scale)
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       self.width * scale, self.height * scale)

    def get_bounding_box(self):
        half_w, half_h = self.width // 2, self.height // 2
        return self.x - half_w, self.shadow_y - half_h, self.x + half_w, self.shadow_y + half_h

    def get_z(self):
        half_h = self.height // 2
        return self.z - half_h, self.z + half_h

    def handle_collision(self, groub, other):
        if groub == 'tennis_player:ball':
            self.last_check_collision_groub = groub
        if groub == 'tennis_player:serve_ball':
            self.last_check_collision_groub = groub
        if groub == 'ball:net':
            tennis_referee.bound_net()

    def is_in_court(self):
        court_width = get_court_width(self.y)
        court_top_height, court_bottom_height = get_court_heights()
        if self.x > COURT_CENTER_X + (court_width // 2):
            return False
        if self.x < COURT_CENTER_X - (court_width // 2):
            return False
        if self.y > COURT_CENTER_Y + court_top_height:
            return False
        if self.y < COURT_CENTER_Y - court_bottom_height:
            return False

        return True


def kmph_to_pps(kmph_speed):
    mps = (kmph_speed * 1000.0 / 60.0) / 60.0
    return mps * game_framework.PIXEL_PER_METER


def pps_to_kmph(pps_speed):
    mps = pps_speed / game_framework.PIXEL_PER_METER
    mpm = mps * 60.0
    mph = mpm * 60.0
    return mph / 1000.0
