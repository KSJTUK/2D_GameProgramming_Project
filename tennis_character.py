from animation_info import *
from check_event_funtions import *
from pico2d import load_image


class Run:
    @staticmethod
    def enter(character, event):
        if arrow_right_down(event) or arrow_left_up(event):  # 오른쪽으로 움직임
            character.dir_x, character.face_x = 1, '_right'
        elif arrow_left_down(event) or arrow_right_up(event):
            character.dir_x, character.face_x = -1, '_left'
        else:
            character.dir_x, character.face_x = 0, ''

        # 위 아래 체크는 아직 안하므로 face_y는 '' 유지
        character.dir_y, character.face_y = 0, ''

        character.animation = 'Run' + character.face_x + character.face_y

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        # 캐릭터 위치 이동
        character.x += character.dir_x * 1
        character.y += character.dir_y * 1

        # 프레임 업데이트
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % micky_animation[character.animation][4]

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        width, height = (micky_animation[character.animation][2][character.frame],
                         micky_animation[character.animation][3])
        character_w, character_h = width * 3, height * 3  # 캐릭터 크기를 이미지 비율에 맞게 확대

        character.image.clip_composite_draw(character.frame_start_x, micky_animation[character.animation][1],
                                            width, height, 0, ' ',
                                            character.x, character.y, character_w, character_h)


# 상태의 enter, exit 함수들은 어떤 이유에서 나가고 들어오는지를 판단하기위해
# 이벤트를 받음
class Idle:
    @staticmethod
    def enter(character, event):
        # 이전 상태가 Run에서 들어왔다면 움직임 관련 변수 모두 초기화
        # Idle애니메이션은 위 아래 두 방향밖에 존재 X -> face_y만 검사
        character.dir_x, character.face_x = 0, ''
        character.dir_y, character.face_y = 0, '_back'

        character.animation = 'Idle' + character.face_y
        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % micky_animation[character.animation][4]

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def exit(character, event):
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
            Idle: {arrow_right_down: Run, arrow_left_down: Run, arrow_left_up: Run, arrow_right_up: Run},
            Run: {arrow_right_down: Idle, arrow_left_down: Idle, arrow_left_up: Idle, arrow_right_up: Idle},
        }

    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_event, next_state in self.transition_state_dic[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False

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

        # 캐릭터가 바라보는 방향을 문자열로 지정
        # 애니메이션에 문자열을 더해주는 방식으로 사용할 예정
        self.face_x, self.face_y = '', '_back'

        # 캐릭터의 상태기계 생성
        self.state_machine = CharacterSatateMachine(self)
        self.state_machine.start()

    # 캐릭터 애니메이션 프레임 업데이트
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    # 딕셔너리 내에 저장된 애니메이션 정보를 토대로 그려줄 함수 구현
    def draw(self):
        self.state_machine.draw()
