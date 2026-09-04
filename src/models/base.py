"""
Core data model for per-laptop keyboard/lighting layouts.

Each supported laptop model gets one module (e.g. legion_pro7_16iax10h.py)
that builds a single `KeyboardModel` instance called MODEL. That instance
is the *only* hand-maintained source of truth for that laptop: zone lists,
name->code lookups, key groups, and the web UI's grid layout are all
derived from it rather than kept as separate parallel tables.
"""

from dataclasses import dataclass, field
from functools import cached_property

# Shared conventions, not a closed set. Every model has a physical key
# matrix and (so far) some kind of accent strip, so these two names are
# reused across models for consistency. Beyond that, a model is free to
# define whatever zone names its hardware actually has — e.g. 'logo' for
# a lid-logo LED, 'power_button' for a lit power button, or something
# else entirely for hardware we haven't seen yet. Nothing in this module
# enumerates the full set up front; a KeyboardModel reports its own zones
# via the `zones` property below.
ZONE_KEYBOARD = 'keyboard'
ZONE_PERIMETER = 'perimeter'


@dataclass(frozen=True)
class Key:
    """A single addressable LED: a main key, a perimeter LED, or any other
    model-specific single-LED zone (lid logo, power button, etc.)."""
    name: str            # short identifier, e.g. 'esc', 'w', 'perim_rear_top_1'
    code: int            # keycode sent to the device, e.g. 0x0001
    zone: str            # e.g. 'keyboard', 'perimeter', 'logo', 'power_button'

    # Grid position for the web UI visualizer. Only meaningful for
    # ZONE_KEYBOARD keys that sit on the CSS grid; every other zone
    # leaves these as None.
    col: int | None = None
    col_span: int | None = None
    row: int | None = None
    row_span: int | None = None

    def __post_init__(self):
        if self.zone == ZONE_KEYBOARD and self.col is None:
            raise ValueError(
                f"Key {self.name!r} (0x{self.code:04x}) is in the "
                f"'{ZONE_KEYBOARD}' zone but has no grid position (col/row). "
                f"Every keyboard-zone key must be placeable on the "
                f"visualizer grid."
            )
        if self.zone != ZONE_KEYBOARD and self.col is not None:
            raise ValueError(
                f"Key {self.name!r} (0x{self.code:04x}) is in zone "
                f"'{self.zone}' but has a grid position set. Only "
                f"'{ZONE_KEYBOARD}' zone keys render on the grid."
            )


@dataclass(frozen=True)
class KeyboardModel:
    """Everything needed to talk to and visualize one laptop's lighting hardware."""
    pid: str                        # USB product ID, e.g. 'C195'
    display_name: str               # e.g. 'Legion 5 15IRX10'
    keys: list[Key]
    groups: dict[str, list[str]] = field(default_factory=dict)  # 'wasd' -> ['w','a','s','d']
    grid_cols: int = 0
    grid_rows: int = 0

    def __post_init__(self):
        names = [k.name for k in self.keys]
        codes = [k.code for k in self.keys]

        dup_names = {n for n in names if names.count(n) > 1}
        if dup_names:
            raise ValueError(f"{self.display_name}: duplicate key name(s): {sorted(dup_names)}")

        dup_codes = {c for c in codes if codes.count(c) > 1}
        if dup_codes:
            dup_str = ', '.join(f'0x{c:04x}' for c in sorted(dup_codes))
            raise ValueError(f"{self.display_name}: duplicate keycode(s): {dup_str}")

        for group_name, member_names in self.groups.items():
            unknown = [n for n in member_names if n not in names]
            if unknown:
                raise ValueError(
                    f"{self.display_name}: group {group_name!r} references "
                    f"unknown key name(s): {unknown}"
                )

    # -- derived indices, built once and cached -----------------------------

    @cached_property
    def by_name(self) -> dict[str, Key]:
        return {k.name: k for k in self.keys}

    @cached_property
    def by_code(self) -> dict[int, Key]:
        return {k.code: k for k in self.keys}

    @cached_property
    def zones(self) -> frozenset[str]:
        """Which zone names this specific model actually has. Use this
        instead of assuming any zone (even 'logo') exists universally."""
        return frozenset(k.zone for k in self.keys)

    # -- convenience accessors ------------------------------------------------

    def keys_in_zone(self, zone: str) -> list[int]:
        return [k.code for k in self.keys if k.zone == zone]

    def resolve_group(self, group_name: str) -> list[int]:
        return [self.by_name[n].code for n in self.groups[group_name]]

    def grid_keys(self) -> list[Key]:
        """Keys with a grid position, for the web UI visualizer."""
        return [k for k in self.keys if k.col is not None]
