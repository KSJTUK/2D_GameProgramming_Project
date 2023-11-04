from pico2d import load_image
import game_framework


class Ball:
    image = None

    # direction -> tuple로 받을 예정
    def __init__(self, x, y, speed_x, speed_y):
        self.x, self.y = x, y
        self.move_speed_x, self.move_speed_y = speed_x, speed_y

        self.pps_speed_x, self.pps_speed_y = kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y)

        self.w_meter, self.h_meter = 0.3, 0.3

        if Ball.image == None:
            Ball.image = load_image('tennis_ball.png')

    def hit_ball(self, power_x, power_y):
        self.move_speed_x, self.move_speed_y = power_x, power_y

    def update(self):
        self.pps_speed_x, self.pps_speed_y = kmph_to_pps(self.move_speed_x), kmph_to_pps(self.move_speed_y)
        self.x += self.pps_speed_x * game_framework.frame_time
        self.y += self.pps_speed_y * game_framework.frame_time

        self.move_speed_y -= kmph_to_pps((9.8 * game_framework.frame_time) / 2.0)
        print(self.move_speed_y)

    def render(self):
        pixel_per_meter = game_framework.PIXEL_PER_METER
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       self.w_meter * pixel_per_meter, self.h_meter * pixel_per_meter)


def kmph_to_pps(kmph_speed):
    mps = (kmph_speed * 1000.0 / 60.0) / 60.0
    return mps * game_framework.PIXEL_PER_METER

def pps_to_kmph(pps_speed):
    mps = pps_speed / game_framework.PIXEL_PER_METER
    mpm = mps * 60.0
    mph = mpm * 60.0
    return mph / 1000.0