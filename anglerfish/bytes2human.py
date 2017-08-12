#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convert bytes to kilobytes, megabytes, gigabytes, etc."""


from math import log2


def bytes2human(integer_bytes: int, to_unit: str=None) -> str:
    """Convert bytes to kilobytes, megabytes, gigabytes, etc."""
    size, to = int(abs(integer_bytes)), to_unit.lower() if to_unit else to_unit
    sfx = ('', 'Kilo', 'Mega', 'Giga', 'Tera', 'Peta', 'Exa', 'Zetta', 'Yotta')
    if to:  # Force a specific data unit from args.
        for i in range(sfx.index(to)):
            size = size / 1_024
        unit, value = to.title().strip(), int(size)
    else:  # Auto-scale data unit.
        order = int(log2(size) / 10) if size else 0
        value, unit = int(size / (1 << (order * 10))), sfx[order]
    return f"{ value } { unit }bytes"
