from pico2d import *

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
character = load_image('tennis_character_micki.png')
frame = 0

while running:
    handle_events()
    character.clip_draw(0, 50, 50, 50, 100, 100)
    update_canvas()

close_canvas()