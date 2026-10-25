import sys

from models.legion_pro7_16iax10h import MODEL
from models import get_model_for_detected_pid
from utils.hid_helpers import find_spectrum_device

keyboard_model = get_model_for_detected_pid('C197')
KEY_NAMES = keyboard_model.by_code
KEY_GROUPS = MODEL.zones


def resolve_key(name):
    """Resolve a key name/hex/group to a list of keycodes."""
    name = name.lower().strip()
    if name in KEY_GROUPS:
        return [KEY_NAMES[k] for k in KEY_GROUPS[name]]
    if name in KEY_NAMES:
        return [KEY_NAMES[name]]
    if name.startswith('0x'):
        return [int(name, 16)]
    raise ValueError(f"Unknown key: {name}. Use 'keymap' to see available names.")


def open_device():
    devpath = find_spectrum_device()
    if not devpath:
        print("ERROR: Spectrum device not found (048d:c197)")
        sys.exit(1)
    return open(devpath, 'rb+', buffering=0)
