"""This module contains the data models for the game."""

from __future__ import annotations

from enum import Enum, auto
from typing import Union
from pydantic import BaseModel

# TODO: add use_enum_values to classes that use enums
# ? add validate_all to meta config of classes?


class Gender(int, Enum):
    F = auto()
    M = auto()


class WeaponType(int, Enum):
    AXE = auto()
    BEASTSTONE = auto()
    BOW = auto()
    DRAGONSTONE = auto()
    LANCE = auto()
    STAFF = auto()
    SWORD = auto()
    TOME = auto()


class Character(BaseModel):
    name: str
    gender: Gender
    unlock_episode: str
    class_options: Union[list[str], None] = None
    can_marry: Union[list[str], None] = None
    child: Union[str, None] = None


class Skill(BaseModel):
    name: str
    unlock_level: int
    # activation_rate: str
    description: str


class StarterClass(BaseModel):
    name: str
    hitpoints: int
    strength: int
    magic: int
    skill: int
    speed: int
    luck: int
    defense: int
    resistance: int
    promotes_to: list[str]
    gender_lock: Union[str, None] = None
    abilities: Union[list[Skill], None] = None
    weapon_options: Union[list[WeaponType], None] = None


class AdvancedClass(BaseModel):
    name: str
    hitpoints: int
    strength: int
    magic: int
    skill: int
    speed: int
    luck: int
    defense: int
    resistance: int
    gender_lock: Union[str, None] = None
    abilities: Union[list[Skill], None] = None
    weapon_options: Union[list[WeaponType], None] = None


class Weapon(BaseModel):
    name: str
    rank: str
    might: int
    to_hit: int
    to_crit: int
    uses: int
    worth: int
    kind: WeaponType
