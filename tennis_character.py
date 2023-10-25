from animation_info import *
from pico2d import load_image, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT

class Run:
    @staticmethod
    def enter(character, event):
        print("Run Entered")

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def draw(character):
        pass


# 상태의 enter, exit 함수들은 어떤 이유에서 나가고 들어오는지를 판단하기위해
# 이벤트를 받음
class Idle:
    @staticmethod
    def enter(character, event):
        print("Idle Entered")

    @staticmethod
    def do(character):
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % micky_animation[character.animation][4]

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def draw(character):
        # 이미지 너비, 높이 받기
        width, height = (micky_animation[character.animation][2][character.frame],
                         micky_animation[character.animation][3])
        character_w, character_h = width * 3, height * 3  # 캐릭터 크기를 이미지 비율에 맞게 확대

        character.image.clip_composite_draw(character.frame_start_x, micky_animation[character.animation][1],
                                            width, height, 0, ' ',
                                            character.x, character.y, character_w, character_h)


# 캐릭터의 상태 기계
class CharacterSatateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transition_state_dic = {
            None
        }

    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_event, next_state in self.transition_state_dic[self.cur_state].items():
            pass

    def draw(self):
        self.cur_state.draw(self.character)


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

        # 캐릭터의 상태기계 생성
        self.state_machine = CharacterSatateMachine(self)
        self.state_machine.start()

    # 캐릭터 애니메이션 프레임 업데이트
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # self.state_machine.handle_event('INPUT', event)
        pass

    # 딕셔너리 내에 저장된 애니메이션 정보를 토대로 그려줄 함수 구현
    def draw(self):
        self.state_machine.draw()
