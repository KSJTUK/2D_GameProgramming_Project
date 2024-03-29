import codes.game_world as game_world
import codes.game_framework as game_framework
import codes.tennis_court as tennis_court
import codes.tennis_game_score as tennis_game_score
import codes.ending_mode as ending_mode

NEW_COURT_START_TIME = 3.0
SCORE_FONT_SIZE = 30
END_SET_SCORE = 3


def new_set_start():
    global turn, deuce_mode_turn
    turn = (turn + 1) % 2
    deuce_mode_turn = turn


def new_court_start():
    global is_court_end, play_ball, deuce_mode_turn
    is_court_end = False
    tennis_game_score.new_court_game_start()

    if tennis_game_score.is_in_deuce_mode():
        deuce_mode_turn = (deuce_mode_turn + 1) % 2

    main_player_set_score, opponent_player_set_score = tennis_game_score.get_set_scores()
    if main_player_set_score == END_SET_SCORE or\
        opponent_player_set_score == END_SET_SCORE:
        game_framework.pop_mode()
        game_framework.change_mode(ending_mode)
        return

    if play_ball:
        game_world.remove_object(play_ball)
        play_ball = None

    game_framework.pop_mode()
    tennis_players_position_reset()
    set_serve_turn()


def tennis_players_position_reset():
    characters_default_diff_y = 40 * game_framework.RATIO_FROM_DEFAULT_H
    characters_default_diff_x = 100 * game_framework.RATIO_FROM_DEFAULT_W
    court_top = tennis_court.COURT_CENTER_Y + tennis_court.COURT_TOP_HEIGHT
    court_bottom = tennis_court.COURT_CENTER_Y - tennis_court.COURT_BOTTOM_HEIGHT

    main_player.x = tennis_court.COURT_CENTER_X - characters_default_diff_x
    main_player.y = court_bottom - characters_default_diff_y
    opponent_player.x = tennis_court.COURT_CENTER_X + characters_default_diff_x
    opponent_player.y = court_top + characters_default_diff_y


def set_serve_turn():
    if tennis_game_score.is_in_deuce_mode():
        if deuce_mode_turn == 1:
            main_player.state_machine.handle_event(('SERVE_TURN', 0))
            opponent_player.handle_event(('NOT_SERVE_TURN', 0))
        else:
            main_player.state_machine.handle_event(('NOT_SERVE_TURN', 0))
            opponent_player.handle_event(('SERVE_TURN', 0))
        return

    if turn == 1:
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


def set_referee():
    global play_ball, main_player, opponent_player, last_hit_player, turn, deuce_mode_turn
    global is_court_end, court_end_time, any_player_win
    global win_player, lose_player

    play_ball = None
    main_player = None
    opponent_player = None
    last_hit_player = None
    win_player = None
    court_end_time = 0.0

    any_player_win = False
    is_court_end = False

    turn = 0
    deuce_mode_turn = 0


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
    if play_ball is ball:
        play_ball = None


def calc_new_court_start_time():
    global court_end_time, any_player_win
    if court_end_time < NEW_COURT_START_TIME:
        court_end_time += game_framework.frame_time
        return

    court_end_time = 0.0
    if tennis_game_score.is_new_set_start():
        tennis_game_score.new_set_game_start()
        new_set_start()
    else:
        new_court_start()



def update():
    global is_court_end

    if is_court_end:
        calc_new_court_start_time()
        return

    if play_ball == None or main_player == None:
        return

    if play_ball.bound_count == 2:
        if last_hit_player is main_player:
            main_player_win()
        else:
            opponent_player_win()
        calculate_game_score()
        is_court_end = True

def render():
    tennis_game_score.draw_set_score_in_play_mode(SCORE_FONT_SIZE)

def calculate_game_score():
    global any_player_win
    if win_player is main_player:
        any_player_win = tennis_game_score.main_player_win()
    else:
        any_player_win = tennis_game_score.opponent_player_win()


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

    calculate_game_score()

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
    global win_player, lose_player, main_player, opponent_player
    win_player, lose_plyer = main_player, opponent_player
    main_player.state_machine.handle_event(('WIN', 0))
    opponent_player.handle_event(('LOSE', 0))


def opponent_player_win():
    global win_player, lose_player, main_player, opponent_player
    win_player, lose_plyer = opponent_player, main_player
    opponent_player.handle_event(('WIN', 0))
    main_player.state_machine.handle_event(('LOSE', 0))
