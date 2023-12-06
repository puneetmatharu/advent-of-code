import re
from math import prod
from pathlib import Path


def load(f: Path) -> list[str]:
    return [[int(i) for i in re.sub(r"\s+", " ", l).split(": ")[1].split(" ")] for l in f.read_text().splitlines()]


def part1(file: Path):
    return prod([sum([i * (t - i) > d for i in range(1, t)]) for (t, d) in list(zip(*load(file)))])


def part2(file: Path):
    return prod([sum([i * (t - i) > d for i in range(1, t)]) for (t, d) in [(int("".join([str(i) for i in load(file)[0]])), int("".join([str(i) for i in load(file)[1]])))]])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 288

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 800280

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 71503

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 45128024
