from effects.builder import (
    build_effect,
    send_effects,
)

from models.legion_pro7_16iax10h import ZONES

from utils.protocol_operations import get_profile
# ---------------------------------------------------------------------------
# Effect types
# ---------------------------------------------------------------------------
EFFECTS = {
    'screw-rainbow': 1,
    'rainbow-wave':  2,
    'color-change':  3,
    'color-pulse':   4,
    'color-wave':    5,
    'smooth':        6,
    'rain':          7,
    'ripple':        8,
    'audio-bounce':  9,
    'audio-ripple':  10,
    'static':        11,
    'type':          12,
}

# Effects that need a speed parameter
EFFECTS_WITH_SPEED = {
    'screw-rainbow', 'rainbow-wave', 'color-change', 'color-pulse',
    'color-wave', 'smooth', 'rain', 'ripple', 'type',
}

# Effects that use direction
EFFECTS_WITH_DIRECTION = {'color-wave', 'rainbow-wave'}

# Effects that use clockwise
EFFECTS_WITH_CLOCKWISE = {'screw-rainbow'}

# Directions
DIRECTIONS = {
    'up':    1,
    'down':  2,
    'right': 3,
    'left':  4,
}

# ---------------------------------------------------------------------------
# High-level commands
# ---------------------------------------------------------------------------
def _resolve_zone_keys(zone_name):
    """Resolve a zone name to a list of keycodes."""
    if zone_name in ZONES:
        return ZONES[zone_name]
    # Allow comma-separated zone names: "keyboard,logo"
    keys = []
    for z in zone_name.split(','):
        z = z.strip()
        if z in ZONES:
            keys.extend(ZONES[z])
        else:
            raise ValueError(f"Unknown zone: {z}. Valid: {', '.join(ZONES.keys())}")
    return keys


def parse_color(s):
    """Parse a color string: 'R,G,B' or '#RRGGBB' or a named color."""
    named = {
        'white':   (255, 255, 255),
        'red':     (255, 0, 0),
        'green':   (0, 255, 0),
        'blue':    (0, 0, 255),
        'cyan':    (0, 255, 255),
        'magenta': (255, 0, 255),
        'yellow':  (255, 255, 0),
        'orange':  (255, 128, 0),
        'purple':  (128, 0, 255),
        'pink':    (255, 64, 128),
        'off':     (0, 0, 0),
        'black':   (0, 0, 0),
    }
    s = s.strip().lower()
    if s in named:
        return named[s]
    if s.startswith('#') and len(s) == 7:
        return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))
    # Bare 6-char hex without # prefix
    if len(s) == 6 and all(c in '0123456789abcdef' for c in s):
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    parts = s.split(',')
    if len(parts) == 3:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    raise ValueError(f"Invalid color: {s}. Use name, R,G,B, or #RRGGBB")


def cmd_preset(dev, name, zones, colors, speed=2, direction=0, clockwise=0):
    """Apply a named effect preset to the given zones."""
    profile = get_profile(dev)

    if name not in EFFECTS:
        raise ValueError(f"Unknown effect: {name}. Valid: {', '.join(EFFECTS.keys())}")
    etype = EFFECTS[name]

    effects = []
    effect_no = 1

    for zone_name in zones:
        keys = _resolve_zone_keys(zone_name)
        zone_colors = colors if colors else []
        # For static with no color specified, default white
        if name == 'static' and not zone_colors:
            zone_colors = [(255, 255, 255)]
        effects.append(build_effect(
            effect_no, etype, zone_colors, keys,
            speed=speed, direction=direction, clockwise=clockwise,
        ))
        effect_no += 1

    send_effects(dev, profile, effects)


def cmd_multi(dev, zone_specs):
    """Apply different effects/colors to different zones at once.
    zone_specs is a list of (zone, effect_name, colors, speed, direction, clockwise).
    """
    profile = get_profile(dev)
    effects = []
    effect_no = 1

    for zone_name, ename, colors, speed, direction, clockwise in zone_specs:
        etype = EFFECTS[ename]
        keys = _resolve_zone_keys(zone_name)
        effects.append(build_effect(
            effect_no, etype, colors, keys,
            speed=speed, direction=direction, clockwise=clockwise,
        ))
        effect_no += 1

    send_effects(dev, profile, effects)


def cmd_keys(dev, key_colors):
    """Set individual keys to specific colors (everything else off).
    key_colors: dict of keycode -> (r, g, b)
    """
    profile = get_profile(dev)
    effects = []
    effect_no = 1

    # Group by color for efficiency
    color_groups = {}
    for kc, color in key_colors.items():
        color_groups.setdefault(color, []).append(kc)

    for color, keycodes in color_groups.items():
        effects.append(build_effect(
            effect_no, EFFECTS['static'], [color], keycodes,
        ))
        effect_no += 1

    send_effects(dev, profile, effects)
