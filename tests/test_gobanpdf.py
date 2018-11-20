#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gobanpdf` package."""


import unittest
from click.testing import CliRunner

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
        runner = CliRunner()
        result = runner.invoke(gobanpdf.board_to_pdf)
        assert result.exit_code == 0
        assert 'gobanpdf.cli.main' in result.output
        help_result = runner.invoke(gobanpdf.board_to_pdf, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
