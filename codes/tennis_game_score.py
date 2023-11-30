from pico2d import load_image

import game_framework
import score_mode
import tennis_game_ui


def init():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global new_set_started
    global deuce_mode
    global score_images, set_score_images
    global alphabet_images
    global main_player_deuce_score, opponent_player_deuce_score

    main_player_score = 40
    opponent_player_score = 30
    main_player_set_score = 0
    opponent_player_set_score = 0
    main_player_deuce_score = 0
    opponent_player_deuce_score = 0

    new_set_started = False
    deuce_mode = False


def draw_score(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    if new_set_started:
        return
    elif deuce_mode:
        draw_score_in_deuce_mode(score_font_size)
        return
    elif main_player_score == 40 or opponent_player_score == 40:
        tennis_game_ui.ui_images['match_point'].composite_draw(0, ' ', cw, ch + 100, 200, 50)

    tennis_game_ui.draw_string(cw - score_font_size * 2, ch + score_font_size * 2, 'your score',
                score_font_size, 'right')
    tennis_game_ui.draw_string(cw + score_font_size * 2, ch + score_font_size * 2, 'ai\'s score',
                score_font_size, 'left')
    tennis_game_ui.draw_string(cw, ch, f'{main_player_score:>2d}  -  {opponent_player_score:>2d}',
                score_font_size * 2, 'center')

def draw_score_in_deuce_mode(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    tennis_game_ui.ui_images['deuce'].composite_draw(0, ' ', cw, ch + 100, 200, 50)

    tennis_game_ui.draw_string(cw - score_font_size * 2, ch + score_font_size * 2, 'your score',
                               score_font_size, 'right')
    tennis_game_ui.draw_string(cw + score_font_size * 2, ch + score_font_size * 2, 'ai\'s score',
                               score_font_size, 'left')
    tennis_game_ui.draw_string(cw, ch, f'{main_player_deuce_score:>2d}  -  {opponent_player_deuce_score:>2d}',
                               score_font_size * 2, 'center')


def draw_set_score_in_play_mode(font_size):
    draw_font_y = game_framework.CANVAS_H - 15
    tennis_game_ui.draw_string(0, draw_font_y,
                f'set point: {main_player_set_score}-{opponent_player_set_score}', font_size, 'left')
    draw_font_y -= 30
    tennis_game_ui.draw_string(0, draw_font_y,
                f'game point: {main_player_score:>2d}-{opponent_player_score:>2d}', font_size, 'left')

def draw_set_win(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    tennis_game_ui.ui_images['deuce'].composite_draw(0, ' ', cw, ch + 100, 200, 50)

    tennis_game_ui.draw_string(cw - score_font_size * 2, ch + score_font_size * 2, 'your score',
                               score_font_size, 'right')
    tennis_game_ui.draw_string(cw + score_font_size * 2, ch + score_font_size * 2, 'ai\'s score',
                               score_font_size, 'left')
    tennis_game_ui.draw_string(cw, ch, f'{main_player_deuce_score:>2d}  -  {opponent_player_deuce_score:>2d}',
                               score_font_size * 2, 'center')

def in_deuce_mode():
    global deuce_mode
    deuce_mode = True


def is_new_set_start():
    return new_set_started


def is_in_deuce_mode():
    return deuce_mode


def new_set_game_start():
    global new_set_started
    new_set_started = False


def start_new_set_game():
    global main_player_score, opponent_player_score, new_set_started
    main_player_score, opponent_player_score = 0, 0
    new_set_started = True


def deuce_main_player_win():
    global new_set_started, deuce_mode, main_player_deuce_score, main_player_set_score

    main_player_deuce_score += 1

    if main_player_deuce_score - opponent_player_deuce_score == 2:
        main_player_set_score += 1
        new_set_started = True
        deuce_mode = False
        start_new_set_game()
        return True

    return False


def deuce_opponent_player_win():
    global new_set_started, deuce_mode, opponent_player_deuce_score, opponent_player_set_score

    opponent_player_deuce_score += 1

    if opponent_player_deuce_score - main_player_deuce_score == 2:
        opponent_player_set_score += 1
        new_set_started = True
        deuce_mode = False
        start_new_set_game()
        return True

    return False


def is_score_equal():
    return main_player_score == 40 and opponent_player_score == 40


def main_player_win():
    global main_player_score, main_player_set_score, deuce_mode

    if deuce_mode:
        game_framework.push_mode(score_mode)
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
        game_framework.push_mode(score_mode)
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
