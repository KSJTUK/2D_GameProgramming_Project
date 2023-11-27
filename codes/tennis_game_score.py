from pico2d import load_image

import game_framework
import score_mode

SCORE_IMAGE_WIDTH = 33
SCORE_IMAGE_HEIGHT = 34

DASH_IMAGE_SIZE = 16

ALPHABET_IMAGE_SIZE = 17


def init():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global new_set_started
    global deuce_mode, main_player_deuce_mode_win, opponent_player_deuce_mode_win
    global score_images, set_score_images
    global alphabet_images

    main_player_score = 0
    opponent_player_score = 0
    main_player_set_score = 0
    opponent_player_set_score = 0

    new_set_started = False
    deuce_mode = False

    main_player_deuce_mode_win = False
    opponent_player_deuce_mode_win = False

    score_images = [load_image(f'./../resources/num_font_yellow/score_image{x}.png') for x in range(0, 10)]
    upper_alpha = { chr(alpha):load_image(f'./../resources/alphabet_upper_font/alphabet_{chr(alpha)}.png')
                    for alpha in range(ord('A'), ord('Z') + 1)}
    lower_alpha = { chr(alpha):load_image(f'./../resources/alphabet_lower_font/alphabet_{chr(alpha)}.png')
                    for alpha in range(ord('a'), ord('z') + 1)}

    alphabet_images = upper_alpha | lower_alpha
    alphabet_images['-'] = load_image(f'./../resources/dash_image.png')
    print(alphabet_images)
    # set_score_images = [load_image(f'./../resources/num_font_green/set_score_image_{x}.png') for x in range(0, 10)]


def draw_score():
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    global main_player_score, opponent_player_score
    test_string = 'MakeATestString'
    font_size = 30
    draw_string(cw, ch + SCORE_IMAGE_HEIGHT * 2, test_string, font_size,'left')
    draw_scores(main_player_score, cw, ch + SCORE_IMAGE_HEIGHT)
    draw_string(cw, ch, test_string, font_size, 'center')
    draw_scores(opponent_player_score, cw, ch - SCORE_IMAGE_HEIGHT)
    draw_string(cw, ch - SCORE_IMAGE_HEIGHT * 2, test_string, font_size, 'right')


def draw_set_score_in_score_mode():
    pass


def draw_set_score_in_play_mode():
    pass


def draw_scores(score, x, y):
    global score_images

    divide_score = divmod(score, 10)

    score_images[divide_score[0]].composite_draw(0, ' ',
                                            x - SCORE_IMAGE_WIDTH, y, SCORE_IMAGE_WIDTH * 2, SCORE_IMAGE_HEIGHT * 2)
    score_images[divide_score[1]].composite_draw(0, ' ',
                                            x + SCORE_IMAGE_WIDTH, y, SCORE_IMAGE_WIDTH * 2, SCORE_IMAGE_HEIGHT * 2)


def draw_string(cx, cy, string, font_size=ALPHABET_IMAGE_SIZE, text_aligned='center'):
    if text_aligned == 'center':
        draw_string_aligned_center(cx, cy, string, font_size)
    elif text_aligned == 'left':
        draw_string_aligned_left(cx, cy, string, font_size)
    elif text_aligned == 'right':
        draw_string_aligned_right(cx, cy, string, font_size)
    else:
        raise ValueError(f'not exist text aligned option: {text_aligned}')


def draw_string_aligned_center(cx, cy, string, font_size):
    HALF_IMAGE_SIZE = font_size // 2
    left = cx - ((len(string) * font_size) // 2) + HALF_IMAGE_SIZE
    for i in range(len(string)):
        # alphabet_images[string[i]].draw(left + i * ALPHABET_IMAGE_SIZE, cy)
        alphabet_images[string[i]].composite_draw(0, ' ', left + i * font_size, cy,
                                                  font_size, font_size)

def draw_string_aligned_left(cx, cy, string, font_size):
    HALF_IMAGE_SIZE = font_size // 2
    for i in range(len(string)):
        # alphabet_images[string[i]].draw(cx + i * ALPHABET_IMAGE_SIZE + HALF_IMAGE_SIZE, cy)
        alphabet_images[string[i]].composite_draw(0, ' ', cx + i * font_size + HALF_IMAGE_SIZE, cy,
                                                  font_size, font_size)

def draw_string_aligned_right(cx, cy, string, font_size):
    HALF_IMAGE_SIZE = font_size // 2
    left = cx - (len(string) * font_size) + HALF_IMAGE_SIZE
    for i in range(len(string)):
        # alphabet_images[string[i]].draw(left + i * ALPHABET_IMAGE_SIZE, cy)
        alphabet_images[string[i]].composite_draw(0, ' ', left + i * font_size, cy,
                                                  font_size, font_size)


def in_deuce_mode():
    global deuce_mode
    deuce_mode = True


def is_new_set_start():
    return new_set_started


def new_set_game_start():
    global new_set_started
    new_set_started = False


def start_new_set_game():
    global main_player_score, opponent_player_score, new_set_started
    main_player_score, opponent_player_score = 0, 0
    new_set_started = True


def deuce_main_player_win():
    global main_player_deuce_mode_win, opponent_player_deuce_mode_win, new_set_started, deuce_mode

    if main_player_deuce_mode_win:
        new_set_started = True
        deuce_mode = False
        return True

    main_player_deuce_mode_win = True
    opponent_player_deuce_mode_win = False
    return False


def deuce_opponent_player_win():
    global main_player_deuce_mode_win, opponent_player_deuce_mode_win, new_set_started, deuce_mode

    if opponent_player_deuce_mode_win:
        new_set_started = True
        deuce_mode = False
        return True

    main_player_deuce_mode_win = False
    opponent_player_deuce_mode_win = True
    return False


def is_score_equal():
    return main_player_score == 40 and opponent_player_score == 40


def main_player_win():
    global main_player_score, main_player_set_score, deuce_mode

    if deuce_mode:
        return deuce_main_player_win()

    isPlayerWin = False
    if main_player_score == 30:
        main_player_score += 10

        if is_score_equal():
            deuce_mode = True

    elif main_player_score == 40:
        main_player_set_score += 1
        start_new_set_game()
        isPlayerWin = True
    else:
        main_player_score += 15

    game_framework.push_mode(score_mode)

    return isPlayerWin


def opponent_player_win():
    global opponent_player_score, opponent_player_set_score, deuce_mode

    if deuce_mode:
        return deuce_opponent_player_win()

    isPlayerWin = False
    if opponent_player_score == 30:
        opponent_player_score += 10

        if is_score_equal():
            deuce_mode = True

    elif opponent_player_score == 40:
        opponent_player_score += 10
        opponent_player_set_score += 1
        start_new_set_game()
        isPlayerWin = True
    else:
        opponent_player_score += 15

    game_framework.push_mode(score_mode)

    return isPlayerWin
