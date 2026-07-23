#!/usr/bin/env python3
"""Deterministically cast a three-number I Ching hexagram."""

import argparse
import json


TRIGRAMS = {
    1: {"name": "乾", "image": "天", "lines": [1, 1, 1]},
    2: {"name": "兑", "image": "泽", "lines": [1, 1, 0]},
    3: {"name": "离", "image": "火", "lines": [1, 0, 1]},
    4: {"name": "震", "image": "雷", "lines": [1, 0, 0]},
    5: {"name": "巽", "image": "风", "lines": [0, 1, 1]},
    6: {"name": "坎", "image": "水", "lines": [0, 1, 0]},
    7: {"name": "艮", "image": "山", "lines": [0, 0, 1]},
    8: {"name": "坤", "image": "地", "lines": [0, 0, 0]},
}

# Rows are upper trigrams 1..8; columns are lower trigrams 1..8.
HEXAGRAM_NAMES = [
    ["乾", "天泽履", "天火同人", "天雷无妄", "天风姤", "天水讼", "天山遁", "天地否"],
    ["泽天夬", "兑", "泽火革", "泽雷随", "泽风大过", "泽水困", "泽山咸", "泽地萃"],
    ["火天大有", "火泽睽", "离", "火雷噬嗑", "火风鼎", "火水未济", "火山旅", "火地晋"],
    ["雷天大壮", "雷泽归妹", "雷火丰", "震", "雷风恒", "雷水解", "雷山小过", "雷地豫"],
    ["风天小畜", "风泽中孚", "风火家人", "风雷益", "巽", "风水涣", "风山渐", "风地观"],
    ["水天需", "水泽节", "水火既济", "水雷屯", "水风井", "坎", "水山蹇", "水地比"],
    ["山天大畜", "山泽损", "山火贲", "山雷颐", "山风蛊", "山水蒙", "艮", "山地剥"],
    ["地天泰", "地泽临", "地火明夷", "地雷复", "地风升", "地水师", "地山谦", "坤"],
]

LINE_NAMES = {1: "初爻", 2: "二爻", 3: "三爻", 4: "四爻", 5: "五爻", 6: "上爻"}


def normalized_remainder(value, modulus):
    remainder = value % modulus
    return remainder if remainder else modulus


def trigram_number(lines):
    for number, trigram in TRIGRAMS.items():
        if trigram["lines"] == lines:
            return number
    raise ValueError(f"Unknown trigram lines: {lines}")


def describe_trigram(number):
    trigram = TRIGRAMS[number]
    return f'{trigram["name"]}（{trigram["image"]}）'


def hexagram_name(upper, lower):
    return HEXAGRAM_NAMES[upper - 1][lower - 1]


def cast(first, second, third):
    lower = normalized_remainder(first, 8)
    upper = normalized_remainder(second, 8)
    moving = normalized_remainder(third, 6)

    lines = TRIGRAMS[lower]["lines"] + TRIGRAMS[upper]["lines"]
    original_line = lines[moving - 1]
    changed_lines = list(lines)
    changed_lines[moving - 1] = 1 - original_line

    changed_lower = trigram_number(changed_lines[:3])
    changed_upper = trigram_number(changed_lines[3:])

    return {
        "input": [first, second, third],
        "original": {
            "name": hexagram_name(upper, lower),
            "upper": describe_trigram(upper),
            "lower": describe_trigram(lower),
            "lines_bottom_to_top": lines,
        },
        "moving_line": {
            "position": moving,
            "name": LINE_NAMES[moving],
            "change": "阳变阴" if original_line else "阴变阳",
        },
        "changed": {
            "name": hexagram_name(changed_upper, changed_lower),
            "upper": describe_trigram(changed_upper),
            "lower": describe_trigram(changed_lower),
            "lines_bottom_to_top": changed_lines,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Cast a hexagram from three integers.")
    parser.add_argument("first", type=int, help="First number: lower trigram")
    parser.add_argument("second", type=int, help="Second number: upper trigram")
    parser.add_argument("third", type=int, help="Third number: moving line")
    args = parser.parse_args()
    print(json.dumps(cast(args.first, args.second, args.third), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

