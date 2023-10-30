from animation_info import *
from check_event_funtions import *
from pico2d import load_image
from math import pi, radians, sin, cos


class Ready:
    @staticmethod
    def enter(character, event):
        character.animation = 'Idle' + character.face_y if character.face_y != '' else 'Idle_back'
        character.face_x = ''
        character.dir_x, character.dir_y = 0, 0

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
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
        character_default_draw_animation(character)


class HighHit:
    @staticmethod
    def enter(character, event):
        character.animation = "High_hit" + character.face_y if character.face_y != '' else "High_hit_back"

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

        # 애니메이션이 더 자연스러워 보이기위해 초기 y값을 더해줌
        character.jump_angle = 0
        character.start_y = character.y
        character.y += 5 * character.scale

    @staticmethod
    def do(character):
        # 프레임 업데이트
        frame_size = micky_animation[character.animation][4]
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % frame_size

        # 캐릭터 애니메이션에 따라 점프
        character.jump_angle += 360 // frame_size
        character.y += 15 * character.scale * sin(radians(character.jump_angle))

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]
            character.state_machine.handle_event(('ANIMATION_END', 0))

    @staticmethod
    def exit(character, event):
        character.y = character.start_y
        character.jump_angle = 0

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


class PreparingServe:
    @staticmethod
    def enter(character, event):
        character.animation = 'Preparing_serve' + character.face_y if character.face_y != '' else 'Preparing_serve_back'

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        # 프레임 업데이트
        if character.frame < micky_animation[character.animation][4] - 1:
            character.frame_start_x += micky_animation[character.animation][2][character.frame]
            character.frame = character.frame + 1

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


class Diving:
    @staticmethod
    def enter(character, event):
        character.animation = 'Diving' + character.face_x if character.face_x != '' else 'Hit_right'
        character.animation = character.animation + character.face_y if character.face_y != '' else character.animation + '_back'

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

        character.start_y = character.y
        character.jump_angle = 0

    @staticmethod
    def do(character):
        character.x += character.dir_x * character.speed * 5
        character.y += character.dir_y * character.speed * 5

        # 프레임 업데이트
        frame_size = micky_animation[character.animation][4]
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % frame_size

        # 캐릭터 애니메이션에 따라 점프
        if character.face_y == '':
            character.jump_angle += 360 // frame_size
            character.y += 10 * character.scale * sin(radians(character.jump_angle))

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]
            character.state_machine.handle_event(('ANIMATION_END', 0))
            character.y = character.start_y
            character.jump_angle = 0

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


class Hit:
    @staticmethod
    def enter(character, event):
        character.dir_x, character.dir_y = 0, 0
        # 지금은 Run 상태에서의 캐릭터의 방향을 따라가지만 나중에는 공의 위치에 따라 변경해야함
        # 공의 움직임 구현할 때 같이 구현 할것
        character.animation = 'Hit' + character.face_x if character.face_x != '' else 'Hit_right'
        character.animation = character.animation + character.face_y if character.face_y != '' else character.animation + '_back'

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        # 프레임 업데이트
        character.frame_start_x += micky_animation[character.animation][2][character.frame]
        character.frame = (character.frame + 1) % micky_animation[character.animation][4]

        if character.frame == 0:
            character.frame_start_x = micky_animation[character.animation][0]
            character.state_machine.handle_event(('ANIMATION_END', 0))

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


class Run:
    @staticmethod
    def enter(character, event):
        # 각 방향키가 눌려있는지 확인
        right, left, up, down = is_right_arrow_downed(), is_left_arrow_downed(), is_up_arrow_downed(), is_down_arrow_downed()

        if (right and left) or (not right and not left):  # 왼쪽키와 오른쪽키 동시 입력 또는 둘다 입력 X
            character.dir_x, character.face_x = 0, ''
        elif right:  # 오른쪽키 입력
            character.dir_x, character.face_x = 1, '_right'
        elif left:  # 왼쪽키 입력
            character.dir_x, character.face_x = -1, '_left'

        if (up and down) or (not up and not down):  # 위키와 아래키 동시 입력 또는 둘다 입력 X
            character.dir_y, character.face_y = 0, ''
        elif up:  # 위키 입력
            character.dir_y, character.face_y = 1, '_back'
        elif down:  # 아래키 입력
            character.dir_y, character.face_y = -1, '_front'

        character.animation = 'Run' + character.face_x + character.face_y

        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        # 캐릭터 위치 이동
        character.x += character.dir_x * character.speed
        character.y += character.dir_y * character.speed

        # 프레임 업데이트
        character_default_frame_update(character)

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


# 상태의 enter, exit 함수들은 어떤 이유에서 나가고 들어오는지를 판단하기위해
# 이벤트를 받음
class Idle:
    @staticmethod
    def enter(character, event):
        # 이전 상태가 Run에서 들어왔다면 움직임 관련 변수 모두 초기화
        character.running = False

        character.dir_x, character.face_x = 0, ''
        character.dir_y = 0

        # face_y의 문자열을 따라가되 빈 문자열이면 default인 Idle_back으로 애니메이션을 정함
        character.animation = 'Idle' + character.face_y if character.face_y != '' else 'Idle_back'

        # 프레임 초기화
        character.frame = 0
        character.frame_start_x = micky_animation[character.animation][0]

    @staticmethod
    def do(character):
        character_default_frame_update(character)

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def draw(character):
        character_default_draw_animation(character)


# 캐릭터의 상태 기계
class CharacterSatateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Ready
        self.transition_state_dic = {
            Ready: {space_down: PreparingServe},
            Idle: {right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                   down_arrow_down: Run, up_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run,
                   space_down: Hit},  # court_start_end_space_down:
            Run: {diff_arrow_downed_same_time: Idle, not_downed: Idle,
                  right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                  up_arrow_down: Run, down_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run,
                  space_down: Hit, key_down_v: Diving},
            Hit: {animation_end_and_keydown: Run, animation_end: Idle},
            Diving: {animation_end_and_keydown: Run, animation_end: Idle},
            PreparingServe: {space_down: HighHit},
            HighHit: {animation_end_and_keydown: Run, animation_end: Idle}
        }

    def start(self):
        self.cur_state.enter(self.character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        # 키다운/업으로 인해 상태가 전이 되지 않는 애니메이션이 키다운/업으로 인해 다른 애니메이션에 영향을 끼치지 않기위해 먼저 검사
        check_arrow_all(e)  # 먼저 방향키가 눌렸는지 확인 해준다(이후에 발생할 오류들을 예방하기 위함)

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
        self.scale = 2
        self.speed = 5

        # 점프동작이 섞여있는 애니메이션을 위한 변수들
        self.start_y = self.y
        self.jump_angle = 0

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


def character_default_frame_update(character):
    # 프레임 업데이트
    character.frame_start_x += micky_animation[character.animation][2][character.frame]
    character.frame = (character.frame + 1) % micky_animation[character.animation][4]

    if character.frame == 0:
        character.frame_start_x = micky_animation[character.animation][0]


# 변경없이 계속 중복되던 draw기능 함수화
def character_default_draw_animation(character):
    width, height = (micky_animation[character.animation][2][character.frame],
                     micky_animation[character.animation][3])

    # 캐릭터 크기를 이미지 비율에 맞게 확대
    character_w, character_h = width * character.scale, height * character.scale

    character.image.clip_composite_draw(character.frame_start_x, micky_animation[character.animation][1],
                                        width, height, 0, ' ',
                                        character.x, character.y, character_w, character_h)
