import pytest

from click.testing import CliRunner
from bitcut.cli import cli

def test_slice_basic():
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "0x34", "5:4", "3:0"])
    assert result.exit_code == 0
    assert "[5:0] - b'110100'" in result.output
    assert "[5:4] - b'11'" in result.output
    assert "[3:0] - b'0100'" in result.output

def test_slice_decimal_nbits():
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "52", "-n", "32", "7:0"])
    assert result.exit_code == 0
    assert "[31:0 ] - b'00000000000000000000000000110100'" in result.stdout
    assert "[ 7:0 ] - b'00110100'" in result.stdout

def test_slice_index_higher_than_n_bits():
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "52", "-n", "32", "32:0"])
    assert result.exit_code == 1

def test_range_not_given():
    runner = CliRunner()
    result = runner.invoke(cli, ["slice", "52", "-n", "32", "31:16:8"])
    assert result.exit_code == 1

def test_splice_basic():
    runner = CliRunner()
    result = runner.invoke(cli, ["splice", "3:0=1100", "5:4=01"])
    assert "[5:4] - b'01'" in result.stdout
    assert "[3:0] - b'1100'" in result.stdout
    assert "Binary String: 00011100" in result.stdout
    assert "Hexadecimal  : 0x1c" in result.stdout
    assert "Unsigned int : 28" in result.stdout
    assert result.exit_code == 0
    assert "011100" in result.stdout

def test_build_binstr_larger_than_range():
    runner = CliRunner()
    result = runner.invoke(cli, ["build", "3:0=11100"])
    assert result.exit_code == 2

def test_splice_binstr_smaller_than_range():
    runner = CliRunner()
    with pytest.warns(UserWarning, match="Zero padding MSB of binstr"):
        result = runner.invoke(cli, ["splice", "3:0=100"])
    assert result.exit_code == 0
