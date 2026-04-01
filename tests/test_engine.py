import pytest
from bitcut.engine import create_binary_slices, flip_idx, round_up_to_multiple

CREATE_BINARY_SLICES_TEST_CASES = [
    # value, ranges, n_bits, expected
    (10, [(3,2), (2, 0)], 4, {(3,0): "1010", (3,2): "10", (2,0): "010"} ),
    (11, [(2,2)], 4, {(3,0): "1011", (2,2): "0"} )
]
@pytest.mark.parametrize("value, ranges, n_bits, expected", CREATE_BINARY_SLICES_TEST_CASES)
def test_create_binary_slices(value, ranges, n_bits, expected):
    got = create_binary_slices(value, ranges, n_bits=n_bits)
    assert got == expected

FLIP_IDX_TEST_CASES = [
    # to_flip, total_bits, expected
    (31, 32, 0),
    (30, 32, 1),
    (0, 32, 31),
    (4, 8, 3),
    (7, 8, 0),
    (0, 8, 7),
    (15, 16, 0),
    (10, 16, 5),
    (13, 16, 2),
]

@pytest.mark.parametrize("to_flip, total_bits, expected", FLIP_IDX_TEST_CASES)
def test_flip_idx(to_flip, total_bits, expected):
    got = flip_idx(to_flip, total_bits)
    assert got == expected


ROUND_UP_TO_MULTPLE_TEST_CASES = [
    # n, multiple, expected
    (31, 4, 32),
    (3, 4, 4),
    (1, 4, 4),
    (5, 4, 8),
    (13, 4, 16),
    (4, 4, 4),
    (8, 4, 8),
    (9, 3, 9),
    (14, 4, 16),
]
@pytest.mark.parametrize("n, multiple, expected", ROUND_UP_TO_MULTPLE_TEST_CASES)
def test_round_up_to_multiple(n, multiple, expected):
    got = round_up_to_multiple(n, multiple)
    assert got == expected
