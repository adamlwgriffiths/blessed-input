import sys
from blessed import Terminal, keyboard
from blessed_input import keys

term = Terminal()

def execute(*cmds):
    print(*cmds, end='', flush=True)

def print_(*args):
    execute(*args)
    execute(term.move_down(), term.move_x(0))

def clear():
    execute(term.home, term.clear)

def row(left='', centre='', right=''):
    text = term.center(centre)
    text = left + text[len(left):]
    text = text[:-len(right)] + right
    return text

def top_row(left='', centre='', right=''):
    with term.location(0, 0):
        text = row(left, centre, right)
        execute(term.black_on_darkkhaki(text))

def bottom_row(left='', centre='', right=''):
    with term.location(0, term.height - 1):
        text = row(left, centre, right)
        execute(term.black_on_darkkhaki(text))

def should_quit(keypress):
    return keypress == [keys.KEY_ESCAPE]


with (
    term.raw(),
    term.location(),
    term.fullscreen(),
    term.cbreak(),
):
    clear()
    top_row(' <- Back', 'KBOL', '')
    bottom_row('Footer', '', 'Help (?)')

    execute(term.move_xy(0, 5))

    while True:
        input = keys.get_key(term)
        if   input is None:                 continue
        elif should_quit(input):            break
        elif input == [keys.KEY_LEFT]:      execute(term.move_left())
        elif input == [keys.KEY_RIGHT]:     execute(term.move_right())
        elif input == [keys.KEY_UP]:        execute(term.move_up())
        elif input == [keys.KEY_DOWN]:      execute(term.move_down())
        elif input == [keys.KEY_HOME]:      execute(term.move_x(0))
        elif input == [keys.KEY_END]:       execute(term.move_x(term.width - 1))
        elif input == [keys.KEY_CTRL, keys.KEY_HOME]:   execute(term.move_xy(0, 0))
        elif input == [keys.KEY_CTRL, keys.KEY_END]:    execute(term.move_xy(term.width - 1, term.height - 1))
        else: print_('unknown key')
