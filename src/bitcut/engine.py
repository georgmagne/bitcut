"""
Module to do the data processing, assumes data is parsed beforehand.
"""

from bitstring import BitArray

def flip_idx(idx_to_flip: int, total_bits: int) -> int:
    """
    Flips an index to index a list from the opposite side, to make it easier to index bitstrings from LSB first.
    :param idx_to_flip: Int of the index to flip
    :param total_bits: Int number of elements in the list to be inrexed.
    :return: The flipped index as Int.
    """
    highest_idx = total_bits - 1
    new_idx = highest_idx - idx_to_flip
    return new_idx

def round_up_to_multiple(n: int, multiple:int=4) -> int:
    """
    Round up to nearest multiple of some factor.
    :param n: Int to round up
    :param multiple: Int of multiple to round up to (default=4)
    """
    if (n % multiple) == 0:
        return n
    return n + (multiple - n % multiple)

def mapping_to_ba(slice_mapping: dict[tuple[int, int], str]) -> BitArray:
    """
    Turn a dict with tuple of MSB:LSB and a string representing a binary into a bitstring.BitArray.
    :param slice_mapping: dict with tuple(MSB,LSB) as key and the binsary string representation as the value.
    :return: BitArray with the value of the given range mappings, with zeros added where no range is given.
    Length is the highes value in the ranges given rounded up to nearest nibble.
    """
    # Create blank bit array
    total_bits = max(max(slice_mapping.keys())) + 1
    total_bits = round_up_to_multiple(total_bits, multiple=4)
    ba = BitArray(length=total_bits)

    # Place each slice at correct position
    for (msb, _), binstr in slice_mapping.items():
        idx = flip_idx(msb, total_bits)
        ba.overwrite("0b"+binstr, idx)
    return ba

def create_binary_slices(value: int, ranges: list[tuple[int, int]], n_bits:int = 32) -> dict[tuple[int, int]: str]:
    """
    Creates a dict with tuples(MSB,LSB) as key and a str defining the binary.
    :param value: The hex/decimal value to slice with the given ranges. Where no range is given a single bit is added.
    :param ranges: Ranges to slice value with.
    :param n_bits: Number of bits the value should represent.
    :return: dict with tuples(MSB,LSB)=binstr
    """
    ba = BitArray(uint=value, length=n_bits)
    slice_mapping = {}
    whole_bin_slice = {(n_bits-1, 0): ba.bin}
    ba.reverse()
    for r in ranges:
        msb = r[0]
        lsb = r[1]
        if msb >= n_bits:
            raise ValueError("Slice index is higer than the number of bits of the given value.")
        ba_slice = ba.bin[lsb:msb+1]
        slice_mapping[r] = ba_slice[::-1]
    sorted_slice_mapping = whole_bin_slice | dict(sorted(slice_mapping.items(), reverse=True))
    return sorted_slice_mapping

def print_slice_mapping(slice_mapping: dict[tuple[int, int]: str]):
    """
    Print a slice mapping dict.
    :param slice_mapping: dict with tuples(MSB,LSB)=binstr
    """
    highest_idx = max(max(slice_mapping.keys()))
    n_digits = len(str(highest_idx))
    for r, s in slice_mapping.items():
        msb = r[0]
        lsb = r[1]
        print(f"[{msb:>{n_digits}}:{lsb:<{n_digits}}] - b'{s}'")

def print_constructed_ba(ba: BitArray):
    """ Prints a given bitstring.BitArray as binary string, hex and decimal.
    :param ba: BitArry to print.
    """
    print(f"Binary String: {ba.bin}")
    print(f"Hexadecimal  : 0x{ba.hex}")
    print(f"Unsigned int : {ba.uint}")
