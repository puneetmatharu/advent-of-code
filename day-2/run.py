from math import prod
from pathlib import Path


def load(f: Path) -> list[list[dict]]:
    return [{c:max([sg.get(c, 0) for sg in[{c[0]:int(j) for (j, c) in (c.split(" ") for c in s.split(", "))} for s in g.split(": ")[1].split("; ")]]) for c in ("r", "g", "b")} for g in f.read_text().splitlines()]


def part1(file: Path):
    return sum([i + 1 for (i, gm) in enumerate(load(file)) if all([gm[c] <= {"r": 12, "g": 13, "b": 14}[c] for c in ("r", "g", "b")])])


def part2(file: Path):
    return sum([prod(game_maxes.values()) for game_maxes in load(file)])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 8

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 1931

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 2286

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 83105
