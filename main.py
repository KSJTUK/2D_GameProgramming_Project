from pico2d import open_canvas, close_canvas

import codes.game_framework as game_framework

import codes.title_mode as start_mode
# import codes.play_mode as start_mode
# import codes.ending_mode as start_mode
import codes.tennis_game_ui as tennis_game_ui

open_canvas(game_framework.CANVAS_W, game_framework.CANVAS_H)
tennis_game_ui.init()
game_framework.run(start_mode)
close_canvas()
