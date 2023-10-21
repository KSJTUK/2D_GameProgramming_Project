from pico2d import *


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# 딕셔너리 내에 저장된 애니메이션 정보를 토대로 그려줄 함수 구현
def draw_character_animation_in_dict(animation_name):
    global frame_start_x, frame
    if (frame == 0):
        frame_start_x = 0

    width, height = animation[animation_name][2][frame], animation[animation_name][3]
    character_w, character_h = width * 3, height * 3
    # 캐릭터 크기를 키우기 위해 clip_composite_draw사용
    # 크기 비율은 3배로 늘림
    character.clip_composite_draw(frame_start_x, animation[animation_name][1],
                        width, height,
                        0, ' ', 400, 300, character_w, character_h)

    frame_start_x += animation[animation_name][2][frame]
    frame = (frame + 1) % animation[animation_name][4]


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
# dictionary = { animation_name: tuple(frame_start_x, frame_start_y, frame_height, farme_count)
animation = {"Lose": (0, 78, [29, 32, 25, 32, 26], 28, 5),
             "Win": (0, 111, [26, 35, 33, 39], 28, 4),
             }

cur_animation = "Win"

frame_start_x = animation[cur_animation][0]

# 캐릭터의 임시 위치
test_position = (400, 300)

while running:
    clear_canvas()

    handle_events()

    draw_character_animation_in_dict(cur_animation)

    update_canvas()

    delay(1)

close_canvas()
