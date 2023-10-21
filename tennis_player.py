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

# start_animation_y = 80 # 80부터 위로 올라가야함
# animtion_row = 20

# 애니메이션 정보 찾기
# animation_name, (start_x, start_y, width, height, frame)

frame = 0
x_size, y_size = 30, 25
while running:
    clear_canvas()

    handle_events()
    character.clip_draw(0, 80, 30, 25, 100, 100)

    frame += 1
    update_canvas()

close_canvas()