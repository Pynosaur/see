#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-27


def parse_slice_str(slice_str):
    """Parse slice string (exactly like Python).
    
    With colon (slice):
        "5:" -> slice(5, None)
        "0:5" -> slice(0, 5)
        ":5" -> slice(None, 5)
        "0:10:2" -> slice(0, 10, 2)
        "-5:" -> slice(-5, None)
    
    With comma (specific indices):
        "1,3,5" -> [1, 3, 5]
    
    Without colon or comma (single index):
        "5" -> [5]
        "-5" -> [-5]
    
    Returns:
        slice object for ranges with colon, list for specific lines
    """
    if ':' in slice_str:
        parts = slice_str.split(':')
        if len(parts) == 2:
            start = int(parts[0]) if parts[0] else None
            stop = int(parts[1]) if parts[1] else None
            return slice(start, stop)
        elif len(parts) == 3:
            start = int(parts[0]) if parts[0] else None
            stop = int(parts[1]) if parts[1] else None
            step = int(parts[2]) if parts[2] else None
            return slice(start, stop, step)
        else:
            raise ValueError(f"Invalid slice format: {slice_str}")
    
    if ',' in slice_str:
        try:
            return [int(x.strip()) for x in slice_str.split(',')]
        except ValueError:
            raise ValueError(f"Invalid line numbers: {slice_str}")
    
    try:
        return [int(slice_str)]
    except ValueError:
        raise ValueError(f"Invalid slice format: {slice_str}")


def extract_slice_args(argv):
    """Extract and remove -l/-c/-E arguments to handle negative indices properly.
    
    Returns: (cleaned_argv, lines_value, chars_value, emphasize_lines_value)
    """
    result = []
    lines_value = None
    chars_value = None
    emphasize_lines_value = None
    i = 0
    
    while i < len(argv):
        arg = argv[i]
        
        if arg in ('-l', '--lines'):
            if i + 1 < len(argv):
                lines_value = argv[i + 1]
                i += 2
                continue
        elif arg.startswith('-l=') or arg.startswith('--lines='):
            lines_value = arg.split('=', 1)[1]
            i += 1
            continue
        elif arg in ('-c', '--chars'):
            if i + 1 < len(argv):
                chars_value = argv[i + 1]
                i += 2
                continue
        elif arg.startswith('-c=') or arg.startswith('--chars='):
            chars_value = arg.split('=', 1)[1]
            i += 1
            continue
        elif arg in ('-E', '--emphasize-lines'):
            if i + 1 < len(argv):
                emphasize_lines_value = argv[i + 1]
                i += 2
                continue
        elif arg.startswith('-E=') or arg.startswith('--emphasize-lines='):
            emphasize_lines_value = arg.split('=', 1)[1]
            i += 1
            continue
        
        result.append(arg)
        i += 1
    
    return result, lines_value, chars_value, emphasize_lines_value
