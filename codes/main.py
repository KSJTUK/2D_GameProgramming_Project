from pico2d import open_canvas, close_canvas

import game_framework

# import play_mode as start_mode
# import title_mode as start_mode
import ending_mode as start_mode
import tennis_game_ui

open_canvas(game_framework.CANVAS_W, game_framework.CANVAS_H)
tennis_game_ui.init()
game_framework.run(start_mode)
close_canvas()
