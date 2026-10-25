from utils.hid_helpers import (
    make_request, set_feature,
    get_feature, REPORT_SIZE
)

# ---------------------------------------------------------------------------
# Spectrum protocol operation types
# ---------------------------------------------------------------------------
OP_COMPATIBILITY    = 0xD1
OP_KEY_COUNT        = 0xC4
OP_KEY_PAGE         = 0xC5
OP_PROFILE_CHANGE   = 0xC8
OP_PROFILE_DEFAULT  = 0xC9
OP_PROFILE          = 0xCA
OP_EFFECT_CHANGE    = 0xCB
OP_EFFECT           = 0xCC
OP_GET_BRIGHTNESS   = 0xCD
OP_BRIGHTNESS       = 0xCE
OP_AURORA_START_STOP = 0xD0
OP_AURORA_SEND_BITMAP = 0xA1
OP_GET_LOGO_STATUS  = 0xA5
OP_LOGO_STATUS      = 0xA6

# ---------------------------------------------------------------------------
# Protocol operations
# ---------------------------------------------------------------------------
def get_brightness(dev):
    set_feature(dev, make_request(OP_GET_BRIGHTNESS))
    return get_feature(dev)[4]


def set_brightness(dev, level):
    set_feature(dev, make_request(OP_BRIGHTNESS, bytes([max(0, min(9, level))])))


def get_profile(dev):
    set_feature(dev, make_request(OP_PROFILE))
    return get_feature(dev)[4]


def set_profile(dev, profile):
    set_feature(dev, make_request(OP_PROFILE_CHANGE, bytes([max(0, min(6, profile))])))


def set_profile_default(dev, profile):
    set_feature(dev, make_request(OP_PROFILE_DEFAULT, bytes([max(0, min(6, profile))])))


def get_logo_status(dev):
    set_feature(dev, make_request(OP_GET_LOGO_STATUS))
    return get_feature(dev)[4] == 1


def set_logo_status(dev, on):
    set_feature(dev, make_request(OP_LOGO_STATUS, bytes([1 if on else 0])))


def check_compatibility(dev):
    set_feature(dev, make_request(OP_COMPATIBILITY))
    return get_feature(dev)[4] == 0


def get_key_count(dev):
    set_feature(dev, make_request(OP_KEY_COUNT, bytes([0x07])))
    resp = get_feature(dev)
    return resp[5], resp[6]  # rows, cols


def get_current_state(dev):
    """Read per-key RGB state from the device."""
    resp = get_feature(dev)
    # Response is packed LENOVO_SPECTRUM_KEY_STATE entries: u16 keycode, u8 r, g, b
    keys = {}
    offset = 4  # skip header
    while offset + 4 < REPORT_SIZE:
        kc = resp[offset] | (resp[offset+1] << 8)
        if kc == 0:
            break
        r, g, b = resp[offset+2], resp[offset+3], resp[offset+4]
        keys[kc] = (r, g, b)
        offset += 5
    return keys
