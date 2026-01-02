# see

Display file contents with optional formatting, slicing, and emphasis.

Version: 0.1.0

## Features

- **Line Slicing**: Display specific line ranges
- **Character Slicing**: Display specific character ranges
- **Pattern Emphasis**: Highlight specific patterns with colors
- **Line Numbers**: Display files with line numbers
- **stdin Support**: Read from standard input when no files specified

## Usage

```bash
# Basic usage
see file.txt
see --help
see --version

# Line slicing (with colon :)
see -l 0:10 file.txt           # Slice: lines 0-10
see -l :5 file.txt             # Slice: first 5 lines
see -l 5: file.txt             # Slice: from line 5 to end
see -l -5: file.txt            # Slice: last 5 lines
see -l -10:-5 file.txt         # Slice: lines -10 to -5
see -l 0:20:2 file.txt         # Slice: every 2nd line from 0-20
see -l ::-1 file.txt           # Slice: reverse file

# Specific line indices (no colon)
see -l 5 file.txt              # Single: just line 5
see -l -5 file.txt             # Single: line at index -5
see -l 0,2,4 file.txt          # Multiple: lines 0, 2, and 4
see -l 10,20,30 file.txt       # Multiple: lines 10, 20, and 30

# Character slicing
see -c 0:100 file.txt          # First 100 characters
see -c 50:150 file.txt         # Characters 50-150

# Pattern emphasis (highlighting)
see -e "error" file.txt                           # Highlight "error"
see -e "TODO" -e "FIXME" file.txt                 # Multiple patterns
see --color=yellow --bold -e "warning" file.txt   # Yellow bold
see -i -e "warning" file.txt                      # Case-insensitive

# Line emphasis (entire lines)
see -E 1,3,5 file.txt                             # Emphasize lines 1, 3, 5
see -E 0:10 --color=green file.txt                # Emphasize lines 0-10

# Line numbers
see -n file.txt                                   # Show line numbers

# Combine features
see -n -l 0:20 -e "error" --color=red file.txt
```

## Options

- `-h, --help` - Show help message
- `-v, --version` - Show version information
- `-l, --lines SLICE` - Display lines: `start:stop[:step]` or `N,N,N` (all 0-indexed)
- `-c, --chars SLICE` - Display characters: `start:stop[:step]`
- `-e, --emphasize PATTERN` - Highlight pattern (can be used multiple times)
- `-E, --emphasize-lines LINES` - Emphasize entire lines: `N,N,N` or `start:stop`
- `--color COLOR` - Emphasis color: red, green, yellow, blue, magenta, cyan (default: red)
- `--bold` - Use bold text for emphasis
- `-i, --ignore-case` - Case-insensitive pattern matching
- `-n, --number` - Show line numbers

## Examples

Display a file:
```bash
see README.md
```

Show lines 0-10 with line numbers:
```bash
see -n -l 0:10 README.md
```

Highlight errors and warnings in log files:
```bash
see -e "error" -e "warning" --color=red --bold log.txt
```

Find TODO items in source code:
```bash
see -e "TODO" -e "FIXME" --color=yellow src/main.py
```

Preview last 20 lines of a file:
```bash
see -l -20: large_file.log
```

Read from stdin:
```bash
echo "Hello, World!" | see
cat file.txt | see -e "important"
ls -la | see -e ".py"
```

## Installation

### Build from source
```bash
git clone https://github.com/pynosaur/see.git
cd see
bazel build //:see_bin
cp bazel-bin/see ~/.local/bin/  # Or anywhere in your PATH
```

### Development
```bash
# Run directly with Python
python app/main.py file.txt

# Run unit tests
python test/test_main.py

# Run integration tests (matches CI - run before committing)
python test/test_integration.py

# Run all tests
python -m unittest discover -s test -v
```
