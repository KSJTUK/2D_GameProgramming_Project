import pico2d
import random

import game_world
from animation_info import *
from check_event_funtions import *
from ball import Ball
from pico2d import load_image
from math import pi, radians, sin, cos

import game_framework

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPS = (RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * game_framework.PIXEL_PER_METER


class Ready:
    @staticmethod
    def enter(character, event):
        character.cur_animation = 'Idle' + character.face_y if character.face_y != '' else 'Idle_back'
        character.face_x = ''
        character.dir_x, character.dir_y = 0, 0

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.calculation_action_time()

    @staticmethod
    def do(character):
        # 프레임 업데이트
        character_default_frame_update(character)

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        pass


class HighHit:
    @staticmethod
    def enter(character, event):
        character.cur_animation = "High_hit" + character.face_y if character.face_y != '' else "High_hit_back"

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information[start_x]

        # 애니메이션이 더 자연스러워 보이기위해 초기 y값을 더해줌
        character.jump_angle = 0
        character.start_y = character.y
        character.y += 5 * character.character_height

        character.calculation_action_time()

    @staticmethod
    def do(character):
        # 프레임 업데이트
        prev_frame = int(character.frame % character.frame_per_action)

        character.frame = ((character.frame + character.frame_per_time * game_framework.frame_time)
                               % character.frame_per_action)

        delta_frame = int(character.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) >= character.frame_per_action - 1:
            character.frame_start_x = character.animation_information['start_x']
            character.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            character.frame_start_x += character.animation_information['frame_widths'][int(character.frame - 1)]

            # 추가 코드또한 프레임이 업데이트 될때만 실행되도록함
            # 캐릭터 애니메이션에 따라 점프
            character.jump_angle += 360 // character.frame_per_action
            character.y += 15 * character.character_height * sin(radians(character.jump_angle))

    @staticmethod
    def exit(character, event):
        character.y = character.start_y
        character.jump_angle = 0

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        # 캐릭터가 서브 공을 쳤다면 그 볼은 더이상 serve_ball이 아닌 일반 ball로 전환
        if groub == 'character:serve_ball':
            game_world.remove_collision_object(character)
            character.throw_ball('character:ball', 10, 50, 40)



class PreparingServe:
    @staticmethod
    def enter(character, event):
        character.cur_animation = 'Preparing_serve' + character.face_y if character.face_y != '' else 'Preparing_serve_back'

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.calculation_action_time()

        # 공 생성하고 던지기
        character.throw_ball('character:serve_ball', 0, 0, 60)

    @staticmethod
    def do(character):
        # 애니메이션의 끝에 다다르면 더이상 실행하지 않도록 함
        if int(character.frame) < character.frame_per_action - 1:
            prev_frame = int(character.frame % character.frame_per_action)

            # 프레임이 점프되는걸 방지하기 위한 작업
            if game_framework.frame_time * character.frame_per_time > 1.0:
                character.frame = (prev_frame + 1) % character.frame_per_action
            else:
                character.frame = ((character.frame + character.frame_per_time * game_framework.frame_time)
                                   % character.frame_per_action)

            delta_frame = int(character.frame) - prev_frame

            if delta_frame == 1:
                character.frame_start_x += character.animation_information['frame_widths'][int(character.frame - 1)]
        else:
            game_world.add_collision_pair('character:serve_ball', character, None)


    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        game_world.remove_collision_object(character)
        character.state_machine.handle_event((groub, 0))


class Diving:
    @staticmethod
    def enter(character, event):
        character.cur_animation = 'Diving' + character.face_x if character.face_x != '' else 'Hit_right'
        character.cur_animation = character.cur_animation + character.face_y if character.face_y != '' else character.cur_animation + '_back'

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.start_y = character.y
        character.jump_angle = 0

        character.calculation_action_time()

    @staticmethod
    def do(character):
        character.x += character.dir_x * (RUN_SPEED_PPS) * game_framework.frame_time
        character.y += character.dir_y * (RUN_SPEED_PPS) * game_framework.frame_time

        # 프레임 업데이트
        prev_frame = int(character.frame % character.frame_per_action)

        # 프레임이 점프되는걸 방지하기 위한 작업
        if game_framework.frame_time * character.frame_per_time > 1.0:
            character.frame = (prev_frame + 1) % character.frame_per_action
        else:
            character.frame = ((character.frame + character.frame_per_time * game_framework.frame_time)
                               % character.frame_per_action)

        delta_frame = int(character.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) == character.frame_per_action - 1:
            character.frame_start_x = character.animation_information['start_x']
            character.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            character.frame_start_x += character.animation_information['frame_widths'][int(character.frame - 1)]

            # 추가 코드 또한 프레임이 업데이트 될 떄만 실행되도록함
            # 캐릭터 애니메이션에 따라 점프
            if character.face_y == '':
                character.jump_angle += 360 // character.frame_per_action
                character.y += 10 * character.character_height * sin(radians(character.jump_angle))

    @staticmethod
    def exit(character, event):
        character.y = character.start_y

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        pass

class Hit:
    @staticmethod
    def enter(character, event):
        character.dir_x, character.dir_y = 0, 0
        # 지금은 Run 상태에서의 캐릭터의 방향을 따라가지만 나중에는 공의 위치에 따라 변경해야함
        # 공의 움직임 구현할 때 같이 구현 할것
        character.cur_animation = 'Hit' + character.face_x if character.face_x != '' else 'Hit_right'
        character.cur_animation = character.cur_animation + character.face_y if character.face_y != '' else character.cur_animation + '_back'

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.calculation_action_time()

    @staticmethod
    def do(character):
        # 프레임 업데이트
        prev_frame = int(character.frame % character.frame_per_action)

        character.frame = ((character.frame + character.frame_per_time * game_framework.frame_time)
                           % character.frame_per_action)

        delta_frame = int(character.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) == character.frame_per_action - 1:
            character.frame_start_x = character.animation_information['start_x']
            character.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            character.frame_start_x += character.animation_information['frame_widths'][int(character.frame - 1)]

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        canvas_width, canvas_height = game_framework.CANVAS_W, game_framework.CANVAS_H
        if groub == 'character:ball':
            dist_from_center_x, dist_from_center_y = (canvas_width // 2) - character.x, (canvas_height // 2) - character.y
            z_power_scale = 1.5
            racket_speed_x, racket_speed_y, racket_speed_z = 50, 30, 50

            # 최대 파워를 40으로 설정
            hit_power_limit = 40.0

            hit_power_x, hit_power_y, hit_power_z = min(dist_from_center_x / character.x * racket_speed_x, hit_power_limit),\
                min(dist_from_center_y / character.y * racket_speed_y, hit_power_limit),\
                min(dist_from_center_y / character.y * z_power_scale * racket_speed_z, hit_power_limit)

            print(f'hit_power_z: {hit_power_z}')

            other.hit_ball(hit_power_x, hit_power_y, hit_power_z)

class Run:
    @staticmethod
    def enter(character, event):
        # 각 방향키가 눌려있는지 확인
        right, left, up, down = is_right_arrow_downed(), is_left_arrow_downed(), is_up_arrow_downed(), is_down_arrow_downed()

        if (right and left) or (not right and not left):  # 왼쪽키와 오른쪽키 동시 입력 또는 둘다 입력 X
            character.dir_x, character.face_x = 0.0, ''
        elif right:  # 오른쪽키 입력
            character.dir_x, character.face_x = 1.0, '_right'
        elif left:  # 왼쪽키 입력
            character.dir_x, character.face_x = -1.0, '_left'

        if (up and down) or (not up and not down):  # 위키와 아래키 동시 입력 또는 둘다 입력 X
            character.dir_y, character.face_y = 0.0, ''
        elif up:  # 위키 입력
            character.dir_y, character.face_y = 1.0, '_back'
        elif down:  # 아래키 입력
            character.dir_y, character.face_y = -1.0, '_front'

        character.cur_animation = 'Run' + character.face_x + character.face_y

        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.calculation_action_time()

    @staticmethod
    def do(character):
        # 캐릭터 위치 이동
        character.x += character.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        character.y += character.dir_y * RUN_SPEED_PPS * game_framework.frame_time

        # 프레임 업데이트
        character_default_frame_update(character)

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        pass


# 상태의 enter, exit 함수들은 어떤 이유에서 나가고 들어오는지를 판단하기위해
# 이벤트를 받음
class Idle:
    @staticmethod
    def enter(character, event):
        # 이전 상태가 Run에서 들어왔다면 움직임 관련 변수 모두 초기화
        # character.running = False

        character.dir_x, character.dir_y = 0, 0

        # face_y의 문자열을 따라가되 빈 문자열이면 default인 Idle_back으로 애니메이션을 정함
        character.cur_animation = 'Idle' + character.face_y if character.face_y != '' else 'Idle_back'

        # 프레임 초기화
        character.animation_information = micky_animation[character.cur_animation]

        character.frame = 0
        character.frame_start_x = character.animation_information['start_x']

        character.calculation_action_time()

    @staticmethod
    def do(character):
        character_default_frame_update(character)

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def render(character):
        character_default_draw_animation(character)

    @staticmethod
    def handle_collision(character, groub, other):
        pass


# 캐릭터의 상태 기계
class CharacterSatateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
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
            PreparingServe: {space_down: HighHit, collision_character_serveball: Ready},
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

    def render(self):
        self.cur_state.render(self.character)

    def handle_collision(self, groub, other):
        self.cur_state.handle_collision(self.character, groub, other)


# 애니메이션 정보 찾기

# 현재 애니메이션은 프레임마다 정보가 다름
# 프레임 마다 너비, 높이를 리스트에 저장

# Logic
# frame_start_x = frame_width[frame] # frame = (frame + 1) % frame_count
# 프레임의 높이는 애니메이션 마다 다르고 같은 애니메이션 안에서는 같음

# draw함수 파라미터:
# frame_start_x, animation_start_y, frame_width[frame], frame_height, x, y

class Character:
    image = None

    def __init__(self):
        if Character.image == None:
            Character.image = load_image('./../resources/tennis_character_micki.png')
        self.x, self.y = 400, 100  # 캐릭터 위치
        self.cur_animation = "Idle_back"  # 캐릭터 기본 애니메이션
        self.animation_information = micky_animation[self.cur_animation]  # 캐릭터 애니메이션 정보
        self.frame = 0.0  # 캐릭터 애니메이션 프레임
        self.frame_start_x = 0  # png파일에서의 캐릭터 애니메이션 시작좌표
        self.dir_x, self.dir_y = 0, 0  # 캐릭터 이동 방향
        self.character_height = 1.6  # 캐릭터 크기

        self.z = -1

        self.width, self.height = 0, 0

        # 점프동작이 섞여있는 애니메이션을 위한 변수들
        self.start_y = self.y  # 캐릭터의 y 위치
        self.jump_angle = 0  # 점프를 위한 변수

        # 캐릭터가 바라보는 방향을 문자열로 지정
        # 애니메이션에 문자열을 더해주는 방식으로 사용할 예정
        self.face_x, self.face_y = '', '_back'  # 캐릭터가 바라보는 방향

        # 캐릭터의 상태기계 생성
        self.state_machine = CharacterSatateMachine(self)  # 캐릭터 상태 기계
        self.state_machine.start()

        # 캐릭터 IDLE 크기를 기준으로 캐릭터의 크기를 정하게 함
        # 즉 캐릭터의 키가 n미터 이면 IDLE상태의 height값이 n미터가 되도록 하게 함
        self.defualt_height = micky_animation['Idle_back']['frame_height']
        self.pixel_per_meter = game_framework.PIXEL_PER_METER

    # 캐릭터 애니메이션 프레임 업데이트
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    # 딕셔너리 내에 저장된 애니메이션 정보를 토대로 그려줄 함수 구현
    def render(self):
        self.state_machine.render()

    def calculation_action_time(self):
        self.animation_information = micky_animation[self.cur_animation]
        time_per_action = self.animation_information['time_per_action']
        action_per_time = 1.0 / time_per_action
        self.frame_per_action = len(self.animation_information['frame_widths'])
        self.frame_per_time = action_per_time * self.frame_per_action

    def throw_ball(self, groub, power_x=0, power_y=0, power_z=50):
        ball = Ball(self.x, self.y, 0,  power_x, power_y, power_z)
        game_world.add_object(ball, 1)
        game_world.add_collision_pair(groub, None, ball)
        if groub == 'character:ball':
            game_world.add_collision_pair('ball:net', ball, None)

    def get_bounding_box(self):
        half_width, half_height = self.width / 2, self.height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z

    def handle_collision(self, groub, other):
        self.state_machine.handle_collision(groub, other)


def character_default_frame_update(character):
    # 프레임 업데이트
    prev_frame = int(character.frame % character.frame_per_action)

    character.frame = ((character.frame + character.frame_per_time * game_framework.frame_time)
                       % character.frame_per_action)

    delta_frame =  int(character.frame) - prev_frame
    # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
    if abs(delta_frame) == character.frame_per_action - 1:
        character.frame_start_x = character.animation_information['start_x']
    # 아니라면 계속 업데이트
    elif delta_frame == 1:
        character.frame_start_x += character.animation_information['frame_widths'][int(character.frame - 1)]


# 변경없이 계속 중복되던 draw기능 함수화
def character_default_draw_animation(character):
    width, height = (character.animation_information['frame_widths'][int(character.frame)],
                     character.animation_information['frame_height'])


    scale = 1.0 - character.y / 100.0 * 0.05
    # 캐릭터 크기는 고정값인 높이만 정하고 종횡비를 구해서 곱해주는 방식으로 너비를 구함
    # 캐릭터의 크기가 애니메이션마다 달라지는 것을 방지하기 위해 
    # 기준 애니메이션을 정하고 기준과 현재 애니메이션 간의 비율을 계산해서 곱해주는 방식으로 최종 높이를 구함
    aspect = width / height
    h = height / character.defualt_height
    character.height = character.character_height * character.pixel_per_meter * h * scale
    character.width = character.height * aspect * scale

    character.image.clip_composite_draw(character.frame_start_x, character.animation_information['start_y'],
                                        width, height, 0, ' ',
                                        character.x, character.y, character.width, character.height)

    # 디버그용
    pico2d.draw_rectangle(*character.get_bounding_box())
