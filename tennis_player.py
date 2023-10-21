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
        frame_start_x = animation[animation_name][0]

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
             "Taunt_back": (0, 144, [18, 24, 18, 31, 26, 28], 38, 6),
             "Taunt_front": (161, 144, [18, 24, 18, 31, 26, 28], 38, 6),
             "Diving_left_back": (0, 252, [24, 55, 44, 38, 25], 24, 5),
             "Diving_left_front": (223, 252, [25, 54, 48, 37, 30], 24, 5),
             "Diving_right_back": (0, 283, [33, 57, 46, 38, 31], 31, 5),
             "Diving_right_front": (223, 283, [36, 57, 46, 39, 32], 31, 5),
             "Hit_left_back": (0, 318, [23, 39, 20, 28, 20], 34, 5),
             "Hit_left_front": (223, 318, [23, 39, 20, 28, 20], 34, 5),
             "Hit_right_back": (0, 359, [28, 42, 19, 34, 23], 33, 5),
             "Hit_right_front": (223, 359, [27, 42, 19, 36, 24], 33, 5)
             }

cur_animation = "Hit_right_front"

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
