import sys
import time

# fill here

# 픽셀당 크기는 2센치로 설정
PIXEL_PER_METER = 10.0 / 0.2
CANVAS_W, CANVAS_H = 1280, 800
ASPECT = CANVAS_W / CANVAS_H

DEFAUTL_CANVAS_W, DEFAULT_CANVAS_H = 1280, 800
RATIO_FROM_DEFAULT_W, RATIO_FROM_DEFAULT_H = CANVAS_W / DEFAULT_CANVAS_H, CANVAS_H / DEFAULT_CANVAS_H

# 몇 픽셀당 사이즈를 몇 퍼센트 만큼 줄일 것인지 설정
# y 100픽셀당 2퍼센트 씩 줄임
SCALE_PER_Y_PIXEL = (2.0 / 100.0) / 100.0
SCALE_PER_Z_PIXEL = (0.5 / 100.0) / 100.0


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()

    print(f'current time: {current_time}')

    # fill here
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].render()
        # fill here

        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time if abs(frame_time) >= sys.float_info.epsilon else 0.0
        current_time += frame_time
        # # 시간 출력용
        # print(f'delta time: {frame_time}, fps: {frame_rate}')

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
