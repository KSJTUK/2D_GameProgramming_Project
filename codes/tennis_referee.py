def set_refree():
    global play_ball, main_player, opponent_player, turn
    play_ball = None
    main_player = None
    opponent_player = None

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
    if play_ball is ball:
        play_ball = None

def update():
    if play_ball == None or main_player == None:
        return

    if play_ball.bound_count >= 2:
        main_player.state_machine.handle_event(('WIN', 0))