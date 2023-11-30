from pico2d import update_canvas, clear_canvas, get_events, \
    SDL_KEYDOWN, SDL_QUIT, SDLK_SPACE, SDLK_ESCAPE
import game_framework
import tennis_game_ui
import play_mode

def init():
    pass

def finish():
    pass

def update():
    pass

def render():
    cw, ch = game_framework.CANVAS_W, game_framework.CANVAS_H
    clear_canvas()
    tennis_game_ui.ui_images['title'].composite_draw(0, ' ', cw // 2, ch // 2, cw, ch)
    tennis_game_ui.draw_string(cw // 2, ch // 2, 'TRY AGAIN?', 50, 'center')
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_mode)
