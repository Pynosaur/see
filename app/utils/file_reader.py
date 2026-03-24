#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-27

import sys
from pathlib import Path


def read_file(filepath):
    """Read file contents.

    Returns:
        Tuple of (success, content_string)
    """
    try:
        path = Path(filepath)
        if not path.exists():
            print(f"see: {filepath}: No such file or directory", file=sys.stderr)
            return (False, None)
        if not path.is_file():
            print(f"see: {filepath}: Is a directory", file=sys.stderr)
            return (False, None)

        content = path.read_text()
        return (True, content)

    except PermissionError:
        print(f"see: {filepath}: Permission denied", file=sys.stderr)
        return (False, None)
    except Exception as e:
        print(f"see: {filepath}: {e}", file=sys.stderr)
        return (False, None)


def read_stdin():
    """Read from stdin.

    Returns:
        String content or None on error
    """
    try:
        return sys.stdin.read()
    except KeyboardInterrupt:
        return None

