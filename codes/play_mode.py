from pico2d import *
from random import randint

import codes.game_framework as game_framework

import codes.game_world as game_world
import codes.tennis_court as tennis_court
from codes.tennis_character import TennisPlayer
from codes.tennis_net import TennisNet, Wall
# test
from codes.ball import Ball
import codes.tennis_referee as tennis_referee
import codes.tennis_game_score as tennis_game_score
from codes.ai_tennis_player import TennisAI


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            tennis_player.handle_event(event)


def init():
    global court
    global tennis_player

    tennis_game_score.init()
    court = tennis_court.TennisCourt(0)
    game_world.add_object(court, 0)

    tennis_referee.set_referee()

    characters_default_diff_y = 40 * game_framework.RATIO_FROM_DEFAULT_H
    characters_default_diff_x = 100 * game_framework.RATIO_FROM_DEFAULT_W
    court_top = tennis_court.COURT_CENTER_Y + tennis_court.COURT_TOP_HEIGHT
    court_bottom = tennis_court.COURT_CENTER_Y - tennis_court.COURT_BOTTOM_HEIGHT

    tennis_player = TennisPlayer(tennis_court.COURT_CENTER_X - characters_default_diff_x, court_bottom - characters_default_diff_y)
    game_world.add_object(tennis_player, 2)
    game_world.add_collision_pair('tennis_player:ball', tennis_player, None)
    test_opponent_player = TennisAI(tennis_court.COURT_CENTER_X + characters_default_diff_x, court_top + characters_default_diff_y)
    game_world.add_object(test_opponent_player, 1)

    tennis_referee.subscribe_player('main_player', tennis_player)
    tennis_referee.subscribe_player('opponent_player', test_opponent_player)

    net = TennisNet()
    game_world.add_object(net, 2)
    game_world.add_collision_pair('ball:net', None, net)

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
