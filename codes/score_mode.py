import tennis_game_score
import tennis_referee
import game_world

from pico2d import clear_canvas, update_canvas


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
    pass
