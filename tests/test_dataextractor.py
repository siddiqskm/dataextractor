#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dataextractor` package."""

import pytest

from click.testing import CliRunner
from dataextractor import cli


@pytest.fixture()  # type: ignore
def example_fixture() -> str:
    return "hello"


def test_example_fixture(example_fixture: str) -> None:
    assert example_fixture == 'hello'


def test_command_line_interface() -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'dataextractor.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
