#!/usr/bin/env python3
"""
Web UI for Lenovo Legion Gen 10 Spectrum Lighting Controller.
Run with: sudo python3 spectrum-web.py
Then open http://localhost:5555
"""

import http.server
import json
import subprocess
import sys
import os
import struct
import array
import fcntl
import threading
from pathlib import Path

from utils.hid_helpers import find_spectrum_device

PORT = 5555
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spectrum-ctl.py')

# ---------------------------------------------------------------------------
# Inline HID helpers for fast preview (no subprocess spawn)
# ---------------------------------------------------------------------------
HIDIOCSFEATURE = lambda size: 0xC0004806 | (size << 16)
REPORT_SIZE = 960
OP_EFFECT_CHANGE = 0xCB
OP_PROFILE = 0xCA

_hid_lock = threading.Lock()
hid_path = None

HTML_PATH = Path("src/pages/index.html").resolve().absolute()



def _find_spectrum_hid(hid_path = None):
    if hid_path is not None:
        return hid_path
    return find_spectrum_device()

def _hid_set_feature(fd, data):
    buf = array.array('B', data[:REPORT_SIZE].ljust(REPORT_SIZE, b'\x00'))
    fcntl.ioctl(fd, HIDIOCSFEATURE(REPORT_SIZE), buf)

def _hid_get_feature(fd, report_id=0x07):
    buf = array.array('B', [report_id] + [0] * (REPORT_SIZE - 1))
    fcntl.ioctl(fd, 0xC0004807 | (REPORT_SIZE << 16), buf)
    return bytes(buf)

OP_GET_BRIGHTNESS = 0xCD
OP_BRIGHTNESS = 0xCE

def _send_keys_fast(key_color_map):
    """Send per-key static colors directly to HID — no subprocess.
    Opens and closes the device each time (same as CLI) for reliability."""
    with _hid_lock:
        path = _find_spectrum_hid(hid_path)
        if not path:
            return False
        dev = open(path, 'rb+', buffering=0)
        try:
            # Get profile
            _hid_set_feature(dev, bytes([0x07, OP_PROFILE, 0xC0, 0x03]).ljust(REPORT_SIZE, b'\x00'))
            profile = _hid_get_feature(dev)[4]

            # Check brightness — bump to 3 if off (same as CLI)
            _hid_set_feature(dev, bytes([0x07, OP_GET_BRIGHTNESS, 0xC0, 0x03]).ljust(REPORT_SIZE, b'\x00'))
            brightness = _hid_get_feature(dev)[4]
            if brightness == 0:
                _hid_set_feature(dev, bytes([0x07, OP_BRIGHTNESS, 0xC0, 0x03, 3]).ljust(REPORT_SIZE, b'\x00'))

            # Group by color
            color_groups = {}
            for code, (r, g, b) in key_color_map.items():
                color_groups.setdefault((r, g, b), []).append(code)

            # Build effects
            effects = b''
            eno = 1
            for (r, g, b), codes in color_groups.items():
                color_mode = 0x02
                ehdr = bytes([eno, 0x06, 0x01, 11, 0x02, 0, 0x03, 0, 0x04, 0, 0x05, color_mode, 0x06, 0x00])
                ehdr += bytes([1, r, g, b])
                ehdr += bytes([len(codes)])
                for c in codes:
                    ehdr += struct.pack('<H', c)
                effects += ehdr
                eno += 1

            payload = bytes([profile, 0x01, 0x01]) + effects
            data = bytes([0x07, OP_EFFECT_CHANGE, 0xC0, 0x03]) + payload
            _hid_set_feature(dev, data)
            return True
        finally:
            dev.close()

# Effect types for per-key effects
EFFECT_TYPES = {
    'static': 11, 'type': 12, 'rain': 7, 'ripple': 8,
    'color-pulse': 4, 'color-wave': 5, 'rainbow-wave': 2,
    'smooth': 6, 'screw-rainbow': 1, 'color-change': 3,
}

def _send_effect_groups(groups):
    """Send multiple effect groups to HID. Each group: (effect_name, speed, colors, keycodes)."""
    with _hid_lock:
        path = _find_spectrum_hid(hid_path)
        if not path:
            return False
        dev = open(path, 'rb+', buffering=0)
        try:
            _hid_set_feature(dev, bytes([0x07, OP_PROFILE, 0xC0, 0x03]).ljust(REPORT_SIZE, b'\x00'))
            profile = _hid_get_feature(dev)[4]
            _hid_set_feature(dev, bytes([0x07, OP_GET_BRIGHTNESS, 0xC0, 0x03]).ljust(REPORT_SIZE, b'\x00'))
            if _hid_get_feature(dev)[4] == 0:
                _hid_set_feature(dev, bytes([0x07, OP_BRIGHTNESS, 0xC0, 0x03, 3]).ljust(REPORT_SIZE, b'\x00'))

            effects = b''
            eno = 1
            for etype_name, speed, colors, codes in groups:
                etype = EFFECT_TYPES.get(etype_name, 11)
                color_mode = 0x02 if colors else 0x01
                ehdr = bytes([eno, 0x06, 0x01, etype, 0x02, speed, 0x03, 0, 0x04, 0, 0x05, color_mode, 0x06, 0x00])
                ehdr += bytes([len(colors)])
                for r, g, b in colors:
                    ehdr += bytes([r, g, b])
                ehdr += bytes([len(codes)])
                for c in codes:
                    ehdr += struct.pack('<H', c)
                effects += ehdr
                eno += 1

            payload = bytes([profile, 0x01, 0x01]) + effects
            data = bytes([0x07, OP_EFFECT_CHANGE, 0xC0, 0x03]) + payload
            _hid_set_feature(dev, data)
            return True
        finally:
            dev.close()



SYSFS_LEDS = {
    'ylogo': '/sys/class/leds/platform::ylogo/brightness',
    'ioport': '/sys/class/leds/platform::ioport/brightness',
    'kbd_backlight': '/sys/class/leds/platform::kbd_backlight/brightness',
}

def read_sysfs(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except Exception:
        return None

def write_sysfs(path, value):
    try:
        with open(path, 'w') as f:
            f.write(str(value))
        return True
    except Exception:
        return False

def find_legion_hwmon():
    import glob
    for d in glob.glob('/sys/class/hwmon/hwmon*/'):
        name = read_sysfs(d + 'name')
        if name == 'legion_hwmon':
            return d
    return None


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # quiet

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PATH.read_bytes())
        elif self.path == '/sys':
            data = {}
            for name, path in SYSFS_LEDS.items():
                v = read_sysfs(path)
                data[name] = int(v) if v and v.isdigit() else 0
            data['profile'] = read_sysfs('/sys/firmware/acpi/platform_profile') or ''
            hwmon = find_legion_hwmon()
            if hwmon:
                for i, key in [(1, 'fan1'), (2, 'fan2'), (3, 'fan3')]:
                    v = read_sysfs(hwmon + f'fan{i}_input')
                    data[key] = int(v) if v and v.isdigit() else None
                for i, key in [(1, 'cpu_temp'), (2, 'gpu_temp')]:
                    v = read_sysfs(hwmon + f'temp{i}_input')
                    data[key] = round(int(v) / 1000, 1) if v and v.isdigit() else None
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/sys':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            led = body.get('led', '')
            value = body.get('value', 0)
            ok = False
            if led in SYSFS_LEDS:
                ok = write_sysfs(SYSFS_LEDS[led], int(value))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': ok}).encode())
            return
        if self.path == '/effect-keys':
            # Per-key-group effects: {groups: [{effect, speed, colors:["#RRGGBB"], keys:["0xNNNN"]}]}
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            try:
                groups = []
                for g in body.get('groups', []):
                    ename = g.get('effect', 'static')
                    speed = g.get('speed', 2)
                    colors = []
                    for c in g.get('colors', []):
                        h = c.lstrip('#')
                        colors.append((int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)))
                    codes = []
                    for k in g.get('keys', []):
                        codes.append(int(k, 16) if isinstance(k, str) else int(k))
                    groups.append((ename, speed, colors, codes))
                ok = _send_effect_groups(groups)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': ok}).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'err': str(e)}).encode())
            return
        if self.path == '/preview':
            # Fast HID preview — no subprocess, direct ioctl
            # Body: {"keys": {"0x0042": "#ff0000", ...}}
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            keys = body.get('keys', {})
            try:
                key_map = {}
                for code_str, hex_color in keys.items():
                    code = int(code_str, 16) if code_str.startswith('0x') else int(code_str)
                    h = hex_color.lstrip('#')
                    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                    key_map[code] = (r, g, b)
                ok = _send_keys_fast(key_map)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': ok}).encode())
            except Exception as e:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'err': str(e)}).encode())
            return
        if self.path == '/api':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            cmd = body.get('cmd', '')

            try:
                result = subprocess.run(
                    ['python3', SCRIPT] + cmd.split(),
                    capture_output=True, text=True, timeout=10,
                )
                output = (result.stdout + result.stderr).strip()
                # Strip the "Using device:" line
                lines = [l for l in output.split('\n') if not l.startswith('Using device:')]
                output = '\n'.join(lines)
                ok = result.returncode == 0

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': ok, 'output': output}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'output': str(e)}).encode())
        else:
            self.send_error(404)


def main():
    if os.geteuid() != 0:
        print("This needs root for hidraw access. Run with: sudo python3 spectrum-web.py")
        sys.exit(1)

    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"Legion Spectrum Control running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == '__main__':
    main()
