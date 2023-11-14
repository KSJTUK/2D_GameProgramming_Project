import game_world

def new_set_start():
    # global turn
    # turn = (turn + 1) % 2

    global main_player_score, opponent_player_score

    main_player_score, opponent_player_score = 0, 0
    new_court_start()

def new_court_start():
    global is_court_end
    is_court_end = False

    if play_ball:
        game_world.remove_object(play_ball)

    if turn == 0:
        main_player.state_machine.handle_event(('SERVE_TURN', 0))
        opponent_player.state_machine.handle_event(('NOT_SERVE_TURN', 0))
    else:
        main_player.state_machine.handle_event(('NOT_SERVE_TURN', 0))
        opponent_player.state_machine.handle_event(('SERVE_TURN', 0))

def serve_turn_player_hit_serve():
    main_player.state_machine.handle_event(('NEW_COURT_START', 0))
    # opponent_player.state_machine.handle_event(('NEW_COURT_START', 0))

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
        main_player.state_machine.handle_event(('WIN', 0))


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

    if not court_end:
        last_hit_player.state_machine.handle_event(('LOSE', 0))
        calculate_game_score()

    is_court_end = True

def bound_over_court():
    global is_court_end, win_player, lose_player
    if is_court_end: return

    if last_hit_player == None:
        raise ValueError('last hit player is None')

    bound_count_over_1 = play_ball.bound_count > 1

    if bound_count_over_1:
        if last_hit_player is main_player:
            win_player, lose_player = main_player, opponent_player
        else:
            win_player, lose_player = opponent_player, main_player
    else:
        if last_hit_player is main_player:
            win_player, lose_player = opponent_player, main_player
        else:
            win_player, lose_player = main_player, opponent_player
    court_end()

def court_end():
    global is_court_end, win_player, lose_player
    if is_court_end: return

    win_player.state_machine.handle_event(('WIN', 0))
    lose_player.state_machine.handle_event(('LOSE', 0))
    calculate_game_score()

    is_court_end = True