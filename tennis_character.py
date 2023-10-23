from animation_info import *
from pico2d import load_image, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT


# 애니메이션 정보 찾기

# 현재 애니메이션은 프레임마다 정보가 다름
# 프레임 마다 너비, 높이를 리스트에 저장

# Logic
# frame_start_x = frame_width[frame] # frame = (frame + 1) % frame_count
# 프레임의 높이는 애니메이션 마다 다르고 같은 애니메이션 안에서는 같음

# draw함수 파라미터:
# frame_start_x, animation_start_y, frame_width[frame], frame_height, x, y

class Character:
    def __init__(self):
        self.image = load_image('tennis_character_micki.png')
        self.x, self.y = 400, 300
        self.animation = "Idle_back"
        self.frame = 0
        self.frame_start_x = 0
        self.dir_x, self.dir_y = 0, 0

    # 캐릭터 애니메이션 프레임 업데이트
    def update(self):
        self.x += self.dir_x

        # 프레임 업데이트 코드
        self.frame_start_x += micky_animation[self.animation][2][self.frame]
        self.frame = (self.frame + 1) % micky_animation[self.animation][4]

        if (self.frame == 0):
            self.frame_start_x = micky_animation[self.animation][0]

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir_x = 1
            elif event.key == SDLK_LEFT:
                self.dir_x = -1

    # 딕셔너리 내에 저장된 애니메이션 정보를 토대로 그려줄 함수 구현
    def draw(self):
        width, height = micky_animation[self.animation][2][self.frame], micky_animation[self.animation][3]
        character_w, character_h = width * 3, height * 3

        # 캐릭터 크기를 키우기 위해 clip_composite_draw사용
        # 크기 비율은 3배로 늘림
        self.image.clip_composite_draw(self.frame_start_x, micky_animation[self.animation][1],
                                       width, height,
                                       0, ' ', self.x, self.y, character_w, character_h)
