'''Script for testing different parts of the library
This lets you inspect what the response was for a keypress.
Enable/Disable each section as appropriate.
Note: This is _not_ a unit test script.
'''
from blessed import Terminal
from blessed_input import keys

term = Terminal()

def print_(*cmds):
    print(*cmds, end='', flush=True)


with (
    #term.hidden_cursor(),
    term.raw(),
    term.location(),
    term.fullscreen(),
    term.cbreak(),
):
    if False:
        for key in keys.KeyCharacters:
            print_(f'Press key for {key}: ')
            pressed = term.inkey()


            if key.value == pressed:
                print('ok')
            else:
                print(f'Mismatch, "{str(pressed)}" != {str(key.value)}')
            print_(term.move_x(0))

    if False:
        for key in keys.ExtendedKeys:
            print_(f'Press key for {key}: ')
            pressed = term.inkey()

            if key.value == pressed:
                print('ok')
            else:
                print(f'Mismatch, "{str(pressed)}" != {str(key.value)}')
            print_(term.move_x(0))

    if True:
        # sequences
        while True:
            pressed = keys.get_key(term)
            if pressed == [keys.KEY_CTRL, keys.KEY_c]:
                break
            #print_(term.clear)
            if pressed is not None:
                print_(pressed)
            print_(term.move_xy(0, 0))
