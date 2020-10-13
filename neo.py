import pandas as pd
from py2neo import Graph, Node, Relationship
from py2neo.ogm import Model, Label, RelatedFrom, RelatedTo, Related, Repository
from py2neo.matching import NodeMatcher


class Skill(Model):
    __primarykey__ = "name"
    name = Label()
    level = Label()
    activation = Label()
    description = Label()


class StarterClass(Model):
    __primarykey__ = "name"
    name = Label()
    hitpoints = Label()
    strength = Label()
    magic = Label()
    skill = Label()
    speed = Label()
    luck = Label()
    defense = Label()
    resistance = Label()
    gender_lock = Label()

    PROMOTES_TO = RelatedTo("AdvancedClass")
    ACCESSESS = RelatedTo("Ability")
    USES = RelatedTo("WeaponType")


class AdvancedClass(Model):
    __primarykey__ = "name"
    name = Label()
    hitpoints = Label()
    strength = Label()
    magic = Label()
    skill = Label()
    speed = Label()
    luck = Label()
    defense = Label()
    resistance = Label()
    gender_lock = Label()

    ACCESSESS = RelatedTo("Ability")
    USES = RelatedTo("WeaponType")


class WeaponType(Model):
    __primarykey__ = "name"
    name = Label()

    INCLUDES = RelatedTo("Weapon")


class Weapon(Model):
    __primarykey__ = "name"
    name = Label()
    rank = Label()
    might = Label()
    hit = Label()
    crit = Label()
    uses = Label()
    worth = Label()


class MainCharacter(Model):
    __primarykey__ = "name"
    name = Label()
    unlocks = Label()
    gender = Label()

    RECLASSES = RelatedTo("StarterClass")
    PARENTS = RelatedTo("ChildCharacter")
    MARRY = Related("MainCharacter")
    MARRY = Related("ChildCharacter")


class ChildCharacter(Model):
    __primarykey__ = "name"
    name = Label()
    unlocks = Label()
    gender = Label()

    RECLASSES = RelatedTo("StarterClass")


# creates classes
def create_class_nodes(graph):
    class_stats = pd.read_csv("class_stats.csv")

    tx = graph.begin()
    for i, row in class_stats.iterrows():
        if row.Tier == "base":
            tx.create(
                Node(
                    "StarterClass",
                    name=row.ClassName,
                    hitpoints=row.HitPoints,
                    strength=row.Strength,
                    magic=row.Magic,
                    skill=row.Skill,
                    luck=row.Luck,
                    speed=row.Speed,
                    defense=row.Defense,
                    resistance=row.Resistance,
                    gender_lock=row.GenderLock,
                )
            )
        elif row.Tier == "adv":
            tx.create(
                Node(
                    "AdvancedClass",
                    name=row.ClassName,
                    hitpoints=row.HitPoints,
                    strength=row.Strength,
                    magic=row.Magic,
                    skill=row.Skill,
                    luck=row.Luck,
                    speed=row.Speed,
                    defense=row.Defense,
                    resistance=row.Resistance,
                    gender_lock=row.GenderLock,
                )
            )
    tx.commit()


# creates links between start and advanced classes
def link_classes(graph):
    promotions = pd.read_csv("promotions.csv")

    tx = graph.begin()
    for _, row in promotions.iterrows():
        nodes = NodeMatcher(graph)

        if row.BaseClass == "Villager":
            starter = nodes.match("StarterClass").where(name=row.BaseClass).first()
            options = row.AdvancedClassOptions.split("-")
            for promotion in options:
                p = nodes.match("StarterClass", name=promotion).first()
                rel = Relationship(starter, "PROMOTES_TO", p)
                tx.create(rel)
        else:
            starter = nodes.match("StarterClass").where(name=row.BaseClass).first()

            # handles classes with no promotions like Manakete or Taguel
            options = (
                row.AdvancedClassOptions.split("-")
                if type(row.AdvancedClassOptions) == str
                else None
            )

            if options:
                for promotion in options:
                    p = nodes.match("AdvancedClass").where(name=promotion).first()
                    rel = Relationship(starter, "PROMOTES_TO", p)
                    tx.create(rel)
    tx.commit()


# adds WeaponType nodes
def add_weapon_types(graph):
    tx = graph.begin()
    weapons_list = [
        "Axe",
        "Sword",
        "Lance",
        "DragonStone",
        "BeastStone",
        "Tome",
        "Staff",
        "Bow",
    ]
    for weapon_type in weapons_list:
        tx.create(Node("WeaponType", name=weapon_type))
    tx.commit()


# adds WeaponType relationship to classes
def link_weapon_types_to_classes(graph):
    weapon_types = pd.read_csv("weapon_types.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)
    class_node_list = []
    # get all StarterClasses
    sc = nodes.match("StarterClass").all()
    # get all AdvancedClasses
    ac = nodes.match("AdvancedClass").all()
    class_node_list.extend(sc)
    class_node_list.extend(ac)
    for c in class_node_list:
        weapons_string = (
            weapon_types[weapon_types["BaseClass"] == c.get("name")]
            .Weapons.iloc[0]
            .split("-")
        )
        for weapon in weapons_string:
            w = nodes.match("WeaponType").where(name=weapon.strip()).first()
            tx.create(Relationship(c, "USES", w))
    tx.commit()


# adds weapon nodes with links to types
def add_weapons(graph):
    weapons = pd.read_csv("weapons.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)

    for _, row in weapons.iterrows():
        weapon_type = nodes.match("WeaponType").where(name=row.Type).first()
        weapon_node = Node(
            "Weapon",
            name=row.Name,
            rank=row.Rank,
            might=row.Might,
            hit=row.Hit,
            crit=row.Crit,
            uses=row.Uses,
            worth=row.Worth,
        )
        tx.create(weapon_node)
        tx.create(Relationship(weapon_type, "INCLUDES", weapon_node))
    tx.commit()


# adds characters with links to reclass StarterClasses
def add_characters(graph):
    characters = pd.read_csv("characters.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)

    for _, row in characters.iterrows():
        if row.Type == "Main":
            c = Node(
                "MainCharacter", name=row.Name, unlocks=row.UnlockLvl, gender=row.Gender
            )
            potential_classes = []
            for x in row.OptionsList.split("-"):
                m1 = nodes.match("StarterClass").where(name=x).first()
                m2 = nodes.match("AdvancedClass").where(name=x).first()
                if m1:
                    potential_classes.append(m1)
                if m2:
                    potential_classes.append(m2)

            tx.create(c)
            for p in potential_classes:
                tx.create(Relationship(c, "RECLASSES", p))
        elif row.Type == "Child":
            c = Node(
                "ChildCharacter",
                name=row.Name,
                unlocks=row.UnlockLvl,
                gender=row.Gender,
            )
            potential_classes = []
            for x in row.OptionsList.split("-"):
                m1 = nodes.match("StarterClass").where(name=x).first()
                m2 = nodes.match("AdvancedClass").where(name=x).first()
                if m1:
                    potential_classes.append(m1)
                if m2:
                    potential_classes.append(m2)

            tx.create(c)
            for p in potential_classes:
                tx.create(Relationship(c, "RECLASSES", p))
    tx.commit()


# adds child relationship to parents
def add_children(graph):
    kids = pd.read_csv("children.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)

    for _, row in kids.iterrows():
        p = nodes.match("MainCharacter").where(name=row.Main).first()
        c = nodes.match("ChildCharacter").where(name=row.Child).first()
        tx.create(
            Relationship(
                p,
                "PARENTS",
                c,
            )
        )
    tx.commit()


# adds friendships and marriages and children
def add_marriages(graph):
    marriages = pd.read_csv("marriages.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)

    for _, row in marriages.iterrows():
        if not isinstance(row.MarryOptions, str):
            continue
        options = row.MarryOptions.split("-")
        for opt in options:
            n1 = nodes.match("MainCharacter").where(name=opt).first()
            if n1:
                c1 = nodes.match("MainCharacter").where(name=row.Character).first()
                if c1:
                    tx.create(Relationship(n1, "MARRY", c1))
                else:
                    c2 = nodes.match("ChildCharacter").where(name=row.Character).first()
                    tx.create(Relationship(n1, "MARRY", c2))
            else:
                n2 = nodes.match("ChildCharacter").where(name=opt).first()
                c1 = nodes.match("MainCharacter").where(name=row.Character).first()
                if c1:
                    tx.create(Relationship(n2, "MARRY", c1))
                else:
                    c2 = nodes.match("ChildCharacter").where(name=row.Character).first()
                    tx.create(Relationship(n2, "MARRY", c2))

        # manually do MU and FU
        females = nodes.match("MainCharacter").where(gender="F").all()
        males = nodes.match("MainCharacter").where(gender="M").all()
        females.extend(nodes.match("ChildCharacter").where(gender="F").all())
        males.extend(nodes.match("ChildCharacter").where(gender="M").all())

        mu = nodes.match("MainCharacter").where(name="Avatar (M)").first()
        fu = nodes.match("MainCharacter").where(name="Avatar (F)").first()
        for partner in females:
            tx.create(Relationship(mu, "MARRY", partner))
        for partner in males:
            tx.create(Relationship(fu, "MARRY", partner))
    tx.commit()


# adds skill nodes and connections to classes
def add_skills(graph):
    skills = pd.read_csv("skills.csv")
    tx = graph.begin()
    nodes = NodeMatcher(graph)
    for _, row in skills.iterrows():
        c = nodes.match("StarterClass").where(name=row.Class).first()
        if not c:
            c = nodes.match("AdvancedClass").where(name=row.Class).first()
        s = Node(
            "Skill",
            name=row.Skill,
            activation=row.Activation,
            level=row.Level,
            description=row.Effect,
        )
        tx.create(s)
        tx.create(Relationship(c, "ACCESSES", s))
    tx.commit()


def populate_graph(graph):
    print("Adding class nodes...")
    create_class_nodes(graph)
    print("Linking classes...")
    link_classes(graph)
    print("Adding weapon types...")
    add_weapon_types(graph)
    print("Linking weapon types to classes...")
    link_weapon_types_to_classes(graph)
    print("Adding weapons...")
    add_weapons(graph)
    print("Adding characters...")
    add_characters(graph)
    print("Adding children relationships...")
    add_children(graph)
    print("Adding marriage relationships...")
    add_marriages(graph)
    print("Adding skills...")
    add_skills(graph)


if __name__ == "__main__":
    graph = Graph("bolt://localhost:7687", user="neo4j", password="nick0709")
    populate_graph(graph)
