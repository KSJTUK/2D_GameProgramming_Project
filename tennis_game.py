from pico2d import *

import tennis_character
import tennis_court


def handle_events():
    global running, character

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

character = tennis_character.Character()
court = tennis_court.TennisCourt(0)

while running:
    clear_canvas()

    handle_events()

    court.draw()
    character.draw()

    update_canvas()
    character.update()

    delay(0.1)

close_canvas()
