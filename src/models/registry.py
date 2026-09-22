"""
Registry mapping a USB product ID (PID) to the KeyboardModel for that laptop.

Normal flow: hardware detection (find_spectrum_device) reads the PID out of
a hidraw device's uevent, then calls get_model(pid) here to resolve which
laptop's keycode/layout data to use. Nothing about "which model" should be
hardcoded anywhere else — this module is the one place that knows the
PID -> model mapping.

Manual override: set the LEGION_MODEL_PID environment variable to force a
specific model regardless of what's actually plugged in. Useful for
developing/debugging a model's key data without the physical laptop in
front of you, e.g.:

    LEGION_MODEL_PID=C195 python3 spectrum-ctl.py keymap

get_model_for_detected_pid() checks this override first, falling back to
the PID actually read from hardware.
"""

import os

from .base import KeyboardModel
from .legion_pro7_16iax10h import MODEL as LEGION_PRO7_16IAX10H

_MODELS_BY_PID: dict[str, KeyboardModel] = {
    LEGION_PRO7_16IAX10H.pid: LEGION_PRO7_16IAX10H,
    # Add new models here as they're built, e.g.:
    # LEGION5_15IRX10.pid: LEGION5_15IRX10,
}

ENV_OVERRIDE_VAR = 'LEGION_MODEL_PID'


class UnknownModelError(Exception):
    """Raised when a PID doesn't correspond to any registered model."""
    def __init__(self, pid: str):
        known = ', '.join(sorted(_MODELS_BY_PID)) or '(none registered)'
        super().__init__(
            f"No KeyboardModel registered for PID '{pid}'. "
            f"Known PIDs: {known}. If this is a new laptop, add a model "
            f"module for it and register it in models/registry.py."
        )
        self.pid = pid


def get_model(pid: str) -> KeyboardModel:
    """Look up the KeyboardModel for a given PID (case-insensitive)."""
    pid = pid.upper()
    try:
        return _MODELS_BY_PID[pid]
    except KeyError:
        raise UnknownModelError(pid) from None


def known_pids() -> list[str]:
    return sorted(_MODELS_BY_PID)


def get_model_for_detected_pid(detected_pid: str) -> KeyboardModel:
    """Resolve a model, honoring the LEGION_MODEL_PID override if set.

    `detected_pid` is whatever PID was actually read from the hardware's
    uevent. If LEGION_MODEL_PID is set in the environment, it takes
    precedence over the detected value.
    """
    override = os.environ.get(ENV_OVERRIDE_VAR)
    pid = override.strip() if override else detected_pid
    return get_model(pid)
