from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, clamp,\
    SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE
import codes.game_framework as game_framework
import codes.tennis_game_ui as tennis_game_ui
import codes.play_mode as play_mode

def init():
    global font_size, min_font_size, max_font_size, title_font_size
    global font_animation_dir
    min_font_size, max_font_size = 45, 55
    font_size = 30
    title_font_size = font_size * 2
    font_animation_dir = 1

def finish():
    pass

def update():
    font_size_update()

def render():
    clear_canvas()
    cw, ch = game_framework.CANVAS_W, game_framework.CANVAS_H
    tennis_game_ui.ui_images['title'].composite_draw(0, ' ', cw // 2, ch // 2,
                                                     cw, ch)
    tennis_game_ui.draw_string(cw // 2, game_framework.CANVAS_H - ch // 4, 'POWER TENNIS', title_font_size, 'center')
    tennis_game_ui.draw_string(cw // 2, ch // 4, 'PRESS SPACE START', font_size, 'center')
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

def font_size_update():
    global font_size, font_animation_dir
    animation_speed = 10.0
    font_size += font_animation_dir * animation_speed * game_framework.frame_time
    if font_size >= max_font_size:
        font_animation_dir = -1
    elif font_size <= min_font_size:
        font_animation_dir = 1

    font_size = clamp(min_font_size, font_size, max_font_size)
