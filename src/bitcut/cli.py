"""
Click based CLI wrapper around engine.
"""

import click

from bitcut.engine import create_binary_slices, print_slice_mapping, mapping_to_ba, print_constructed_ba
from bitcut.parse import parse_ranges, parse_value, parse_mapping

CONTEXT_SETTINGS = {"help_option_names":['-h', '--help']}

@click.group(context_settings=CONTEXT_SETTINGS, help=
    "bitcut build -h, --help for more info about build COMMAND\n\n"
    "bitcut slice -h, --help for more info about slice COMMAND"
)
def cli():
    """
    Click CLI entrypoint, need this to have multiple commands like slice and build.
    """

@cli.command(name="slice")
@click.argument("value", required=True, callback=parse_value)
@click.argument("ranges", nargs=-1, required=False, callback=parse_ranges)
@click.option(
    "-n", "--n_bits", type=int, default=None,
    help="Number of bits of the value fit into "+
    "only needed to increase the number of bits"
)
def slice_cmd(value, ranges, n_bits):
    """Slice multiple binary slices from VALUE, ex: slice VALUE 5:3 x:y ...\n
    Will always show the whole slice first.

    VALUE: hex (0x34), decimal (52)\n
    RANGES: bit ranges like '31:26', '7:3', '3:0' (multiple allowed)

    Examples:\n
        slice 0x34 5:3 3:0 7:3 31:2\n
        slice 52 -n 32 7:0
    """
    if n_bits is None:
        n_bits = value.bit_length()
    s = create_binary_slices(value, ranges, n_bits=n_bits)
    print_slice_mapping(s)

@cli.command(name="splice")
@click.argument("mapping", nargs=-1, required=True, callback=parse_mapping)
def splice_cmd(mapping):
    """Builds a value from binary slices, ex: build 3:0=1100 5:3=1 7:3=011\n

    MAPPING: msb:lsb=binstr (multiple allowed)

    Example: build 3:0=1100 5:4=1
    """
    print_slice_mapping(mapping)
    ba = mapping_to_ba(mapping)
    print_constructed_ba(ba)

cli.add_command(slice_cmd)
cli.add_command(splice_cmd)

if __name__ == "__main__":
    cli()
