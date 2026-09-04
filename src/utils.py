"""Utilities"""

from constants import SUPPORTED_PIDS

def is_pid_supported(uevent: str) -> bool:
    """Check if the machine PID is in the supported list

    Args:
        uevent (str): device udev event string

    Returns:
        bool: true if one supported PID is in the udev event, false otherwise
    """
    for pid in SUPPORTED_PIDS:
        if pid in uevent.upper():
            return True

    return False
