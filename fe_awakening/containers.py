"""

This module contains the data containers 
representing the graph nodes and relationships
"""

from py2neo.ogm import Model, Property, Related, RelatedTo


class Character(Model):
    __primarykey__ = "name"
    name = Property()
    unlocks = Property()
    gender = Property()

    MARRY = Related("Character")
    PARENT_OF = RelatedTo("Character")


class Skill(Model):
    __primarykey__ = "name"
    name = Property()
    level = Property()
    activation = Property()
    description = Property()


class StarterClass(Model):
    __primarykey__ = "name"
    name = Property()
    hitpoints = Property()
    strength = Property()
    magic = Property()
    skill = Property()
    speed = Property()
    luck = Property()
    defense = Property()
    resistance = Property()
    gender_lock = Property()

    PROMOTES_TO = RelatedTo("AdvancedClass")
    HAS_ABILITY = RelatedTo("Skill")
    USES = RelatedTo("WeaponType")


class AdvancedClass(Model):
    __primarykey__ = "name"
    name = Property()
    hitpoints = Property()
    strength = Property()
    magic = Property()
    skill = Property()
    speed = Property()
    luck = Property()
    defense = Property()
    resistance = Property()
    gender_lock = Property()

    HAS_ABILITY = RelatedTo("Skill")
    USES = RelatedTo("WeaponType")


class WeaponType(Model):
    __primarykey__ = "name"
    name = Property()


class Weapon(Model):
    __primarykey__ = "name"
    name = Property()
    rank = Property()
    might = Property()
    hit = Property()
    crit = Property()
    uses = Property()
    worth = Property()

    TYPE = RelatedTo("WeaponType")
