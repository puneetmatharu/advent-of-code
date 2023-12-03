import numpy as np
import re
from pathlib import Path


def load(fpath: Path) -> list[str]:
    return fpath.read_text().splitlines()


def part1(fpath: Path):
    grid = np.pad(np.array([list(l) for l in load(fpath)], dtype=str), 1, constant_values=".")
    return sum([v for (i, s, e, v) in [[i, *m.span(), int(m.group(0))] for (i, line) in enumerate(load(fpath)) for m in re.finditer(r"(\d+)", line)] if not all([c in "0123456789." for c in [*grid[i, s:e+2], *grid[i+1, [s, e+1]], *grid[i+2, s:e+2]]])])


def part2(fpath: Path):
    return sum([(n[0]*n[1] if len(n) == 2 else 0) for n in [[v for (iv, s, e, v) in [[i, m.span()[0], m.span()[1], int(m.group(0))] for (i, line) in enumerate(load(fpath)) for m in re.finditer(r"(\d+)", line)] if (ia, ja) in ((iv, s-1), (iv, e), *[(iv-1, j) for j in range(s-1, e+1)], *[(iv+1, j) for j in range(s-1, e+1)])] for (ia, ja) in [[i, m.span()[0]] for (i, line) in enumerate(load(fpath)) for m in re.finditer(r"(\*)", line)]]])


if __name__ == "__main__":
    output = part1(Path("example_data1.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 4361

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 532331

    output = part2(Path("example_data2.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 467835

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 82301120
