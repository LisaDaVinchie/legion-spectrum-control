"""
Legion Pro 7 16IAX10H (83F5) — the laptop this project was originally built
and tested on. USB product ID C197.

RECONCILIATION NOTE:
The original spectrum-ctl.py had two tables that disagreed with each other:
KEY_NAMES (CLI) and KB_KEYS (web UI visualizer). KEY_NAMES contained a
confirmed bug — 'lshift' and 'lctrl' were both mapped to 0x01f5, which is
actually PERIM_FRONT[0] (a perimeter accent LED, not a keyboard key). From
there, KEY_NAMES' bottom-left cluster (fn/win/lalt) and its Z-M row were
shifted by one key relative to KB_KEYS — matching a comment already in
spectrum-web.py: "keycodes shifted 1 position right vs KEY_NAMES".

KB_KEYS is the array that was actually rendered and used against real
hardware (it drives the working per-key visualizer), so it was treated as
the source of truth below. KEY_NAMES was discarded where the two conflicted.

UNCERTAIN — please confirm on real hardware if you get the chance:
  - 'win'   (0x0096, diamond/❖ glyph in the original UI) — guessed name,
            positioned where a Windows/Legion key would sit.
  - 'rctrl' (0x009b, hexagon/⬒ glyph in the original UI) — guessed name,
            positioned where a right-Ctrl or context-menu key would sit.
"""

from .base import Key, KeyboardModel, ZONE_KEYBOARD, ZONE_PERIMETER

_KEYBOARD_KEYS = [
    # --- Row 1: function row ---
    Key('esc',       0x0001, ZONE_KEYBOARD, col=1,  col_span=4, row=1, row_span=1),
    Key('f1',        0x0002, ZONE_KEYBOARD, col=6,  col_span=3, row=1, row_span=1),
    Key('f2',        0x0003, ZONE_KEYBOARD, col=9,  col_span=4, row=1, row_span=1),
    Key('f3',        0x0004, ZONE_KEYBOARD, col=13, col_span=3, row=1, row_span=1),
    Key('f4',        0x0005, ZONE_KEYBOARD, col=16, col_span=4, row=1, row_span=1),
    Key('f5',        0x0006, ZONE_KEYBOARD, col=21, col_span=3, row=1, row_span=1),
    Key('f6',        0x0007, ZONE_KEYBOARD, col=24, col_span=4, row=1, row_span=1),
    Key('f7',        0x0008, ZONE_KEYBOARD, col=28, col_span=3, row=1, row_span=1),
    Key('f8',        0x0009, ZONE_KEYBOARD, col=31, col_span=4, row=1, row_span=1),
    Key('f9',        0x000a, ZONE_KEYBOARD, col=36, col_span=3, row=1, row_span=1),
    Key('f10',       0x000b, ZONE_KEYBOARD, col=39, col_span=4, row=1, row_span=1),
    Key('f11',       0x000c, ZONE_KEYBOARD, col=43, col_span=3, row=1, row_span=1),
    Key('f12',       0x000d, ZONE_KEYBOARD, col=46, col_span=4, row=1, row_span=1),
    Key('insert',    0x000e, ZONE_KEYBOARD, col=51, col_span=3, row=1, row_span=1),
    Key('prtsc',     0x000f, ZONE_KEYBOARD, col=54, col_span=3, row=1, row_span=1),
    Key('delete',    0x0010, ZONE_KEYBOARD, col=57, col_span=4, row=1, row_span=1),
    Key('home',      0x0011, ZONE_KEYBOARD, col=62, col_span=3, row=1, row_span=1),
    Key('end',       0x0012, ZONE_KEYBOARD, col=65, col_span=3, row=1, row_span=1),
    Key('pgup',      0x0013, ZONE_KEYBOARD, col=68, col_span=3, row=1, row_span=1),
    Key('pgdn',      0x0014, ZONE_KEYBOARD, col=71, col_span=3, row=1, row_span=1),

    # --- Row 2: number row ---
    Key('tilde',     0x0016, ZONE_KEYBOARD, col=1,  col_span=4, row=2, row_span=1),
    Key('1',         0x0017, ZONE_KEYBOARD, col=5,  col_span=4, row=2, row_span=1),
    Key('2',         0x0018, ZONE_KEYBOARD, col=9,  col_span=4, row=2, row_span=1),
    Key('3',         0x0019, ZONE_KEYBOARD, col=13, col_span=4, row=2, row_span=1),
    Key('4',         0x001a, ZONE_KEYBOARD, col=17, col_span=4, row=2, row_span=1),
    Key('5',         0x001b, ZONE_KEYBOARD, col=21, col_span=4, row=2, row_span=1),
    Key('6',         0x001c, ZONE_KEYBOARD, col=25, col_span=4, row=2, row_span=1),
    Key('7',         0x001d, ZONE_KEYBOARD, col=29, col_span=4, row=2, row_span=1),
    Key('8',         0x001e, ZONE_KEYBOARD, col=33, col_span=4, row=2, row_span=1),
    Key('9',         0x001f, ZONE_KEYBOARD, col=37, col_span=4, row=2, row_span=1),
    Key('0',         0x0020, ZONE_KEYBOARD, col=41, col_span=4, row=2, row_span=1),
    Key('minus',     0x0021, ZONE_KEYBOARD, col=45, col_span=4, row=2, row_span=1),
    Key('equals',    0x0022, ZONE_KEYBOARD, col=49, col_span=4, row=2, row_span=1),
    Key('backspace', 0x0038, ZONE_KEYBOARD, col=53, col_span=8, row=2, row_span=1),
    Key('numlock',   0x0026, ZONE_KEYBOARD, col=62, col_span=3, row=2, row_span=1),
    Key('numdiv',    0x0027, ZONE_KEYBOARD, col=65, col_span=3, row=2, row_span=1),
    Key('nummul',    0x0028, ZONE_KEYBOARD, col=68, col_span=3, row=2, row_span=1),
    Key('numsub',    0x0029, ZONE_KEYBOARD, col=71, col_span=3, row=2, row_span=1),

    # --- Row 3: QWERTY row ---
    Key('tab',       0x0040, ZONE_KEYBOARD, col=1,  col_span=6, row=3, row_span=1),
    Key('q',         0x0042, ZONE_KEYBOARD, col=7,  col_span=4, row=3, row_span=1),
    Key('w',         0x0043, ZONE_KEYBOARD, col=11, col_span=4, row=3, row_span=1),
    Key('e',         0x0044, ZONE_KEYBOARD, col=15, col_span=4, row=3, row_span=1),
    Key('r',         0x0045, ZONE_KEYBOARD, col=19, col_span=4, row=3, row_span=1),
    Key('t',         0x0046, ZONE_KEYBOARD, col=23, col_span=4, row=3, row_span=1),
    Key('y',         0x0047, ZONE_KEYBOARD, col=27, col_span=4, row=3, row_span=1),
    Key('u',         0x0048, ZONE_KEYBOARD, col=31, col_span=4, row=3, row_span=1),
    Key('i',         0x0049, ZONE_KEYBOARD, col=35, col_span=4, row=3, row_span=1),
    Key('o',         0x004a, ZONE_KEYBOARD, col=39, col_span=4, row=3, row_span=1),
    Key('p',         0x004b, ZONE_KEYBOARD, col=43, col_span=4, row=3, row_span=1),
    Key('lbracket',  0x004c, ZONE_KEYBOARD, col=47, col_span=4, row=3, row_span=1),
    Key('rbracket',  0x004d, ZONE_KEYBOARD, col=51, col_span=4, row=3, row_span=1),
    Key('backslash', 0x004e, ZONE_KEYBOARD, col=55, col_span=6, row=3, row_span=1),
    Key('num7',      0x004f, ZONE_KEYBOARD, col=62, col_span=3, row=3, row_span=1),
    Key('num8',      0x0050, ZONE_KEYBOARD, col=65, col_span=3, row=3, row_span=1),
    Key('num9',      0x0051, ZONE_KEYBOARD, col=68, col_span=3, row=3, row_span=1),
    Key('numadd',    0x0068, ZONE_KEYBOARD, col=71, col_span=3, row=3, row_span=2),

    # --- Row 4: home row ---
    Key('caps',      0x0055, ZONE_KEYBOARD, col=1,  col_span=7, row=4, row_span=1),
    Key('a',         0x006d, ZONE_KEYBOARD, col=8,  col_span=4, row=4, row_span=1),
    Key('s',         0x006e, ZONE_KEYBOARD, col=12, col_span=4, row=4, row_span=1),
    Key('d',         0x0058, ZONE_KEYBOARD, col=16, col_span=4, row=4, row_span=1),
    Key('f',         0x0059, ZONE_KEYBOARD, col=20, col_span=4, row=4, row_span=1),
    Key('g',         0x005a, ZONE_KEYBOARD, col=24, col_span=4, row=4, row_span=1),
    Key('h',         0x0071, ZONE_KEYBOARD, col=28, col_span=4, row=4, row_span=1),
    Key('j',         0x0072, ZONE_KEYBOARD, col=32, col_span=4, row=4, row_span=1),
    Key('k',         0x005b, ZONE_KEYBOARD, col=36, col_span=4, row=4, row_span=1),
    Key('l',         0x005c, ZONE_KEYBOARD, col=40, col_span=4, row=4, row_span=1),
    Key('semicolon', 0x005d, ZONE_KEYBOARD, col=44, col_span=4, row=4, row_span=1),
    Key('quote',     0x005f, ZONE_KEYBOARD, col=48, col_span=4, row=4, row_span=1),
    Key('enter',     0x0077, ZONE_KEYBOARD, col=52, col_span=9, row=4, row_span=1),
    Key('num4',      0x0079, ZONE_KEYBOARD, col=62, col_span=3, row=4, row_span=1),
    Key('num5',      0x007b, ZONE_KEYBOARD, col=65, col_span=3, row=4, row_span=1),
    Key('num6',      0x007c, ZONE_KEYBOARD, col=68, col_span=3, row=4, row_span=1),

    # --- Row 5: shift row ---
    Key('lshift',    0x006a, ZONE_KEYBOARD, col=1,  col_span=9,  row=5, row_span=1),
    Key('z',         0x0082, ZONE_KEYBOARD, col=10, col_span=4,  row=5, row_span=1),
    Key('x',         0x0083, ZONE_KEYBOARD, col=14, col_span=4,  row=5, row_span=1),
    Key('c',         0x006f, ZONE_KEYBOARD, col=18, col_span=4,  row=5, row_span=1),
    Key('v',         0x0070, ZONE_KEYBOARD, col=22, col_span=4,  row=5, row_span=1),
    Key('b',         0x0087, ZONE_KEYBOARD, col=26, col_span=4,  row=5, row_span=1),
    Key('n',         0x0088, ZONE_KEYBOARD, col=30, col_span=4,  row=5, row_span=1),
    Key('m',         0x0073, ZONE_KEYBOARD, col=34, col_span=4,  row=5, row_span=1),
    Key('comma',     0x0074, ZONE_KEYBOARD, col=38, col_span=4,  row=5, row_span=1),
    Key('period',    0x0075, ZONE_KEYBOARD, col=42, col_span=4,  row=5, row_span=1),
    Key('slash',     0x0076, ZONE_KEYBOARD, col=46, col_span=4,  row=5, row_span=1),
    Key('rshift',    0x008d, ZONE_KEYBOARD, col=50, col_span=11, row=5, row_span=1),
    Key('num1',      0x008e, ZONE_KEYBOARD, col=62, col_span=3,  row=5, row_span=1),
    Key('num2',      0x0090, ZONE_KEYBOARD, col=65, col_span=3,  row=5, row_span=1),
    Key('num3',      0x0092, ZONE_KEYBOARD, col=68, col_span=3,  row=5, row_span=1),
    Key('numenter',  0x00a7, ZONE_KEYBOARD, col=71, col_span=3,  row=5, row_span=2),

    # --- Row 6: bottom row ---
    Key('lctrl',     0x007f, ZONE_KEYBOARD, col=1,  col_span=6,  row=6, row_span=1),
    Key('fn',        0x0080, ZONE_KEYBOARD, col=7,  col_span=4,  row=6, row_span=1),
    Key('win',       0x0096, ZONE_KEYBOARD, col=11, col_span=5,  row=6, row_span=1),  # UNCERTAIN, see module docstring
    Key('lalt',      0x0097, ZONE_KEYBOARD, col=16, col_span=5,  row=6, row_span=1),
    Key('space',     0x0098, ZONE_KEYBOARD, col=21, col_span=22, row=6, row_span=1),
    Key('ralt',      0x009a, ZONE_KEYBOARD, col=43, col_span=5,  row=6, row_span=1),
    Key('rctrl',     0x009b, ZONE_KEYBOARD, col=48, col_span=5,  row=6, row_span=1),  # UNCERTAIN, see module docstring
    Key('up',        0x009d, ZONE_KEYBOARD, col=55, col_span=3,  row=6, row_span=1),
    Key('num0',      0x00a3, ZONE_KEYBOARD, col=62, col_span=6,  row=6, row_span=1),
    Key('numdot',    0x00a5, ZONE_KEYBOARD, col=68, col_span=3,  row=6, row_span=1),

    # --- Row 7: arrow cluster ---
    Key('left',      0x009c, ZONE_KEYBOARD, col=52, col_span=3, row=7, row_span=1),
    Key('down',      0x009f, ZONE_KEYBOARD, col=55, col_span=3, row=7, row_span=1),
    Key('right',     0x00a1, ZONE_KEYBOARD, col=58, col_span=3, row=7, row_span=1),
]

# Perimeter accent LEDs. Ordering preserved from the original PERIMETER_KEYS
# list: rear strip (18 LEDs, left-to-right across the back), then side+front
# strip (10 LEDs). Split into named sub-groups matching the web UI's visual
# layout (PERIM_REAR_TOP / PERIM_REAR_BOT / PERIM_FRONT).
_PERIMETER_KEYS = [
    # Rear strip, top half (left-to-right)
    Key('perim_rear_top_1',  0x03e9, ZONE_PERIMETER),
    Key('perim_rear_top_2',  0x03ea, ZONE_PERIMETER),
    Key('perim_rear_top_3',  0x03eb, ZONE_PERIMETER),
    Key('perim_rear_top_4',  0x03ec, ZONE_PERIMETER),
    Key('perim_rear_top_5',  0x03ed, ZONE_PERIMETER),
    Key('perim_rear_top_6',  0x03ee, ZONE_PERIMETER),
    Key('perim_rear_top_7',  0x03ef, ZONE_PERIMETER),
    Key('perim_rear_top_8',  0x03f0, ZONE_PERIMETER),
    Key('perim_rear_top_9',  0x03f1, ZONE_PERIMETER),
    Key('perim_rear_top_10', 0x03f2, ZONE_PERIMETER),
    # Rear strip, bottom half (note: physically reversed order, right-to-left,
    # matching PERIM_REAR_BOT in the original web UI)
    Key('perim_rear_bot_1',  0x03fa, ZONE_PERIMETER),
    Key('perim_rear_bot_2',  0x03f9, ZONE_PERIMETER),
    Key('perim_rear_bot_3',  0x03f8, ZONE_PERIMETER),
    Key('perim_rear_bot_4',  0x03f7, ZONE_PERIMETER),
    Key('perim_rear_bot_5',  0x03f6, ZONE_PERIMETER),
    Key('perim_rear_bot_6',  0x03f5, ZONE_PERIMETER),
    Key('perim_rear_bot_7',  0x03f4, ZONE_PERIMETER),
    Key('perim_rear_bot_8',  0x03f3, ZONE_PERIMETER),
    # Side + front strip (left-to-right)
    Key('perim_front_1',  0x01f5, ZONE_PERIMETER),
    Key('perim_front_2',  0x01f6, ZONE_PERIMETER),
    Key('perim_front_3',  0x01f7, ZONE_PERIMETER),
    Key('perim_front_4',  0x01f8, ZONE_PERIMETER),
    Key('perim_front_5',  0x01f9, ZONE_PERIMETER),
    Key('perim_front_6',  0x01fa, ZONE_PERIMETER),
    Key('perim_front_7',  0x01fb, ZONE_PERIMETER),
    Key('perim_front_8',  0x01fc, ZONE_PERIMETER),
    Key('perim_front_9',  0x01fd, ZONE_PERIMETER),
    Key('perim_front_10', 0x01fe, ZONE_PERIMETER),
]

_LOGO_KEY = [
    # The lid "LEGION" text LED. This zone name is specific to this model —
    # it is not a universal zone every laptop has. The 15IRX10, for
    # instance, has a power-button LED here instead ('power_button'), not
    # a lid logo.
    Key('logo', 0x05DD, 'logo'),
]

_GROUPS = {
    'wasd':   ['w', 'a', 's', 'd'],
    'arrows': ['up', 'down', 'left', 'right'],
    'numpad': [
        'numlock', 'numdiv', 'nummul', 'numsub',
        'num7', 'num8', 'num9', 'numadd',
        'num4', 'num5', 'num6',
        'num1', 'num2', 'num3', 'numenter',
        'num0', 'numdot',
    ],
    'fkeys': ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'],
}

MODEL = KeyboardModel(
    pid='C197',
    display_name='Legion Pro 7 16IAX10H',
    keys=_KEYBOARD_KEYS + _PERIMETER_KEYS + _LOGO_KEY,
    groups=_GROUPS,
    grid_cols=74,
    grid_rows=7,
)

"""Keyboard keys definition for Legion Pro 7 16IAX10H (22x9 Full Spectrum layout)"""

KEYBOARD_KEYS = [
    0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008,
    0x0009, 0x000a, 0x000b, 0x000c, 0x000d, 0x000e, 0x000f, 0x0010,
    0x0011, 0x0012, 0x0013, 0x0014, 0x0016, 0x0017, 0x0018, 0x0019,
    0x001a, 0x001b, 0x001c, 0x001d, 0x001e, 0x001f, 0x0020, 0x0021,
    0x0022, 0x0026, 0x0027, 0x0028, 0x0029, 0x0038, 0x0040, 0x0042,
    0x0043, 0x0044, 0x0045, 0x0046, 0x0047, 0x0048, 0x0049, 0x004a,
    0x004b, 0x004c, 0x004d, 0x004e, 0x004f, 0x0050, 0x0051, 0x0055,
    0x0058, 0x0059, 0x005a, 0x005b, 0x005c, 0x005d, 0x005f, 0x0068,
    0x006a, 0x006d, 0x006e, 0x006f, 0x0070, 0x0071, 0x0072, 0x0073,
    0x0074, 0x0075, 0x0076, 0x0077, 0x0079, 0x007b, 0x007c, 0x007f,
    0x0080, 0x0082, 0x0083, 0x0087, 0x0088, 0x008d, 0x008e, 0x0090,
    0x0092, 0x0096, 0x0097, 0x0098, 0x009a, 0x009b, 0x009c, 0x009d,
    0x009f, 0x00a1, 0x00a3, 0x00a5, 0x00a7,
]

PERIMETER_KEYS = [
    # Rear accent (row 0)
    0x03e9, 0x03ea, 0x03eb, 0x03ec, 0x03ed, 0x03ee, 0x03ef,
    0x03f0, 0x03f1, 0x03f2, 0x03f3, 0x03f4, 0x03f5, 0x03f6,
    0x03f7, 0x03f8, 0x03f9, 0x03fa,
    # Side + front accent
    0x01f5, 0x01f6, 0x01f7, 0x01f8, 0x01f9, 0x01fa,
    0x01fb, 0x01fc, 0x01fd, 0x01fe,
]

LOGO_KEY = 0x05DD
ALL_KEY  = 0x0065  # special "all lights" code

ZONES = {
    'keyboard':  KEYBOARD_KEYS,
    'perimeter': PERIMETER_KEYS,
    'logo':      [LOGO_KEY],
    'all':       [ALL_KEY],
}
