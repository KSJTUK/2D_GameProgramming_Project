from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, \
    SDLK_SPACE, SDLK_v, SDLK_r

left_arrow_downed = False
right_arrow_downed = False
up_arrow_downed = False
down_arrow_downed = False
diff_arrow_downed_same_time = False

def new_court_start(e):
    return e[0] == 'NEW_COURT_START'

def is_right_arrow_downed():
    return right_arrow_downed


def is_left_arrow_downed():
    return left_arrow_downed


def is_up_arrow_downed():
    return up_arrow_downed


def is_down_arrow_downed():
    return down_arrow_downed


def right_arrow_down(e):
    global right_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT:
        right_arrow_downed = True
        return True


def right_arrow_up(e):
    global right_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT:
        right_arrow_downed = False
        return True


def left_arrow_down(e):
    global left_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT:
        left_arrow_downed = True
        return True


def left_arrow_up(e):
    global left_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT:
        left_arrow_downed = False
        return True


def up_arrow_down(e):
    global up_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP:
        up_arrow_downed = True
        return True


def down_arrow_down(e):
    global down_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN:
        down_arrow_downed = True
        return True


def up_arrow_up(e):
    global up_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP:
        up_arrow_downed = False
        return True


def down_arrow_up(e):
    global down_arrow_downed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN:
        down_arrow_downed = False
        return True


def check_arrow_all(e):
    right_arrow_down(e), left_arrow_down(e), left_arrow_up(e), right_arrow_up(e),
    down_arrow_down(e), up_arrow_down(e), down_arrow_up(e), up_arrow_up(e)


def is_player_has_no_direction(e):
    return e[0] == 'PLAYER_HAS_NO_DIRECTION'


# 반대 방향의 방향키가 같이 눌려있다면 True리턴
def is_diff_arrow_downed_same_time(e):
    global right_arrow_downed, left_arrow_downed, up_arrow_downed, down_arrow_downed, diff_arrow_downed_same_time
    if e[0] != 'INPUT':
        return False

    check_arrow_all(e)
    if down_arrow_downed and up_arrow_downed and not left_arrow_downed and not right_arrow_downed:
        diff_arrow_downed_same_time = True
        return True
    elif right_arrow_downed and left_arrow_downed and not down_arrow_downed and not up_arrow_downed:
        diff_arrow_downed_same_time = True
        return True
    elif right_arrow_downed and left_arrow_downed and up_arrow_downed and down_arrow_downed:
        diff_arrow_downed_same_time = True
        return True
    else:
        return False


# 모든 방향키가 눌리지 않았다면 True리턴
def not_downed(e):
    global right_arrow_downed, left_arrow_downed, up_arrow_downed, down_arrow_downed
    if e[0] != 'INPUT':
        return False

    check_arrow_all(e)
    if not down_arrow_downed and not up_arrow_downed and not left_arrow_downed and not right_arrow_downed:
        return True
    else:
        return False


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def key_down_v_and_not_updown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[
        1].key == SDLK_v and not up_arrow_downed and not down_arrow_downed


def key_down_r(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r


def animation_end(e):
    return e[0] == 'ANIMATION_END'


def animation_end_and_keydown(e):
    return e[0] == 'ANIMATION_END' and (left_arrow_downed or right_arrow_downed or down_arrow_downed or up_arrow_downed)


def collision_character_serveball(e):
    return e[0] == 'tennis_player:serve_ball'

def player_win(e):
    return e[0] == 'WIN'

def player_lose(e):
    return e[0] == 'LOSE'
