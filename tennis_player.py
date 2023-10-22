from pico2d import *

import tennis_character
import tennis_court


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas()

running = True

character = tennis_character.Character()
court = tennis_court.TennisCourt(0)

# 캐릭터의 임시 위치
test_position = (400, 300)

while running:
    clear_canvas()

    handle_events()

    court.draw()
    character.draw()

    update_canvas()

    delay(0.3)

close_canvas()
