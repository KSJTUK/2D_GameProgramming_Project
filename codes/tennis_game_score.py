from pico2d import load_image

def init():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global new_set_started
    global deuce_mode, main_player_deuce_mode_win, opponent_player_deuce_mode_win
    global score_images, set_score_images

    main_player_score = 0
    opponent_player_score = 0
    main_player_set_score = 0
    opponent_player_set_score = 0

    new_set_started = False
    deuce_mode = False

    main_player_deuce_mode_win = False
    opponent_player_deuce_mode_win = False

    score_images = [load_image(f'./../resources/score_images/score_image_{x}.png') for x in range(1, 10 + 1)]
    set_score_images = [load_image(f'./../resources/score_images/set_score_image_{x}.png') for x in range(1, 10 + 1)]

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

    print_scores()

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

    print_scores()

    return isPlayerWin

def print_scores():
    print(f'main_player set score: {main_player_set_score} , opponent_player set score: {opponent_player_set_score}')
    print(f'main_player score: {main_player_score} , opponent_player score: {opponent_player_score}')