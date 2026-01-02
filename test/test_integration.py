#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integration tests for see - run before committing."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestIntegration(unittest.TestCase):
    """Integration tests that match CI pipeline."""
    
    @classmethod
    def setUpClass(cls):
        """Create test file."""
        cls.test_file = Path(tempfile.gettempdir()) / "test_see_integration.txt"
        cls.test_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\n")
    
    @classmethod
    def tearDownClass(cls):
        """Remove test file."""
        if cls.test_file.exists():
            cls.test_file.unlink()
    
    def run_see(self, *args):
        """Run see command and return result."""
        cmd = [sys.executable, "app/main.py"] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def test_basic_display(self):
        """Test basic file display."""
        result = self.run_see(str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 1", result.stdout)
    
    def test_help(self):
        """Test --help flag."""
        result = self.run_see("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("see -", result.stdout)
    
    def test_version(self):
        """Test --version flag."""
        result = self.run_see("--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn("0.1.0", result.stdout)
    
    def test_line_slice_range(self):
        """Test line slicing with range (0:3)."""
        result = self.run_see("-l", "0:3", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 1", result.stdout)
        self.assertIn("Line 3", result.stdout)
        self.assertNotIn("Line 4", result.stdout)
    
    def test_line_slice_open_end(self):
        """Test line slicing from position (:5)."""
        result = self.run_see("-l", ":5", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 1", result.stdout)
        self.assertIn("Line 5", result.stdout)
        self.assertNotIn("Line 6", result.stdout)
    
    def test_line_slice_with_step(self):
        """Test line slicing with step (0:8:2)."""
        result = self.run_see("-l", "0:8:2", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 1", result.stdout)
        self.assertIn("Line 3", result.stdout)
        self.assertNotIn("Line 2", result.stdout)
    
    def test_negative_slice(self):
        """Test negative slicing (-5:)."""
        result = self.run_see("-l", "-5:", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 4", result.stdout)
        self.assertIn("Line 8", result.stdout)
    
    def test_negative_range(self):
        """Test negative range (-5:-2)."""
        result = self.run_see("-l", "-5:-2", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 4", result.stdout)
        self.assertNotIn("Line 1", result.stdout)
        self.assertNotIn("Line 8", result.stdout)
    
    def test_specific_lines(self):
        """Test specific line numbers (0,2,4) - 0-indexed."""
        result = self.run_see("-l", "0,2,4", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Line 1", result.stdout)
        self.assertIn("Line 3", result.stdout)
        self.assertIn("Line 5", result.stdout)
        self.assertNotIn("Line 2", result.stdout)
        self.assertNotIn("Line 4", result.stdout)
    
    def test_emphasis(self):
        """Test pattern emphasis."""
        result = self.run_see("-e", "Line", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        # Should contain ANSI color codes
        self.assertIn("\033[", result.stdout)
    
    def test_line_numbers(self):
        """Test line numbers."""
        result = self.run_see("-n", str(self.test_file))
        self.assertEqual(result.returncode, 0)
        self.assertIn("1  ", result.stdout)
        self.assertIn("2  ", result.stdout)
    
    def test_stdin(self):
        """Test stdin input."""
        cmd = [sys.executable, "app/main.py"]
        result = subprocess.run(cmd, input="test input\n", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("test input", result.stdout)
    
    def test_nonexistent_file(self):
        """Test nonexistent file handling."""
        result = self.run_see("/tmp/nonexistent_file_12345.txt")
        self.assertEqual(result.returncode, 1)
        self.assertIn("No such file", result.stderr)


if __name__ == "__main__":
    print("Running integration tests (matches CI pipeline)...")
    print("=" * 60)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("✅ All integration tests passed!")
        print("Safe to commit and push.")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        print("Fix issues before committing.")
        sys.exit(1)

