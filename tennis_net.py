import pico2d

import game_framework
import game_world

# 벽의 z를 충분히 크게하면 실제로 부딪힐 상황이 아니어도 부딪히는 상황 발생
# 물체의 실제 y값을 따로 두고 실제 y값을 기준으로 박스를 정의 하면 어떻게 될까?
# 지금은 y값과 z값을 그렇게 명확하게 구분짓지는 않고 있음
# 그래서 캐릭터는 z값을 쓰징 않으려 -1을 넣어둠
# 지금 생각나는 방법: real_y = object.y
# update -> real_y = y_speed * time
# get_bb -> real_y - height // 2, real_y + height // 2
# get_z -> object_z
# real_top -> real_y - height // 2, real_bottom -> real_y + height // 2
# collision -> object1.real_top < object2.real_bottom: false
#           -> object1.real_bottom > object2.real_top: false

class Wall:
    def __init__(self):
        self.x, self.y, self.z = 0, game_framework.CANVAS_H - 100, 100
        self.width, self.height = game_framework.CANVAS_W, 100

    def get_bb(self):
        return self.x, self.y - self.height // 2, self.width, self.y + self.height // 2

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bb())

    def handle_collision(self, groub, other):
        if groub == 'ball:wall':
            other.y -= 1.0
            move_powers = other.move_speed_x / 1.5, -other.move_speed_y / 1.3, 1.0
            other.hit_ball(*move_powers)

class TennisNet:
    def __init__(self):
        self.x, self.y, self.z = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2 - 35, 25
        self.width, self.height = 400, 40

    def get_bb(self):
        return self.x - self.width // 2, self.y - self.height // 2, self.x + self.width // 2, self.y + self.height // 2

    def get_z(self):
        return self.z

    def update(self):
        pass

    def render(self):
        pico2d.draw_rectangle(*self.get_bb())

    def handle_collision(self, groub, other):
        if groub == 'ball:net':
            other.y -= 1.0
            move_powers = other.move_speed_x / 1.5, -other.move_speed_y / 1.3, 1.0
            other.hit_ball(*move_powers)