import struct

from utils.hid_helpers import (
    make_header,
    set_feature
)

from utils.protocol_operations import OP_EFFECT_CHANGE

# ---------------------------------------------------------------------------
# Effect builder
# ---------------------------------------------------------------------------
def _build_effect_header(effect_type, speed=0, direction=0, clockwise=0, color_mode=2):
    return bytes([
        0x06, 0x01, effect_type,
        0x02, speed,
        0x03, clockwise,
        0x04, direction,
        0x05, color_mode,
        0x06, 0x00,
    ])


def build_effect(effect_no, effect_type, colors, keycodes,
                 speed=0, direction=0, clockwise=0):
    """Build a single effect binary blob."""
    color_mode = 0x02 if colors else (0x01 if effect_type != 11 else 0x00)
    header = _build_effect_header(effect_type, speed, direction, clockwise, color_mode)

    data = bytes([effect_no])
    data += header
    data += bytes([len(colors)])
    for r, g, b in colors:
        data += bytes([r, g, b])
    data += bytes([len(keycodes)])
    for kc in keycodes:
        data += struct.pack('<H', kc)
    return data


def send_effects(dev, profile, effects_data):
    """Send a full effect description to the device.
    effects_data is a list of bytes blobs from build_effect().
    """
    payload = bytes([profile, 0x01, 0x01])
    for e in effects_data:
        payload += e
    data = make_header(OP_EFFECT_CHANGE) + payload
    set_feature(dev, data)
