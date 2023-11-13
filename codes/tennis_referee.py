def new_set_start():
    global turn
    turn = (turn + 1) % 2

    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score

    main_player_score, opponent_player_score = 0, 0

    main_player.state_machine.handle_event(('NEW_COURT_START', 0))


def set_refree():
    global play_ball, main_player, opponent_player, turn
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score

    play_ball = None
    main_player = None
    opponent_player = None
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

    if play_ball.bound_count >= 2:
        main_player.state_machine.handle_event(('WIN', 0))


def bound_over_court():
    print('ball bound over the court')