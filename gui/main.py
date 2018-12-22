""" Main functions for gui-related tasks """
import os
import codecs
from collections import deque
import logging
logging.basicConfig(filename=r'E:\Python\WordRPG\gui\gui_error.log',level=logging.ERROR)
logging.debug('debug logging:')
# import textwrap
from colorama import init as colorama_init
# imports from gui module
from . import const
from . import font



def setup_terminal():
    """ sets the size of the terminal window and clears it before printing"""
    colorama_init( convert = True )
    cols, lines = const.SCREEN_SIZE
    os.system(f"mode con cols={cols} lines={lines}")


def clear():
    """ clear terminal window """
    os.system('cls' if os.name == 'nt' else 'clear')


def make_unicode(text):
    """ Ensures that text is encoded as unicode for error-logging """
    # if type(text) != unicode:
    #     return text.decode('utf-8')
    # else:
    return text.encode( encoding="utf-8")


def draw(screen):
    """ Prints to the output window

    Prints the given 'screen' to the output window.

    **Arguments:**
        :``screen``: `str` Multi-line string to print.
     """
    clear()
    print(screen)


def load_txt(filename, codec = 'utf-8'):
    """ Load .txt file

    Reads in contets of a .txt file into a variable

    Arguments:
        filename {[type]} -- [description]

    Keyword Arguments:
        codec {str} -- [description] (default: {'utf-8'})

    Returns:
        [type] -- [description]
    """

    with codecs.open(filename, encoding = codec)as f:
        return f.read()


def string_to_char_array(_string, seperator = '\n'):
    """ Convert string to 2D array

    Converts a multi-line string into a two-dimensional deque array of string
    characters.

    **Arguments:**

        :``_string``: `str` Multi-line string block

    **Keword Arguments:**

        :``seperator``: `str` Character to split _string by. Default is newline ('\n')
        :``ignore_first``: `bool` If True, ignore the first line of _string.
        :``ignore_last``: `bool` If True, ignore the last line of _string.
    """
    # split text into lines/rows
    _rows = _string.split(seperator)

    # cols, rows = const.FIELD_SIZE
    # return deque([deque(col, maxlen=cols + 1) for col in _rows], maxlen=rows + 3)
    return [list(col) for col in _rows]


def char_array_to_string(_array ):
    """ Convert array to string

    Converts a two-dimensional deque array of string characters into a
    multi-line string that can be printed to the output window.

    **Arguments:**
        :``_array``: `list` 2D array of characters

    **Keword Arguments:**
        None
    """

    lines = [''.join(char) for char in _array]
    return '\n'.join(lines)


def center_text(text, width, fillchar = ' '):
    """ Centers text

    Centers the given text string in the given 'width' and fills empty space
    with the supplied 'fillchar'. This modifies the original string object.

    Arguments:
        text {str} -- Text to be centered
        width {int} -- Width of the text field to center within

    Keyword Arguments:
        fillchar {str} -- String character to fill empty space (default: {' '})

    Returns:
        str -- New centered and space-filled string
    """

    return text.center( width, fillchar )


def center_offset(text, width):
    """ Get offset to center text

    Gets the offset needed to center the given 'text' string within the given
    'width' of the field. Unlike '.center_text()' this does not modify the
    'text string.

    Arguments:
        text {str} -- string to center
        width {int} -- widgth of the field in characters

    Returns:
        int -- column offset as an int
    """

    return int((width - len(text)) / 2)


def write_character(char,array,col=0,row=0):
    """ write character to a specific [row][col] in the array """
    try:
        array[row][col] = char
    except IndexError:
        err = f".write_character( ) - IndexError\nTried to assign {char} to [{col}][{row}] in a {len(array)}x{len(array[0])} array."
        logging.warning(err)


def write_to_array(text, array, col=0, row=0, format_text=const.FORMAT_TEXT, format_space=False,
                    fgcolor = None, bgcolor = None, style = None, ):
    """ Writes a string to an array

    Arguments:
        text {str} -- string to wrie to the array
        array {deque} -- 2D array of string characters to write to
        col {int} -- column to offset start of arr1

    Keyword Arguments:
        row {int} -- row to offset start of arr1 (default: {0})
    """

    # get string formatters
    formatted = font.get_formatter(fgcolor, bgcolor, style)
    unformatted = font.get_formatter('RESET', 'RESET', 'RESET_ALL')

    # writing a string to an array
    if isinstance(text, str):
        logging.info('Writing string to screen_buffer...')

        # remove any newline characters from line
        # clean_line = [c for c in text if c != '\n']
        for c, char in enumerate(text):
            if format_text:
                char = f'{formatted["fgcolor"]}{formatted["bgcolor"]}{formatted["style"]}{char}'
            if char == ' ' and not format_space:        #if format_space is False don't add color or style to space characters
                char = f'{unformatted["fgcolor"]}{unformatted["bgcolor"]}{unformatted["style"]}{char}'

            info = f'"{char}" @ col:{col} + {c}, row:{row}'
            logging.info(make_unicode(info))
            write_character(char, array, col = col + c, row = row)
        return array

    # writing an array to an array
    if isinstance(text, deque) or isinstance(text, list):
        logging.info('Writing array to screen_buffer...')
        for r, line in enumerate(text):
            info = f'{line}\n'
            logging.info(make_unicode(info))

            # remove any newline characters from line
            # clean_line = [c for c in line if c != '\n']
            for c, char in enumerate(line):
                if format_text:
                    char = f'{formatted["fgcolor"]}{formatted["bgcolor"]}{formatted["style"]}{char}'
                if char == ' ' and not format_space:
                    char = f'{unformatted["fgcolor"]}{unformatted["bgcolor"]}{unformatted["style"]}{char}'

                info = f'"{char}" @ col:{col} + {c}, row:{row} + {r}'
                logging.info(make_unicode(info))
                write_character(char, array, col = col + c, row = row + r)
        return array
