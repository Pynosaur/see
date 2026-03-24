#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-27

import re
from ..utils.colors import Colors


def emphasize_text(text, patterns, color='red', bold=False, case_insensitive=False):
    """Emphasize patterns in text with color."""
    if not patterns:
        return text

    color_code = Colors.get_color(color)
    prefix = Colors.BOLD + color_code if bold else color_code

    for pattern in patterns:
        flags = re.IGNORECASE if case_insensitive else 0
        text = re.sub(
            f'({re.escape(pattern)})',
            f'{prefix}\\1{Colors.RESET}',
            text,
            flags=flags
        )

    return text


def emphasize_lines(lines, line_spec, color='red', bold=False):
    """Emphasize entire lines by index or slice.

    Args:
        lines: List of lines
        line_spec: slice object or list of indices (0-indexed, negative indices supported)
        color: Color name
        bold: Use bold

    Returns:
        List of lines with emphasized lines colored
    """
    if not line_spec:
        return lines

    # Convert slice to list of indices
    if isinstance(line_spec, slice):
        indices = set(range(len(lines))[line_spec])
    elif isinstance(line_spec, list):
        # Normalize negative indices to positive
        normalized = set()
        for idx in line_spec:
            if idx < 0:
                normalized.add(len(lines) + idx)
            else:
                normalized.add(idx)
        indices = normalized
    else:
        return lines

    color_code = Colors.get_color(color)
    prefix = Colors.BOLD + color_code if bold else color_code

    result = []
    for i, line in enumerate(lines):
        if i in indices:
            # Emphasize entire line
            emphasized = (
                f'{prefix}{line.rstrip()}{Colors.RESET}\n'
                if line.endswith('\n')
                else f'{prefix}{line}{Colors.RESET}'
            )
            result.append(emphasized)
        else:
            result.append(line)

    return result


def apply_line_slice(lines, slice_spec):
    """Apply line slicing and track original line numbers.

    Returns:
        Tuple of (selected_lines, original_line_numbers)
    """
    if isinstance(slice_spec, slice):
        indices = range(len(lines))[slice_spec]
        original_line_numbers = list(indices)
        return lines[slice_spec], original_line_numbers
    elif isinstance(slice_spec, list):
        unique_lines = sorted(set(slice_spec), key=lambda x: (x < 0, abs(x)))
        selected = []
        original_line_numbers = []
        for line_num in unique_lines:
            if 0 <= line_num < len(lines):
                selected.append(lines[line_num])
                original_line_numbers.append(line_num)
            elif line_num < 0 and abs(line_num) <= len(lines):
                selected.append(lines[line_num])
                original_line_numbers.append(len(lines) + line_num)
        return selected, original_line_numbers

    return lines, None


def apply_char_slice(content, slice_spec):
    """Apply character slicing."""
    if isinstance(slice_spec, slice):
        return content[slice_spec]
    elif isinstance(slice_spec, list):
        selected = []
        for char_num in slice_spec:
            if 0 <= char_num < len(content):
                selected.append(content[char_num])
            elif char_num < 0 and abs(char_num) <= len(content):
                selected.append(content[char_num])
        return ''.join(selected)

    return content


def add_line_numbers(lines, original_line_numbers=None):
    """Add line numbers to lines."""
    numbered_lines = []

    if original_line_numbers:
        for line_num, line in zip(original_line_numbers, lines):
            numbered_lines.append(f"{line_num:6d}  {line}")
    else:
        for i, line in enumerate(lines):
            numbered_lines.append(f"{i:6d}  {line}")

    return numbered_lines


def process_content(content, args):
    """Process content based on arguments.

    Returns:
        Tuple of (processed_content, original_line_numbers)
    """
    lines = content.splitlines(keepends=True)
    original_line_numbers = None

    # Apply line slicing
    if args.lines:
        lines, original_line_numbers = apply_line_slice(lines, args.lines)

    # Apply line emphasis (before reconstruction)
    if hasattr(args, 'emphasize_lines') and args.emphasize_lines:
        lines = emphasize_lines(
            lines,
            args.emphasize_lines,
            color=args.color,
            bold=args.bold,
        )

    # Reconstruct content
    content = ''.join(lines)

    # Apply character slicing
    if args.chars:
        content = apply_char_slice(content, args.chars)

    # Apply pattern emphasis
    if args.emphasize:
        content = emphasize_text(
            content,
            args.emphasize,
            color=args.color,
            bold=args.bold,
            case_insensitive=args.ignore_case
        )

    # Add line numbers
    if args.number:
        lines = content.splitlines(keepends=True)
        numbered_lines = add_line_numbers(lines, original_line_numbers)
        content = ''.join(numbered_lines)

    return content, original_line_numbers

