import pico2d

import game_framework
import game_world


# 벽의 z를 충분히 크게하면 실제로 부딪힐 상황이 아니어도 부딪히는 상황 발생
# 물체의 실제 y값을 따로 두고 실제 y값을 기준으로 박스를 정의 하면 어떻게 될까?
# 지금은 y값과 z값을 그렇게 명확하게 구분짓지는 않고 있음
# 그래서 캐릭터는 z값을 쓰징 않으려 -1을 넣어둠
# 지금 생각나는 방법: real_y = object.y
# update -> real_y = y_speed * time
# get_bounding_box -> real_y - height // 2, real_y + height // 2
# get_z -> object_z
# real_top -> real_y - height // 2, real_bottom -> real_y + height // 2
# collision -> object1.real_top < object2.real_bottom: false
#           -> object1.real_bottom > object2.real_top: false

class Wall:
    def __init__(self):
        self.x, self.y, self.z = 0, game_framework.CANVAS_H - 100, 100
        self.width, self.height = game_framework.CANVAS_W, 100

    def get_bounding_box(self):
        return self.x, self.y - self.height // 2, self.width, self.y + self.height // 2

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bounding_box())

    def handle_collision(self, groub, other):
        if groub == 'ball:wall':
            push_out_object_y = -1.0

            bound_coefficient = 1.5
            other.y -= push_out_object_y
            after_bounding_speeds = (other.move_speed_x / bound_coefficient,
                                     -other.move_speed_y / bound_coefficient, bound_coefficient)
            other.hit_ball(*after_bounding_speeds)


class TennisNet:
    def __init__(self):
        self.x, self.y, self.z = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2 - 35, 25
        self.width, self.height = 600, 40

    def get_bounding_box(self):
        half_width, half_height = self.width // 2, self.height // 2
        return self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bounding_box())

    def handle_collision(self, groub, other):
        if groub == 'ball:net':
            ball_move_dir_y = other.move_speed_y / abs(other.move_speed_y)
            push_out_object_y = self.height + other.height

            bound_coefficient = 1.5
            other.y += push_out_object_y if ball_move_dir_y < 0 else -push_out_object_y
            other.shadow_y += push_out_object_y if ball_move_dir_y < 0 else -push_out_object_y
            after_bounding_speeds = (other.move_speed_x / bound_coefficient,
                                     -other.move_speed_y / bound_coefficient, bound_coefficient)
            other.hit_ball(*after_bounding_speeds)
