import tennis_game_score
import tennis_referee
import game_framework
import game_world

from pico2d import clear_canvas, update_canvas, get_events, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE


def init():
    print('enter score mode')
    tennis_game_score.print_scores()


def finish():
    print('exit score mode')


def update():
    game_world.update()
    tennis_referee.update()


def render():
    clear_canvas()
    game_world.render()
    tennis_game_score.draw_score()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
