from pico2d import *

import game_framework

import game_world
from tennis_court import TennisCourt
from tennis_character import Character
# test
from ball import Ball


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            pass
        else:
            character.handle_event(event)


def init():
    global court
    global character

    running = True

    court = TennisCourt(0)
    game_world.add_object(court, 0)

    character = Character()
    game_world.add_object(character, 1)

    ball = Ball(400, 10, 0, 60)
    game_world.add_object(ball, 1)

    game_world.add_collision_pair('character:ball', character, ball)
    pass


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
