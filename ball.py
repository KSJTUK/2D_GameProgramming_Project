from pico2d import load_image
import game_framework


class Ball:
    image = None

    # direction -> tuple로 받을 예정
    def __init__(self, x, y, direction_x, direction_y):
        self.x, self.y = x, y
        self.move_direction_x = direction_x
        self.move_direction_y = direction_y
        self.move_power = 0

        self.w_meter, self.h_meter = 0.2, 0.2

        if Ball.image == None:
            Ball.image = load_image('tennis_ball.png')

    def hit_ball(self, direction_x, direction_y, power):
        self.move_direction_x, self.move_direction_y = direction_x, direction_y
        self.move_power = power

    def update(self):
        self.x += self.move_direction_x
        self.y += self.move_direction_y

    def render(self):
        pixel_per_meter = game_framework.PIXEL_PER_METER
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       self.w_meter * pixel_per_meter, self.h_meter * pixel_per_meter)
