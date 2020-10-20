import csv

import containers
from py2neo.ogm import Repository

# TODO: Add Weapon Type links, Promotions, Marriages, and Children relationships


def create_repo() -> Repository:
    return Repository("bolt://neo4j@localhost:7687", password="nick0709")


def create_characters(repo: Repository):
    file_path = "data/characters.csv"
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for i, line in enumerate(csv_reader):
            if i == 0:
                print(f'Column names are {", ".join(line)}')

            print(
                f"{line['Name']}, {line['OptionsList']}, {line['Type']}, {line['Gender']}, {line['UnlockLvl']}"
            )
        print(f"Processed {i} lines.")


def create_skills(repo: Repository):
    file_path = "data/skills.csv"
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for i, line in enumerate(csv_reader):
            if i == 0:
                print(f'Column names are {", ".join(line)}')

            print(
                f"{line['Skill']}, {line['Class']}, {line['Level']}, {line['Activation']}, {line['Effect']}"
            )
        print(f"Processed {i} lines.")


def create_classes(repo: Repository):
    file_path = "data/class_stats.csv"
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for i, line in enumerate(csv_reader):
            if i == 0:
                print(f'Column names are {", ".join(line)}')

            print(
                f"{line['ClassName']}, {line['HitPoints']}, {line['Strength']}, {line['Magic']}, {line['Skill']}, {line['Speed']}, {line['Luck']}, {line['Defense']}, {line['Resistance']}, {line['GenderLock']}, {line['Tier']}"
            )
        print(f"Processed {i} lines.")


def create_weapon_types(repo: Repository):
    file_path = "data/weapon_types.csv"
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for i, line in enumerate(csv_reader):
            if i == 0:
                print(f'Column names are {", ".join(line)}')

            print(f"{line['BaseClass']}, {line['Weapons']}")
        print(f"Processed {i} lines.")


def create_weapons(repo: Repository):
    file_path = "data/weapons.csv"
    with open(file_path, mode="r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f)
        for i, line in enumerate(csv_reader):
            if i == 0:
                print(f'Column names are {", ".join(line)}')

            print(
                f"{line['Name']}, {line['Rank']}, {line['Might']}, {line['Hit']}, {line['Crit']}, {line['Uses']}, {line['Worth']}, {line['Type']}"
            )
        print(f"Processed {i} lines.")


create_characters(12)
create_skills(1)
create_classes("h")
create_weapon_types(None)
create_weapons("")
