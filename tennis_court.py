from pico2d import load_image

# width = 431 - (num % 2)
# height = 296
# left = 433 * (num % 2)
# bottom = 1 + 297 * (num // 2)

# 배경 전체의 크기는 가로 15미터, 세로 28미터로 설정
# 픽셀당 크기는?
BACKGROUND_PIXEL = (431, 296)
PIXEL_PER_METER = (BACKGROUND_PIXEL[0] / 15.0, BACKGROUND_PIXEL[1] / 28.0)

class TennisCourt:
    def __init__(self, court_number):
        global BACKGROUND_PIXEL, PIXEL_PER_METER
        self.image = load_image('tennis_courts.png')
        self.number = court_number
        self.w, self.h = 431 - (self.number % 2), 296
        self.w_meter, self.h_meter = (15.0, 28.0)

        # 이미지가 바뀌었을 경우를 대비해 재설정
        BACKGROUND_PIXEL = (self.w, self.h)
        PIXEL_PER_METER = (BACKGROUND_PIXEL[0] / self.w_meter, BACKGROUND_PIXEL[1] / self.h_meter)
        self.image_l, self.image_b = 433 * (self.number % 2), 1 + 297 * (self.number // 2)

    def update(self):
        pass

    def render(self):
        self.image.clip_composite_draw(self.image_l, self.image_b, self.w, self.h,
                                       0, ' ', 400, 300, 800, 600)