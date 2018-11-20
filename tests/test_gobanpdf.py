#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gobanpdf` package."""


import unittest
from click.testing import CliRunner
import os

from gobanpdf import gobanpdf


class TestGobanpdf(unittest.TestCase):
    """Tests for `gobanpdf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""

        sgf_example = """(
            ;GM[1]FF[4]CA[UTF-8]KM[7.5]SZ[19]
            ;B[ar]
            ;W[as]
            ;B[bs]
        )"""

        runner = CliRunner()
        help_result = runner.invoke(gobanpdf.board_to_pdf, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

        with runner.isolated_filesystem():
            with open('example.sgf', 'w') as f:
                f.write(sgf_example)
            result = runner.invoke(gobanpdf.board_to_pdf, ['example.sgf', '4', 'example.pdf'])
            assert result.exit_code == 0
            assert os.path.isfile('./example.pdf')
