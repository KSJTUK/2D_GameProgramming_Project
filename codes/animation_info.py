# 프레임 정보를 찾는데 이용한 사이트: http://www.spritecow.com/

# 애니메이션들의 시작위치는 대부분 0이나 0이 아닌 애니메이션 존재
# dictionary = { animation_name: tuple(frame_start_x, frame_start_y, frame_height, farme_count)

micky_animation = {
    'Lose': {
        'start_x': 0, 'start_y': 78, 'frame_widths': [29, 32, 25, 32, 26], 'frame_height': 28, 'time_per_action': 1.0
    },
    'Win': {
        'start_x': 0, 'start_y': 111, 'frame_widths': [26, 35, 33, 39], 'frame_height': 28, 'time_per_action': 1.0
    },
    'Taunt_back': {
        'start_x': 0, 'start_y': 144, 'frame_widths': [18, 24, 18, 31, 26, 28], 'frame_height': 38,
        'time_per_action': 1.0
    },
    'Taunt_front': {
        'start_x': 161, 'start_y': 144, 'frame_widths': [18, 24, 18, 31, 26, 28], 'frame_height': 38,
        'time_per_action': 1.0
    },
    'Diving_left_back': {
        'start_x': 0, 'start_y': 252, 'frame_widths': [24, 55, 44, 38, 25], 'frame_height': 24, 'time_per_action': 0.5
    },
    'Diving_right_front': {
        'start_x': 223, 'start_y': 252, 'frame_widths': [25, 54, 48, 37, 30], 'frame_height': 24, 'time_per_action': 0.5
    },
    'Diving_right_back': {
        'start_x': 0, 'start_y': 283, 'frame_widths': [33, 57, 46, 38, 31], 'frame_height': 31, 'time_per_action': 0.5
    },
    'Diving_left_front': {
        'start_x': 223, 'start_y': 283, 'frame_widths': [36, 57, 46, 39, 32], 'frame_height': 31, 'time_per_action': 0.5
    },
    'Hit_left_back': {
        'start_x': 0, 'start_y': 318, 'frame_widths': [23, 39, 20, 28, 20], 'frame_height': 34, 'time_per_action': 0.25
    },
    'Hit_left_front': {
        'start_x': 223, 'start_y': 318, 'frame_widths': [23, 39, 20, 28, 20], 'frame_height': 34,
        'time_per_action': 0.25
    },
    'Hit_right_back': {
        'start_x': 0, 'start_y': 359, 'frame_widths': [28, 42, 19, 34, 23], 'frame_height': 33, 'time_per_action': 0.25
    },
    'Hit_right_front': {
        'start_x': 223, 'start_y': 359, 'frame_widths': [27, 42, 19, 36, 24], 'frame_height': 33,
        'time_per_action': 0.25
    },
    'Run_back': {
        'start_x': 0, 'start_y': 642, 'frame_widths': [25, 27, 21, 28, 21, 27], 'frame_height': 32,
        'time_per_action': 0.3
    },
    'Run_right_back': {
        'start_x': 0, 'start_y': 606, 'frame_widths': [33, 38, 22, 29, 23, 34], 'frame_height': 31,
        'time_per_action': 0.3
    },
    'Run_right': {
        'start_x': 0, 'start_y': 571, 'frame_widths': [29, 39, 30, 39, 33, 35], 'frame_height': 30,
        'time_per_action': 0.3
    },
    'Run_right_front': {
        'start_x': 0, 'start_y': 537, 'frame_widths': [20, 27, 28, 39, 30, 26], 'frame_height': 29,
        'time_per_action': 0.3
    },
    'Run_front': {
        'start_x': 0, 'start_y': 502, 'frame_widths': [26, 28, 21, 28, 21, 27], 'frame_height': 30,
        'time_per_action': 0.25
    },
    'Run_left_front': {
        'start_x': 0, 'start_y': 468, 'frame_widths': [33, 38, 23, 29, 24, 34], 'frame_height': 29,
        'time_per_action': 0.25
    },
    'Run_left': {
        'start_x': 0, 'start_y': 433, 'frame_widths': [29, 38, 31, 39, 35, 34], 'frame_height': 30,
        'time_per_action': 0.4
    },
    'Run_left_back': {
        'start_x': 0, 'start_y': 397, 'frame_widths': [20, 26, 27, 38, 31, 25], 'frame_height': 31,
        'time_per_action': 0.25
    },
    'Idle_back': {
        'start_x': 0, 'start_y': 681, 'frame_widths': [20, 25, 18, 25, 19], 'frame_height': 28, 'time_per_action': 1.0
    },
    'Idle_front': {
        'start_x': 157, 'start_y': 681, 'frame_widths': [20, 25, 18, 25, 19], 'frame_height': 28, 'time_per_action': 1.0
    },
    'High_hit_back': {
        'start_x': 0, 'start_y': 714, 'frame_widths': [25, 26, 24, 39, 25], 'frame_height': 46, 'time_per_action': 0.75
    },
    'High_hit_front': {
        'start_x': 157, 'start_y': 714, 'frame_widths': [23, 26, 25, 38, 25], 'frame_height': 46, 'time_per_action': 0.75
    },
    'Preparing_serve_back': {
        'start_x': 0, 'start_y': 765, 'frame_widths': [27, 38, 18, 31], 'frame_height': 35, 'time_per_action': 0.5
    },
    'Preparing_serve_front': {
        'start_x': 157, 'start_y': 765, 'frame_widths': [27, 37, 17, 29], 'frame_height': 35, 'time_per_action': 0.5
    },
}
