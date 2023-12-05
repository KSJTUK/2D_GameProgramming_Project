from pico2d import load_image

ALPHABET_IMAGE_SIZE = 17

supported_special_symbols = ['*', '=', '-', '.', ':', '\'', ',', 'None', '!', '?', 'rev!', ' ', '/']
resource_dir = './resources/'
font_dir = resource_dir + 'font/'
ui_image_dir = resource_dir + 'ui_image/'
sound_dir = resource_dir + 'sounds/'

def init():
    global ui_images
    ui_images = { }
    load_ui_image('title', ui_image_dir + 'title.png')
    load_ui_image('deuce', ui_image_dir + 'deuce.png')
    load_ui_image('match_point', ui_image_dir + 'match_point.png')
    load_fonts()


def load_fonts():
    global alphabet_images, score_images

    upper_alpha = {chr(alpha): load_image(font_dir+f'alphabet_upper_font/alphabet_{chr(alpha)}.png')
                   for alpha in range(ord('A'), ord('Z') + 1)}
    lower_alpha = {chr(alpha): load_image(font_dir+f'alphabet_lower_font/alphabet_{chr(alpha)}.png')
                   for alpha in range(ord('a'), ord('z') + 1)}
    special_symbols = {supported_special_symbols[symbol_idx]:
                           load_image(font_dir+f'special_symbols/special_symbols_{symbol_idx + 1}.png')
                       for symbol_idx in range(len(supported_special_symbols))}
    numbers = {str(num): load_image(font_dir+f'number_font/number_{num}.png')
               for num in range(10)}

    alphabet_images = upper_alpha | lower_alpha | special_symbols | numbers

def load_ui_image(key, image_file_path):
    global ui_images
    ui_images[key] = load_image(image_file_path)


def draw_string(x, y, string, font_size=ALPHABET_IMAGE_SIZE, text_aligned='center'):
    if text_aligned == 'center':
        draw_string_aligned_center(x, y, string, font_size)
    elif text_aligned == 'left':
        draw_string_aligned_left(x, y, string, font_size)
    elif text_aligned == 'right':
        draw_string_aligned_right(x, y, string, font_size)
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
        alphabet_images[string[i]].composite_draw(0, ' ', left + i * font_size, cy,
                                                  font_size, font_size)
    return right