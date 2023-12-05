import random

import codes.game_world as game_world
from codes.animation_info import *
from codes.ball import Ball
from pico2d import load_image, clamp, draw_rectangle, load_wav
from math import pi, radians, sin, cos, atan2
from codes.behavior_tree import *

import codes.game_framework as game_framework
import codes.tennis_referee as tennis_referee
import codes.tennis_court as tennis_court
import codes.tennis_game_ui as tennis_game_ui

RUN_SPEED_KMPH = 35.0
RUN_SPEED_MPS = (RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * game_framework.PIXEL_PER_METER

class Win:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_information = False
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

            if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
                tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
            else:
                tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                       % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]
        else:
            tennis_player.animation_end = True

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
        tennis_player.animation_end = False
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

            if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
                tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
            else:
                tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                       % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]
        else:
            tennis_player.animation_end = True

    @staticmethod
    def exit(tennis_player, event):
        pass

    @staticmethod
    def render(tennis_player):
        character_default_draw_animation(tennis_player)

    @staticmethod
    def handle_collision(tennis_player, groub, other):
        pass


class ReadyInNotServeTurn:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
        tennis_player.cur_animation = 'Idle' + tennis_player.face_y if tennis_player.face_y != '' else 'Idle_front'
        tennis_player.face_x = ''
        tennis_player.dir_x, tennis_player.dir_y = 0, 0

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


class Ready:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
        tennis_player.cur_animation = 'Idle' + tennis_player.face_y if tennis_player.face_y != '' else 'Idle_front'
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
        tennis_player.animation_end = False
        tennis_player.cur_animation = "High_hit" + tennis_player.face_y if tennis_player.face_y != '' else "High_hit_front"

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

        if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
            tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
        else:
            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

        delta_frame = int(tennis_player.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) >= tennis_player.frame_per_action - 1:
            tennis_player.frame_start_x = tennis_player.animation_information['start_x']
            tennis_player.animation_end = True
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
            tennis_player.handle_collision_with_ball(other)

            tennis_referee.serve_turn_player_hit_serve()
            tennis_player.my_serve_turn = False


class PreparingServe:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
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

            if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
                tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
            else:
                tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                       % tennis_player.frame_per_action)

            delta_frame = int(tennis_player.frame) - prev_frame

            if delta_frame == 1:
                tennis_player.frame_start_x += tennis_player.animation_information['frame_widths'][
                    int(tennis_player.frame - 1)]
        else:
            tennis_player.animation_end = True
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


class Diving:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
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
            tennis_player.animation_end = True
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
            tennis_player.handle_collision_with_ball(other)


class Hit:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
        tennis_player.dir_x, tennis_player.dir_y = 0, 0
        tennis_player.animation_information = micky_animation[tennis_player.cur_animation]

        tennis_player.frame = 0
        tennis_player.frame_start_x = tennis_player.animation_information['start_x']

        tennis_player.calculation_action_time()

    @staticmethod
    def do(tennis_player):
        # 프레임 업데이트
        prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

        if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
            tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
        else:
            tennis_player.frame = ((tennis_player.frame + tennis_player.frame_per_time * game_framework.frame_time)
                                   % tennis_player.frame_per_action)

        delta_frame = int(tennis_player.frame) - prev_frame
        # prev_frame이 애니메이션 인덱스의 끝이고 frame이 업데이트 되어 0이 되었을때 초기화
        if abs(delta_frame) == tennis_player.frame_per_action - 1:
            tennis_player.frame_start_x = tennis_player.animation_information['start_x']
            tennis_player.animation_end = True
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
            tennis_player.handle_collision_with_ball(other)


class Run:
    @staticmethod
    def enter(tennis_player, event):
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
        if tennis_player.run_sound_play_time < tennis_player.time_count:
            tennis_player.run_sound.play()
            tennis_player.time_count = 0.0
        tennis_player.time_count += game_framework.frame_time

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
        tennis_player.animation_end = False
        tennis_player.dir_x, tennis_player.dir_y = 0, 0

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


class TennisAI:
    image = None
    shadow = None
    hit_sound = None
    run_sound = None

    def __init__(self, init_x=400, init_y=100):
        if TennisAI.image == None:
            TennisAI.image = load_image(tennis_game_ui.resource_dir+'game_image/tennis_character_micki.png')
        if TennisAI.shadow == None:
            TennisAI.shadow = load_image(tennis_game_ui.resource_dir+'game_image/ball_shadow.png')
        if TennisAI.hit_sound == None:
            TennisAI.hit_sound = load_wav(tennis_game_ui.sound_dir+'hit_sound.wav')
            TennisAI.hit_sound.set_volume(10)
        if TennisAI.run_sound == None:
            TennisAI.run_sound = load_wav(tennis_game_ui.sound_dir+'character_foot_step.wav')
            TennisAI.run_sound.set_volume(16)

        self.x, self.y = init_x, init_y
        self.face_x, self.face_y = '', '_front'
        self.cur_state = Idle
        self.cur_animation = 'Idle_front'
        self.animation_end = False
        self.frame = 0.0
        self.frame_start_x = 0
        self.character_height = 1.4 * game_framework.RATIO_FROM_DEFAULT_H

        self.cur_state.enter(self, ('NONE', 0))
        self.animation_information = micky_animation[self.cur_animation]

        self.my_serve_turn = False
        self.tennis_game_state = 'RUNNING'  # RUNNING, WIN, LOSE
        self.random_power_range = 60.0

        self.z = 0

        self.width, self.height = 0, 0

        self.start_y = self.y  # 캐릭터의 y 위치
        self.jump_angle = 0  # 점프를 위한 변수
        self.face_x, self.face_y = '', '_front'  # 캐릭터가 바라보는 방향
        self.defualt_height = micky_animation['Idle_front']['frame_height']
        self.pixel_per_meter = game_framework.PIXEL_PER_METER

        self.run_sound_play_time = 0.2
        self.time_count = 0.0

        self.dir = 0.0
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def update(self):
        self.cur_state.do(self)

        self.behavior_tree.run()

    def handle_event(self, event):
        if event[0] == 'WIN':
            self.tennis_game_state = 'WIN'
        if event[0] == 'LOSE':
            self.tennis_game_state = 'LOSE'
        if event[0] == 'SERVE_TURN':
            self.to_ready_state()
            self.my_serve_turn = True
            self.tennis_game_state = 'RUNNING'
        if event[0] == 'NOT_SERVE_TURN':
            self.to_ready_state()
            self.my_serve_turn = False
            self.tennis_game_state = 'RUNNING'
        if event[0] == 'PLAYER_HIT_SERVE':
            self.my_serve_turn = False
            self.tennis_game_state = 'RUNNING'
            self.idle_state()

    def render(self):
        self.cur_state.render(self)

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

        game_world.add_collision_pair('ball:net', ball, None)

    def decide_random_hit_power_range(self):
        court_top = tennis_court.COURT_CENTER_Y + tennis_court.COURT_TOP_HEIGHT
        court_width = tennis_court.get_court_width(court_top)
        if self.x > tennis_court.COURT_CENTER_X + court_width // 2:
            return (-self.random_power_range, -self.random_power_range / 10.0)
        elif self.x < tennis_court.COURT_CENTER_X - court_width // 2:
            return (self.random_power_range / 10.0, self.random_power_range)
        else:
            if self.x < tennis_court.COURT_CENTER_X:
                return (-self.random_power_range / 10.0, self.random_power_range)
            else:
                return (-self.random_power_range, self.random_power_range / 10.0)

    def calc_hit_power(self):
        canvas_width, canvas_height = game_framework.CANVAS_W, game_framework.CANVAS_H
        dist_from_center_x, dist_from_center_y = tennis_court.COURT_CENTER_X - self.x, tennis_court.COURT_CENTER_Y - self.y
        if abs(dist_from_center_x) < 1.0: dist_from_center_x = 1.0
        percentage_from_canvas_w = abs(dist_from_center_x / (canvas_width // 2))
        percentage_from_canvas_h = abs(dist_from_center_y / (canvas_height // 2))

        hit_dir_y = dist_from_center_y / abs(dist_from_center_y)
        # 최소, 최대 파워 설정, z값 보정 상수 설정
        racket_speed = 60
        minimum_hit_power, hit_power_limit, z_power_scale = (10.0, 30.0, 10.0), (40.0, 40.0, 45.0), 5.0
        random_speed = random.randint(*self.decide_random_hit_power_range())
        hit_dir_x = random_speed / abs(random_speed) if random_speed != 0 else 1

        hit_power_x = hit_dir_x * clamp(minimum_hit_power[0], abs(percentage_from_canvas_w * random_speed),
                                        hit_power_limit[0])
        if self.cur_animation == 'High_hit_back' or self.cur_animation == 'High_hit_front':
            hit_power_x = 20.0

        hit_power_y = hit_dir_y * clamp(minimum_hit_power[1], percentage_from_canvas_h * racket_speed,
                                        hit_power_limit[1])
        hit_power_z = min(abs(percentage_from_canvas_h * racket_speed * z_power_scale), hit_power_limit[2])
        return hit_power_x, hit_power_y, hit_power_z

    def block_move_over_play_area(self):
        center_x, center_y = tennis_court.COURT_CENTER_X, tennis_court.COURT_CENTER_Y
        self.x = clamp(center_x - 10.0 * self.pixel_per_meter, self.x, center_x + 10.0 * self.pixel_per_meter)
        self.y = clamp(center_y + 0.5 * self.pixel_per_meter, self.y, center_y + 6.0 * self.pixel_per_meter)

    def handle_collision_with_ball(self, ball):
        if ball.last_check_collision_groub == 'tennis_player:ball' and tennis_referee.last_hit_player == self:
            return

        game_world.add_collision_pair('ball:net', ball, None)

        tennis_referee.last_hit_player = self

        hit_power_x, hit_power_y, hit_power_z = self.calc_hit_power()
        if self.cur_state == HighHit: hit_power_x = -abs(hit_power_x)

        TennisAI.hit_sound.play()
        ball.hit_ball(hit_power_x, hit_power_y, hit_power_z)

    def hit_ball(self):
        if self.cur_state != Hit:
            self.cur_state = Hit
            self.face_y = '_front'
            self.face_x = '_right' if tennis_referee.play_ball.x < self.x else '_left'
            self.cur_animation = 'Hit' + self.face_x + self.face_y
            self.cur_state.enter(self, ('NONE', 0))

        return BehaviorTree.SUCCESS

    def serve_ball_throw(self):
        if self.cur_state != PreparingServe:
            self.cur_state = PreparingServe
            self.face_y = '_front'
            self.cur_animation = 'Preparing_serve' + self.face_y
            self.cur_state.enter(self, ('NONE', 0))

        return BehaviorTree.SUCCESS

    def is_player_in_hit_state(self):
        if self.cur_state != Hit and self.cur_state != HighHit:
            return BehaviorTree.FAIL

        if self.animation_end:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def get_bounding_box(self):
        half_width, half_height = self.width / 2, self.height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z, self.z + self.height * 1.3

    def handle_collision(self, groub, other):
        self.cur_state.handle_collision(self, groub, other)

    def pixel_distance_less_than(self, x1, x2, y1, y2, pixel_dist):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (pixel_dist * game_framework.PIXEL_PER_METER) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * cos(self.dir) * game_framework.frame_time
        self.y += self.speed * sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.pixel_distance_less_than(self.tx, self.x, self.ty, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def to_ready_state(self):
        if self.cur_state != Ready:
            self.cur_state = Ready
            self.cur_animation = 'Ready_front'
            self.cur_state.enter(self, ('NONE', 0))
        return BehaviorTree.SUCCESS

    def idle_state(self):
        if self.cur_state != Idle:
            self.cur_state = Idle
            self.cur_animation = 'Idle_front'
            self.cur_state.enter(self, ('None', 0))
        return BehaviorTree.SUCCESS

    def is_my_serve_turn(self):
        if self.cur_state != Ready and self.cur_state != PreparingServe:
            return BehaviorTree.FAIL

        if self.my_serve_turn:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def serve_ball_nearby(self):
        if not self.my_serve_turn or not tennis_referee.play_ball:
            return BehaviorTree.FAIL

        detect_range = 2.5
        ball_x, ball_y = tennis_referee.play_ball.x, tennis_referee.play_ball.y
        if self.pixel_distance_less_than(ball_x, self.x, ball_y, self.y, detect_range):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def hit_serve_ball(self):
        if self.cur_state == PreparingServe and not self.animation_end:
            return BehaviorTree.FAIL

        if self.cur_state != HighHit:
            self.cur_state = HighHit
            self.face_y = '_front'
            self.cur_animation = 'High_hit' + self.face_y
            self.cur_state.enter(self, ('NONE, 0'))

        return BehaviorTree.SUCCESS

    def set_move_target_location(self, target_x=None, target_y=None):
        if not target_x or not target_y:
            raise ValueError('ai_players target location is None')
        self.tx, self.ty = target_x, target_y
        self.cur_state = Run
        self.face_x = '_right' if self.tx > self.x else '_left'
        self.face_y = '_back' if self.ty > self.y else '_front'
        self.cur_animation = 'Run' + self.face_x + self.face_y
        self.cur_state.enter(self, ('NONE', 0))
        return BehaviorTree.SUCCESS

    def is_not_nearby_target_pos(self):
        if self.pixel_distance_less_than(self.x, self.tx, self.y, self.ty, 0.5):
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def set_random_target_location(self):
        self.tx, self.ty = random.randint(100, game_framework.CANVAS_W - 100), random.randint(100,
                                                                                              game_framework.CANVAS_H - 100)
        self.cur_state = Run
        self.face_x = '_right' if self.tx > self.x else '_left'
        self.face_y = '_back' if self.ty > self.y else '_front'
        self.cur_animation = 'Run' + self.face_x + self.face_y
        self.cur_state.enter(self, ('NONE', 0))
        return BehaviorTree.SUCCESS

    def is_game_end(self):
        if self.tennis_game_state != 'RUNNING':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_game_win(self):
        if self.tennis_game_state == 'WIN':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def game_win(self):
        if self.cur_state != Win:
            self.cur_state = Win
            self.face_y = '_front'
            self.cur_animation = 'Win_front'
            self.cur_state.enter(self, ('NONE', 0))

        return BehaviorTree.SUCCESS

    def game_lose(self):
        if self.cur_state != Lose:
            self.cur_state = Lose
            self.face_y = '_front'
            self.cur_animation = 'Lose_front'
            self.cur_state.enter(self, ('NONE', 0))

        return BehaviorTree.SUCCESS

    def trace_ball(self):
        self.tx, self.ty = tennis_referee.play_ball.x, tennis_referee.play_ball.y
        face_x = '_right' if self.tx > self.x else '_left'
        face_y = '_back' if self.ty > self.y else '_front'
        if face_x != self.face_x or face_y != self.face_y or self.cur_state != Run:
            self.face_x, self.face_y = face_x, face_y
            self.cur_state = Run
            self.cur_animation = 'Run' + self.face_x + self.face_y
            self.cur_state.enter(self, ('NONE', 0))

        self.move_slightly_to(self.tx, self.ty)
        if self.pixel_distance_less_than(self.tx, self.ty, self.x, self.y, 1.0):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_play_ball_exist(self):
        if tennis_referee.play_ball:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_play_ball_in_my_area(self):
        detect_range = 2.0  # meter
        if tennis_referee.play_ball.shadow_y >= tennis_court.COURT_CENTER_Y + detect_range * game_framework.PIXEL_PER_METER:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_not_serve_state(self):
        if self.my_serve_turn:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def is_nearby_ball(self, r=0.75):
        tx, ty = tennis_referee.play_ball.x, tennis_referee.play_ball.shadow_y
        if self.pixel_distance_less_than(tx, self.x, ty, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        # action node part
        action_set_move_target = Action('set move target', self.set_move_target_location,
                                        tennis_court.COURT_CENTER_X,
                                        tennis_court.COURT_CENTER_Y + tennis_court.COURT_TOP_HEIGHT)
        action_move_to = Action('move to', self.move_to)
        action_hit_ball = Action('hit ball', self.hit_ball)
        action_trace_ball = Action('trace ball', self.trace_ball)

        action_idle_state = Action('idle state', self.idle_state)
        action_win = Action('game win', self.game_win)
        action_lose = Action('game lose', self.game_lose)
        action_hit_serve_ball = Action('hit serve ball', self.hit_serve_ball)
        action_throw_serve_ball = Action('throw ball', self.serve_ball_throw)

        # condition node part
        condition_my_serve_turn = Condition('is my serve turn ?', self.is_my_serve_turn)
        condition_game_end = Condition('game end?', self.is_game_end)
        condition_game_win = Condition('game win?', self.is_game_win)
        condition_ball_exist = Condition('play ball exist?', self.is_play_ball_exist)
        condition_ball_in_my_area = Condition('play ball in my court area?', self.is_play_ball_in_my_area)
        condition_is_nearby_ball = Condition('nearby ball?', self.is_nearby_ball)
        condition_is_nearby_serve_ball = Condition('nearby serve ball?', self.serve_ball_nearby)
        condition_is_player_in_hit_state = Condition('hit state(animation) end?', self.is_player_in_hit_state)
        condition_is_player_not_in_serve_state = Condition('not in serve state?',
                                                           self.is_not_serve_state)

        # SEQ, SEL tree part
        SEQ_win = Sequence('win', condition_game_win, action_win)
        SEL_win_or_lose = Selector('win or lose', SEQ_win, action_lose)
        SEQ_game_end = Sequence('game end', condition_game_end, SEL_win_or_lose)
        SEQ_trace_ball = Sequence('ball exist and in my area-> trace ball',
                                  condition_ball_exist, condition_ball_in_my_area, action_trace_ball)
        SEQ_near_ball_hit = Sequence('near ball hit', condition_ball_exist, condition_is_nearby_ball, action_hit_ball)
        SEQ_keep_running_hit = Sequence('keep running hit', condition_is_player_in_hit_state, action_hit_ball)
        SEL_keep_running_hit_or_trace = Selector('keep running hit state or trace', SEQ_keep_running_hit,
                                                 SEQ_trace_ball)
        SEL_trace_or_hit_ball = Selector('trace and hit', SEQ_near_ball_hit, SEL_keep_running_hit_or_trace)
        SEQ_trace_or_hit_not_in_serve = Sequence('trace or hit not in serve state',
                                                 condition_is_player_not_in_serve_state, SEL_trace_or_hit_ball)

        SEQ_hit_serve = Sequence('hit serve ball',
                                 condition_is_nearby_serve_ball, action_hit_serve_ball)
        SEQ_throw_ball = Sequence('throw if my serve turn', condition_my_serve_turn, action_throw_serve_ball)
        SEL_throw_or_hit_serve = Selector('throw or serve', SEQ_hit_serve, SEQ_throw_ball)

        SEL_trace_ball_or_game_end = Selector('game end or move and hit or idle',
                                              SEQ_game_end, SEQ_trace_or_hit_not_in_serve, action_idle_state)
        root = SEL_serve_or_ready = Selector('serve or ready', SEL_throw_or_hit_serve, SEL_trace_ball_or_game_end)
        self.behavior_tree = BehaviorTree(root)


def character_default_frame_update(tennis_player):
    # 프레임 업데이트
    prev_frame = int(tennis_player.frame % tennis_player.frame_per_action)

    if game_framework.frame_time * tennis_player.frame_per_time > 1.0:
        tennis_player.frame = (prev_frame + 1) % tennis_player.frame_per_action
    else:
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

    scale = 1.0 - tennis_player.y * game_framework.SCALE_PER_Y_PIXEL

    aspect = width / height
    h = height / tennis_player.defualt_height
    tennis_player.height = tennis_player.character_height * tennis_player.pixel_per_meter * h * scale
    tennis_player.width = tennis_player.height * aspect * scale

    tennis_player.shadow.composite_draw(0, '', tennis_player.x, tennis_player.y - tennis_player.height / 2.0,
                                        tennis_player.width, tennis_player.width / 3.0)
    tennis_player.image.clip_composite_draw(tennis_player.frame_start_x, tennis_player.animation_information['start_y'],
                                            width, height, 0, ' ',
                                            tennis_player.x, tennis_player.y, tennis_player.width, tennis_player.height)
