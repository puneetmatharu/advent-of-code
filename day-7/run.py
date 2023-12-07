from enum import IntEnum
from pathlib import Path


class HandType(IntEnum):
    FIVEOFAKIND = 7
    FOUROFAKIND = 6
    FULLHOUSE = 5
    THREEOFAKIND = 4
    TWOPAIR = 3
    ONEPAIR = 2
    HIGHCARD = 1


def load(f: Path) -> list[str]:
    return [[list(l.split(" ")[0]), int(l.split(" ")[1])] for l in f.read_text().splitlines()]


def get_card_rank(c: str, enable_joker: bool) -> int:
    return "J23456789TQKA".index(c) if enable_joker else "23456789TJQKA".index(c)


def get_hand_type(cards: list[str], enable_joker: bool) -> HandType:
    uniq_cards = set(cards)
    counts = [cards.count(uc) for uc in uniq_cards]
    match len(uniq_cards):
        case 1:
            return HandType.FIVEOFAKIND
        case 2:
            return HandType.FOUROFAKIND if 4 in counts else HandType.FULLHOUSE
        case 3:
            return HandType.THREEOFAKIND if (3 in counts) else HandType.TWOPAIR
        case 4:
            return HandType.ONEPAIR
        case 5:
            return HandType.HIGHCARD
    raise ValueError(cards)


def get_str_value(hb: tuple[list[str], int], enable_joker: bool) -> str:
    def get_value(hand, bid="0"):
        return "".join([
            f"{get_hand_type(hand, enable_joker):02d}",
            *[f"{get_card_rank(c, enable_joker):02d}" for c in hand],
            f"{bid:03}"
        ])
    if enable_joker and "J" in hb[0]:
        print(f"{''.join(hb[0])} --> ", end="")
        uniq_non_joker_cards = list(set(hb[0]) ^ set("J"))
        num_joker = hb[0].count("J")
        if num_joker == 5:
            hb[0] = ["A"] * 5
        elif (num_joker == 4) or (len(uniq_non_joker_cards) == 1):
            hb[0] = uniq_non_joker_cards * 5
        elif num_joker == 3:
            (oc1, oc2) = uniq_non_joker_cards
            other_card = oc1 if get_card_rank(oc1, True) > get_card_rank(oc2, True) else oc2
            hb[0] = "".join(hb[0]).replace("J", other_card)
        elif (num_joker == 2) and (len(uniq_non_joker_cards) == 2):
            (oc1, oc2) = uniq_non_joker_cards
            other_card = oc1 if hb[0].count(oc1) > hb[0].count(oc2) else oc2
            hb[0] = "".join(hb[0]).replace("J", other_card)
        elif num_joker == 2:
            best_hand = []
            max_hand_value = ""
            for c1 in "23456789TQKA":
                for c2 in "23456789TQKA":
                    new_hand = list("".join(hb[0]).replace("J", c1, 1).replace("J", c2, 1))
                    if (hv := get_value(new_hand)) > max_hand_value:
                        max_hand_value = hv
                        best_hand = new_hand
            hb[0] = best_hand
        elif num_joker == 1:
            best_hand = []
            max_hand_value = ""
            for c1 in "23456789TQKA":
                new_hand = list("".join(hb[0]).replace("J", c1))
                if (hv := get_value(new_hand)) > max_hand_value:
                    max_hand_value = hv
                    best_hand = new_hand
            hb[0] = best_hand
        print(f"{''.join(hb[0])}")
    return get_value(hb[0], hb[1])


def part1(fpath: Path):
    return sum([(i + 1) * bid for (i, (_, bid)) in enumerate(sorted(load(fpath), key=lambda x : get_str_value(x, enable_joker=False)))])


def part2(fpath: Path):
    for (h, b) in sorted(load(fpath), key=lambda x : get_str_value(x, enable_joker=True)):
        print("".join(h), b)
    return sum([(i + 1) * bid for (i, (_, bid)) in enumerate(sorted(load(fpath), key=lambda x : get_str_value(x, enable_joker=True)))])


if __name__ == "__main__":
    output = part1(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 1 output: {output}")
    assert output == 6440

    output = part1(Path("test_data.txt"))
    print(f"[TEST] Part 1 output: {output}")
    assert output == 250453939

    output = part2(Path("example_data.txt"))
    print(f"[EXAMPLE] Part 2 output: {output}")
    assert output == 5905

    output = part2(Path("test_data.txt"))
    print(f"[TEST] Part 2 output: {output}")
    assert output == 248698819 and output not in (output == 248648771, 248698819, 248649960)
    # low: 248648771, high: 248698819
    # NOT RIGHT 248649960
