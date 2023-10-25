from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN

def arrow_right_down(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT:
        return True

def arrow_right_up(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT:
        return True

def arrow_left_down(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT:
        return True

def arrow_left_up(e):
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT:
        return True