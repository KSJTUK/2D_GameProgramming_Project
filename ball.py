from pico2d import load_image
import game_framework
import game_world


class Ball:
    image = None

    # direction -> tuple로 받을 예정
    def __init__(self, x, y, speed_x, speed_y):
        self.x, self.y = x, y
        self.move_speed_x, self.move_speed_y = speed_x, speed_y

        self.pps_speed_x, self.pps_speed_y = kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y)

        self.w_meter, self.h_meter = 0.3, 0.3
        self.width, self.height = 0, 0

        if Ball.image == None:
            Ball.image = load_image('tennis_ball.png')

    def hit_ball(self, power_x, power_y):
        self.move_speed_x, self.move_speed_y = power_x, power_y

    def update(self):
        self.pps_speed_x, self.pps_speed_y = kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y)
        self.x += self.pps_speed_x * game_framework.frame_time
        self.y += self.pps_speed_y * game_framework.frame_time

        pixel_per_meter = game_framework.PIXEL_PER_METER
        self.width, self.height = self.w_meter * pixel_per_meter, self.h_meter * pixel_per_meter

        self.move_speed_y -= kmph_to_pps((9.8 * game_framework.frame_time) / 2.0)
        # print(self.move_speed_y)

        if (self.x > game_framework.CANVAS_W or self.x < 0.0) or (self.y > game_framework.CANVAS_H or self.y < 0.0):
            print(f'remove object: {self}')
            game_world.remove_object(self)

    def render(self):
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       self.width, self.height)

    def get_bb(self):
        half_w, half_h = self.width / 2, self.height / 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, groub, other):
        if groub == 'character:ball':
            print(f'COLLISION ball: {groub}')


def kmph_to_pps(kmph_speed):
    mps = (kmph_speed * 1000.0 / 60.0) / 60.0
    return mps * game_framework.PIXEL_PER_METER


def pps_to_kmph(pps_speed):
    mps = pps_speed / game_framework.PIXEL_PER_METER
    mpm = mps * 60.0
    mph = mpm * 60.0
    return mph / 1000.0
