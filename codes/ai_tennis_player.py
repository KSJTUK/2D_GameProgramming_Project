import pico2d
import random

import game_world
from animation_info import *
from ball import Ball
from pico2d import load_image
from math import pi, radians, sin, cos, atan2
from behavior_tree import *

import game_framework
import tennis_referee
from tennis_court import COURT_CENTER_X, COURT_CENTER_Y

RUN_SPEED_KMPH = 20.0
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
        tennis_player.cur_animation = 'Idle' + tennis_player.face_y if tennis_player.face_y != '' else 'Idle_back'
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
        tennis_player.animation_end = False
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
            tennis_player.hit_ball(other)

            tennis_referee.serve_turn_player_hit_serve()


class PreparingServe:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
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
            tennis_player.hit_ball(other)


class Hit:
    @staticmethod
    def enter(tennis_player, event):
        tennis_player.animation_end = False
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
            tennis_player.hit_ball(other)


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

class TennisAI:
    image = None

    def __init__(self, init_x=400, init_y=100):
        if TennisAI.image == None:
            TennisAI.image = load_image('./../resources/tennis_character_micki.png')

        self.x, self.y = init_x, init_y
        self.face_x, self.face_y = '', ''
        self.cur_state = Idle
        self.cur_state.enter(self, ('NONE', 0))
        self.cur_animation = "Idle_front"
        self.animation_information = micky_animation[self.cur_animation]
        self.animation_end = False
        self.frame = 0.0
        self.frame_start_x = 0
        self.character_height = 1.6

        self.tennis_game_state = 'RUNNING' # RUNNING, WIN, LOSE

        self.z = 0

        self.width, self.height = 0, 0

        self.start_y = self.y  # 캐릭터의 y 위치
        self.jump_angle = 0  # 점프를 위한 변수
        self.face_x, self.face_y = '', '_front'  # 캐릭터가 바라보는 방향
        self.defualt_height = micky_animation['Idle_back']['frame_height']
        self.pixel_per_meter = game_framework.PIXEL_PER_METER

        self.dir = 0.0
        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

    def update(self):
        self.cur_state.do(self)

        self.behavior_tree.run()

    def handle_event(self, event):
        if event[0] == 'WIN':
            self.tennis_game_state = 'WIN'
            self.cur_animation = 'Win_front'
            self.cur_state.enter(self, event)
        if event[0] == 'LOSE':
            self.tennis_game_state = 'LOSE'
            self.cur_animation = 'Lose_front'
            self.cur_state.enter(self, event)
        if event[0] == 'SERVE_TURN':
            self.tennis_game_state = 'RUNNING'
            self.cur_animation = 'Ready_front'
            self.cur_state.enter(self, event)
        if event[0] == 'NOT_SERVE_TURN':
            self.tennis_game_state = 'RUNNING'
            self.cur_animation = 'Ready_front'
            self.cur_state.enter(self, event)

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

        if groub == 'tennis_player:ball':
            game_world.add_collision_pair('ball:net', ball, None)

    def handle_collision_with_ball(self, ball):
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

    def hit_ball(self):
        self.face_y = '_front'
        if self.cur_state != Hit:
            self.cur_state = Hit
            self.cur_animation = 'Hit' + self.face_y
            self.cur_state.enter(self, ('NONE', 0))

        if self.animation_end:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def get_bounding_box(self):
        half_width, half_height = self.width / 2, self.height / 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z, self.z + self.height // 2

    def handle_collision(self, groub, other):
        self.cur_state.handle_collision(self, groub, other)

    def pixel_distance_less_than(self, x1, x2, y1, y2, pixel_dist):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (pixel_dist ** 2)


    def move_slightly_to(self, tx, ty):
        self.dir = atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * cos(self.dir) * game_framework.frame_time
        self.y += self.speed * sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.pixel_distance_less_than(self.tx, self.x, self.ty, self.y, r * game_framework.PIXEL_PER_METER):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def idle_state(self):
        if self.cur_state != Idle:
            self.cur_state = Idle
            self.cur_animation = 'Idle_front'
            self.cur_state.enter()
        return BehaviorTree.SUCCESS

    def is_nearby_ball(self):
        pass

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

    def set_random_target_location(self):
        self.tx, self.ty = random.randint(100, game_framework.CANVAS_W - 100), random.randint(100, game_framework.CANVAS_H - 100)
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
            self.cur_animation = 'Win_front'
            self.cur_state.enter(self, ('NONE', 0))
            self.face_y = '_front'

        return BehaviorTree.SUCCESS

    def game_lose(self):
        if self.cur_state != Lose:
            self.cur_state = Lose
            self.cur_animation = 'Lose_front'
            self.cur_state.enter(self, ('NONE', 0))
            self.face_y = '_front'

        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        action_set_move_target = Action('set move target', self.set_move_target_location, 100, 100)
        action_set_random_move_target = Action('set random move target', self.set_random_target_location)
        action_move_to = Action('move to', self.move_to)
        action_hit_ball = Action('hit ball', self.hit_ball)

        action_idle_state = Action('idle state', self.idle_state)
        action_win = Action('game win', self.game_win)
        action_lose = Action('game lose', self.game_lose)

        condition_game_end = Condition('game end?', self.is_game_end)
        condition_game_win = Condition('game win?', self.is_game_win)

        SEQ_win = Sequence('win', condition_game_win, action_win)

        SEL_win_or_lose =  Selector('win or lose', SEQ_win, action_lose)
        SEQ_game_end = Sequence('game end', condition_game_end, SEL_win_or_lose)
        root = SEL_idle_or_game_end = Selector('idle or game end', SEQ_game_end, action_idle_state)


        SEQ_move_to_and_hit = Sequence('move and hit', action_set_random_move_target, action_move_to, action_hit_ball)
        self.behavior_tree = BehaviorTree(root)


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

    scale = 1.0 - tennis_player.y / 100.0 * 0.01

    aspect = width / height
    h = height / tennis_player.defualt_height
    tennis_player.height = tennis_player.character_height * tennis_player.pixel_per_meter * h * scale
    tennis_player.width = tennis_player.height * aspect * scale

    tennis_player.image.clip_composite_draw(tennis_player.frame_start_x, tennis_player.animation_information['start_y'],
                                            width, height, 0, ' ',
                                            tennis_player.x, tennis_player.y, tennis_player.width, tennis_player.height)

    # 디버그용
    pico2d.draw_rectangle(*tennis_player.get_bounding_box())
