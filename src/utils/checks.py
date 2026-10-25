from utils.protocol_operations import (
    get_brightness,
    get_profile,
    get_logo_status,
    check_compatibility, get_key_count
)

from models.legion_pro7_16iax10h import MODEL

def get_info(dev):
    print(f"Compatible: {check_compatibility(dev)}")
    rows, cols = get_key_count(dev)
    print(f"Layout:     {cols}x{rows}")
    print(f"Brightness: {get_brightness(dev)}/9")
    print(f"Profile:    {get_profile(dev)}")
    print(f"Logo:       {'on' if get_logo_status(dev) else 'off'}")
    print(f"Keyboard:   {len(MODEL.keys_in_zone('keyboard'))} keys")
    print(f"Perimeter:  {len(MODEL.keys_in_zone('perimeter'))} LEDs")

def status(dev):
    b = get_brightness(dev)
    p = get_profile(dev)
    logo = get_logo_status(dev)
    print(f"Brightness: {b}/9")
    print(f"Profile:    {p}")
    print(f"Logo:       {'on' if logo else 'off'}")
