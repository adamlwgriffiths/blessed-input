# Blessed Input

_A terminal input sanitiser_

This is a small module which attempts to provide a sane method of determining
what keys have been pressed, in order to enable more complicated input handling.
Ie, Ctrl, Alt, Shift, Meta, F-key combinations.

*Without blessed-input*
```
# Ctrl + Down Arrow
if key == '\x1b[1;5B':
    move_cursor_y(1)
# Ctrl + HOME
if key == '\x1b[1;5H':
    set_cursor_x(0)
```

*With blessed-input*
```
if key == [KEY_CTRL, KEY_DOWN]:
    move_cursor_y(1)
if key == [KEY_CTRL, KEY_HOME]:
    set_cursor_x(0)
```


Normally when a key is pressed in blessed/ncurses, it's either a character, or
a series of terminal escape sequences, or a legacy mapping.

This can be incredibly unhelpful when you're trying to write simple code that
just wants to perform an action on a key combination.

With this module, when an input is pressed, you instead get a a list of the keys
that were part of that event.


## Usage

As a `blessed.inkey` replacement:
```
from blessed_input import get_key

...

pressed = keys.get_key(term)
print(pressed)
```

This function attempts to detect key sequences, and will receive
further key events if this is the case using `receive_sequence`.
It then sends the key press 'string' input to `convert_keys`
for conversion to a list of key presses.

Key sequences are always in the order:
`[ KEY_META, KEY_CTRL, KEY_ALT, KEY_SHIFT, <key> ]`

This should make matching patterns easier, as you don't need to look inside the list of each key, you just provide the sequence of keys you want in the above order.

For best compatibility, set your application to use `term.raw()` and `term.cbreak()`.

To get the 'text' version of a key, simply call `key.value` (as they are an enumeration).

Note: that upper and lower-case keys are considered different characters.
So for standard characters, you should _not_ include the KEY_SHIFT in the combination.

Ie.
`KEY_A                   = 'A'`
`KEY_a                   = 'a'`

It should be noted that the meta keys will print the terminal key sequence.

Ie. `KEY_ESCAPE              = '\x1b'`

Function-keys + Meta are converted properly.
Ie. you won't get F-24 being pressed, you'll get F1-F12 with the appropriate META key.

## Demos

See demo.py for an example of a "Text Editor-like" application.

See debug_keys.py for an example of receiving key-events and printing out the key combinations.

## Manual conversion

If you want to convert a key you've received from blessed/ncurses,
refer to the `get_key` implementation.

## Caveats

The different ncurses modes act differently and have different reserved
key-combinations. YMMV.

I've tried to parse every key combination I could get working (Ctrl, Alt, Shift, Meta, F-keys).
I believe I got all the ones I can get working, to work.

Terminals don't let you use some key sequences, as they are internal.
Eg. Ctrl+s turns on scroll-lock and cannot be used for "Save".

Known reserved key combinations that cannot be handled:

* CTRL + i = TAB
* CTRL + j = ENTER in non-"raw" mode
* CTRL + m = ENTER in "raw" mode
* CTRL + [ = ESCAPE

There are most likely others (CTRL+z, CTRL+s).

## Opinion

Having to write this code demonstrated that it is _impossible_ to use a standard
Unix terminal to write any sort of rich-input based application.

The difficulty in just getting a sane list of key events is just excessive.
And the terminal's reserved key combinations occupy common industry established
key-combinations.

This is a deal-breaker.

Use something native or make something in an embeddable webapp (webpy, etc),
and make it act like a terminal.
