from random import randrange

from . import const, main



def draw_screen(screen):
    text = main.char_array_to_string(screen)
    main.draw(text)


def fill_screen(char = '#'):
    cols, rows = const.FIELD_SIZE
    line = f'{char}' * cols
    text = f'{line}\n' * rows
    # text = [x[:] for x in [''.join([char] * cols)] * rows]
    # convert text to array of characters
    return main.string_to_char_array(text)


def create_splash():
    filename = r"E:\Python\WordRPG\gui\screens_80x25\splash.txt"
    text = main.load_txt(filename)
    # convert text to array of characters
    return main.string_to_char_array(text)


def create_frame():
    filename = r"E:\Python\WordRPG\gui\screens_80x25\frame.txt"
    text = main.load_txt(filename)
    # convert text to array of characters
    screen = main.string_to_char_array(text)
    # writing the frame over itself using formatting keywords to set color
    return main.write_to_array(screen, screen, col=0, row=0, fgcolor='cyan', bgcolor='blue')


def create_title():
    filename = r"E:\Python\WordRPG\gui\screens_80x25\title.txt"
    text = main.load_txt(filename)
    # convert text to array of characters
    return main.string_to_char_array(text)


def empty():
    screen = fill_screen(char=' ')
    # print the screen
    draw_screen(screen)


def fill():
    screen = fill_screen(char='#')
    # print the screen
    draw_screen(screen)


def splash():
    screen = fill_screen(char=' ')

    _splash = create_splash()
    main.write_to_array(_splash, screen, col = 0, row = 0, fgcolor = 'red')

    text = f'<<  COMBOY GAMING - 2018  >>'
    start = main.center_offset(text, const.SCREEN_SIZE[0])
    main.write_to_array(text, screen, col = start, row = 25, fgcolor = 'red')
   
    # print the screen
    draw_screen(screen)


def menu():
    screen = create_frame()

    header = f'> {const.HEADER} <'
    start = main.center_offset(header, const.SCREEN_SIZE[0])
    main.write_to_array(header, screen, col = start, row = 0, fgcolor = 'red')
    # print the screen
    draw_screen(screen)


def title():
    screen = create_frame()
    _title = create_title()
    main.write_to_array(_title, screen, col = 20, row = 8, fgcolor='cyan', bgcolor='magenta')
    # print the screen
    draw_screen(screen)


def random_words():
    screen = create_frame()
    text = 'WORDS'
    col, rows = const.FIELD_SIZE
    # put text in random places
    col_max = col - len(text)
    for _ in range( 30 ):
        rand_col = randrange( 0, col_max)
        rand_row = randrange( 0, rows)
        main.write_to_array(text, screen, col = rand_col, row = rand_row)
    # print the screen
    draw_screen(screen)