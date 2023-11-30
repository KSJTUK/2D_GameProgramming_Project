from pico2d import load_image

import game_framework
import score_mode
import tennis_game_ui
import tennis_referee


def init():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global new_set_started, set_scores_draw_mode, game_end_draw_mode
    global deuce_mode
    global score_images, set_score_images
    global alphabet_images
    global main_player_deuce_score, opponent_player_deuce_score
    global is_main_player_win

    main_player_score = 40
    opponent_player_score = 30
    main_player_set_score = 2
    opponent_player_set_score = 0
    main_player_deuce_score = 0
    opponent_player_deuce_score = 0

    set_scores_draw_mode, game_end_draw_mode = False, False
    new_set_started = False
    is_main_player_win = False
    deuce_mode = False


def draw_score(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    if game_end_draw_mode:
        draw_game_end(score_font_size * 3)
        return

    if new_set_started:
        draw_set_end(score_font_size)
        return
    elif set_scores_draw_mode:
        draw_set_score(score_font_size)
        return
    elif deuce_mode:
        draw_score_in_deuce_mode(score_font_size)
        return
    elif main_player_score == 40 or opponent_player_score == 40:
        tennis_game_ui.ui_images['match_point'].composite_draw(0, ' ', cw, ch + 100, 200, 50)

    draw_game_score(score_font_size)

def draw_game_score(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2
    tennis_game_ui.draw_string(cw - score_font_size * 2, ch + score_font_size * 2, 'your score',
                score_font_size, 'right')
    tennis_game_ui.draw_string(cw + score_font_size * 2, ch + score_font_size * 2, 'ai\'s score',
                score_font_size, 'left')
    tennis_game_ui.draw_string(cw, ch, f'{main_player_score:>2d}  -  {opponent_player_score:>2d}',
                score_font_size * 2, 'center')

def draw_set_score(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2
    tennis_game_ui.draw_string(cw - score_font_size * 2, ch + score_font_size * 2, 'your set score',
                score_font_size, 'right')
    tennis_game_ui.draw_string(cw + score_font_size * 2, ch + score_font_size * 2, 'ai\'s set score',
                score_font_size, 'left')
    tennis_game_ui.draw_string(cw, ch, f'{main_player_set_score:>2d}  -  {opponent_player_set_score:>2d}',
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

def draw_set_end(score_font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    if is_main_player_win:
        tennis_game_ui.draw_string(cw, ch,
                                   'Set End You Win!!', score_font_size, 'center')
    else:
        tennis_game_ui.draw_string(cw, ch,
                                   'Set End You Lose...', score_font_size, 'center')

def draw_game_end(font_size):
    cw, ch = game_framework.CANVAS_W // 2, game_framework.CANVAS_H // 2

    if is_main_player_win:
        tennis_game_ui.draw_string(cw, ch,
                                   'You Win!!', font_size, 'center')
    else:
        tennis_game_ui.draw_string(cw, ch,
                                   'You Lose...', font_size, 'center')

def in_deuce_mode():
    global deuce_mode
    deuce_mode = True


def is_new_set_start():
    return new_set_started


def is_in_deuce_mode():
    return deuce_mode


def new_set_game_start():
    global new_set_started, set_scores_draw_mode
    new_set_started = False
    set_scores_draw_mode = True

def new_court_game_start():
    global set_scores_draw_mode
    set_scores_draw_mode = False

def tennis_game_end():
    global game_end_draw_mode
    game_end_draw_mode = True


def start_new_set_game():
    global main_player_score, opponent_player_score, new_set_started
    main_player_score, opponent_player_score = 0, 0
    new_set_started = True


def deuce_main_player_win():
    global new_set_started, deuce_mode, main_player_deuce_score, main_player_set_score, is_main_player_win

    main_player_deuce_score += 1

    if main_player_deuce_score - opponent_player_deuce_score >= 2:
        main_player_set_score += 1
        is_main_player_win = True
        new_set_started = True
        deuce_mode = False
        start_new_set_game()

        if main_player_set_score == tennis_referee.END_SET_SCORE:
            tennis_game_end()
        return True

    return False


def deuce_opponent_player_win():
    global new_set_started, deuce_mode, opponent_player_deuce_score, opponent_player_set_score, is_main_player_win

    opponent_player_deuce_score += 1

    if opponent_player_deuce_score - main_player_deuce_score >= 2:
        opponent_player_set_score += 1
        is_main_player_win = False
        new_set_started = True
        deuce_mode = False
        start_new_set_game()

        if opponent_player_set_score == tennis_referee.END_SET_SCORE:
            tennis_game_end()
        return True

    return False


def is_score_equal():
    return main_player_score == 40 and opponent_player_score == 40


def main_player_win():
    global main_player_score, main_player_set_score, deuce_mode, is_main_player_win

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
        is_main_player_win = True
        start_new_set_game()
        isPlayerWin = True
    else:
        main_player_score += 15

    if main_player_set_score == tennis_referee.END_SET_SCORE:
        tennis_game_end()

    game_framework.push_mode(score_mode)

    return isPlayerWin


def opponent_player_win():
    global opponent_player_score, opponent_player_set_score, deuce_mode, is_main_player_win

    if deuce_mode:
        game_framework.push_mode(score_mode)
        return deuce_opponent_player_win()

    isPlayerWin = False
    if opponent_player_score == 30:
        opponent_player_score += 10

        if is_score_equal():
            deuce_mode = True

    elif opponent_player_score == 40:
        opponent_player_set_score += 1
        is_main_player_win = False
        start_new_set_game()
        isPlayerWin = True
    else:
        opponent_player_score += 15

    if opponent_player_set_score == tennis_referee.END_SET_SCORE:
        tennis_game_end()

    game_framework.push_mode(score_mode)

    return isPlayerWin


def get_set_scores():
    return main_player_set_score, opponent_player_set_score