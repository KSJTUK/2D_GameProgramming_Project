from pico2d import load_image
import game_framework


# width = 431 - (num % 2)
# height = 296
# left = 433 * (num % 2)
# bottom = 1 + 297 * (num // 2)

class TennisCourt:
    def __init__(self, court_number):
        self.image = load_image('tennis_courts.png')
        self.number = court_number
        self.w, self.h = 431 - (self.number % 2), 296
        self.image_l, self.image_b = 433 * (self.number % 2), 1 + 297 * (self.number // 2)

    def update(self):
        pass

    def render(self):
        self.image.clip_composite_draw(self.image_l, self.image_b, self.w, self.h,
                                       0, ' ', game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2,
                                       game_framework.CANVAS_W, game_framework.CANVAS_H)
