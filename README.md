# bitcut

A simple CLI for slicing and splicing binary bit ranges. Aimed at embedded style bit‑field hacking and quick validation against datasheets.

- Ever been annoyed with double checking if the hexadecimal value you are writing to a register actually set specifc bits you want to set? 

- Tired of decoding hex/decimals to see which bits are actually set and triple checking with a datasheet?

Look no further! Bitcut makes it easy to go from binary strings to hex and vice versa.

- **slice** a value into bit ranges,
- **splice** a value from ranges.

For bit‑field hacking, protocol specs and embedded.

---

## Example Usage

Slice a value into bit ranges:

```bash
$ bitcut slice 0x42 6:4 3:0
[6:0] - b'1000010' # Full Slice
[6:4] - b'100'
[3:0] - b'0010'
```

Splice a value from bit ranges:

```bash
$ bitcut splice 6:4=100 3:0=0010
[6:4] - b'100'
[3:0] - b'0010'
Binary String: 01000010
Hexadecimal  : 0x42
Unsigned int : 66
```

See full help:

```bash
$ bitcut --help
$ bitcut slice --help
$ bitcut splice --help
```

---

## Installation
From PyPI:

```bash
pip install bitcut
```

From a local checkout:

```bash
pip install .
```

(Requires Python ≥3.10.)

---

## Development

This repo uses `uv` for development

```bash
uv venv
uv sync              # installs dependencies + dev deps
uv pip install -e .
```

Run tests (coverage via `pytest.ini`):

```bash
uv run pytest
```

Coverage HTML report is written to `htmlcov/index.html`.

---

## License

MIT
