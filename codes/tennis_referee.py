import game_world
import game_framework
import tennis_court

NEW_COURT_START_TIME = 3.0


def new_set_start():
    global turn
    turn = (turn + 1) % 2

    new_court_start()


def new_court_start():
    global is_court_end, play_ball
    is_court_end = False

    if play_ball:
        game_world.remove_object(play_ball)
        play_ball = None

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
    global play_ball, main_player, opponent_player, last_hit_player, turn
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global is_court_end, court_end_time
    global win_player, lose_player

    play_ball = None
    main_player = None
    opponent_player = None
    last_hit_player = None
    win_player = None
    court_end_time = 0.0

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


def calc_new_court_start_time():
    global court_end_time
    if court_end_time > NEW_COURT_START_TIME:
        court_end_time = 0.0
        if main_player_score >= 45 or opponent_player_score >= 45:
            new_set_start()
        else:
            new_court_start()
    else:
        court_end_time += game_framework.frame_time


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


def calculate_game_score():
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    if win_player is main_player:
        main_player_score += 15
        if main_player_score >= 45:
            main_player_set_score += 1
            main_player_score, opponent_player_score = 0, 0
    else:
        opponent_player_score += 15
        if opponent_player_score >= 45:
            opponent_player_set_score += 1
            main_player_score, opponent_player_score = 0, 0

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
    global win_player, lose_player, main_player, opponent_player
    win_player, lose_plyer = main_player, opponent_player
    main_player.state_machine.handle_event(('WIN', 0))
    opponent_player.handle_event(('LOSE', 0))


def opponent_player_win():
    global win_player, lose_player, main_player, opponent_player
    win_player, lose_plyer = opponent_player, main_player
    opponent_player.handle_event(('WIN', 0))
    main_player.state_machine.handle_event(('LOSE', 0))
