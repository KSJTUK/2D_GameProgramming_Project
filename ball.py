from pico2d import load_image


class Ball:
    image = None

    # direction -> tuple로 받을 예정
    def __init__(self, x, y, direction_x, direction_y):
        self.x, self.y = x, y
        self.move_direction_x = direction_x
        self.move_direction_y = direction_y
        self.move_power = 0
        if Ball.image == None:
            Ball.image = load_image('tennis_ball.png')

    def hit_ball(self, direction_x, direction_y, power):
        self.move_direction_x, self.move_direction_y = direction_x, direction_y
        self.move_power = power

    def update(self):
        self.x += self.move_direction_x
        self.y += self.move_direction_y

    def render(self):
        Ball.image.clip_composite_draw(0, 0, 128, 128,
                                       0, '', self.x, self.y,
                                       100, 100)
