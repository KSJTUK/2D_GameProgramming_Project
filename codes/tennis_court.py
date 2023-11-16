from pico2d import load_image, draw_rectangle
import game_framework

# 아래는 코트 영역에 대한 정보임
COURT_CENTER_X, COURT_CENTER_Y = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2
ORIGIN_CENTER_X, ORIGIN_CENTER_Y = 216, 129
DIFF_BETWEEN_IMAGE_COURT_CENTER = ORIGIN_CENTER_Y
ORIGIN_COURT_PIXEL_WIDTH, ORIGIN_COURT_PIXEL_HEIGHT = 210, 140

DELTA_X_PER_Y_PIXEL = 12.0 / 140.0
COURT_WIDTH, COURT_HEIGHT = ORIGIN_COURT_PIXEL_WIDTH, ORIGIN_COURT_PIXEL_HEIGHT

ORIGIN_COURT_TOP_HEIGHT, ORIGIN_COURT_BOTTOM_HEIGHT = 196 - ORIGIN_CENTER_Y, ORIGIN_CENTER_Y - 52
ORIGIN_COURT_B_LEFT, ORIGIN_COURT_B_RIGHT = 112, 128

COURT_TOP_HEIGHT, COURT_BOTTOM_HEIGHT = ORIGIN_COURT_TOP_HEIGHT, ORIGIN_COURT_BOTTOM_HEIGHT
COURT_B_LEFT, COURT_B_RIGHT = ORIGIN_COURT_B_LEFT, ORIGIN_COURT_B_RIGHT


class TennisCourt:
    def __init__(self, court_number):
        self.image = load_image('./../resources/tennis_courts.png')
        self.court_number = court_number
        self.image_width, self.image_height = 431 - (self.court_number % 2), 296
        self.image_left, self.image_bottom = 433 * (self.court_number % 2), 1 + 297 * (self.court_number // 2)

        self.calc_court_area()

    def calc_court_area(self):
        w_ratio = game_framework.CANVAS_W / self.image_width
        h_ratio = game_framework.CANVAS_H / self.image_height

        global DIFF_BETWEEN_IMAGE_COURT_CENTER, COURT_CENTER_Y, DELTA_X_PER_Y_PIXEL
        DIFF_BETWEEN_IMAGE_COURT_CENTER = (self.image_height // 2 - ORIGIN_CENTER_Y) * h_ratio
        COURT_CENTER_Y = game_framework.CANVAS_H // 2 - DIFF_BETWEEN_IMAGE_COURT_CENTER
        DELTA_X_PER_Y_PIXEL = DELTA_X_PER_Y_PIXEL * w_ratio

        global COURT_WIDTH, COURT_HEIGHT
        COURT_WIDTH = ORIGIN_COURT_PIXEL_WIDTH * w_ratio
        COURT_HEIGHT = ORIGIN_COURT_PIXEL_HEIGHT * h_ratio

        global COURT_TOP_HEIGHT, COURT_BOTTOM_HEIGHT, COURT_B_LEFT, COURT_B_RIGHT
        COURT_HEIGHT = ORIGIN_COURT_PIXEL_HEIGHT * h_ratio
        COURT_TOP_HEIGHT = ORIGIN_COURT_TOP_HEIGHT * h_ratio
        COURT_BOTTOM_HEIGHT = ORIGIN_COURT_BOTTOM_HEIGHT * h_ratio
        COURT_B_LEFT = ORIGIN_COURT_B_LEFT * w_ratio
        COURT_B_RIGHT = ORIGIN_COURT_B_RIGHT * w_ratio

    def update(self):
        pass

    def render(self):
        self.image.clip_composite_draw(self.image_left, self.image_bottom, self.image_width, self.image_height,
                                       0, ' ', game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2,
                                       game_framework.CANVAS_W, game_framework.CANVAS_H)

        # 코트 영역 확인용
        # 코트 영역 그리기
        bottom = COURT_CENTER_Y - COURT_BOTTOM_HEIGHT
        top = COURT_CENTER_Y + COURT_TOP_HEIGHT
        for y in range(0, int(COURT_HEIGHT)):
            draw_rectangle(COURT_CENTER_X - ((COURT_WIDTH - y * DELTA_X_PER_Y_PIXEL) // 2), bottom + y - 1,
                           COURT_CENTER_X + ((COURT_WIDTH - y * DELTA_X_PER_Y_PIXEL) // 2), bottom + y + 1)

def get_court_width(object_y):
    in_court_y = object_y - (COURT_CENTER_Y - COURT_BOTTOM_HEIGHT)
    return COURT_WIDTH - (in_court_y * DELTA_X_PER_Y_PIXEL)

def get_court_heights():
    return COURT_TOP_HEIGHT, COURT_BOTTOM_HEIGHT