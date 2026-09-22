import os
import glob
import fcntl
import array

from src.constants import SUPPORTED_PIDS

REPORT_SIZE = 960
HIDIOCSFEATURE = lambda size: 0xC0004806 | (size << 16)
HIDIOCGFEATURE = lambda size: 0xC0004807 | (size << 16)

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

def find_spectrum_device():
    """Find hidraw for 048d:c197 (ITE 8258) — the Spectrum protocol responder."""
    for hidraw in sorted(glob.glob('/sys/class/hidraw/hidraw*')):
        name = os.path.basename(hidraw)
        try:
            with open(f'{hidraw}/device/uevent') as f:
                uevent = f.read()
            if '048D' not in uevent.upper():
                continue

            if not is_pid_supported(uevent):
                continue

            with open(f'{hidraw}/device/report_descriptor', 'rb') as f:
                desc = f.read()
            if b'\x06\x89\xff' in desc:
                return f'/dev/{name}'
        except (IOError, OSError):
            continue
    return None


def set_feature(dev, data):
    buf = array.array('B', data[:REPORT_SIZE].ljust(REPORT_SIZE, b'\x00'))
    fcntl.ioctl(dev, HIDIOCSFEATURE(REPORT_SIZE), buf)


def get_feature(dev, report_id=0x07):
    buf = array.array('B', [report_id] + [0] * (REPORT_SIZE - 1))
    fcntl.ioctl(dev, HIDIOCGFEATURE(REPORT_SIZE), buf)
    return bytes(buf)


def make_header(op_type, size=0xC0):
    return bytes([0x07, op_type, size & 0xFF, 0x03])


def make_request(op_type, payload=b'', size=0xC0):
    return (make_header(op_type, size) + payload).ljust(REPORT_SIZE, b'\x00')