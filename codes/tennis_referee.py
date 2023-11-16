import game_world
from tennis_court import *

def new_set_start():
    global turn
    turn = (turn + 1) % 2

    global main_player_score, opponent_player_score

    main_player_score, opponent_player_score = 0, 0
    set_serve_turn()
    new_court_start()

def new_court_start():
    global is_court_end, play_ball
    is_court_end = False

    if play_ball:
        game_world.remove_object(play_ball)
        play_ball = None

def set_serve_turn():
    if turn == 0:
        main_player.state_machine.handle_event(('SERVE_TURN', 0))
        opponent_player.handle_event(('NOT_SERVE_TURN', 0))
    else:
        main_player.state_machine.handle_event(('NOT_SERVE_TURN', 0))
        opponent_player.handle_event(('SERVE_TURN', 0))

def serve_turn_player_hit_serve():
    game_world.add_collision_pair('tennis_player:ball', main_player, play_ball)
    game_world.add_collision_pair('tennis_player:ball', opponent_player, None)
    main_player.state_machine.handle_event(('NEW_COURT_START', 0))
    opponent_player.handle_event(('NEW_COURT_START', 0))

def set_refree():
    global play_ball, main_player, opponent_player, last_hit_player, turn
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global is_court_end
    global win_player, lose_player

    play_ball = None
    main_player = None
    opponent_player = None
    last_hit_player = None
    win_player = None

    is_court_end = False
    main_player_score, opponent_player_score = 0, 0
    main_player_set_score, opponent_player_set_score = 0, 0

    turn = 0

def subscribe_player(player_tag, player):
    global main_player, opponent_player
    if player_tag == 'opponent_player':
        opponent_player = player
    elif player_tag == 'main_player':
        main_player = player

def subscribe_ball(ball):
    global play_ball
    play_ball = ball

def remove_ball(ball):
    global play_ball
    print('remove ball in referee')
    if play_ball is ball:
        play_ball = None

def update():
    if play_ball == None or main_player == None:
        return

    if play_ball.bound_count == 2:
        if last_hit_player is main_player:
            main_player_win()
        else:
            opponent_player_win()


def calculate_game_score():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    if win_player is main_player:
         main_player_score += 15
         if main_player_score >= 45:
             main_player_set_score += 1
             new_set_start()
    else:
        opponent_player_score += 15
        if opponent_player_score >= 45:
            opponent_player_set_score += 1
            new_set_start()

    print(f'main_player set score: {main_player_set_score} , opponent_player set score: {opponent_player_set_score}')
    print(f'main_player score: {main_player_score} , opponent_player score: {opponent_player_score}')

def bound_net():
    global is_court_end
    if is_court_end: return

    if last_hit_player == main_player:
        opponent_player_win()
    else:
        main_player_win()

    calculate_game_score()

    is_court_end = True

def ball_in_over_court():
    global play_ball
    global is_court_end
    if is_court_end: return

    if play_ball.bound_count == 0:
        if last_hit_player is main_player:
            opponent_player_win()
        else:
            main_player_win()
    else:
        if last_hit_player is main_player:
            main_player_win()
        else:
            opponent_player_win()

    play_ball = None
    is_court_end = True

def bound_over_court():
    global is_court_end, win_player, lose_player
    if is_court_end: return

    if last_hit_player == None:
        raise ValueError('last hit player is None')

    if not play_ball:
        return

    if play_ball.bound_count > 1:
        if last_hit_player is main_player:
            main_player_win()
        else:
            opponent_player_win()
    else:
        if last_hit_player is main_player:
            opponent_player_win()
        else:
            main_player_win()

    calculate_game_score()

    is_court_end = True

def main_player_win():
    main_player.state_machine.handle_event(('WIN', 0))
    opponent_player.handle_event(('LOSE', 0))
def opponent_player_win():
    opponent_player.handle_event(('WIN', 0))
    main_player.state_machine.handle_event(('LOSE', 0))