from utils.protocol_operations import (
    get_brightness, set_brightness, set_logo_status,
)
from utils.cli_helpers import open_device
from effects.commands import cmd_multi

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def white():
    dev = open_device()
    cmd_multi(dev, [
            ('keyboard', 'static', [WHITE], 0, 0, 0),
            ('perimeter', 'static', [BLACK], 0, 0, 0),
            ('logo', 'static', [BLACK], 0, 0, 0),
        ])
        # Make sure brightness is up
    if get_brightness(dev) == 0:
        set_brightness(dev, 3)
    print("White keyboard, perimeter off")
    dev.close()

def rgb():
    dev = open_device()
    cmd_multi(dev, [
            ('keyboard', 'rainbow-wave', [], 2, 4, 0),
            ('perimeter', 'rainbow-wave', [], 2, 4, 0),
            ('logo', 'color-pulse', [(128, 0, 255), (0, 128, 255)], 2, 0, 0),
        ])
    set_logo_status(dev, True)
    if get_brightness(dev) == 0:
        set_brightness(dev, 3)
    print("Rainbow wave on all zones")
    dev.close()

def stealth():
    dev = open_device()
    cmd_multi(dev, [
            ('keyboard', 'static', [BLACK], 0, 0, 0),
            ('perimeter', 'static', [BLACK], 0, 0, 0),
            ('logo', 'static', [BLACK], 0, 0, 0),
        ])
    set_brightness(dev, 0)
    set_logo_status(dev, False)
    print("All lights off")
    dev.close()
