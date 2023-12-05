import portion as P
from dataclasses import dataclass
from functools import reduce
from portion.interval import Interval
from pathlib import Path


@dataclass
class Range:
    dest: int
    source: int
    size: int

    def map_range(self, v: Interval) -> bool:
        return P.closed(self.dest + (v.lower - self.source), self.dest + (v.upper - self.source))

    def contains(self, v: int) -> bool:
        return True if (self.source <= v < self.source + self.size) else False


def load(fpath: Path) -> list[list[Range]]:
    return ([int(i) for i in [b.split("\n") for b in fpath.read_text().split("\n\n")][0][0].split(": ")[1].split(" ")], [[Range(*[int(i) for i in s.split(" ")]) for s in m[1:]] for m in [b.split("\n") for b in fpath.read_text().split("\n\n")][1:]])


def apply_map(m: list[Range], input_range: Interval) -> list[Interval]:
    output_range = P.empty()
    for r in m:
        if not (ir := P.closed(r.source, r.source + r.size - 1)).overlaps(input_range):
            continue
        for subint in (ir & input_range):
            input_range -= subint
            output_range |= r.map_range(subint)
        if input_range.empty:
            return output_range
    return output_range | input_range


def find_min_location(maps: list[list[Range]], it: Interval) -> int:
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
