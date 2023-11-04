from pico2d import *

# import game_framework

import game_world
from tennis_court import TennisCourt
from tennis_character import Character

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            # game_framework.quit()
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # game_framework.quit()
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


def finish():
    game_world.clear()


def update():
    game_world.update()
    # delay(0.5)


def render():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

