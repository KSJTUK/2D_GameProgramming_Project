import pico2d
import random

import game_world
from animation_info import *
from check_event_funtions import *
from ball import Ball
from pico2d import load_image
from math import pi, radians, sin, cos

import game_framework
import tennis_referee
from tennis_court import COURT_CENTER_X, COURT_CENTER_Y

RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPS = (RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * game_framework.PIXEL_PER_METER


class Win:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.cur_animation = 'Win'

        tennis_player.face_x = ''
        tennis_player.dir_x, tennis_player.dir_y = 0, 0

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 애니메이션의 끝에 다다르면 더이상 실행하지 않도록 함
        if int(tennis_player.frame) < tennis_player.frame_per_action - 1:
            prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass


class Lose:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.cur_animation = 'Lose'

        tennis_player.face_x = ''
        tennis_player.dir_x, tennis_player.dir_y = 0, 0

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 애니메이션의 끝에 다다르면 더이상 실행하지 않도록 함
        if int(tennis_player.frame) < tennis_player.frame_per_action - 1:
            prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]

    @staticmethod
    def exit(tennis_player):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass

class Ready:
    @staticmethod
    def enter(tennis_player, event):
        tennis_referee.turn == 0
        tennis_player.my_surve_turn = True

        tennis_player.cur_animation = 'Idle' + tennis_player.face_y if tennis_player.face_y != '' else 'Idle_back'
        tennis_player.face_x = ''
        tennis_player.dir_x, tennis_player.dir_y = 0, 0

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 프레임 업데이트
        character_default_frame_update(tennis_player)

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass


class HighHit:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.cur_animation = "High_hit" + tennis_player.face_y if tennis_player.face_y != '' else "High_hit_back"

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        # 애니메이션이 더 자연스러워 보이기위해 초기 y값을 더해줌
        tennis_player.jump_angle = 0
        tennis_player.start_y = tennis_player.y
        tennis_player.y += 5 * tennis_player.character_height

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 프레임 업데이트
        prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

        tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                               % tennis_player.frame_per_action)

        delta_frame = int(tennis_player.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) >= tennis_player.frame_per_action - 1:
            tennis_player.frame_start_x = tennis_player.animation_information['start_x']
            tennis_player.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                int(tennis_player.frame - 1)]

            # 추가 코드또한 프레임이 업데이트 될때만 실행되도록함
            # 캐릭터 애니메이션에 따라 점프
            tennis_player.jump_angle += 360 // tennis_player.frame_per_action
            tennis_player.y += 15 * tennis_player.character_height * sin(radians(tennis_player.jump_angle))

    @staticmethod
    def exit(tennis_player, event):
        tennis_player.y = tennis_player.start_y
        tennis_player.jump_angle = 0

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        # 캐릭터가 서브 공을 쳤다면 그 볼은 더이상 serve_ball이 아닌 일반 ball로 전환
        if groub == 'tennis_player:serve_ball':
            game_world.remove_collision_object(other)
            game_world.remove_collision_object(tennis_player)

            game_world.add_collision_pair('tennis_player:ball', tennis_player, other)
            tennis_player.hit_ball(other)


class PreparingServe:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.cur_animation = 'Preparing_serve' + tennis_player.face_y if tennis_player.face_y != '' else 'Preparing_serve_back'

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

        # 공 생성하고 던지기
        tennis_player.throw_ball('tennis_player:serve_ball', 0, 0, 60)

    @staticmethod
    def do(tennis_player):
        # 애니메이션의 끝에 다다르면 더이상 실행하지 않도록 함
        if int(tennis_player.frame) < tennis_player.frame_per_action - 1:
            prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]
        else:
            game_world.add_collision_pair('tennis_player:serve_ball', tennis_player, None)

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        game_world.remove_object(other)
        game_world.remove_collision_object(tennis_player)
        tennis_player.state_machine.handle_event((groub, 0))


class Diving:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.cur_animation = 'Diving' + tennis_player.face_x if tennis_player.face_x != '' else 'Hit_right'
        tennis_player.cur_animation = tennis_player.cur_animation + tennis_player.face_y if tennis_player.face_y != '' else tennis_player.cur_animation + '_back'

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.start_y = tennis_player.y
        tennis_player.jump_angle = 0

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        diving_speed = 2.0 * RUN_SPEED_PPS
        tennis_player.x += tennis_player.dir_x * diving_speed * game_framework.frame_time
        tennis_player.y += tennis_player.dir_y * diving_speed * game_framework.frame_time

        # 프레임 업데이트
        prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

        # 프레임이 점프되는걸 방지하기 위한 작업
        if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
            tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
        else:
            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

        delta_frame = int(tennis_player.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) == tennis_player.frame_per_action - 1:
            tennis_player.frame_start_x = tennis_player.animation_information['start_x']
            tennis_player.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                int(tennis_player.frame - 1)]

            # 추가 코드 또한 프레임이 업데이트 될 떄만 실행되도록함
            # 캐릭터 애니메이션에 따라 점프
            if tennis_player.face_y == '':
                diving_height = 10.0
                tennis_player.jump_angle += 360 // tennis_player.frame_per_action
                tennis_player.y += diving_height * tennis_player.character_height * sin(
                    radians(tennis_player.jump_angle))

    @staticmethod
    def exit(tennis_player, event):
        tennis_player.y = tennis_player.start_y

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        if groub == 'tennis_player:ball':
            tennis_player.hit_ball(other)


class Hit:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.dir_x, tennis_player.dir_y = 0, 0
        # 지금은 Run 상태에서의 캐릭터의 방향을 따라가지만 나중에는 공의 위치에 따라 변경해야함
        # 공의 움직임 구현할 때 같이 구현 할것
        tennis_player.cur_animation = 'Hit' + tennis_player.face_x if tennis_player.face_x != '' else 'Hit_right'
        tennis_player.cur_animation = tennis_player.cur_animation + tennis_player.face_y if tennis_player.face_y != '' else tennis_player.cur_animation + '_back'

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 프레임 업데이트
        prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

        tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                               % tennis_player.frame_per_action)

        delta_frame = int(tennis_player.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) == tennis_player.frame_per_action - 1:
            tennis_player.frame_start_x = tennis_player.animation_information['start_x']
            tennis_player.state_machine.handle_event(('ANIMATION_END', 0))
        # 아니라면 계속 업데이트
        elif delta_frame == 1:
            tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                int(tennis_player.frame - 1)]

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        if groub == 'tennis_player:ball':
            tennis_player.hit_ball(other)


class Run:
    @staticmethod
    def enter(tennis_player, event):
        # 각 방향키가 눌려있는지 확인
        right, left, up, down = is_right_arrow_downed(), is_left_arrow_downed(), is_up_arrow_downed(), is_down_arrow_downed()

        if (right and left) or (not right and not left):  # 왼쪽키와 오른쪽키 동시 입력 또는 둘다 입력 X
            tennis_player.dir_x, tennis_player.face_x = 0.0, ''
        elif right:  # 오른쪽키 입력
            tennis_player.dir_x, tennis_player.face_x = 1.0, '_right'
        elif left:  # 왼쪽키 입력
            tennis_player.dir_x, tennis_player.face_x = -1.0, '_left'

        if (up and down) or (not up and not down):  # 위키와 아래키 동시 입력 또는 둘다 입력 X
            tennis_player.dir_y, tennis_player.face_y = 0.0, ''
        elif up:  # 위키 입력
            tennis_player.dir_y, tennis_player.face_y = 1.0, '_back'
        elif down:  # 아래키 입력
            tennis_player.dir_y, tennis_player.face_y = -1.0, '_front'

        tennis_player.cur_animation = 'Run' + tennis_player.face_x + tennis_player.face_y
        if tennis_player.cur_animation == 'Run':
            tennis_player.state_machine.handle_event(('PLAYER_HAS_NO_DIRECTION', 0))
            return

        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 캐릭터 위치 이동
        tennis_player.x += tennis_player.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        tennis_player.y += tennis_player.dir_y * RUN_SPEED_PPS * game_framework.frame_time

        # 프레임 업데이트
        character_default_frame_update(tennis_player)

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass


# 상태의 enter, exit 함수들은 어떤 이유에서 나가고 들어오는지를 판단하기위해
# 이벤트를 받음
class Idle:
    @staticmethod
    def enter(tennis_player, event):
        # 이전 상태가 Run에서 들어왔다면 움직임 관련 변수 모두 초기화
        # tennis_player.running = False

        tennis_player.dir_x, tennis_player.dir_y = 0, 0

        # face_y의 문자열을 따라가되 빈 문자열이면 default인 Idle_back으로 애니메이션을 정함
        tennis_player.cur_animation = 'Idle' + tennis_player.face_y if tennis_player.face_y != '' else 'Idle_back'

        # 프레임 초기화
        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        character_default_frame_update(tennis_player)

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass


# 캐릭터의 상태 기계
class TennisPlayerStateMachine:
    def __init__(self, tennis_player):
        self.tennis_player = tennis_player
        self.cur_state = Ready
        self.transition_state_dic = {
            Win: { },
            Lose: { },
            Ready: {space_down: PreparingServe, player_win: Win, player_lose: Lose},
            Idle: {right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                   down_arrow_down: Run, up_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run,
                   space_down: Hit, player_win: Win, player_lose: Lose},  # court_start_end_space_down:
            Run: {is_diff_arrow_downed_same_time: Idle, not_downed: Idle, is_player_has_no_direction: Idle,
                  right_arrow_down: Run, left_arrow_down: Run, left_arrow_up: Run, right_arrow_up: Run,
                  up_arrow_down: Run, down_arrow_down: Run, up_arrow_up: Run, down_arrow_up: Run,
                  space_down: Hit, key_down_v_and_not_updown: Diving, player_win: Win, player_lose: Lose},
            Hit: {animation_end_and_keydown: Run, animation_end: Idle, player_win: Win, player_lose: Lose},
            Diving: {animation_end_and_keydown: Run, animation_end: Idle, player_win: Win, player_lose: Lose},
            PreparingServe: {space_down: HighHit, collision_character_serveball: Ready,
                             player_win: Win, player_lose: Lose},
            HighHit: {animation_end_and_keydown: Run, animation_end: Idle, player_win: Win, player_lose: Lose}
        }

    def start(self):
        self.cur_state.enter(self.tennis_player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.tennis_player)

    def handle_event(self, e):
        # 키다운/업으로 인해 상태가 전이 되지 않는 애니메이션이 키다운/업으로 인해 다른 애니메이션에 영향을 끼치지 않기위해 먼저 검사
        check_arrow_all(e)  # 먼저 방향키가 눌렸는지 확인 해준다(이후에 발생할 오류들을 예방하기 위함)

        for check_event, next_state in self.transition_state_dic[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.tennis_player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.tennis_player, e)
                return True

        return False

    def render(self):
        self.cur_state.render(self.tennis_player)

    def handle_collision(self, groub, other):
        self.cur_state.handle_collision(self.tennis_player, groub, other)


# 애니메이션 정보 찾기

# 현재 애니메이션은 프레임마다 정보가 다름
# 프레임 마다 너비, 높이를 리스트에 저장

# Logic
# frame_start_x = frame_width[frame] # frame = (frame + 1) % frame_count
# 프레임의 높이는 애니메이션 마다 다르고 같은 애니메이션 안에서는 같음

# draw함수 파라미터:
# frame_start_x, animation_start_y, frame_width[frame], frame_height, x, y

class TennisPlayer:
    image = None

    def __init__(self):
        if TennisPlayer.image == None:
            TennisPlayer.image = load_image('./../resources/tennis_character_micki.png')

        self.x, self.y = 400, 100  # 캐릭터 위치
        self.cur_animation = "Idle_back"  # 캐릭터 기본 애니메이션
        self.animation_information = micky_animation[self.cur_animation]  # 캐릭터 애니메이션 정보
        self.frame = 0.0  # 캐릭터 애니메이션 프레임
        self.frame_start_x = 0  # png파일에서의 캐릭터 애니메이션 시작좌표
        self.dir_x, self.dir_y = 0, 0  # 캐릭터 이동 방향
        self.character_height = 1.6  # 캐릭터 크기

        self.z = 0

        self.width, self.height = 0, 0

        # 점프동작이 섞여있는 애니메이션을 위한 변수들
        self.start_y = self.y  # 캐릭터의 y 위치
        self.jump_angle = 0  # 점프를 위한 변수

        # 캐릭터가 바라보는 방향을 문자열로 지정
        # 애니메이션에 문자열을 더해주는 방식으로 사용할 예정
        self.face_x, self.face_y = '', '_back'  # 캐릭터가 바라보는 방향

        # 캐릭터의 상태기계 생성
        self.state_machine = TennisPlayerStateMachine(self)  # 캐릭터 상태 기계
        self.state_machine.start()

        # 캐릭터 IDLE 크기를 기준으로 캐릭터의 크기를 정하게 함
        # 즉 캐릭터의 키가 n미터 이면 IDLE상태의 height값이 n미터가 되도록 하게 함
        self.defualt_height = micky_animation['Idle_back']['frame_height']
        self.pixel_per_meter = game_framework.PIXEL_PER_METER

        self.my_surve_turn = False

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
        ball = Ball(self.x, self.y, 0, power_x, power_y, power_z)
        game_world.add_object(ball, 1)
        game_world.add_collision_pair(groub, None, ball)

        tennis_referee.subscribe_ball(ball)
        tennis_referee.last_hit_player = self

        if groub == 'tennis_player:ball':
            game_world.add_collision_pair('ball:net', ball, None)

    def hit_ball(self, ball):
        tennis_referee.last_hit_player = self

        canvas_width, canvas_height = game_framework.CANVAS_W, game_framework.CANVAS_H
        dist_from_center_x, dist_from_center_y = COURT_CENTER_X - self.x, COURT_CENTER_Y - self.y
        percentage_from_canvas_w, percentage_from_canvas_h = (dist_from_center_x / (canvas_width // 2),
                                                              dist_from_center_y / (canvas_height // 2))

        # 최대 파워를 40으로 설정
        racket_speed = 60
        hit_power_limit, z_power_scale = 40.0, 2.0

        hit_power_x = min(percentage_from_canvas_w * racket_speed, hit_power_limit)
        hit_power_y = min(percentage_from_canvas_h * racket_speed, hit_power_limit)
        hit_power_z = min(abs(percentage_from_canvas_h * racket_speed * z_power_scale), hit_power_limit)

        ball.hit_ball(hit_power_x, hit_power_y, hit_power_z)

    def get_bounding_box(self):
        half_width, half_height = self.width / 2, self.height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z, self.z + self.height // 2

    def handle_collision(self, groub, other):
        self.state_machine.handle_collision(groub, other)


def character_default_frame_update(tennis_player):
    # 프레임 업데이트
    prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

    tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                           % tennis_player.frame_per_action)

    delta_frame = int(tennis_player.frame) - prev_frame
    # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
    if abs(delta_frame) == tennis_player.frame_per_action - 1:
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']
    # 아니라면 계속 업데이트
    elif delta_frame == 1:
        tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][int(tennis_player.frame - 1)]


# 변경없이 계속 중복되던 draw기능 함수화
def character_default_draw_animation(tennis_player):
    width, height = (tennis_player.animation_information['frame_widths'][int(tennis_player.frame)],
                     tennis_player.animation_information['frame_height'])

    scale = 1.0 - tennis_player.y / 100.0 * 0.05
    # 캐릭터 크기는 고정값인 높이만 정하고 종횡비를 구해서 곱해주는 방식으로 너비를 구함
    # 캐릭터의 크기가 애니메이션마다 달라지는 것을 방지하기 위해 
    # 기준 애니메이션을 정하고 기준과 현재 애니메이션 간의 비율을 계산해서 곱해주는 방식으로 최종 높이를 구함
    aspect = width / height
    h = height / tennis_player.defualt_height
    tennis_player.height = tennis_player.character_height * tennis_player.pixel_per_meter * h * scale
    tennis_player.width = tennis_player.height * aspect * scale

    tennis_player.image.clip_composite_draw(tennis_player.frame_start_x, tennis_player.animation_information['start_y'],
                                            width, height, 0, ' ',
                                            tennis_player.x, tennis_player.y, tennis_player.width, tennis_player.height)

    # 디버그용
    pico2d.draw_rectangle(*tennis_player.get_bounding_box())
