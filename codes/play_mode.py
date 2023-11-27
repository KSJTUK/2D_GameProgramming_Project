from pico2d import *
from random import randint

import game_framework

import game_world
import tennis_court
from tennis_character import TennisPlayer
from tennis_net import TennisNet, Wall
# test
from ball import Ball
import tennis_referee
from ai_tennis_player import TennisAI


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            test_throw_ball(800, 600, randint(-40, 10), randint(-40, -30), randint(40, 50))
        elif event.type == SDL_KEYDOWN and event.key == SDLK_0:
            tennis_referee.new_court_start()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            tennis_referee.new_set_start()
        else:
            tennis_player.handle_event(event)


def test_throw_ball(x, y, speed_x, speed_y, speed_z):
    new_test_ball = Ball(x, y, 0, speed_x, speed_y, speed_z)
    game_world.add_object(new_test_ball, 1)
    game_world.add_collision_pair('tennis_player:ball', None, new_test_ball)


def init():
    global court
    global tennis_player
    running = True
    court = tennis_court.TennisCourt(0)
    game_world.add_object(court, 0)

    tennis_referee.set_referee()

    characters_default_diff_y = 40 * game_framework.RATIO_FROM_DEFAULT_H
    characters_default_diff_x = 100 * game_framework.RATIO_FROM_DEFAULT_W
    court_top = tennis_court.COURT_CENTER_Y + tennis_court.COURT_TOP_HEIGHT
    court_bottom = tennis_court.COURT_CENTER_Y - tennis_court.COURT_BOTTOM_HEIGHT

    tennis_player = TennisPlayer(tennis_court.COURT_CENTER_X - characters_default_diff_x, court_bottom - characters_default_diff_y)
    game_world.add_object(tennis_player, 1)
    game_world.add_collision_pair('tennis_player:ball', tennis_player, None)
    test_opponent_player = TennisAI(tennis_court.COURT_CENTER_X + characters_default_diff_x, court_top + characters_default_diff_y)
    game_world.add_object(test_opponent_player, 1)

    tennis_referee.subscribe_player('main_player', tennis_player)
    tennis_referee.subscribe_player('opponent_player', test_opponent_player)

    net = TennisNet()
    game_world.add_object(net, 1)

    tennis_referee.new_set_start()

def finish():
    game_world.clear()


def update():
    game_world.update()
    tennis_referee.update()
    # delay(0.5)
    game_world.handle_collision()


def render():
    clear_canvas()
    game_world.render()
    tennis_referee.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
