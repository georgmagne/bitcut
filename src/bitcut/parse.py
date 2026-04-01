"""
Module to hande parsing user input before sending it into engine.
"""

import warnings
import click

from click.exceptions import UsageError

def value_fit_range(bit_range: tuple[int, int],
                    binstr: str) -> str:
    """ Checks if the gven binstr actually fits into the range give by a tuple.
    :param bit_range:
    :param binstr:
    :return: Zero padded binstr up to the highest range value.
    """
    n_bits_in_range = bit_range[0] - bit_range[1] + 1
    n_bits_in_binstr = len(binstr)
    binstr_not_fitting = n_bits_in_binstr > n_bits_in_range
    binstr_too_few_bits = n_bits_in_binstr < n_bits_in_range

    if binstr_not_fitting:
        raise UsageError(f"Given {binstr=} has too many bits to fit into given {range=}")

    if binstr_too_few_bits:
        warnings.warn(f"Zero padding MSB of {binstr=} to fit {range=}", UserWarning)
        n_bits_missing = n_bits_in_range - n_bits_in_binstr
        pad = "0" * n_bits_missing
        correct_size_binstr = pad + binstr
    else:
        correct_size_binstr = binstr
    return correct_size_binstr

def parse_ranges(_ctx: "click.Context",
                 _param: "click.Parameter",
                 ranges: tuple[str, ...]) -> list[tuple[int, int]]:
    """
    Click callback function to parse slice ranges from user.
    :param ranges: Unparsed ranges from CLI.
    :return: Parsed ranges as list of tuples.
    """
    detected_indices = set()
    ranges_tuple = []
    for r in ranges:
        range_lst_int = list(map(int, r.split(":")))
        if len(range_lst_int) > 2:
            raise ValueError

        msb = max(range_lst_int)
        lsb = min(range_lst_int)
        range_tuple = (msb, lsb)
        ranges_tuple.append(range_tuple)
        for index in range(lsb, msb+1):
            if index in detected_indices:
                warnings.warn(f"Detected overlap in the given ranges, {index=} occurs multiple times", UserWarning)
            detected_indices.add(index)
    return ranges_tuple

def parse_value(_ctx: "click.Context",
                _param: "click.Parameter",
                value: str) -> int:
    """
    Click callback function to parse values from CLI user input.
    :param value: Value as either hex or decimal.
    :return: the parsed value as int.
    """
    if value[:2].lower() == "0x":
        # Hex value
        parsed = int(value[2:], 16)
    else:
        # Decimal or string
        # Raises Exception if it cannot be converted
        parsed = int(value, 10)
    return parsed

def parse_mapping(_ctx: "click.Context",
                  _param: "click.Parameter",
                  mappings: str) -> dict[tuple[int, int], str]:
    """
    Click callback function to parse mappings from User input.
    :param mapping: String on the for X:Y=bbbb.
    :return: dict with tuple with the range as key and the binstr as value.
    """
    unparsed_ranges = []
    parsed_values = []
    for mapping in mappings:
        if ":" not in mapping and "=" not in mapping:
            raise UsageError(
                "A mapping must be given on the format X:Y=bbbb,\n"+
                "where X:Y is the range and bbbb is the binary format.")
        split = mapping.split("=")
        unparsed_ranges.append(split[0]) # Store ranges to be parsed with common function
        v = split[1]

        is_hex = v[:2].lower() == "0x"
        is_not_binary_string = not set(v).issubset({"0", "1"})
        if is_hex:
            parsed_values.append(bin(int(v, 16))[2:])
        elif is_not_binary_string:
            raise ValueError
        else:
            # Must be binary string at this point
            parsed_values.append(v)

        # Parse ranges, and raise error with ranges overlap
        try:
            warnings.filterwarnings("error", message="Detected overlap in the given ranges")
            warnings.filterwarnings("error", category=UserWarning, module="main")
            ranges = parse_ranges(None, None, unparsed_ranges)
        except UserWarning as e:
            raise ValueError(f"Range overlap not allowed: {e}\nRanges given: {unparsed_ranges}") from e
        slice_mapping = dict(zip(ranges, parsed_values))

    for bit_range, value in slice_mapping.items():
        correct_size_value = value_fit_range(bit_range, value)
        slice_mapping[bit_range] = correct_size_value
    sorted_slice_mapping = dict(sorted(slice_mapping.items(), reverse=True))
    return sorted_slice_mapping
