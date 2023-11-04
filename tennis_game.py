from pico2d import *

import tennis_character
import tennis_court
import game_world


def handle_events():
    global running
    global character

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            character.handle_event(event)


open_canvas()

running = True

def reset_world():
    global character

    character = tennis_character.Character()
    court = tennis_court.TennisCourt(0)

    game_world.add_object(court, 0)
    game_world.add_object(character, 1)

reset_world()

while running:
    clear_canvas()

    handle_events()

    game_world.update()

    game_world.render()

    update_canvas()

    delay(0.1)

close_canvas()
