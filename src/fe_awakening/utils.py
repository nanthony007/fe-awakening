"""This module provides utilities for loading data."""

import json
import csv
from typing import Union
from . import models

from rich import print


# TODO: remove all csv functionality and only read from json
# ! OR
# TODO: make functionality for 'update' to update the main json record from \
# the csv files and then separate load functionality to load from main package data file

# TODO: fix marriage options, not correctly listed in csv file


def _set_children(characters: list[models.Character]) -> list[models.Character]:
    with open("data/children.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            parent = next(c for c in characters if c.name == row.get("Main"))
            child = next(c for c in characters if c.name == row.get("Child"))
            parent.child = child.name
    return characters


def _set_partners(characters: list[models.Character]) -> list[models.Character]:
    with open("data/marriages2.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            options = row.get("MarriageOptions")
            if options:
                c1 = next(c for c in characters if c.name == row.get("Character"))
                partners = [c for c in characters if c.name in options.split("-")]
                c1.can_marry = [p.name for p in partners]
    return characters


def update_characters():
    # characters.csv
    # children.csv
    # marriages.csv
    characters: list[models.Character] = []
    with open("data/characters.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            character = models.Character(
                name=row.get("Name", ""),
                gender=models.Gender[row.get("Gender", "")],
                unlock_episode=row.get("UnlockLvl", ""),
                class_options=row.get("OptionsList").split("-"),
            )
            characters.append(character)
    characters_with_children = _set_children(characters)
    characters_with_partners = _set_partners(characters_with_children)

    with open("data/data.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    data["characters"] = [c.dict() for c in characters_with_partners]
    with open("data/data.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, sort_keys=True, indent=4)

    return characters


def update_weapons():
    # weapons.csv
    weapons = []
    with open("data/weapons.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            weapon = models.Weapon(
                name=row.get("Name"),
                rank=row.get("Rank"),
                might=row.get("Might"),
                to_hit=row.get("Hit"),
                to_crit=row.get("Crit"),
                uses=row.get("Uses"),
                worth=row.get("Worth"),
                kind=models.WeaponType[row.get("Type").upper()],
            )
            weapons.append(weapon)
    with open("data/data.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    data["weapons"] = [w.dict() for w in weapons]
    with open("data/data.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, sort_keys=True, indent=4)
    return weapons


def update_classes():
    # class_stats.csv
    # promotions.csv
    # weapon_types.csv
    # skills.csv
    class_list: list[Union[models.StarterClass, models.AdvancedClass]] = []

    with open("data/weapon_types.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        weapons = {
            row.get("BaseClass"): row.get("Weapons").split("-") for row in csvread
        }

    with open("data/promotions.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        promotions = {
            row.get("BaseClass"): row.get("AdvancedClassOptions").split("-")
            for row in csvread
        }

    with open("data/skills.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        skills = [
            (row.get("Skill"), row.get("Class"), row.get("Level"), row.get("Effect"))
            for row in csvread
        ]

    with open("data/class_stats.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            if row.get("Tier") == "base":
                c = models.StarterClass(
                    name=row.get("ClassName"),
                    hitpoints=row.get("HitPoints"),
                    strength=row.get("Strength"),
                    magic=row.get("Magic"),
                    skill=row.get("Skill"),
                    speed=row.get("Speed"),
                    luck=row.get("Luck"),
                    defense=row.get("Defense"),
                    resistance=row.get("Resistance"),
                    promotes_to=promotions.get(row.get("ClassName")),
                    abilities=[
                        models.Skill(
                            name=skill[0], unlock_level=skill[2], description=skill[-1]
                        )
                        for skill in skills
                        if skill[1] == row.get("ClassName")
                    ],
                    weapon_options=[
                        models.WeaponType[w.upper()]
                        for w in weapons.get(row.get("ClassName"))
                    ],
                )
                if gender := row.get("GenderLock"):
                    c.gender_lock = gender
                class_list.append(c)
            elif row.get("Tier") == "adv":
                c = models.AdvancedClass(
                    name=row.get("ClassName"),
                    hitpoints=row.get("HitPoints"),
                    strength=row.get("Strength"),
                    magic=row.get("Magic"),
                    skill=row.get("Skill"),
                    speed=row.get("Speed"),
                    luck=row.get("Luck"),
                    defense=row.get("Defense"),
                    resistance=row.get("Resistance"),
                    abilities=[
                        models.Skill(
                            name=skill[0], unlock_level=skill[2], description=skill[-1]
                        )
                        for skill in skills
                        if skill[1] == row.get("ClassName")
                    ],
                    weapon_options=[
                        models.WeaponType[w.upper()]
                        for w in weapons.get(row.get("ClassName"))
                    ],
                )
                if gender := row.get("GenderLock"):
                    c.gender_lock = gender
                class_list.append(c)
    with open("data/data.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    data["classes"] = [c.dict() for c in class_list]
    with open("data/data.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, sort_keys=True, indent=4)
    return class_list


# ? needed?
def update_skills():
    # skills.csv
    skills = []
    with open("data/skills.csv", "r", encoding="utf-8-sig") as f:
        csvread = csv.DictReader(f)
        for row in csvread:
            skill = models.Skill(
                name=row.get("Skill"),
                level_unlocked=row.get("Level"),
                description=row.get("Effect"),
            )
            skills.append(skill)
    return skills


def load_data() -> tuple[
    list[models.Character],
    list[models.Weapon],
    list[Union[models.StarterClass, models.AdvancedClass]],
]:
    with open("data/data.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    characters = [models.Character(**c) for c in data["characters"]]
    weapons = [models.Weapon(**c) for c in data["weapons"]]
    classes = [
        models.StarterClass(**c) if c.get("promotes_to") else models.AdvancedClass(**c)
        for c in data["classes"]
    ]
    return characters, weapons, classes
