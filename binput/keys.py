from enum import Enum, EnumMeta, auto
import re
from blessed.keyboard import Keystroke

# this is a bit of a shit-show
# ncurses/xterm sends absolutely horrible key sequences to us
# there is not always a consistent way to handle this
# some character combinations have had to be manually defined
# and they can actually overlap over combinations, creating spurious
# results

class EnumerationMeta(EnumMeta):
    def __contains__(cls, item):
        # fix inability to see if a value is in an enum
        # ie `"x" in Enum`
        try:
            cls(item)
            return True
        except ValueError:
            return False

    def __getitem__(cls, item):
        _reversed = {v.value:v for k,v in cls.__members__.items()}
        return _reversed[item]

class Enumeration(Enum):
    def __str__(self):
        # don't prepend the classname to enums
        return self.name


class KeyCharacters(Enumeration, metaclass=EnumerationMeta):
    '''Keys that are generally printable characters and are passed to us as such'''

    KEY_A                   = 'A'
    KEY_B                   = 'B'
    KEY_C                   = 'C'
    KEY_D                   = 'D'
    KEY_E                   = 'E'
    KEY_F                   = 'F'
    KEY_G                   = 'G'
    KEY_H                   = 'H'
    KEY_I                   = 'I'
    KEY_J                   = 'J'
    KEY_K                   = 'K'
    KEY_L                   = 'L'
    KEY_M                   = 'M'
    KEY_N                   = 'N'
    KEY_O                   = 'O'
    KEY_P                   = 'P'
    KEY_Q                   = 'Q'
    KEY_R                   = 'R'
    KEY_S                   = 'S'
    KEY_T                   = 'T'
    KEY_U                   = 'U'
    KEY_V                   = 'V'
    KEY_W                   = 'W'
    KEY_X                   = 'X'
    KEY_Y                   = 'Y'
    KEY_Z                   = 'Z'

    KEY_a                   = 'a'
    KEY_b                   = 'b'
    KEY_c                   = 'c'
    KEY_d                   = 'd'
    KEY_e                   = 'e'
    KEY_f                   = 'f'
    KEY_g                   = 'g'
    KEY_h                   = 'h'
    KEY_i                   = 'i'
    KEY_j                   = 'j'
    KEY_k                   = 'k'
    KEY_l                   = 'l'
    KEY_m                   = 'm'
    KEY_n                   = 'n'
    KEY_o                   = 'o'
    KEY_p                   = 'p'
    KEY_q                   = 'q'
    KEY_r                   = 'r'
    KEY_s                   = 's'
    KEY_t                   = 't'
    KEY_u                   = 'u'
    KEY_v                   = 'v'
    KEY_w                   = 'w'
    KEY_x                   = 'x'
    KEY_y                   = 'y'
    KEY_z                   = 'z'

    KEY_TILDE               = '~'
    KEY_0                   = '0'
    KEY_1                   = '1'
    KEY_2                   = '2'
    KEY_3                   = '3'
    KEY_4                   = '4'
    KEY_5                   = '5'
    KEY_6                   = '6'
    KEY_7                   = '7'
    KEY_8                   = '8'
    KEY_9                   = '9'
    KEY_DASH                = '-'
    KEY_EQUALS              = '='

    KEY_COLON               = ':'
    KEY_SEMICOLON           = ';'
    KEY_SINGLEQUOTE         = "'"
    KEY_DOUBLEQUOTE         = '"'

    KEY_COMMA               = ','
    KEY_FULLSTOP            = '.'
    KEY_SLASH               = '/'
    KEY_LEFT_ANGLE_BRACKET  = '<'
    KEY_RIGHT_ANGLE_BRACKET = '>'
    KEY_QUESTIONMARK        = '?'

    KEY_LEFT_BRACKET        = '['
    KEY_RIGHT_BRACKET       = ']'
    KEY_BACKSLASH           = '\\'
    KEY_LEFT_BRACE          = '{'
    KEY_RIGHT_BRACE         = '}'
    KEY_PIPE                = '|'

    KEY_BACKTICK            = '`'
    KEY_EXCLAMATION         = '!'
    KEY_AT                  = '@'
    KEY_HASH                = '#'
    KEY_DOLLAR              = '$'
    KEY_PERCENT             = '%'
    KEY_HAT                 = '^'
    KEY_AMPERSAND           = '&'
    KEY_ASTERISK            = '*'
    KEY_LEFT_PAREN          = '('
    KEY_RIGHT_PAREN         = ')'
    KEY_UNDERSCORE          = '_'
    KEY_PLUS                = '+'

    KEY_SPACE               = ' '
    KEY_ENTER               = '\n' # ENTER in NON term.raw mode
    KEY_TAB                 = '\t'


class ExtendedKeys(Enumeration, metaclass=EnumerationMeta):
    '''Single keys that generate a sequence'''
    # we can derive most of these through our escape sequence calculation
    # but we still need an enum definition somewhere, so these remain
    # despite the redundancy

    KEY_ENTER_              = '\r' # ENTER in term.raw mode

    KEY_ESCAPE              = '\x1b'

    KEY_UP                  = '\x1b[A'
    KEY_DOWN                = '\x1b[B'
    KEY_RIGHT               = '\x1b[C'
    KEY_LEFT                = '\x1b[D'

    KEY_END                 = '\x1b[F'
    KEY_HOME                = '\x1b[H'

    KEY_F1                  = '\x1bOP'
    KEY_F2                  = '\x1bOQ'
    KEY_F3                  = '\x1bOR'
    KEY_F4                  = '\x1bOS'
    KEY_F5                  = '\x1b[15~'
    KEY_F6                  = '\x1b[17~'
    KEY_F7                  = '\x1b[18~'
    KEY_F8                  = '\x1b[19~'
    KEY_F9                  = '\x1b[20~'
    KEY_F10                 = '\x1b[21~'
    KEY_F11                 = '\x1b[23~'
    KEY_F12                 = '\x1b[24~'

    KEY_BACKSPACE           = '\x7f'
    KEY_DELETE              = '\x1b[3~'
    KEY_PAGE_DOWN           = '\x1b[6~'
    KEY_PAGE_UP             = '\x1b[5~'
    KEY_INSERT              = '\x1b[2~'

    KEY_KEYPAD_5            = '\x1b[E'


class Modifiers(Enumeration, metaclass=EnumerationMeta):
    KEY_SHIFT               = 1
    KEY_ALT                 = 2
    KEY_CTRL                = 4
    KEY_META                = 8


for key in KeyCharacters:
    locals()[str(key)] = key
for key in ExtendedKeys:
    locals()[str(key)] = key
for key in Modifiers:
    locals()[str(key)] = key


'''Special mappings which represent multiple keys'''
special_key_mappings = {
    'KEY_CTRL_BACKTICK':       (chr(0), [KEY_CTRL, KEY_BACKTICK]),
    'KEY_CTRL_a':              (chr(1), [KEY_CTRL, KEY_a]),
    'KEY_CTRL_b':              (chr(2), [KEY_CTRL, KEY_b]),
    'KEY_CTRL_c':              (chr(3), [KEY_CTRL, KEY_c]),
    'KEY_CTRL_d':              (chr(4), [KEY_CTRL, KEY_d]),
    'KEY_CTRL_e':              (chr(5), [KEY_CTRL, KEY_e]),
    'KEY_CTRL_f':              (chr(6), [KEY_CTRL, KEY_f]),
    'KEY_CTRL_g':              (chr(7), [KEY_CTRL, KEY_g]),
    'KEY_CTRL_h':              (chr(8), [KEY_CTRL, KEY_h]),
    #'KEY_CTRL_i':              (chr(9), [KEY_CTRL, KEY_i]),  # overlaps with TAB
    #'KEY_CTRL_j':              (chr(10), [KEY_CTRL, KEY_j]), # overlaps with ENTER
    'KEY_CTRL_k':              (chr(11), [KEY_CTRL, KEY_k]),
    'KEY_CTRL_l':              (chr(12), [KEY_CTRL, KEY_l]),
    #'KEY_CTRL_m':              (chr(13), [KEY_CTRL, KEY_m]), # overlaps with ENTER in term.raw mode
    'KEY_CTRL_n':              (chr(14), [KEY_CTRL, KEY_n]),
    'KEY_CTRL_o':              (chr(15), [KEY_CTRL, KEY_o]),
    'KEY_CTRL_p':              (chr(16), [KEY_CTRL, KEY_p]),
    'KEY_CTRL_q':              (chr(17), [KEY_CTRL, KEY_q]),
    'KEY_CTRL_r':              (chr(18), [KEY_CTRL, KEY_r]),
    'KEY_CTRL_s':              (chr(19), [KEY_CTRL, KEY_s]),
    'KEY_CTRL_t':              (chr(20), [KEY_CTRL, KEY_t]),
    'KEY_CTRL_u':              (chr(21), [KEY_CTRL, KEY_u]),
    'KEY_CTRL_v':              (chr(22), [KEY_CTRL, KEY_v]),
    'KEY_CTRL_w':              (chr(23), [KEY_CTRL, KEY_w]),
    'KEY_CTRL_x':              (chr(24), [KEY_CTRL, KEY_x]),
    'KEY_CTRL_y':              (chr(25), [KEY_CTRL, KEY_y]),
    'KEY_CTRL_z':              (chr(26), [KEY_CTRL, KEY_z]),
    #'KEY_CTRL_LEFT_BRACKET':   (chr(27), [KEY_CTRL, KEY_LEFT_BRACKET]), # overlaps with escape
    'KEY_CTRL_BACKSLASH':      (chr(28), [KEY_CTRL, KEY_BACKSLASH]),
    'KEY_CTRL_RIGHT_BRACKET':  (chr(29), [KEY_CTRL, KEY_RIGHT_BRACKET]),
    'KEY_CTRL_SLASH':          (chr(31), [KEY_CTRL, KEY_SLASH]),
    'KEY_CTRL_DOUBLEQUOTE':    (chr(39), [KEY_CTRL, KEY_DOUBLEQUOTE]),
    'KEY_CTRL_COMMA':          (chr(44), [KEY_CTRL, KEY_COMMA]),
    'KEY_CTRL_FULLSTOP':       (chr(46), [KEY_CTRL, KEY_FULLSTOP]),
    'KEY_CTRL_SEMICOLON':      (chr(59), [KEY_CTRL, KEY_SEMICOLON]),
    'KEY_SHIFT_TAB':           ('\x1b[Z', [KEY_SHIFT, KEY_TAB]),
}

SpecialMappings = Enumeration('SpecialMappings', special_key_mappings)


def sequence_to_keys(keystrokes):
    '''Given a sequence, return the keys that were pressed
    '''
    def has_bit_mask(value, mask):
        return value & mask == mask
    def convert_modifiers(mod):
        mod -= 1
        modifiers = []
        if has_bit_mask(mod, KEY_META.value):   modifiers += [KEY_SHIFT]
        if has_bit_mask(mod, KEY_CTRL.value):   modifiers += [KEY_CTRL]
        if has_bit_mask(mod, KEY_ALT.value):    modifiers += [KEY_ALT]
        if has_bit_mask(mod, KEY_SHIFT.value):  modifiers += [KEY_SHIFT]
        return modifiers
    def key_lookup(key):
        if   key == 'A':    return KEY_UP
        elif key == 'B':    return KEY_DOWN
        elif key == 'C':    return KEY_RIGHT
        elif key == 'D':    return KEY_LEFT
        elif key == 'H':    return KEY_HOME
        elif key == 'F':    return KEY_END
        elif key == 'OP':   return KEY_F1
        elif key == 'OQ':   return KEY_F2
        elif key == 'OR':   return KEY_F3
        elif key == 'OS':   return KEY_F4
        elif key == 'P':    return KEY_F1
        elif key == 'Q':    return KEY_F2
        elif key == 'R':    return KEY_F3
        elif key == 'S':    return KEY_F4
        elif key == '1':    return KEY_HOME
        elif key == '2':    return KEY_INSERT
        elif key == '3':    return KEY_DELETE
        elif key == '4':    return KEY_END
        elif key == '5':    return KEY_PAGE_UP
        elif key == '6':    return KEY_PAGE_DOWN
        elif key == '7':    return KEY_HOME # dupe
        elif key == '8':    return KEY_END # dupe
        elif key == '11':   return KEY_F1 # dupe
        elif key == '12':   return KEY_F2 # dupe
        elif key == '13':   return KEY_F3 # dupe
        elif key == '14':   return KEY_F4 # dupe
        elif key == '15':   return KEY_F5
        elif key == '17':   return KEY_F6
        elif key == '18':   return KEY_F7
        elif key == '19':   return KEY_F8
        elif key == '20':   return KEY_F9
        elif key == '21':   return KEY_F10
        elif key == '23':   return KEY_F11
        elif key == '24':   return KEY_F12
    def keycharacters_lookup(key):
        if key in KeyCharacters:
            return KeyCharacters[key]

    # <char>                                         -> char
    # <esc> <nochar>                                 -> esc
    # <esc> <esc>                                    -> esc
    # <esc> <char>                                   -> Alt-keypress or keycode sequence
    # <esc> '[' <nochar>                             -> Alt-[
    # <esc> '[' (<modifier>) <char>                  -> keycode sequence, <modifier> is a decimal number and defaults to 1 (xterm)
    # <esc> '[' (<keycode>) (';'<modifier>) '~'      -> keycode sequence, <keycode> and <modifier> are decimal numbers and default to 1 (vt)


    # \x1b[1;{mod+}{key+}
    # eg \x1b[1;2P = SHIFT + F1
    if match := re.match(r'\x1b\[1;(?P<mod>\d+)(?P<key>[^~]+)$', keystrokes):
        return convert_modifiers(int(match['mod'])) + [key_lookup(match['key'])]
    # \x1b[{key+};{mod+}~
    # \x1b[15;2~ = SHIFT + F5
    elif match := re.match(r'\x1b\[(?P<key>\d+);(?P<mod>\d+)~$', keystrokes):
        return convert_modifiers(int(match['mod'])) + [key_lookup(match['key'])]
    # \x1b[{mod+}{key+}
    # eg ??
    elif match := re.match(r'\x1b\[(?P<mod>\d+)(?P<key>[^~]+)$', keystrokes):
        return convert_modifiers(int(match['mod'])) + [key_lookup(match['key'])]
    # \x1b[{key+}~
    # eg \x1b[15~ = F5
    elif match := re.match(r'\x1b\[(?P<key>.+)~$', keystrokes):
        key = key_lookup(match['key'])
        if key:
            return [key]
        return [KEY_ALT, keycharacters_lookup(match['key'])]
    # \x1b[{key+}
    elif match := re.match(r'\x1b\[\[(?P<key>[^~]+)$', keystrokes):
        key = key_lookup(match['key'])
        if key:
            return [key]
        return [KEY_ALT, keycharacters_lookup(match['key'])]
    # \x1b[{key+}
    # eg \x1b[D = LEFT
    # eg \x1b[[ = ALT + [
    # eg \x1b[ = CTRL + [
    elif match := re.match(r'\x1b\[(?P<key>[^~]+)$', keystrokes):
        key = key_lookup(match['key'])
        if key:
            return [key]
        return [KEY_ALT, keycharacters_lookup(match['key'])]
    # \x1b{key+}
    # eg \x1bOP = F1
    # eg \x1b] = CTRL + ]
    elif match := re.match(r'\x1b(?P<key>[^~\[]+)$', keystrokes):
        key = key_lookup(match['key'])
        if key:
            return [key]
        key = keycharacters_lookup(match['key'])
        # if its a letter, lowercase indicates ALT, uppercase indicates CTRL
        # otherwise its CTRL
        if key.value.isalpha():
            meta = KEY_ALT
            if key.value.isupper():
                meta = KEY_CTRL
        else:
            meta = KEY_CTRL
        return [meta, key]
    # \x1b
    elif '\x1b' == keystrokes:
        return [KEY_ESCAPE]


def receive_sequence(term, first_key):
    keys = [first_key]
    while next_key := term.inkey(timeout=0, esc_delay=0):
        keys += [next_key]
    return keys

def convert_keys(keys):
    for special_key in SpecialMappings:
        if keys == special_key.value[0]:
            return special_key.value[1]
    if keys in ExtendedKeys:
        return [ExtendedKeys[keys]]
    if keys in KeyCharacters:
        return [KeyCharacters[keys]]
    # escape often preceeds a sequence
    if str(keys).startswith(KEY_ESCAPE.value):
        return sequence_to_keys(keys)

def get_key(term, timeout=None):
    key = term.inkey(timeout=timeout, esc_delay=0.1)
    if key is None: return None

    # escape often preceeds a sequence
    if str(key).startswith(KEY_ESCAPE.value):
        key = receive_sequence(term, key)
        key = ''.join(key)

    return convert_keys(key)




STOP_ON_FAIL = True

def test_sequence(input, expected):
    result = convert_keys(input)
    if result != expected:
        print(f'"{input[1:]}" expected {expected}, got {result} instead')
        return False
    return True

results = [
    test_sequence('[',            [KEY_LEFT_BRACKET]),
    test_sequence('a',            [KEY_a]),
    #test_sequence('\x1b[a',       [KEY_ALT, KEY_a]),
    #test_sequence('\x1b[A',       [KEY_CTRL, KEY_a]),
    test_sequence('A',            [KEY_A]),
    test_sequence('\n',           [KEY_ENTER]),
    test_sequence('\r',           [KEY_ENTER_]),
    test_sequence('\t',           [KEY_TAB]),
    test_sequence('\x1b[Z',       [KEY_SHIFT, KEY_TAB]),
    test_sequence('\x1b[E',       [KEY_KEYPAD_5]),
    #test_sequence('\x1b[',        [KEY_CTRL, KEY_LEFT_BRACKET]), #ignored, this is the same as escape
    test_sequence('\x1b]',        [KEY_CTRL, KEY_RIGHT_BRACKET]),
    test_sequence('\x1b[[',       [KEY_ALT, KEY_LEFT_BRACKET]),
    test_sequence('\x1b[]',       [KEY_ALT, KEY_RIGHT_BRACKET]),
    test_sequence('\x1b[_',       [KEY_ALT, KEY_UNDERSCORE]),
    test_sequence('\x1b[/',       [KEY_ALT, KEY_SLASH]),
    test_sequence('\x1b',         [KEY_ESCAPE]),
    test_sequence('\x1b[A',       [KEY_UP]),
    test_sequence('\x1b[1;3A',    [KEY_ALT, KEY_UP]),
    test_sequence('\x1b[1;5A',    [KEY_CTRL, KEY_UP]),
    test_sequence('\x1b[B',       [KEY_DOWN]),
    test_sequence('\x1b[1;3B',    [KEY_ALT, KEY_DOWN]),
    test_sequence('\x1b[1;5B',    [KEY_CTRL, KEY_DOWN]),
    test_sequence('\x1b[C',       [KEY_RIGHT]),
    test_sequence('\x1b[1;3C',    [KEY_ALT, KEY_RIGHT]),
    test_sequence('\x1b[1;5C',    [KEY_CTRL, KEY_RIGHT]),
    test_sequence('\x1b[D',       [KEY_LEFT]),
    test_sequence('\x1b[1;3D',    [KEY_ALT, KEY_LEFT]),
    test_sequence('\x1b[1;5D',    [KEY_CTRL, KEY_LEFT]),
    test_sequence('\x1b[F',       [KEY_END]),
    test_sequence('\x1b[1;3F',    [KEY_ALT, KEY_END]),
    test_sequence('\x1b[H',       [KEY_HOME]),
    test_sequence('\x1b[1;3H',    [KEY_ALT, KEY_HOME]),
    test_sequence('\x1b[1;5H',    [KEY_CTRL, KEY_HOME]),
    test_sequence('\x1bOP',       [KEY_F1]),
    test_sequence('\x1bOQ',       [KEY_F2]),
    test_sequence('\x1bOR',       [KEY_F3]),
    test_sequence('\x1bOS',       [KEY_F4]),
    test_sequence('\x1b[15~',     [KEY_F5]),
    test_sequence('\x1b[17~',     [KEY_F6]),
    test_sequence('\x1b[18~',     [KEY_F7]),
    test_sequence('\x1b[19~',     [KEY_F8]),
    test_sequence('\x1b[20~',     [KEY_F9]),
    test_sequence('\x1b[21~',     [KEY_F10]),
    test_sequence('\x1b[23~',     [KEY_F11]),
    test_sequence('\x1b[24~',     [KEY_F12]),
    test_sequence('\x7f',         [KEY_BACKSPACE]),
    test_sequence('\x1b[3~',      [KEY_DELETE]),
    test_sequence('\x1b[3;5~',    [KEY_CTRL, KEY_DELETE]),
    test_sequence('\x1b[6~',      [KEY_PAGE_DOWN]),
    test_sequence('\x1b[6;3~',    [KEY_ALT, KEY_PAGE_DOWN]),
    test_sequence('\x1b[5~',      [KEY_PAGE_UP]),
    test_sequence('\x1b[5;3~',    [KEY_ALT, KEY_PAGE_UP]),
    test_sequence('\x1b[2~',      [KEY_INSERT]),
    test_sequence('\x1b[2;3~',    [KEY_ALT, KEY_INSERT]),
]


for mod_keys, mod_value in [
    ([KEY_SHIFT],            '2'),
    ([KEY_ALT],              '3'),
    ([KEY_ALT, KEY_SHIFT],   '4'),
    ([KEY_CTRL],             '5'),
    ([KEY_CTRL, KEY_SHIFT],  '6'),
    ([KEY_CTRL, KEY_ALT, KEY_SHIFT],  '8'),
]:
    for f_string, f_keys in [
        ('\x1b[1;{}P', [KEY_F1]),
        ('\x1b[1;{}Q', [KEY_F2]),
        ('\x1b[1;{}R', [KEY_F3]),
        ('\x1b[1;{}S', [KEY_F4]),
        ('\x1b[15;{}~', [KEY_F5]),
        ('\x1b[17;{}~', [KEY_F6]),
        ('\x1b[18;{}~', [KEY_F7]),
        ('\x1b[19;{}~', [KEY_F8]),
        ('\x1b[20;{}~', [KEY_F9]),
        ('\x1b[21;{}~', [KEY_F10]),
        ('\x1b[23;{}~', [KEY_F11]),
        ('\x1b[24;{}~', [KEY_F12]),
    ]:
        sequence = f_string.format(mod_value)
        keys = mod_keys + f_keys

        results.append(test_sequence(sequence, keys))

if STOP_ON_FAIL:
    if not all(results):
        exit()
