import portion as P
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from portion.interval import Interval


def load(fpath: Path) -> list[list[tuple[int, int, int]]]:
    return ([int(i) for i in [b.split("\n") for b in fpath.read_text().split("\n\n")][0][0].split(": ")[1].split(" ")], [[[int(i) for i in s.split(" ")] for s in m[1:]] for m in [b.split("\n") for b in fpath.read_text().split("\n\n")][1:]])


def apply_map(m: list[tuple[int, int, int]], input_range: Interval) -> list[Interval]:
    output_range = P.empty()
    for r in m:
        for subint in (P.closed(r[1], r[1] + r[2] - 1) & input_range):
            input_range -= subint
            output_range |= P.closed(r[0] + (subint.lower - r[1]), r[0] + (subint.upper - r[1]))
    return output_range | input_range


def find_min_location(maps: list[list[tuple[int, int, int]]], it: Interval) -> int:
    return it.lower if (len(maps) == 0) else find_min_location(maps[1:], apply_map(maps[0], it))


def part1(fpath: Path):
    return find_min_location(load(fpath)[1], reduce(lambda x, y: x | y, [P.singleton(s) for s in load(fpath)[0]]))


def part2(fpath: Path):
    return find_min_location(load(fpath)[1], reduce(lambda x, y: x | y, [P.closed(s, s + d - 1) for (s, d) in zip(load(fpath)[0][::2], load(fpath)[0][1::2])]))


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 35

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 313045984

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 46

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 20283860
