import codes.tennis_game_score as tennis_game_score
import codes.tennis_referee as tennis_referee
import codes.game_framework as game_framework
import codes.game_world as game_world
import codes.check_event_funtions as check_event_funtions

from pico2d import clear_canvas, update_canvas, get_events, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
SCORE_FONT_SIZE = 30


def init():
    pass


def finish():
    check_event_funtions.reset_arrow_key_state()


def update():
    game_world.update()
    tennis_referee.update()


def render():
    clear_canvas()
    game_world.render()
    tennis_referee.render()
    tennis_game_score.draw_score(SCORE_FONT_SIZE)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
