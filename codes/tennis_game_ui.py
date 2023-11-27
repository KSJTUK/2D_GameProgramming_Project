from pico2d import load_image

ALPHABET_IMAGE_SIZE = 17

supported_special_symbols = ['*', '=', '-', '.', ':', '\'', ',', 'None', '!', '?', 'rev!', ' ', '/']

def init():
    load_fonts()


def load_fonts():
    global alphabet_images, score_images

    upper_alpha = {chr(alpha): load_image(f'./../resources/alphabet_upper_font/alphabet_{chr(alpha)}.png')
                   for alpha in range(ord('A'), ord('Z') + 1)}
    lower_alpha = {chr(alpha): load_image(f'./../resources/alphabet_lower_font/alphabet_{chr(alpha)}.png')
                   for alpha in range(ord('a'), ord('z') + 1)}
    special_symbols = {supported_special_symbols[symbol_idx]:
                           load_image(f'./../resources/special_symbols/special_symbols_{symbol_idx + 1}.png')
                       for symbol_idx in range(len(supported_special_symbols))}
    numbers = {str(num): load_image(f'./../resources/number_font/number_{num}.png')
               for num in range(10)}

    alphabet_images = upper_alpha | lower_alpha | special_symbols | numbers

def draw_string(cx, cy, string, font_size=ALPHABET_IMAGE_SIZE, text_aligned='center'):
    if text_aligned == 'center':
        draw_string_aligned_center(cx, cy, string, font_size)
    elif text_aligned == 'left':
        draw_string_aligned_left(cx, cy, string, font_size)
    elif text_aligned == 'right':
        draw_string_aligned_right(cx, cy, string, font_size)
    else:
        raise ValueError(f'not exist text aligned option: {text_aligned}')


def draw_string_aligned_center(cx, cy, string, font_size):
    HALF_FONT_SIZE = font_size // 2
    left = cx - ((len(string) * font_size) // 2) + HALF_FONT_SIZE
    right = left
    for i in range(len(string)):
        alphabet_images[string[i]].composite_draw(0, ' ', left + i * font_size, cy,
                                                  font_size, font_size)
        right += font_size
    return right


def draw_string_aligned_left(cx, cy, string, font_size):
    HALF_FONT_SIZE = font_size // 2
    right = cx
    for i in range(len(string)):
        alphabet_images[string[i]].composite_draw(0, ' ', cx + i * font_size + HALF_FONT_SIZE, cy,
                                                  font_size, font_size)
        right += font_size
    return right


def draw_string_aligned_right(cx, cy, string, font_size):
    HALF_FONT_SIZE = font_size // 2
    left = cx - (len(string) * font_size) + HALF_FONT_SIZE
    right = left + font_size
    for i in range(len(string)):
        # alphabet_images[string[i]].draw(left + i * ALPHABET_IMAGE_SIZE, cy)
        alphabet_images[string[i]].composite_draw(0, ' ', left + i * font_size, cy,
                                                  font_size, font_size)
    return right