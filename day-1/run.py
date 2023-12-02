import re
from pathlib import Path


def load(f: Path) -> list[str]:
    return f.read_text().splitlines()


def num_replace(x, l=list(enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]))):
    return x if (l == []) else num_replace(x.replace(l[0][1], f"{l[0][1]}{l[0][0]+1}{l[0][1]}"), l[1:])


def part1(file: Path):
    return sum([int("".join([re.findall("\d", line)[i] for i in (0, -1)])) for line in load(file)])


def part2(file: Path):
    return sum([int("".join([re.findall("\d", num_replace(line))[i] for i in (0, -1)])) for line in load(file)])


if __name__ == "__main__":
    output = part1(Path("example_data1.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 142

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 55488

    output = part2(Path("example_data2.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 281

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 55614
