#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest
from pathlib import Path
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import see_file
from app.core.processor import emphasize_text, process_content
from app.utils.colors import Colors
from app.utils.slice_parser import parse_slice_str


class MockArgs:
    """Mock arguments object for testing."""
    def __init__(self):
        self.lines = None
        self.chars = None
        self.emphasize = None
        self.color = 'red'
        self.bold = False
        self.ignore_case = False
        self.number = False


class TestParseSlice(unittest.TestCase):
    """Test slice parsing functionality."""
    
    def test_parse_single_number(self):
        """Test parsing single number '5' (single index, not slice)."""
        result = parse_slice_str('5')
        self.assertEqual(result, [5])
    
    def test_parse_range(self):
        """Test parsing range '0:5'."""
        result = parse_slice_str('0:5')
        self.assertEqual(result, slice(0, 5))
    
    def test_parse_open_end(self):
        """Test parsing open end '5:'."""
        result = parse_slice_str('5:')
        self.assertEqual(result, slice(5, None))
    
    def test_parse_open_start(self):
        """Test parsing open start ':5'."""
        result = parse_slice_str(':5')
        self.assertEqual(result, slice(None, 5))
    
    def test_parse_with_step(self):
        """Test parsing with step '0:10:2'."""
        result = parse_slice_str('0:10:2')
        self.assertEqual(result, slice(0, 10, 2))
    
    def test_parse_reverse(self):
        """Test parsing reverse '::-1'."""
        result = parse_slice_str('::-1')
        self.assertEqual(result, slice(None, None, -1))
    
    def test_parse_specific_lines(self):
        """Test parsing specific lines '1,3,5'."""
        result = parse_slice_str('1,3,5')
        self.assertEqual(result, [1, 3, 5])
    
    def test_parse_negative_single(self):
        """Test parsing negative single '-5' (single index, not slice)."""
        result = parse_slice_str('-5')
        self.assertEqual(result, [-5])


class TestEmphasize(unittest.TestCase):
    """Test text emphasis functionality."""
    
    def test_emphasize_single_pattern(self):
        """Test emphasizing a single pattern."""
        text = "This is an error message"
        result = emphasize_text(text, ['error'], color='red')
        self.assertIn(Colors.RED, result)
        self.assertIn('error', result)
        self.assertIn(Colors.RESET, result)
    
    def test_emphasize_multiple_patterns(self):
        """Test emphasizing multiple patterns."""
        text = "Error and warning messages"
        result = emphasize_text(text, ['Error', 'warning'], color='red')
        self.assertIn('Error', result)
        self.assertIn('warning', result)
    
    def test_emphasize_case_insensitive(self):
        """Test case-insensitive emphasis."""
        text = "ERROR and Error and error"
        result = emphasize_text(text, ['error'], color='red', case_insensitive=True)
        # All variations should be emphasized
        self.assertIn(Colors.RED, result)
    
    def test_emphasize_bold(self):
        """Test bold emphasis."""
        text = "Important message"
        result = emphasize_text(text, ['Important'], color='red', bold=True)
        self.assertIn(Colors.BOLD, result)
        self.assertIn(Colors.RED, result)
    
    def test_emphasize_no_patterns(self):
        """Test emphasis with no patterns."""
        text = "Plain text"
        result = emphasize_text(text, None, color='red')
        self.assertEqual(text, result)


class TestProcessContent(unittest.TestCase):
    """Test content processing functionality."""
    
    def test_process_line_slice(self):
        """Test line slicing."""
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"
        args = MockArgs()
        args.lines = slice(1, 3)  # Lines 2-3 (0-indexed)
        result, _ = process_content(content, args)
        self.assertIn("Line 2", result)
        self.assertIn("Line 3", result)
        self.assertNotIn("Line 1", result)
        self.assertNotIn("Line 4", result)
    
    def test_process_negative_line_slice(self):
        """Test negative line slicing."""
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"
        args = MockArgs()
        args.lines = slice(-2, None)  # Last 2 lines
        result, _ = process_content(content, args)
        self.assertIn("Line 4", result)
        self.assertIn("Line 5", result)
    
    def test_process_specific_lines(self):
        """Test specific line numbers (0-indexed)."""
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n"
        args = MockArgs()
        args.lines = [0, 2, 4]  # Lines 0, 2, 4 (0-indexed) = "Line 1", "Line 3", "Line 5"
        result, _ = process_content(content, args)
        self.assertIn("Line 1", result)
        self.assertIn("Line 3", result)
        self.assertIn("Line 5", result)
        self.assertNotIn("Line 2", result)
        self.assertNotIn("Line 4", result)
    
    def test_process_char_slice(self):
        """Test character slicing."""
        content = "Hello, World!"
        args = MockArgs()
        args.chars = slice(0, 5)
        result, _ = process_content(content, args)
        self.assertEqual("Hello", result)
    
    def test_process_emphasis(self):
        """Test emphasis in processing."""
        content = "This is an error"
        args = MockArgs()
        args.emphasize = ['error']
        result, _ = process_content(content, args)
        self.assertIn(Colors.RED, result)
        self.assertIn('error', result)
    
    def test_process_line_numbers(self):
        """Test adding line numbers (0-indexed)."""
        content = "Line 1\nLine 2\nLine 3\n"
        args = MockArgs()
        args.number = True
        result, _ = process_content(content, args)
        self.assertIn('0  ', result)
        self.assertIn('1  ', result)
        self.assertIn('2  ', result)
    
    def test_process_combined_features(self):
        """Test combining multiple features."""
        content = "Line 1\nLine 2 error\nLine 3\nLine 4\n"
        args = MockArgs()
        args.lines = slice(1, 3)
        args.emphasize = ['error']
        args.number = True
        result, _ = process_content(content, args)
        self.assertIn('error', result)
        self.assertIn(Colors.RED, result)
        self.assertIn('1  ', result)  # 0-indexed, so line at index 1


class TestSeeFile(unittest.TestCase):
    """Test file reading functionality."""
    
    def setUp(self):
        """Create test file."""
        self.test_file = Path("/tmp/test_see_file.txt")
        self.test_file.write_text("Hello, World!\nTest content\n")
        self.args = MockArgs()
    
    def tearDown(self):
        """Remove test file."""
        if self.test_file.exists():
            self.test_file.unlink()
    
    def test_see_file_basic(self):
        """Test basic file reading."""
        result = see_file(str(self.test_file), self.args)
        self.assertTrue(result)
    
    def test_see_nonexistent_file(self):
        """Test reading nonexistent file."""
        result = see_file("/tmp/nonexistent_file_12345.txt", self.args)
        self.assertFalse(result)
    
    def test_see_directory(self):
        """Test reading directory (should fail)."""
        result = see_file("/tmp", self.args)
        self.assertFalse(result)
    
    def test_see_file_with_emphasis(self):
        """Test file reading with emphasis."""
        self.args.emphasize = ['World']
        # Redirect stdout to capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            result = see_file(str(self.test_file), self.args)
            output = sys.stdout.getvalue()
            self.assertTrue(result)
            self.assertIn('World', output)
        finally:
            sys.stdout = old_stdout
    
    def test_see_file_with_line_numbers(self):
        """Test file reading with line numbers (0-indexed)."""
        self.args.number = True
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            result = see_file(str(self.test_file), self.args)
            output = sys.stdout.getvalue()
            self.assertTrue(result)
            self.assertIn('0  ', output)
            self.assertIn('1  ', output)
        finally:
            sys.stdout = old_stdout


class TestColors(unittest.TestCase):
    """Test color functionality."""
    
    def test_get_color_red(self):
        """Test getting red color."""
        color = Colors.get_color('red')
        self.assertEqual(color, Colors.RED)
    
    def test_get_color_green(self):
        """Test getting green color."""
        color = Colors.get_color('green')
        self.assertEqual(color, Colors.GREEN)
    
    def test_get_color_default(self):
        """Test getting default color for unknown."""
        color = Colors.get_color('unknown')
        self.assertEqual(color, Colors.RED)


if __name__ == "__main__":
    unittest.main()
