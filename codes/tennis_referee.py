def new_set_start():
    global turn
    turn = (turn + 1) % 2

    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score

    main_player_score, opponent_player_score = 0, 0

    main_player.state_machine.handle_event(('NEW_COURT_START', 0))

def set_refree():
    global play_ball, main_player, opponent_player, last_hit_player, turn
    global main_player_score, opponent_player_score
    global main_player_set_score, opponent_player_set_score
    global court_end

    play_ball = None
    main_player = None
    opponent_player = None
    last_hit_player = None

    court_end = False
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
    if last_hit_player == main_player:
        opponent_player_score += 15
    else:
        main_player_score += 15

    print(f'main_player score: {main_player_score} , opponent_player score: {opponent_player_score}')

    if main_player_score >= 45 or opponent_player_score >= 45:
        pass


def bound_over_court():
    global court_end

    if last_hit_player == None:
        raise ValueError('last hit player is None')

    if not court_end:
        last_hit_player.state_machine.handle_event(('LOSE', 0))
        calculate_game_score()

    court_end = True