#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2025-12-24

import argparse
import sys
from pathlib import Path

# Allow running both as module and as script
if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "app"

from app import __version__
from app.core.processor import process_content
from app.utils.doc_reader import read_app_doc
from app.utils.file_reader import read_file, read_stdin
from app.utils.slice_parser import parse_slice_str, extract_slice_args


def print_help():
    """Print help message from documentation."""
    doc = read_app_doc('see')
    
    desc = doc.get('description', 'Display file contents with optional formatting')
    usage = doc.get('usage', ['see [OPTIONS] [FILE...]'])
    options = doc.get('options', [])
    examples = doc.get('examples', [])
    
    print(f"see - {desc}")
    print("\nUSAGE:")
    for u in usage:
        print(f"    {u}")
    
    if options:
        print("\nOPTIONS:")
        for opt in options:
            print(f"    {opt}")
    
    if examples:
        print("\nEXAMPLES:")
        for ex in examples:
            print(f"    {ex}")


def print_version():
    """Print version."""
    doc = read_app_doc('see')
    print(doc.get('version', __version__))


def see_file(filepath, args):
    """Read and print file contents with processing."""
    success, content = read_file(filepath)
    if not success:
        return False
    
    processed, _ = process_content(content, args)
    print(processed, end='')
    return True


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='Display file contents with optional formatting',
        add_help=False
    )
    
    parser.add_argument('files', nargs='*', help='Files to display')
    parser.add_argument('-h', '--help', action='store_true', help='Show help message')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    
    # Line and char slicing (handled manually)
    parser.add_argument('-l', '--lines', type=str, metavar='SLICE',
                        help='Line slice: start:stop[:step] or N,N,... (0-indexed)')
    parser.add_argument('-c', '--chars', type=str, metavar='SLICE',
                        help='Character slice: start:stop[:step] (0-indexed)')
    
    # Emphasis
    parser.add_argument('-e', '--emphasize', action='append', metavar='PATTERN',
                        help='Emphasize/highlight pattern (can be used multiple times)')
    parser.add_argument('-E', '--emphasize-lines', type=str, metavar='LINES',
                        help='Emphasize entire lines: N,N,N or start:stop')
    parser.add_argument('--color', default='red',
                        choices=['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'],
                        help='Color for emphasis (default: red)')
    parser.add_argument('--bold', action='store_true',
                        help='Use bold for emphasis')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='Case-insensitive emphasis')
    
    # Line numbers
    parser.add_argument('-n', '--number', action='store_true',
                        help='Show line numbers')
    
    return parser


def main():
    """Main entry point."""
    # Handle no arguments (stdin mode)
    if len(sys.argv) == 1:
        try:
            for line in sys.stdin:
                print(line, end='')
            return 0
        except KeyboardInterrupt:
            return 130
    
    # Extract slice arguments before argparse
    cleaned_argv, lines_value, chars_value, emphasize_lines_value = extract_slice_args(sys.argv[1:])
    
    parser = create_parser()
    args = parser.parse_args(cleaned_argv)
    
    # Manually set the extracted slice values
    if lines_value:
        args.lines = lines_value
    if chars_value:
        args.chars = chars_value
    if emphasize_lines_value:
        args.emphasize_lines = emphasize_lines_value
    
    # Handle help and version
    if args.help:
        print_help()
        return 0
    
    if args.version:
        print_version()
        return 0
    
    # Parse slices
    if args.lines:
        try:
            args.lines = parse_slice_str(args.lines)
        except ValueError as e:
            print(f"see: {e}", file=sys.stderr)
            return 1
    
    if args.chars:
        try:
            args.chars = parse_slice_str(args.chars)
        except ValueError as e:
            print(f"see: {e}", file=sys.stderr)
            return 1
    
    # Parse line emphasis
    if args.emphasize_lines:
        try:
            parsed = parse_slice_str(args.emphasize_lines)
            # Convert to list of indices
            if isinstance(parsed, slice):
                # Will be applied to actual lines later
                args.emphasize_lines = parsed
            elif isinstance(parsed, list):
                args.emphasize_lines = parsed
        except ValueError as e:
            print(f"see: {e}", file=sys.stderr)
            return 1
    else:
        args.emphasize_lines = None
    
    # Handle stdin if no files specified
    if not args.files:
        content = read_stdin()
        if content is None:
            return 130
        
        processed, _ = process_content(content, args)
        print(processed, end='')
        return 0
    
    # Process files
    success = True
    for filepath in args.files:
        if not see_file(filepath, args):
            success = False
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
