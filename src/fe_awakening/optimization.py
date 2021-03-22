from typing import Union
from . import models
from . import utils

from rich import print, pretty

pretty.install()

characters, weapons, classes = utils.load_data()


def count_children(character: models.Character) -> int:
    return 1 if character.child else 0


def find_min(character_list: list[models.Character]) -> Union[models.Character, None]:
    minimum = min(len(c.can_marry) for c in character_list if c.can_marry)
    least_options_character = next(
        c for c in character_list if c.can_marry and len(c.can_marry) == minimum
    )
    min_index = character_list.index(least_options_character)
    return character_list[min_index]


def find_best_partner(
    character: models.Character, character_list: list[models.Character]
) -> models.Character:

    character_children = count_children(character)
    max = 0
    best_partner = None
    for potential_partner in character.can_marry:
        partner_character = next(
            (c for c in character_list if c.name == potential_partner), None
        )
        if partner_character:
            potential_children = character_children + count_children(partner_character)
            if potential_children > max:
                max = potential_children
                best_partner = partner_character
    return best_partner


def remove_pair(
    pair: tuple[models.Character, models.Character],
    character_list: list[models.Character],
) -> list[models.Character]:
    chars_list = character_list.copy()
    p1_index = chars_list.index(pair[0])
    chars_list.pop(p1_index)
    p2_index = chars_list.index(pair[1])
    chars_list.pop(p2_index)
    return chars_list


def run_pairing(main_char_list: list[models.Character]) -> list[models.Character]:
    c1 = find_min(main_char_list)
    if not c1:
        return run_pairing([c for c in main_char_list if c != c1])
    p1 = find_best_partner(c1, main_char_list)
    if not p1:
        return run_pairing([c for c in main_char_list if c != c1])
    characters = remove_pair((c1, p1), main_char_list)
    print(
        f"Character: {c1.name} -- Partner: {p1.name} -- Kid Count: {count_children(c1) + count_children(p1)}"
    )
    return characters


def run_pair_optimization(character_list: list[models.Character]):
    chars = character_list.copy()
    list_len = len(chars)
    while list_len > 1:
        chars = run_pairing(chars)
        list_len = len(chars)
        print(list_len)


run_pair_optimization(characters)
