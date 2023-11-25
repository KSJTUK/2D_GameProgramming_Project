from pico2d import load_image

main_player_score = 0
opponent_player_score = 0
main_player_set_score = 0
opponent_player_set_score = 0

# score_number_imgae = load_image('./../resources/tennis_ball.png')

def start_new_set_game():
    global main_player_score, opponent_player_score
    main_player_score, opponent_player_score = 0, 0

def main_player_win():
    global main_player_score, main_player_set_score
    isPlayerWin = False

    if main_player_score == 30:
        main_player_score += 10
    elif main_player_score == 40:
        main_player_set_score += 1
        start_new_set_game()
        isPlayerWin = True
    else:
        main_player_score += 15

    print_scores()

    return isPlayerWin


def opponent_player_win():
    global opponent_player_score, opponent_player_set_score
    isPlayerWin = False

    if opponent_player_score == 30:
        opponent_player_score += 10
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