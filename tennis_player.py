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

# 애니메이션 정보 찾기

# 현재 애니메이션은 프레임마다 정보가 다름
# 프레임 마다 너비, 높이를 리스트에 저장

# Logic
# frame_start_x = frame_width[frame] # frame = (frame + 1) % frame_count
# 프레임의 높이는 애니메이션 마다 다르고 같은 애니메이션 안에서는 같음

# draw함수 파라미터:
# frame_start_x, animation_start_y, frame_width[frame], frame_height, x, y

# 프레임 정보를 찾는데 이용한 사이트: http://www.spritecow.com/

# 애니메이션들의 시작위치는 대부분 0이나 0이 아닌 애니메이션 존재
frame_start_x = 0

while running:
    clear_canvas()

    handle_events()

    frame = (frame + 1) % 4



    update_canvas()

    delay(1)

close_canvas()