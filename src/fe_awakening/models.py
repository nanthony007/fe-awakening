"""This module contains the data models for the game."""

from __future__ import annotations

from enum import Enum, auto
from typing import Union

from pydantic import BaseModel
from pydantic.main import BaseConfig

# TODO: add use_enum_values to classes that use enums
# ? add validate_all to meta config of classes?


class Gender(Enum):
    FEMALE = auto()
    MALE = auto()


class WeaponType(Enum):
    AXE = auto()
    BEASTSTONE = auto()
    BOW = auto()
    DRAGONSTONE = auto()
    LANCE = auto()
    STAFF = auto()
    SWORD = auto()
    TOME = auto()


class MyConfig(BaseConfig):
    frozen = True
    use_enum_values = True


class Character(BaseModel, config=MyConfig):
    name: str
    unlock_lvl: int
    gender: Gender
    can_marry: tuple[Character]
    child: Character


class Skill(BaseModel, config=MyConfig):
    name: str
    level_unlocked: int
    # activation_rate: str
    description: str


class StarterClass(BaseModel, config=MyConfig):
    name: str
    hitpoints: int
    strength: int
    magic: int
    skill: int
    speed: int
    luck: int
    defense: int
    resistance: int
    gender_lock: Union[Gender, None] = None
    abilities: tuple[Skill]
    uses: tuple[Weapon]
    promotes_to: tuple[AdvancedClass]


class AdvancedClass(BaseModel, config=MyConfig):
    name: str
    hitpoints: int
    strength: int
    magic: int
    skill: int
    speed: int
    luck: int
    defense: int
    resistance: int
    gender_lock: Gender
    abilities: tuple[Skill]
    uses: tuple[Weapon]


class Weapon(BaseModel, config=MyConfig):
    name: str
    rank: str
    might: int
    to_hit: int
    to_crit: int
    uses: int
    worth: int
    kind: WeaponType


Character.update_forward_refs()
