from pico2d import *
from random import randint

import game_framework

import game_world
from tennis_court import TennisCourt
from tennis_character import Character
from tennis_net import TennisNet, Wall
# test
from ball import Ball


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            test_throw_ball(800, 600, randint(-40, 10), randint(-40, -30), randint(40, 50))
        else:
            character.handle_event(event)

def test_throw_ball(x, y, speed_x, speed_y, speed_z):
    new_test_ball = Ball(x, y, 0, speed_x, speed_y, speed_z)
    game_world.add_object(new_test_ball, 1)
    game_world.add_collision_pair('character:ball', None, new_test_ball)

def init():
    global court
    global character

    running = True

    court = TennisCourt(0)
    game_world.add_object(court, 0)

    character = Character()
    game_world.add_object(character, 1)

    # 반대방향 테스트용 공
    test_ball = Ball(800, 600, 0,  -30, -40, 50)
    game_world.add_object(test_ball, 1)
    game_world.add_collision_pair('character:ball', None, test_ball)

    # # 테스트용 벽
    # wall = Wall()
    # game_world.add_object(wall, 3)
    # game_world.add_collision_pair('ball:wall', None, wall)

    net = TennisNet()
    game_world.add_object(net, 1)
    game_world.add_collision_pair('ball:net', None, net)

    game_world.add_collision_pair('character:ball', character, None)


def finish():
    game_world.clear()


def update():
    game_world.update()
    # delay(0.5)
    game_world.handle_collision()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
