from click.exceptions import UsageError
import pytest
from bitcut.parse import parse_ranges, parse_value, parse_mapping

PARSE_RANGES_TEST_CASES = [
    # ranges, expected, warning
    (["3:0"], [(3, 0)], ""),
    (["0:0"], [(0, 0)], ""),
    (["1:1"], [(1, 1)], ""),
    (["3:0", "3:1", "14:1", "2:5"], [(3, 0), (3, 1), (14, 1), (5, 2)], "overlap"),
]

@pytest.mark.parametrize("ranges, expected, warning", PARSE_RANGES_TEST_CASES)
def test_parse_ranges_multiple(ranges, expected, warning):
    if warning != "":
        with pytest.warns(UserWarning, match=warning):
            got = parse_ranges(None, None, ranges)
    else:
        got = parse_ranges(None, None, ranges)
    assert got == expected

PARSE_VALUE_TEST_CASES = [
    # value, expected, error
    ("0x12", 0x12, None),
    ("12", 12, None),
    ("a", None, ValueError),
    ("0x", 0, ValueError),
]

@pytest.mark.parametrize("value, expected, error", PARSE_VALUE_TEST_CASES)
def test_parse_value_multiple(value, expected, error):
    if error is not None:
        with pytest.raises(error):
            parse_value(None, None, value)
    else:
        got = parse_value(None, None, value)
        assert got == expected

PARSE_MAPPING_TEST_CASES = [
    # mapping, expected, warning, error
    (["3:0=1010"], {(3,0):"1010"}, None, None),
    (["3:0=0xA"], {(3,0):"1010"}, None, None),
    (["3:0=A"], None, None, ValueError), # Not hex or binstr
    (["3:0=1010", "1:0=01"], None, None, ValueError), # Range overlap
    (["3->0 1010", "1:0=01"], None, None, UsageError), # Range overlap
]

@pytest.mark.parametrize("mapping, expected, warning, error", PARSE_MAPPING_TEST_CASES)
def test_parse_mapping(mapping, expected, warning, error):
    if error is not None:
        with pytest.raises(error):
            parse_mapping(None, None, mapping)
    else:
        got = parse_mapping(None, None, mapping)
        assert got == expected
