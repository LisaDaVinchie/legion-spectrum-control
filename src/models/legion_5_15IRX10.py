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

from .base import Key, KeyboardModel, ZONE_KEYBOARD

_KEYBOARD_KEYS = [
    Key('0',  0x0001, ZONE_KEYBOARD, col=1,  col_span=4, row=1, row_span=1),
    Key('1',  0x0002, ZONE_KEYBOARD, col=6,  col_span=3, row=1, row_span=1),
    Key('2',  0x0003, ZONE_KEYBOARD, col=9,  col_span=4, row=1, row_span=1),
    Key('3',  0x0004, ZONE_KEYBOARD, col=13, col_span=3, row=1, row_span=1),
    Key('4',  0x0005, ZONE_KEYBOARD, col=16, col_span=4, row=1, row_span=1),
    Key('5',  0x0006, ZONE_KEYBOARD, col=21, col_span=3, row=1, row_span=1),
    Key('6',  0x0007, ZONE_KEYBOARD, col=24, col_span=4, row=1, row_span=1),
    Key('7',  0x0008, ZONE_KEYBOARD, col=28, col_span=3, row=1, row_span=1),
    Key('8',  0x0009, ZONE_KEYBOARD, col=31, col_span=4, row=1, row_span=1),
    Key('9',  0x000a, ZONE_KEYBOARD, col=36, col_span=3, row=1, row_span=1),
    Key('10', 0x000b, ZONE_KEYBOARD, col=39, col_span=4, row=1, row_span=1),
    Key('11', 0x000c, ZONE_KEYBOARD, col=43, col_span=3, row=1, row_span=1),
    Key('12', 0x000d, ZONE_KEYBOARD, col=46, col_span=4, row=1, row_span=1),
    Key('13', 0x000e, ZONE_KEYBOARD, col=51, col_span=3, row=1, row_span=1),
    Key('14', 0x000f, ZONE_KEYBOARD, col=54, col_span=3, row=1, row_span=1),
    Key('15', 0x0010, ZONE_KEYBOARD, col=57, col_span=4, row=1, row_span=1),
    Key('16', 0x0011, ZONE_KEYBOARD, col=62, col_span=3, row=1, row_span=1),
    Key('17', 0x0012, ZONE_KEYBOARD, col=65, col_span=3, row=1, row_span=1),
    Key('18', 0x0013, ZONE_KEYBOARD, col=68, col_span=3, row=1, row_span=1),
    Key('19', 0x0014, ZONE_KEYBOARD, col=71, col_span=3, row=1, row_span=1),
    Key('20', 0x0016, ZONE_KEYBOARD, col=1,  col_span=4, row=2, row_span=1),
    Key('21', 0x0017, ZONE_KEYBOARD, col=5,  col_span=4, row=2, row_span=1),
    Key('22', 0x0018, ZONE_KEYBOARD, col=9,  col_span=4, row=2, row_span=1),
    Key('23', 0x0019, ZONE_KEYBOARD, col=13, col_span=4, row=2, row_span=1)
]

# Perimeter accent LEDs. Ordering preserved from the original PERIMETER_KEYS
# list: rear strip (18 LEDs, left-to-right across the back), then side+front
# strip (10 LEDs). Split into named sub-groups matching the web UI's visual
# layout (PERIM_REAR_TOP / PERIM_REAR_BOT / PERIM_FRONT).
_PERIMETER_KEYS = []

_LOGO_KEY = []

_GROUPS = {
    'arrows': ['17', '18', '19'],
    'numpad': ['21', '22', '23']
}

MODEL = KeyboardModel(
    pid='C195',
    display_name='Legion 5 Gen 10 15IRX10',
    keys=_KEYBOARD_KEYS + _PERIMETER_KEYS + _LOGO_KEY,
    groups=_GROUPS,
    grid_cols=24,
    grid_rows=0,
)

ALL_KEY  = 0x0065  # special "all lights" code

ZONES = {
    'keyboard':  [k.code for k in _KEYBOARD_KEYS],
    'perimeter': [],
    'logo':      [],
    'all':       [ALL_KEY],
}
