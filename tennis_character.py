from animation_info import *
from check_event_funtions import *
from pico2d import load_image


class Run:
    @staticmethod
    def enter(character, event):
        right, left, up, down = is_right_arrow_downed(), is_left_arrow_downed(),\
            is_up_arrow_downed(), is_down_arrow_downed()

        if right:  # 오른쪽으로 움직임
            character.dir_x, character.face_x = 1, '_right'
        elif left:
            character.dir_x, character.face_x = -1, '_left'
        elif not(right or left):
            character.dir_x, character.face_x = 0, ''

        if up:  # 위로 움직임
            character.dir_y, character.face_y = 1, '_back'
        elif down:
            character.dir_y, character.face_y = -1, '_front'
        else:
            if not(up or down):
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
        character.running = False

        character.dir_x, character.face_x = 0, ''
        character.dir_y = 0

        character.animation = 'Idle' + character.face_y if character.face_y != '' else 'Idle_back'
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
            Idle: {right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                   up_arrow_down: Run, down_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run},
            Run: {diff_arrow_downed_same_time: Idle, not_downed: Idle,
                  right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                  up_arrow_down: Run, down_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run},
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
