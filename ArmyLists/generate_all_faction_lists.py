#!/usr/bin/env python3
"""Generate Apocalypse army list CSV and JSON files for Drukhari, Sisters of Battle, and AdMech."""

import csv
import json
from pathlib import Path

from army_list_options import format_options_from_texts, normalize_options

OUTPUT_DIR = Path(__file__).resolve().parent

CSV_HEADER = [
    "No", "Type", "Name", "M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt",
    "Weapon", "Type", "Rng", "A", "SAP", "SAT", "Abilties", "Keywords", "Options",
]


def split_keywords(keywords):
    """Split keywords into faction line and type line (two-line CSV format)."""
    faction_keys = {"Aeldari", "Drukhari", "T'au Empire", "Farsight Enclaves", "T'au Sept",
                    "Kroot", "Vespid", "Imperium", "Adeptus Ministorum",
                    "Adepta Sororitas", "Adeptus Mechanicus", "Cult Mechanicus", "Skitarii",
                    "Incubi", "Prophets of Flesh", "Cult of Strife",
                    "Order of Our Martyred Lady", "Mars",
                    "Questor Mechanicus", "Chaos", "Heretic Astartes", "Astra Militarum",
                    "Adeptus Astartes", "Knights", "Imperial Knights", "Chaos Knights",
                    "Servants of the Abyss", "Legiones Daemonica", "Daemon",
                    "Cadian", "Officio Prefectus", "Militarum Tempestus", "Militarum Auxilia",
                    "Astra Telepathica", "Scholastica Psykana", "Aeronautica Imperialis",
                    "Black Legion", "Khorne", "Nurgle", "Slaanesh", "Tzeentch",
                    "Orks", "Freebooterz", "Goff", "Bad Moons", "Deathskulls", "Blood Axe", "Evil Sunz", "Snakebites",
                    "Tyranids", "Tyranid Hive Fleets", "Genestealer Cults", "Brood Brothers",
                    "Necrons", "C'tan Shards", "Canoptek", "Sautekh", "<Dynasty>", "Infiltrators"}
    placeholder_keys = {"<Kabal>", "<Wych Cult>", "<Haemonculus Coven>", "<Sept>",
                        "<Order>", "<Forge World>", "<Legion>", "<Mark of Chaos>",
                        "<Chapter>", "<Regiment>", "<Questor Allegiance>", "<Questor Traitoris>",
                        "<Household>", "<Craftworld>", "<Clan>", "<Hive Fleet>", "<Cult>", "<Dynasty>"}
    line1, line2 = [], []
    for kw in keywords:
        if kw in faction_keys or kw in placeholder_keys or (
            "Sept" in kw or "Kabal" in kw or "Order" in kw or "Forge" in kw
            or kw.endswith("Enclaves") or kw in ("Kroot", "Vespid", "Incubi", "Mars",
            "Prophets of Flesh", "Cult of Strife", "T'au Sept")
        ):
            line1.append(kw)
        elif not line2:
            line2.append(kw)
        else:
            line2.append(kw)
    if not line1:
        line1 = keywords[: max(1, len(keywords) // 2)]
        line2 = keywords[len(line1):]
    return ", ".join(line1), ", ".join(line2)


def format_keywords_field(abilities, keywords):
    faction_line, type_line = split_keywords(keywords)
    kw_text = f"{faction_line}\n{type_line}"
    if abilities:
        return abilities, kw_text
    return "", kw_text


def write_csv(path, units_by_slot):
    rows = [CSV_HEADER, [""] * len(CSV_HEADER)]
    for slot in units_by_slot:
        no = slot["no"]
        unit = slot["unit"]
        stats = unit["stats"]
        abilities = unit.get("abilities", "")
        keywords = unit.get("keywords", [])
        ab_col, kw_col = format_keywords_field(abilities, keywords)
        options_col = format_options_from_texts(unit.get("options", []))

        rows.append([
            no, slot["type"], unit["name"],
            stats.get("M", ""), stats.get("WS", ""), stats.get("BS", ""),
            stats.get("A", ""), stats.get("W", ""), stats.get("Ld", ""),
            stats.get("Sv", ""), stats.get("N", ""), stats.get("Pt", ""),
            "", "", "", "", "", "", ab_col, kw_col, options_col,
        ])

        for profile in unit.get("profiles", []):
            rows.append([
                no, "", "",
                profile.get("M", ""), profile.get("WS", ""), profile.get("BS", ""),
                profile.get("A", ""), profile.get("W", ""), profile.get("Ld", ""),
                profile.get("Sv", ""), profile.get("N", ""), profile.get("Pt", ""),
                "", "", "", "", "", "", "", "", "",
            ])

        for opt in unit.get("options", []):
            rows.append([no] + [""] * 17 + [opt, "", ""])

        for w in unit.get("weapons", []):
            rows.append([
                no, "", "", "", "", "", "", "", "", "", "", "",
                w.get("name", ""), w.get("type", ""), w.get("range", ""),
                w.get("attacks", ""), w.get("skill", ""), w.get("armorPen", ""),
                w.get("abilities", ""), "", "",
            ])

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def write_json(path, faction, source_name, units_by_slot):
    units = []
    for slot in units_by_slot:
        unit = dict(slot["unit"])
        unit["no"] = slot["no"]
        unit["type"] = slot["type"]
        if unit.get("options"):
            unit["options"] = normalize_options(unit["options"])
        units.append(unit)

    data = {"faction": faction, "source": source_name, "units": units}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def u(name, stats, keywords, weapons, abilities="", profiles=None, options=None):
    entry = {
        "name": name,
        "stats": stats,
        "keywords": keywords,
        "weapons": weapons,
    }
    if abilities:
        entry["abilities"] = abilities
    if profiles:
        entry["profiles"] = profiles
    if options:
        entry["options"] = options
    return entry


def slot(no, stype, unit):
    return {"no": no, "type": stype, "unit": unit}


# ---------------------------------------------------------------------------
# Drukhari unit datasheets (Apoc_Datasheet_Drukhari_web.pdf)
# ---------------------------------------------------------------------------

DRUKHARI = {
    "Drazhar": u(
        "Drazhar",
        {"M": '7"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "6"},
        ["Aeldari", "Drukhari", "Incubi", "Light", "Infantry", "Character", "Drazhar"],
        [{"name": "Demiklaives", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "7+"}],
        "Master of Blades: Add 1 to hit rolls for attacks made with melee weapons by friendly Incubi units whilst they are within 6\" of this unit.",
    ),
    "Archon": u(
        "Archon",
        {"M": '8"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "3+", "N": "1", "Pt": "4"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Character", "Archon"],
        [{"name": "Husk Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "8+"}],
        "Shadowfield: Saving throws taken for this unit cannot be re-rolled for any reason. The first time the result of a saving throw taken for this unit is a 1 or 2, for the rest of the battle this unit's Save characteristic is 8+.\nOverlord: Re-roll hit rolls of 1 for attacks made by friendly <Kabal> units whilst they are within 6\" of this unit.",
    ),
    "Succubus": u(
        "Succubus",
        {"M": '9"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "4"},
        ["Aeldari", "Drukhari", "<Wych Cult>", "Light", "Infantry", "Character", "Succubus"],
        [{"name": "Wych Cult Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"}],
        "Brides of Death: Re-roll hit rolls of 1 for attacks made with melee weapons by friendly <Wych Cult> units whilst they are within 6\" of this unit.\nNo Escape: If an Infantry unit within 1\" of any enemy units with this ability wishes to Fall Back, the players must roll off. The unit can only Fall Back if the player controlling it wins the roll-off.",
    ),
    "Lady Malys": u(
        "Lady Malys",
        {"M": '8"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "3+", "N": "1", "Pt": "6"},
        ["Aeldari", "Drukhari", "Kabal of the Poisoned Tongue", "Light", "Infantry", "Character", "Archon", "Lady Malys"],
        [
            {"name": "The Lady's Blade", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "8+"},
        ],
        "Shadowfield: Saving throws taken for this unit cannot be re-rolled for any reason. The first time the result of a saving throw taken for this unit is a 1 or 2, for the rest of the battle this unit's Save characteristic is 8+.\n"
        "Precognisant: After both players have deployed their armies, select up to three friendly Drukhari units and redeploy them. When doing so, you can set those units up in Tactical Reserves if you wish.",
        options=["Lady Malys is a unit that contains 1 model. It is equipped with: The Lady's Blade. You can only include one of this unit in your army."],
    ),
    "Haemonculus": u(
        "Haemonculus",
        {"M": '7"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "5"},
        ["Aeldari", "Drukhari", "<Haemonculus Coven>", "Light", "Infantry", "Character", "Haemonculus"],
        [{"name": "Haemonculus Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "12+"}],
        "Ignore Damage (6+)\nMaster of Pain: Add 1 to saving throws taken for friendly <Haemonculus Coven> units whilst they are within 6\" of any <Haemonculus Coven> units from your army with this ability.",
    ),
    "Reavers": u(
        "Reavers",
        {"M": '20"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "3", "Pt": "4"},
        ["Aeldari", "Drukhari", "<Wych Cult>", "Light", "Biker", "Fly", "Reavers"],
        [
            {"name": "Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Heat Lance", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "6+"},
            {"name": "Splinter Rifles", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '20"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "8+", "N": "6", "Pt": "8"},
            {"M": '20"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "8+", "N": "9", "Pt": "12"},
            {"M": '20"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "8+", "N": "12", "Pt": "16"},
        ],
        options=["For every 3 models this unit contains, it can also be equipped with one of the following (Power Rating +1 per weapon): 1 Blaster; 1 Heat Lance."],
    ),
    "Kabalite Warriors": u(
        "Kabalite Warriors",
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "5", "Pt": "2"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Kabalite Warriors"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Splinter Rifles", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "4"},
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "10+", "N": "15", "Pt": "6"},
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "8"},
        ],
        options=["For every 10 models this unit contains, it can also be equipped with one of the following (Power Rating +1 per weapon): 1 Dark Lance; 1 Splinter Cannon."],
    ),
    "Wyches": u(
        "Wyches",
        {"M": '9"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "5", "Pt": "2"},
        ["Aeldari", "Drukhari", "<Wych Cult>", "Light", "Infantry", "Wyches"],
        [
            {"name": "Splinter Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "5+", "armorPen": "12+"},
            {"name": "Wych Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "8+"},
        ],
        abilities="No Escape: If an Infantry unit within 1\" of any enemy units with this ability wishes to Fall Back, the players must roll off. The unit can only Fall Back if the player controlling it wins the roll-off.",
        profiles=[
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "8+", "N": "10", "Pt": "4"},
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "8+", "N": "15", "Pt": "6"},
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "8+", "N": "20", "Pt": "8"},
        ],
    ),
    "Incubi": u(
        "Incubi",
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Aeldari", "Drukhari", "Incubi", "Light", "Infantry", "Incubi"],
        [{"name": "Klaives", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "5+", "armorPen": "9+"}],
        "Tormentors: If the result of a Morale test taken for an enemy unit within 6\" of any Incubi units from your army is equal to the Leadership value of that enemy unit, that Morale test is failed.",
        profiles=[{"M": '7"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "10", "Pt": "8"}],
    ),
    "Mandrakes": u(
        "Mandrakes",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "9+", "N": "5", "Pt": "4"},
        ["Aeldari", "Drukhari", "Light", "Infantry", "Mandrakes"],
        [
            {"name": "Baleblasts", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "6+", "armorPen": "9+"},
            {"name": "Glimmersteel Blades", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "9+"},
        ],
        "Deep Strike, Stealth",
        profiles=[{"M": '8"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "9+", "N": "10", "Pt": "7"}],
    ),
    "Grotesques": u(
        "Grotesques",
        {"M": '7"', "WS": "3+", "BS": "6+", "A": "2", "W": "2", "Ld": "6", "Sv": "8+", "N": "3", "Pt": "5"},
        ["Aeldari", "Drukhari", "<Haemonculus Coven>", "Light", "Infantry", "Grotesques"],
        [
            {"name": "Liquifier Gun", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Flesh Gauntlets", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "10+"},
            {"name": "Monstrous Cleaver", "type": "Melee", "range": "Melee", "attacks": "2", "skill": "5+", "armorPen": "8+"},
        ],
        profiles=[
            {"M": '7"', "WS": "3+", "BS": "6+", "A": "4", "W": "4", "Ld": "6", "Sv": "8+", "N": "6", "Pt": "12"},
            {"M": '7"', "WS": "3+", "BS": "6+", "A": "6", "W": "6", "Ld": "6", "Sv": "8+", "N": "9", "Pt": "18"},
            {"M": '7"', "WS": "3+", "BS": "6+", "A": "7", "W": "7", "Ld": "6", "Sv": "8+", "N": "10", "Pt": "20"},
        ],
        options=["For each model this unit contains, it must also be equipped with one of the following: 1 Monstrous Cleaver; 1 Liquifier Gun."],
    ),
    "Wracks": u(
        "Wracks",
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "2", "W": "1", "Ld": "6", "Sv": "9+", "N": "5", "Pt": "3"},
        ["Aeldari", "Drukhari", "<Haemonculus Coven>", "Light", "Infantry", "Wracks"],
        [{"name": "Haemonculus Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "12+"}],
        "Ignore Damage (6+)",
        profiles=[{"M": '7"', "WS": "3+", "BS": "3+", "A": "4", "W": "2", "Ld": "6", "Sv": "9+", "N": "10", "Pt": "5"}],
    ),
    "Hand of Archon": u(
        "Hand of Archon",
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "5", "Pt": "3"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Hand of the Archon"],
        [
            {"name": "Splinter Rifles", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "5+"},
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "5+"},
            {"name": "Power Weapon", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[{"M": '7"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "8+", "N": "10", "Pt": "6"}],
        options=[
            "Hand of the Archon are a unit that contains 5 models. It can contain 10 models (Power Rating 8). It is equipped with: Splinter Rifles; Close Combat Weapons.",
            "For every 5 models this unit contains, up to 2 models can be equipped with 1 Blaster (Power Rating +1 per weapon).",
            "For every 5 models this unit contains, up to 1 model can be equipped with 1 Dark Lance (Power Rating +1 per weapon).",
            "Up to 1 model in this unit can be equipped with 1 Power Weapon.",
        ],
    ),
    "Court of the Archon": u(
        "Court of the Archon",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "4", "Pt": "4"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Court of the Archon"],
        [
            {"name": "Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "6+", "armorPen": "9+"},
        ],
        "Ignore Damage (6+)\n"
        "Court of the Archon: You can re-roll hit rolls for attacks made by this unit whilst it is within 3\" of any friendly <Kabal> Archon units. This unit does not take up a slot in a Detachment that includes any <Kabal> Archon units.\n"
        "Cold-blooded Bodyguard: At the start of the Damage phase, you can select one friendly <Kabal> Archon unit that has at least one blast marker next to it and is within 3\" of this unit. Remove up to D3 blast markers from that Archon unit and place them next to this unit.",
        options=["Court of the Archon is a unit that contains 4 models representing a combined Court of the Archon retinue."],
    ),
    "Scourges with Shard Carbines": u(
        "Scourges with Shard Carbines",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "5", "Pt": "4"},
        ["Aeldari", "Drukhari", "Light", "Infantry", "Fly", "Scourges"],
        [
            {"name": "Shardcarbines", "type": "Small Arms", "range": '18"', "attacks": "x2", "skill": "5+", "armorPen": "12+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[{"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "10", "Pt": "10"}],
        options=["Scourges with Shard Carbines are a unit that contains 5 models. It can contain 10 models (Power Rating 10). It is equipped with: Shardcarbines; Close Combat Weapons."],
    ),
    "Scourges with Heavy Weapons": u(
        "Scourges with Heavy Weapons",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "5", "Pt": "4"},
        ["Aeldari", "Drukhari", "Light", "Infantry", "Fly", "Scourges"],
        [
            {"name": "Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Haywire Blaster", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "12+", "armorPen": "4+"},
            {"name": "Heat Lance", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "6+"},
            {"name": "Shredder", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "6+", "armorPen": "8+"},
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[{"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "10", "Pt": "10"}],
        options=[
            "Scourges with Heavy Weapons are a unit that contains 5 models. It can contain 10 models (Power Rating 10). It is equipped with: Close Combat Weapons.",
            "This unit can also be equipped with up to four of the following in any combination (Power Rating +2 per Shredder or Splinter Cannon; Power Rating +1 per other weapon): 1 Blaster; 1 Dark Lance; 1 Haywire Blaster; 1 Heat Lance; 1 Shredder; 1 Splinter Cannon.",
        ],
    ),
    "Hellions": u(
        "Hellions",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "9+", "N": "5", "Pt": "5"},
        ["Aeldari", "Drukhari", "<Wych Cult>", "Light", "Infantry", "Fly", "Skyboard", "Hellions"],
        [
            {"name": "Splinter Pods", "type": "Small Arms", "range": '18"', "attacks": "x2", "skill": "5+", "armorPen": "12+"},
            {"name": "Hellglaives", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "8+"},
        ],
        "Hit and Run: Whilst this unit Falls Back, double its Move characteristic. When this unit Falls Back, it can finish that Move action in base contact with enemy models.",
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "9+", "N": "10", "Pt": "9"},
            {"M": '14"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "9+", "N": "15", "Pt": "13"},
            {"M": '14"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "9+", "N": "20", "Pt": "17"},
        ],
    ),
    "Khymerae": u(
        "Khymerae",
        {"M": '10"', "WS": "3+", "BS": "-", "A": "1", "W": "1", "Ld": "4", "Sv": "9+", "N": "2", "Pt": "1"},
        ["Aeldari", "Drukhari", "Light", "Beast", "Daemon", "Khymerae"],
        [{"name": "Claws & Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"}],
        profiles=[
            {"M": '10"', "WS": "3+", "BS": "-", "A": "2", "W": "2", "Ld": "4", "Sv": "9+", "N": "4", "Pt": "2"},
            {"M": '10"', "WS": "3+", "BS": "-", "A": "3", "W": "3", "Ld": "4", "Sv": "9+", "N": "6", "Pt": "3"},
            {"M": '10"', "WS": "3+", "BS": "-", "A": "4", "W": "4", "Ld": "4", "Sv": "9+", "N": "8", "Pt": "4"},
            {"M": '10"', "WS": "3+", "BS": "-", "A": "5", "W": "5", "Ld": "4", "Sv": "9+", "N": "10", "Pt": "5"},
            {"M": '10"', "WS": "3+", "BS": "-", "A": "6", "W": "6", "Ld": "4", "Sv": "9+", "N": "12", "Pt": "6"},
        ],
    ),
    "Clawed Fiends": u(
        "Clawed Fiends",
        {"M": '10"', "WS": "4+", "BS": "-", "A": "1", "W": "1", "Ld": "4", "Sv": "9+", "N": "1", "Pt": "2"},
        ["Aeldari", "Drukhari", "Light", "Beast", "Clawed Fiends"],
        [{"name": "Clawed Fists", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "9+"}],
        "Berserk Rage: This unit does not suffer the penalty for being critically damaged. Whilst this unit has any damage markers next to it, add 1 to its Attacks Characteristic.",
        profiles=[
            {"M": '10"', "WS": "4+", "BS": "-", "A": "3", "W": "3", "Ld": "4", "Sv": "9+", "N": "3", "Pt": "5"},
            {"M": '10"', "WS": "4+", "BS": "-", "A": "6", "W": "6", "Ld": "4", "Sv": "9+", "N": "6", "Pt": "10"},
        ],
    ),
    "Razorwing Flocks": u(
        "Razorwing Flocks",
        {"M": '12"', "WS": "4+", "BS": "-", "A": "2", "W": "1", "Ld": "4", "Sv": "10+", "N": "3", "Pt": "2"},
        ["Aeldari", "Drukhari", "Light", "Beast", "Fly", "Swarm", "Razorwing Flocks"],
        [{"name": "Razor Feathers", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"}],
        profiles=[
            {"M": '12"', "WS": "4+", "BS": "-", "A": "4", "W": "2", "Ld": "4", "Sv": "10+", "N": "6", "Pt": "4"},
            {"M": '12"', "WS": "4+", "BS": "-", "A": "6", "W": "3", "Ld": "4", "Sv": "10+", "N": "9", "Pt": "6"},
            {"M": '12"', "WS": "4+", "BS": "-", "A": "8", "W": "4", "Ld": "4", "Sv": "10+", "N": "12", "Pt": "8"},
        ],
    ),
    "Beastmaster": u(
        "Beastmaster",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "1", "Pt": "2"},
        ["Aeldari", "Drukhari", "<Wych Cult>", "Light", "Infantry", "Fly", "Skyboard", "Beastmaster"],
        [{"name": "Agoniser", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "12+"}],
        "Beastmaster: Re-roll hit rolls of 1 for attacks made by friendly Drukhari Beast units whilst they are within 6\" of this unit. Friendly Drukhari Beast units can use this unit's Leadership characteristic instead of their own whilst they are within 6\" of this unit. Drukhari Beast units do not take up slots in a Detachment that contains any units with this ability.",
    ),
    "Talos": u(
        "Talos",
        {"M": '8"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "7"},
        ["Aeldari", "Drukhari", "<Haemonculus Coven>", "Heavy", "Monster", "Fly", "Talos"],
        [
            {"name": "Haywire Blaster", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "12+", "armorPen": "4+"},
            {"name": "Heat Lance", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "6+"},
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Stinger Pod", "type": "Heavy", "range": '18"', "attacks": "3", "skill": "5+", "armorPen": "12+"},
            {"name": "Twin Liquifier Gun", "type": "Heavy", "range": '8"', "attacks": "2", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Gruesome Combat Weapon", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        "Pain Engines: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. Each unit taken for a single Heavy Support slot must be placed at the same time and within 6\" of each other unit taken for the same slot the first time they are set up.",
        options=[
            "Instead of 2 Splinter Cannons, this unit can be equipped with one of the following: 2 Haywire Blasters; 2 Heat Lances; 1 Stinger Pod.",
            "Instead of 1 Gruesome Combat Weapon, this unit can be equipped with 1 Twin Liquifier Gun.",
        ],
    ),
    "Cronos": u(
        "Cronos",
        {"M": '8"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "5"},
        ["Aeldari", "Drukhari", "<Haemonculus Coven>", "Heavy", "Monster", "Fly", "Cronos"],
        [
            {"name": "Spirit Syphon", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Spirit Vortex", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "6+", "armorPen": "9+"},
            {"name": "Spirit Leech Tentacles", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Pain Engines: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. Each unit taken for a single Heavy Support slot must be placed at the same time and within 6\" of each other unit taken for the same slot the first time they are set up.\nSpirit Probe: Re-roll wound rolls of 1 for attacks made with melee weapons by friendly Drukhari units whilst they are within 6\" of this unit.",
        options=["This unit can also be equipped with 1 Spirit Vortex (Power Rating +1)."],
    ),
    "Ravager": u(
        "Ravager",
        {"M": '14"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "7"},
        ["Aeldari", "Drukhari", "<Kabal>", "Heavy", "Vehicle", "Fly", "Ravager"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Disintegrator Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "10+"},
            {"name": "Bladevanes", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.",
        options=[
            "Instead of 1 Dark Lance this unit can be equipped with 1 Disintegrator Cannon.",
            "Instead of 2 Dark Lances this unit can be equipped with 2 Disintegrator Cannons.",
            "Instead of 3 Dark Lances this unit can be equipped with 3 Disintegrator Cannons.",
        ],
    ),
    "Reaper": u(
        "Reaper",
        {"M": '14"', "WS": "4+", "BS": "3+", "A": "1", "W": "3", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "7"},
        ["Aeldari", "Drukhari", "<Kabal>", "Heavy", "Vehicle", "Fly", "Reaper"],
        [
            {"name": "Storm Vortex Projector", "type": "Heavy", "range": '36"', "attacks": "3", "skill": "7+", "armorPen": "7+"},
            {"name": "Bladevanes", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.",
        options=["A Reaper is a unit that contains 1 model. It is equipped with: Storm Vortex Projector; Scythevanes."],
    ),
    "Lelith Hesperax": u(
        "Lelith Hesperax",
        {"M": '10"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "5"},
        ["Aeldari", "Drukhari", "Cult of Strife", "Light", "Infantry", "Character", "Succubus", "Lelith Hesperax"],
        [{"name": "Penetrating Blades", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "9+"}],
        "A League Apart: You can re-roll hit rolls and wound rolls for attacks made with melee weapons by this unit that target Character units.\nBrides of Death: Re-roll hit rolls of 1 for attacks made with melee weapons by friendly Cult of Strife units whilst they are within 6\" of this unit.\nNo Escape: If an Infantry unit within 1\" of any enemy units with this ability wishes to Fall Back, the players must roll off. The unit can only Fall Back if the player controlling it wins the roll-off.",
    ),
    "Urien Rakarth": u(
        "Urien Rakarth",
        {"M": '7"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Aeldari", "Drukhari", "Prophets of Flesh", "Light", "Infantry", "Character", "Haemonculus", "Urien Rakarth"],
        [
            {"name": "The Casket of Flensing", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "9+", "armorPen": "9+", "abilities": "One Use Only"},
            {"name": "Haemonculus Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "12+"},
        ],
        "Ignore Damage (6+)\nSculptor of Torments: Add 1 to wound rolls for attacks made by friendly Prophets of Flesh units when using melee weapons whilst they are within 6\" of this unit.\nMaster of Pain: Add 1 to saving throws taken for friendly Prophets of Flesh units whilst they are within 6\" of any Prophets of Flesh units from your army with this ability.\nContempt for Death: At the start of the Damage phase, you can remove half of the blast markers, rounding down, from this unit. Small blast markers must be removed before large blast markers.",
    ),
    "Raider": u(
        "Raider",
        {"M": '14"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "6"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult> or <Haemonculus Coven>", "Heavy", "Vehicle", "Fly", "Transport", "Raider"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Disintegrator Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "10+"},
            {"name": "Bladevanes", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Open-topped\nHover: Distances are measured to and from this unit's hull, even though it has a base.\nTRANSPORT: This unit can transport up to 10 friendly Drukhari Infantry models. Each Grotesque model takes the space of 2 other Infantry models. It cannot transport Scourge or Skyboard units.",
        options=["Instead of 1 Dark Lance, this unit can be equipped with 1 Disintegrator Cannon."],
    ),
    "Razorwing Jetfighter": u(
        "Razorwing Jetfighter",
        {"M": '20-72"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "10"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult>", "Heavy", "Vehicle", "Fly", "Aircraft", "Razorwing Jetfighter"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Disintegrator Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "10+"},
            {"name": "Razorwing Missiles", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Twin Splinter Rifle", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Bladed Wings", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Supersonic",
        options=[
            "Instead of 2 Disintegrator Cannons, this unit can be equipped with 2 Dark Lances.",
            "Instead of 1 Twin Splinter Rifle, this unit can be equipped with 1 Splinter Cannon.",
        ],
    ),
    "Venom": u(
        "Venom",
        {"M": '16"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "6"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult> or <Haemonculus Coven>", "Heavy", "Vehicle", "Fly", "Transport", "Venom"],
        [
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Twin Splinter Rifle", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Bladevanes", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Open-topped\nHover: Distances are measured to and from this unit's hull, even though it has a base.\nTRANSPORT: This unit can transport up to 5 friendly Drukhari Infantry models. It cannot transport Grotesque, Scourge or Skyboard units.",
        options=["Instead of 1 Twin Splinter Rifle, this unit can be equipped with 1 Splinter Cannon."],
    ),
    "Raven Strike Fighter": u(
        "Raven Strike Fighter",
        {"M": '20-72"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "10"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult>", "Heavy", "Vehicle", "Fly", "Aircraft", "Raven Strike Fighter"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Splinterstorm Cannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Bladed Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Supersonic",
        options=["A Raven Strike Fighter is a unit that contains 1 model. It is equipped with: 2 Dark Lances; Splinterstorm Cannon; Bladed Hull."],
    ),
    "Voidraven Bomber": u(
        "Voidraven Bomber",
        {"M": '20-72"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "7+", "N": "1", "Pt": "10"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult>", "Heavy", "Vehicle", "Fly", "Aircraft", "Voidraven Bomber"],
        [
            {"name": "Dark Scythe", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "4+", "armorPen": "9+"},
            {"name": "Void Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "4+"},
            {"name": "Voidraven Missiles", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Bladed Wings", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Supersonic",
        options=[
            "A Voidraven Bomber is a unit that contains 1 model. It is equipped with: 2 Void Lances; Dark Scythe; Bladed Wings.",
            "This unit can also be equipped with Voidraven Missiles (Power Rating +1).",
        ],
    ),
    "Tantalus": u(
        "Tantalus",
        {"M": '16"', "WS": "4+", "BS": "3+", "A": "2", "W": "4", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "16"},
        ["Aeldari", "Drukhari", "<Kabal> or <Wych Cult> or <Haemonculus Coven>", "Heavy", "Vehicle", "Fly", "Transport", "Tantalus"],
        [
            {"name": "Pulse-disintegrator", "type": "Heavy", "range": '36"', "attacks": "4", "skill": "7+", "armorPen": "7+"},
            {"name": "Dire Scythe Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "10+"},
        ],
        "Open-topped\nHover: Distances are measured to and from this unit's hull, even though it has a base.\n"
        "TRANSPORT: This unit can transport up to 21 friendly Drukhari Infantry models. Each Grotesque model takes the space of 2 other Infantry models. It cannot transport Scourge or Skyboard units.",
        options=["A Tantalus is a unit that contains 1 model. It is equipped with: 2 Pulse-disintegrators; Dire Scythe Blade."],
    ),
    "Asdrubael Vect": u(
        "Asdrubael Vect",
        {"M": '14"', "WS": "2+", "BS": "3+", "A": "2", "W": "4", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "20"},
        ["Aeldari", "Drukhari", "Kabal of the Black Heart", "Heavy", "Vehicle", "Fly", "Character", "Ravager", "Asdrubael Vect"],
        [
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "5+"},
            {"name": "Obsidian Orbs (Ranged)", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "3+", "armorPen": "10+", "abilities": "Destroyer"},
            {"name": "Splinterstorm Cannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Obsidian Orbs (Melee)", "type": "Melee", "range": "Melee", "attacks": "2", "skill": "3+", "armorPen": "10+", "abilities": "Destroyer"},
            {"name": "Retinue Weaponry", "type": "Melee", "range": "Melee", "attacks": "4", "skill": "6+", "armorPen": "8+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.\n"
        "Lord of Commoragh: When taken, this unit is always the Warlord, and if the majority of your army in points is Drukhari, he is your Warmaster.\n"
        "Master of the Gates: Once per battle, at the end of any phase, this unit can be removed from the battlefield and placed into Tactical Reserves.",
        options=[
            "Asdrubael Vect is a unit that contains 1 model aboard a modified Ravager. It is equipped with: 3 Dark Lances; Disintegrator Cannon; Splinterstorm Cannon; Scepter of the Dark City; Bladevanes.",
            "You can only include one of this unit in your army.",
        ],
    ),
    "Webway Gate": u(
        "Webway Gate",
        {"M": "-", "WS": "-", "BS": "-", "A": "-", "W": "3", "Ld": "-", "Sv": "5+", "N": "1", "Pt": "6"},
        ["Aeldari", "Heavy", "Vehicle", "Building", "Webway Gate"],
        [],
        "Shimmering Arrival: When this unit is set up on the battlefield, it can be set up anywhere that is more than 12\" away from your opponent's deployment zone and any enemy units, and more than 3\" away from any other terrain features or the centre of any objective markers.\nWebway Gate: This unit is never Out of Command: an Out of Command marker is never placed next to it. When measuring distances to and from this unit, measure to and from the closest point of this unit. This unit cannot be affected by Command Assets or other units' abilities. If a Webway Gate is destroyed, remove both pieces from the battlefield.\nWebway Strike: After this unit is set up on the battlefield, any friendly Aeldari units, other than Fortifications, that have not already been set up can be set up in a webway spar as Tactical Reserves instead of being set up on the battlefield. In the Set Up Reinforcements step, one unit in a webway spar can emerge from each friendly Webway Gate as reinforcements; a unit emerging from a Webway Gate must be set up wholly within 3\" of that Webway Gate and more than 9\" away from any enemy units. No more than half the total number of units in your army can be set up in Tactical Reserves.",
    ),
}

DRUKHARI_SLOTS = [
    slot(1, "HQ", DRUKHARI["Archon"]),
    slot(2, "HQ", DRUKHARI["Lady Malys"]),
    slot(3, "HQ", DRUKHARI["Haemonculus"]),
    slot(4, "HQ", DRUKHARI["Succubus"]),
    slot(5, "Troops", DRUKHARI["Kabalite Warriors"]),
    slot(6, "Troops", DRUKHARI["Wyches"]),
    slot(7, "Troops", DRUKHARI["Wracks"]),
    slot(8, "Elites", DRUKHARI["Grotesques"]),
    slot(9, "Elites", DRUKHARI["Incubi"]),
    slot(10, "Elites", DRUKHARI["Mandrakes"]),
    slot(11, "Elites", DRUKHARI["Hand of Archon"]),
    slot(12, "Elites", DRUKHARI["Court of the Archon"]),
    slot(13, "Elites", DRUKHARI["Beastmaster"]),
    slot(14, "Fast", DRUKHARI["Scourges with Shard Carbines"]),
    slot(15, "Fast", DRUKHARI["Clawed Fiends"]),
    slot(16, "Fast", DRUKHARI["Hellions"]),
    slot(17, "Fast", DRUKHARI["Khymerae"]),
    slot(18, "Fast", DRUKHARI["Razorwing Flocks"]),
    slot(19, "Fast", DRUKHARI["Reavers"]),
    slot(20, "Heavy", DRUKHARI["Cronos"]),
    slot(21, "Heavy", DRUKHARI["Ravager"]),
    slot(22, "Heavy", DRUKHARI["Reaper"]),
    slot(23, "Heavy", DRUKHARI["Scourges with Heavy Weapons"]),
    slot(24, "Heavy", DRUKHARI["Talos"]),
    slot(25, "Air", DRUKHARI["Raven Strike Fighter"]),
    slot(26, "Air", DRUKHARI["Razorwing Jetfighter"]),
    slot(27, "Air", DRUKHARI["Voidraven Bomber"]),
    slot(28, "Transport", DRUKHARI["Raider"]),
    slot(29, "Transport", DRUKHARI["Venom"]),
    slot(30, "Lord", DRUKHARI["Tantalus"]),
    slot(31, "Lord", DRUKHARI["Asdrubael Vect"]),
    slot(32, "Lord", DRUKHARI["Webway Gate"]),
]


# ---------------------------------------------------------------------------
# Sisters of Battle unit datasheets (Apoc_Datasheet_Adeptus_Sororitas.pdf)
# ---------------------------------------------------------------------------

SISTERS = {
    "Celestine": u(
        "Celestine",
        {"M": '12"', "WS": "2+", "BS": "2+", "A": "1", "W": "2", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "9"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Fly", "Character", "Jump Pack", "Celestine"],
        [
            {"name": "The Ardent Blade (Ranged)", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "The Ardent Blade (Melee)", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        "Beacon of Faith: Improve the Save characteristic (to a maximum of 3+) of friendly Adepta Sororitas units by 1 whilst they are wholly within 6\" of this unit.\nMiraculous Intervention: The first time the number of damage markers next to this unit equals its Wounds characteristic, roll a D6; on a 2+ this unit is not destroyed, and one damage marker is removed from it.\nHealing Tears: At the beginning of the Orders phase, you can remove one damage marker from a friendly Geminae Superia unit within 3\" of this unit.",
    ),
    "Canoness": u(
        "Canoness",
        {"M": '6"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Character", "Canoness"],
        [{"name": "Master-crafted Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"}],
        "Lead the Righteous: Re-roll hit rolls of 1 for attacks made by friendly <Order> units whilst they are within 6\" of this unit.",
    ),
    "Imagifier": u(
        "Imagifier",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "2"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Character", "Imagifier"],
        [{"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"}],
        "Simulacrum Imperialis: If any friendly units with this ability are on the battlefield when an Adepta Sororitas Command Asset is played, roll one D12; on a roll of 10+ return that Command Asset to your hand instead of discarding it. That Command Asset cannot be played again this turn.",
    ),
    "Hospitaller": u(
        "Hospitaller",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "2"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Character", "Hospitaller"],
        [{"name": "Chirurgeon's Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"}],
        "Medicus Ministorum: At the end of the Action phase, this unit can attempt to heal one friendly Adeptus Ministorum Light unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Light unit. Only one attempt to heal each unit can be made each turn.",
    ),
    "Morvenn Vahl": u(
        "Morvenn Vahl",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "2", "W": "3", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "8"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Order of Our Martyred Lady", "Heavy", "Vehicle", "Walker", "Character", "Morvenn Vahl"],
        [
            {"name": "Fidelis", "type": "Small Arms", "range": '36"', "attacks": "User", "skill": "6+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Paragon Missile Launcher (Prioris)", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "5+", "armorPen": "6+"},
            {"name": "Lance of Illumination", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"},
        ],
        "Righteous Reprimand: Re-roll hit rolls of 1 for attacks made by friendly Adepta Sororitas units whilst they are within 6\" of this unit.\n"
        "Leader of the Faithful: Improve the Save characteristic (to a maximum of 3+) of friendly Adepta Sororitas Infantry units by 1 whilst they are wholly within 6\" of this unit.",
        options=["Morvenn Vahl is a unit that contains 1 model. It is equipped with: Fidelis; Paragon Missile Launcher; Lance of Illumination. You can only include one of this unit in your army."],
    ),
    "Junith Eruita": u(
        "Junith Eruita",
        {"M": '10"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "6"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Order of Our Martyred Lady", "Heavy", "Vehicle", "Character", "Fly", "Canoness Superior", "Junith Eruita"],
        [
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "The Mace of Castigation", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "The Pulpit of Saint Holline's Basilica: Improve the Save characteristic (to a maximum of 3+) of friendly Adepta Sororitas Infantry units by 1 whilst they are wholly within 6\" of this unit.\nFiery Conviction: Re-roll hit rolls and wound rolls of 1 for attacks made by friendly Order of Our Martyred Lady units whilst they are within 6\" of this unit.",
    ),
    "Battle Sisters Squad": u(
        "Battle Sisters Squad",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Battle Sisters Squad"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "6"},
            {"M": '6"', "WS": "4+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "12"},
        ],
        options=["This unit can also be equipped with one of the following (Power Rating +1): Heavy Bolter; Heavy Flamer; Multi-melta."],
    ),
    "Zealots": u(
        "Zealots",
        {"M": '6"', "WS": "5+", "BS": "5+", "A": "2", "W": "4", "Ld": "7", "Sv": "10+", "N": "20", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Zealots"],
        [
            {"name": "Autopistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "8+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        profiles=[{"M": '6"', "WS": "5+", "BS": "5+", "A": "3", "W": "6", "Ld": "7", "Sv": "10+", "N": "30", "Pt": "6"}],
        options=["Zealots is a unit that contains 20 models. It can contain 30 models (Power Rating 6). It is equipped with: Autopistols; Close Combat Weapons."],
    ),
    "Dominion Squad": u(
        "Dominion Squad",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Dominion Squad"],
        [
            {"name": "Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Storm Bolter", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        "Infiltrators",
        profiles=[{"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "8"}],
        options=[
            "This unit can also be equipped with up to four of the following in any combination (Power Rating +1 per weapon): Flamer; Meltagun; Storm Bolter.",
            "If this unit is not equipped with any Flamers, Meltaguns or Storm Bolters, and/or if it contains 10 models, it is also equipped with Boltguns.",
        ],
    ),
    "Celestian Squad": u(
        "Celestian Squad",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Celestian Squad"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "8+", "armorPen": "9+"},
        ],
        "Bodyguard: At the start of the Damage phase, you can select one friendly <Order> Light Character unit that has at least one blast marker next to it and is within 6\" of this unit. Remove up to D3 blast markers from that Character unit and place them next to this unit.\nSworn Protectors: You can re-roll hit rolls for attacks made by this unit whilst it is within 6\" of any friendly <Order> Canoness units.",
        profiles=[{"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "10", "Pt": "8"}],
        options=["This unit can also be equipped with one of the following (Power Rating +1): Heavy Bolter; Heavy Flamer; Multi-melta."],
    ),
    "Celestian Sacrosancts": u(
        "Celestian Sacrosancts",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Celestian Sacrosancts"],
        [{"name": "Anointed Halberds", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "7+"}],
        "Sacresant Shield: Improve the Save characteristic (to a maximum of 3+) of models in this unit by 1 against attacks made with melee weapons.\n"
        "Sworn Protectors: You can re-roll hit rolls for attacks made with melee weapons by this unit whilst it is within 6\" of any friendly <Order> Canoness units.",
        profiles=[{"M": '6"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "7", "Sv": "5+", "N": "10", "Pt": "8"}],
        options=["Celestian Sacrosancts is a unit that contains 5 models. It can contain 10 models (Power Rating 8). It is equipped with: Anointed Halberds."],
    ),
    "Retributor Squad": u(
        "Retributor Squad",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Retributor Squad"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        profiles=[{"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "6"}],
        options=[
            "This unit can also be equipped with up to four of the following in any combination (Power Rating +1 per weapon): Heavy Bolter; Heavy Flamer; Multi-melta.",
            "If this unit is not equipped with any Heavy Bolters, Heavy Flamers or Multi-meltas, and/or if it contains 10 models, it is also equipped with Boltguns.",
        ],
    ),
    "Repentia Superior": u(
        "Repentia Superior",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Character", "Repentia Superior"],
        [{"name": "Neural Whips", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"}],
        "Driven Onwards: If an <Order> Sisters Repentia unit starts a Move action within 6\" of any friendly units with this ability, add 3\" to that unit's Move characteristic whilst making that Move action.\nMistress of the Penitent: This unit does not take up slots in a Detachment that contains any <Order> Sisters Repentia units.",
    ),
    "Sisters Repentia": u(
        "Sisters Repentia",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "1", "Ld": "6", "Sv": "11+", "N": "4", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Sisters Repentia"],
        [{"name": "Penitent Eviscerators", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "8+"}],
        "Ignore Damage (6+)\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
        profiles=[{"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "2", "Ld": "6", "Sv": "11+", "N": "9", "Pt": "6"}],
    ),
    "Dialogus": u(
        "Dialogus",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "11+", "N": "1", "Pt": "1"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Character", "Dialogus"],
        [{"name": "Dialogus Staff", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"}],
        "Laud Hailer: You can re-roll Morale tests taken for friendly Adepta Sororitas units whilst they are within 6\" of this unit.",
    ),
    "Geminae Superia": u(
        "Geminae Superia",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "1", "Pt": "2"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Fly", "Character", "Jump Pack", "Geminae Superia"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Geminae Power Swords", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "Divine Guardians: This unit cannot be a Warlord. This unit does not take up slots in a Detachment that contains Celestine.\nLifewards: At the start of the Damage phase, you can select one friendly Celestine unit that has at least one blast marker next to it and is within 6\" of this unit. Remove up to D3 blast markers from that Celestine unit and place them next to this unit.",
        profiles=[{"M": '12"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "2", "Pt": "4"}],
    ),
    "Missionary": u(
        "Missionary",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Character", "Ministorum Priest", "Missionary"],
        [{"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"}],
        "War Hymns: Add 1 to the Attacks characteristic of friendly Adeptus Ministorum Infantry and Astra Militarum Infantry units whilst they are making Fight actions whilst within 6\" of any friendly units with this ability.\nWord of the Emperor: Re-roll failed Morale tests taken for Adeptus Ministorum Infantry units whilst within 6\" of any friendly units with this ability.\nLone Mission: No more than one Missionary unit can be included in each Detachment.\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
    ),
    "Preacher": u(
        "Preacher",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "3"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Character", "Ministorum Priest", "Preacher"],
        [{"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"}],
        "War Hymns: Add 1 to the Attacks characteristic of friendly Adeptus Ministorum Infantry and Astra Militarum Infantry units whilst they are making Fight actions whilst within 6\" of any friendly units with this ability.\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
    ),
    "Seraphim Squad": u(
        "Seraphim Squad",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "5", "Pt": "5"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Fly", "Jump Pack", "Seraphim Squad"],
        [
            {"name": "Twin Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[{"M": '12"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "10", "Pt": "9"}],
    ),
    "Zephyrim Squad": u(
        "Zephyrim Squad",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "5", "Pt": "5"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Jump Pack", "Fly", "Zephyrim Squad"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Zephyrim Power Swords", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "5+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[{"M": '12"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "5+", "N": "10", "Pt": "10"}],
    ),
    "Novitiate Squad": u(
        "Novitiate Squad",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "6"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Light", "Infantry", "Novitiate Squad"],
        [
            {"name": "Autoguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "8+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Novitiate Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        "Infiltrators",
        options=["Novitiate Squad is a unit that contains 10 models. It is equipped with: Novitiate Melee Weapons."],
    ),
    "Sanctifiers": u(
        "Sanctifiers",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "11+", "N": "10", "Pt": "6"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Sanctifiers"],
        [
            {"name": "Braziers of Holy Fire", "type": "Heavy", "range": '12"', "attacks": "3", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Infiltrators\nPurge the Unclean: Re-roll wound rolls of 1 for attacks made by this unit that target Infantry units.",
        options=["Sanctifiers is a unit that contains 10 models. It is equipped with: Braziers of Holy Fire; Close Combat Weapons."],
    ),
    "Crusaders": u(
        "Crusaders",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "6+", "N": "2", "Pt": "1"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Ecclesiarchy Battle Conclave", "Crusaders"],
        [{"name": "Crusader Power Swords", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"}],
        "Ecclesiarchy Battle Conclave: This unit does not take up slots in a Detachment that contains any Ministorum Priests.\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "6+", "N": "4", "Pt": "2"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "3", "W": "3", "Ld": "5", "Sv": "6+", "N": "6", "Pt": "3"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "5", "Sv": "6+", "N": "8", "Pt": "4"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "5", "W": "5", "Ld": "5", "Sv": "6+", "N": "10", "Pt": "5"},
        ],
    ),
    "Death Cult Assassins": u(
        "Death Cult Assassins",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "9+", "N": "2", "Pt": "1"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Ecclesiarchy Battle Conclave", "Death Cult Assassins"],
        [{"name": "Death Cult Power Blades", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "8+", "armorPen": "8+"}],
        "Ecclesiarchy Battle Conclave: This unit does not take up slots in a Detachment that contains any Ministorum Priests.\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
        profiles=[
            {"M": '7"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "9+", "N": "4", "Pt": "2"},
            {"M": '7"', "WS": "3+", "BS": "4+", "A": "3", "W": "3", "Ld": "5", "Sv": "9+", "N": "6", "Pt": "3"},
            {"M": '7"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "5", "Sv": "9+", "N": "8", "Pt": "4"},
            {"M": '7"', "WS": "3+", "BS": "4+", "A": "5", "W": "5", "Ld": "5", "Sv": "9+", "N": "10", "Pt": "5"},
        ],
    ),
    "Arco-flagellants": u(
        "Arco-flagellants",
        {"M": '6"', "WS": "4+", "BS": "-", "A": "1", "W": "1", "Ld": "5", "Sv": "11+", "N": "3", "Pt": "2"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Ecclesiarchy Battle Conclave", "Arco-flagellants"],
        [{"name": "Arco-flails", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"}],
        "Ignore Damage (6+)\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.\nEcclesiarchy Battle Conclave: This unit does not take up slots in a Detachment that contains any Ministorum Priests.",
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "-", "A": "2", "W": "1", "Ld": "5", "Sv": "11+", "N": "5", "Pt": "3"},
            {"M": '6"', "WS": "4+", "BS": "-", "A": "4", "W": "2", "Ld": "5", "Sv": "11+", "N": "10", "Pt": "6"},
        ],
    ),
    "Exorcist": u(
        "Exorcist",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "7"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Heavy", "Vehicle", "Exorcist"],
        [
            {"name": "Exorcist Conflagration Rockets", "type": "Heavy", "range": '48"', "attacks": "3", "skill": "6+", "armorPen": "9+"},
            {"name": "Exorcist Missile Launcher", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "5+"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        options=["Instead of 1 Exorcist Missile Launcher, this unit can be equipped with Exorcist Conflagration Rockets."],
    ),
    "Immolator": u(
        "Immolator",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Heavy", "Vehicle", "Transport", "Immolator"],
        [
            {"name": "Immolation Flamer", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Twin Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Twin Multi-melta", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "10+", "armorPen": "4+"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "TRANSPORT: This unit can transport up to 6 friendly Adeptus Ministorum Infantry models. It cannot transport Jump Pack models and can only transport Adepta Sororitas models if they have the <Order>, Dialogus or Hospitaller keyword.",
        options=["Instead of 1 Immolation Flamer, this unit can be equipped with one of the following: 1 Twin Heavy Bolter; 1 Twin Multi-melta."],
    ),
    "Mortifiers": u(
        "Mortifiers",
        {"M": '9"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Heavy", "Vehicle", "Mortifiers"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Mortifier Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "7+"},
        ],
        "Ignore Damage (6+)",
        profiles=[
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "2", "Pt": "8"},
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "7+", "N": "3", "Pt": "12"},
            {"M": '9"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "7+", "N": "4", "Pt": "16"},
        ],
        options=["For each model this unit contains, it must also be equipped with one of the following: 2 Heavy Bolters; 2 Heavy Flamers; 1 Heavy Bolter and 1 Heavy Flamer."],
    ),
    "Penitent Engines": u(
        "Penitent Engines",
        {"M": '7"', "WS": "4+", "BS": "5+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "1", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Heavy", "Vehicle", "Penitent Engines"],
        [
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Penitent Engine Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "7+"},
        ],
        "Ignore Damage (6+)\nZealot: You can re-roll hit rolls for attacks made with melee weapons by this unit.",
        profiles=[
            {"M": '7"', "WS": "4+", "BS": "5+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "2", "Pt": "8"},
            {"M": '7"', "WS": "4+", "BS": "5+", "A": "3", "W": "3", "Ld": "6", "Sv": "7+", "N": "3", "Pt": "12"},
            {"M": '7"', "WS": "4+", "BS": "5+", "A": "4", "W": "4", "Ld": "6", "Sv": "7+", "N": "4", "Pt": "16"},
        ],
        options=["For each model this unit contains, it must also be equipped with 2 Heavy Flamers."],
    ),
    "Castigator": u(
        "Castigator",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "6"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Heavy", "Vehicle", "Castigator"],
        [
            {"name": "Castigator Autocannons", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "5+", "armorPen": "6+", "abilities": "Rapid Fire"},
            {"name": "Castigator Battle Cannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "7+"},
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        options=[
            "A Castigator is a unit that contains 1 model. It is equipped with: Castigator Autocannons; 3 Heavy Bolters; Armoured Tracks.",
            "Instead of 1 Castigator Autocannons, this unit can be equipped with 1 Castigator Battle Cannon.",
        ],
    ),
    "Paragon Warsuits": u(
        "Paragon Warsuits",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "5+", "N": "3", "Pt": "9"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Heavy", "Vehicle", "Walker", "Paragon Warsuits"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Paragon Storm Bolters", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Paragon War Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+"},
            {"name": "Paragon War Mace", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"},
        ],
        "Righteous Paragons: Re-roll hit rolls of 1 for attacks made by this unit that target Heavy or Super-heavy units.",
        options=[
            "Paragon Warsuits is a unit that contains 3 models. Every model is equipped with: Heavy Bolter; Paragon Storm Bolters; Paragon War Blade.",
            "Any model can have its Heavy Bolter replaced with 1 Multi-melta (Power Rating +1 per model).",
            "Any model can have its Paragon War Blade replaced with 1 Paragon War Mace.",
        ],
    ),
    "Repressor": u(
        "Repressor",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "7"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Heavy", "Vehicle", "Transport", "Repressor"],
        [
            {"name": "Twin Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "2", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Storm Bolter", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Dozer Ram", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "TRANSPORT: This unit can transport up to 10 friendly Adeptus Ministorum Infantry models. It cannot transport Jump Pack models and can only transport Adepta Sororitas models if they have the <Order>, Dialogus or Hospitaller keyword.",
        options=["A Repressor is a unit that contains 1 model. It is equipped with: Twin Heavy Flamer; Storm Bolter; Dozer Ram."],
    ),
    "Celestine & Geminae": u(
        "Celestine & Geminae",
        {"M": '12"', "WS": "2+", "BS": "2+", "A": "3", "W": "4", "Ld": "7", "Sv": "4+", "N": "3", "Pt": "14"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Fly", "Character", "Jump Pack", "Celestine", "Geminae Superia"],
        [
            {"name": "The Ardent Blade (Ranged)", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Ardent Blades", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        "Beacon of Faith: Improve the Save characteristic (to a maximum of 3+) of friendly Adepta Sororitas units by 1 whilst they are wholly within 6\" of this unit.\n"
        "Miraculous Intervention: The first time the number of damage markers next to this unit equals its Wounds characteristic, roll a D6; on a 2+ this unit is not destroyed, and one damage marker is removed from it.\n"
        "Lifewards: At the start of the Damage phase, Remove up to D3 blast markers from this Character.",
        options=["Celestine & Geminae is a unit that contains 3 models: 1 Celestine and 2 Geminae Superia. You can only include one of this unit in your army."],
    ),
    "Triumph of Saint Katherine": u(
        "Triumph of Saint Katherine",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "6"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "Light", "Infantry", "Triumph of Saint Katherine"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Relic Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "8+", "armorPen": "8+"},
        ],
        "The Fiery Heart: Friendly Adepta Sororitas units automatically pass Morale tests whilst they are within 6\" of this unit.\nSolemn Procession: This unit cannot embark aboard Transports.\nRelics of the Matriarchs: This unit has three relic abilities. In the Damage phase, after making saving throws for this unit, reduce the number of relic abilities this unit has for each damage marker it has. To do so, select one relic ability this unit has; this unit no longer has that relic ability. If damage markers are removed from this unit, select the relevant number of relic abilities for this unit to regain. This unit's relic abilities are as follows:\n• Add 1 to hit rolls for attacks made with melee weapons by friendly Adepta Sororitas units whilst they are within 6\" of this unit.\n• If this unit is on the battlefield at the start of the Generate Command Assets step, you generate one extra Command Asset.\n• Once per turn, instead of making a hit roll, wound roll or saving throw for an Adepta Sororitas unit within 6\" of this unit, you can use this ability. That hit roll, wound roll or saving throw is automatically passed (do not roll).",
    ),
    "Uriah Jacobus": u(
        "Uriah Jacobus",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "4"},
        ["Imperium", "Adeptus Ministorum", "Light", "Infantry", "Character", "Ministorum Priest", "Missionary", "Uriah Jacobus"],
        [
            {"name": "The Redeemer", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
        ],
        "Banner of Sanctity: Add 1 to the Leadership characteristic of friendly Adeptus Ministorum and Astra Militarum units whilst they are within 6\" of this unit.\nWar Hymns: Add 1 to the Attacks characteristic of friendly Adeptus Ministorum Infantry and Astra Militarum Infantry units whilst they are making Fight actions whilst within 6\" of any friendly units with this ability.",
    ),
    "Sororitas Rhino": u(
        "Sororitas Rhino",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Ministorum", "Adepta Sororitas", "<Order>", "Heavy", "Vehicle", "Transport", "Rhino", "Sororitas Rhino"],
        [
            {"name": "Storm Bolter", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "TRANSPORT: This unit can transport up to 10 friendly Adeptus Ministorum Infantry models. It cannot transport Jump Pack models and can only transport Adepta Sororitas models if they have the <Order>, Dialogus or Hospitaller keyword.",
    ),
}

SISTERS_SLOTS = [
    slot(1, "HQ", SISTERS["Morvenn Vahl"]),
    slot(2, "HQ", SISTERS["Canoness"]),
    slot(3, "HQ", SISTERS["Missionary"]),
    slot(4, "HQ", SISTERS["Hospitaller"]),
    slot(5, "Troops", SISTERS["Battle Sisters Squad"]),
    slot(6, "Troops", SISTERS["Zealots"]),
    slot(7, "Elites", SISTERS["Imagifier"]),
    slot(8, "Elites", SISTERS["Celestian Squad"]),
    slot(9, "Elites", SISTERS["Celestian Sacrosancts"]),
    slot(10, "Elites", SISTERS["Dialogus"]),
    slot(11, "Elites", SISTERS["Preacher"]),
    slot(12, "Elites", SISTERS["Repentia Superior"]),
    slot(13, "Elites", SISTERS["Sisters Repentia"]),
    slot(14, "Elites", SISTERS["Crusaders"]),
    slot(15, "Elites", SISTERS["Death Cult Assassins"]),
    slot(16, "Elites", SISTERS["Arco-flagellants"]),
    slot(17, "Fast", SISTERS["Dominion Squad"]),
    slot(18, "Fast", SISTERS["Novitiate Squad"]),
    slot(19, "Fast", SISTERS["Sanctifiers"]),
    slot(20, "Fast", SISTERS["Seraphim Squad"]),
    slot(21, "Fast", SISTERS["Zephyrim Squad"]),
    slot(22, "Heavy", SISTERS["Retributor Squad"]),
    slot(23, "Heavy", SISTERS["Exorcist"]),
    slot(24, "Heavy", SISTERS["Immolator"]),
    slot(25, "Heavy", SISTERS["Mortifiers"]),
    slot(26, "Heavy", SISTERS["Penitent Engines"]),
    slot(27, "Heavy", SISTERS["Castigator"]),
    slot(28, "Heavy", SISTERS["Paragon Warsuits"]),
    slot(29, "Transport", SISTERS["Immolator"]),
    slot(30, "Transport", SISTERS["Sororitas Rhino"]),
    slot(31, "Transport", SISTERS["Repressor"]),
    slot(32, "Lord", SISTERS["Celestine & Geminae"]),
]


# ---------------------------------------------------------------------------
# Adeptus Mechanicus unit datasheets (Apoc_Datasheet_Adeptus_Mechanicus_web.pdf)
# ---------------------------------------------------------------------------

ADMECH = {
    "Belisarius Cawl": u(
        "Belisarius Cawl",
        {"M": '6"', "WS": "2+", "BS": "2+", "A": "1", "W": "2", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "10"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "Mars", "Light", "Infantry", "Character", "Tech-Priest", "Belisarius Cawl"],
        [
            {"name": "Solar Atomiser", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "9+", "armorPen": "6+"},
            {"name": "Omnissian Axe", "type": "Melee", "range": "Melee", "attacks": "1", "skill": "8+", "armorPen": "8+"},
        ],
        "Lord of Mars: You can re-roll hit rolls for attacks made by friendly Mars units whilst they are within 6\" of this unit.\nMaster of Machines: At the end of the Action phase, this unit can attempt to repair one friendly Imperium Vehicle unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.\nArchmagos: At the start of the Generate Command Assets step, if this unit is a Warlord and is on the battlefield, you generate one extra Command Asset.\nSelf-repair Mechanisms: At the start of the Action phase, you can remove one damage marker from this unit.",
    ),
    "Tech-Priest Dominus": u(
        "Tech-Priest Dominus",
        {"M": '6"', "WS": "3+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "4+", "N": "1", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Character", "Tech-Priest", "Dominus"],
        [
            {"name": "Tech-Priest Weapons", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "8+", "armorPen": "8+"},
            {"name": "Omnissian Axe", "type": "Melee", "range": "Melee", "attacks": "1", "skill": "8+", "armorPen": "8+"},
        ],
        "Lord of the Machine Cult: Re-roll hit rolls of 1 for attacks made by friendly <Forge World> units whilst they are within 6\" of this unit.\nMaster of Machines: At the end of the Action phase, this unit can attempt to repair one friendly <Forge World> or Questor Mechanicus Vehicle unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.",
    ),
    "Tech-Priest Manipulus": u(
        "Tech-Priest Manipulus",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "4+", "N": "1", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Character", "Tech-Priest", "Manipulus"],
        [
            {"name": "Magnarail Lance", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "8+", "armorPen": "7+"},
            {"name": "Transonic Cannon", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Omnissian Staff", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Galvanic Field: Add 3\" to the Range characteristic of ranged weapons <Forge World> units are equipped with whilst they are within 6\" of any friendly units with this ability.\nMaster of Machines: At the end of the Action phase, this unit can attempt to repair one friendly <Forge World> or Questor Mechanicus Vehicle unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.",
        options=["Instead of 1 Magnarail Lance, this unit can be equipped with 1 Transonic Cannon."],
    ),
    "Skatarii Marshal": u(
        "Skatarii Marshal",
        {"M": '5"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "4"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Character", "Skatarii Marshal"],
        [
            {"name": "Radium Serpenta", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Control Stave", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        "Leadership Edict: Re-roll hit rolls of 1 for attacks made by friendly <Forge World> Skitarii units whilst they are within 6\" of this unit.",
        options=["A Skatarii Marshal is a unit that contains 1 model. It is equipped with: Radium Serpenta; Control Stave."],
    ),
    "Tech-Priest Enginseer": u(
        "Tech-Priest Enginseer",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Character", "Tech-Priest", "Enginseer"],
        [{"name": "Omnissian Axe & Servo-arm", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "7+"}],
        "Master of Machines: At the end of the Action phase, this unit can attempt to repair one friendly <Forge World> or Questor Mechanicus Vehicle unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.",
    ),
    "Sydonian Dragoons": u(
        "Sydonian Dragoons",
        {"M": '10"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Sydonian Dragoons"],
        [
            {"name": "Phosphor Serpenta", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Radium Jezzail", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "6+", "armorPen": "8+", "abilities": "Sniper"},
            {"name": "Taser Lance", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Incense Cloud: This unit is always an obscured target.\nBroad Spectrum Data-tether: Add 1 to the Leadership characteristic of <Forge World> units whilst they are within 3\" of any friendly units with this ability.",
        profiles=[
            {"M": '10"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "7+", "N": "3", "Pt": "15"},
            {"M": '10"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "6", "Sv": "7+", "N": "6", "Pt": "30"},
        ],
        options=[
            "For each model this unit contains, it must be equipped with one of the following: 1 Radium Jezzail; 1 Taser Lance.",
            "For each model this unit contains, it can also be equipped with 1 Phosphor Serpenta (Power Rating +1 per weapon).",
        ],
    ),
    "Skitarii Rangers": u(
        "Skitarii Rangers",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "3"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Skitarii Rangers"],
        [
            {"name": "Galvanic Rifles", "type": "Small Arms", "range": '30"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        profiles=[{"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "6"}],
    ),
    "Skitarii Vanguard": u(
        "Skitarii Vanguard",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "3"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Skitarii Vanguard"],
        [
            {"name": "Radium Carbines", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "7+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        profiles=[{"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "6"}],
    ),
    "Kataphron Breachers": u(
        "Kataphron Breachers",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "5", "Sv": "6+", "N": "3", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Kataphron Breachers"],
        [
            {"name": "Heavy Arc Rifle", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Torsion Cannon", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "5+"},
            {"name": "Kataphron Claws", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "6+"},
        ],
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "4", "Ld": "5", "Sv": "6+", "N": "6", "Pt": "12"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "3", "W": "6", "Ld": "5", "Sv": "6+", "N": "9", "Pt": "18"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "4", "W": "8", "Ld": "5", "Sv": "6+", "N": "12", "Pt": "24"},
        ],
        options=["For each model this unit contains, it must be equipped with one of the following: 1 Heavy Arc Rifle; 1 Torsion Cannon."],
    ),
    "Kataphron Destroyers": u(
        "Kataphron Destroyers",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "3", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Kataphron Destroyers"],
        [
            {"name": "Cognis Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Heavy Grav-cannon", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "7+", "armorPen": "5+"},
            {"name": "Phosphor Blaster", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Plasma Culverin", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "7+", "abilities": "Supercharge"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "4", "Ld": "5", "Sv": "8+", "N": "6", "Pt": "14"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "3", "W": "6", "Ld": "5", "Sv": "8+", "N": "9", "Pt": "21"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "4", "W": "8", "Ld": "5", "Sv": "8+", "N": "12", "Pt": "28"},
        ],
        options=[
            "For each model this unit contains, it must be equipped with one of the following: 1 Heavy Grav-cannon; 1 Plasma Culverin.",
            "For each model this unit contains, it must be equipped with one of the following: 1 Cognis Flamer; 1 Phosphor Blaster.",
        ],
    ),
    "Servitors": u(
        "Servitors",
        {"M": '5"', "WS": "5+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "4", "Pt": "2"},
        ["Imperium", "Adeptus Mechanicus", "<Forge World>", "Light", "Infantry", "Servitors"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Plasma Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "7+", "abilities": "Supercharge"},
            {"name": "Servo-arms", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "Mindlock: Change this unit's Weapon Skill and Ballistic Skill characteristics to 4+ whilst it is within 6\" of at least one friendly <Forge World> Tech-Priest unit.",
        options=["This unit can also be equipped with up to two of the following (Power Rating +1 per weapon): 1 Heavy Bolter; 1 Multi-melta; 1 Plasma Cannon."],
    ),
    "Cybernetica Datasmith": u(
        "Cybernetica Datasmith",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "4+", "N": "1", "Pt": "5"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Character", "Tech-Priest", "Cybernetica Datasmith"],
        [{"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"}],
        "Master of Machines: At the end of the Action phase, this unit can attempt to repair one friendly <Forge World> Kastelan Robots unit in base contact with it. If it does, roll one D6; on a 4+ remove one damage marker from that Kastelan Robots unit. Only one attempt to repair each unit can be made each turn.",
    ),
    "Sicarian Ruststalkers": u(
        "Sicarian Ruststalkers",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Sicarian Ruststalkers"],
        [
            {"name": "Chordclaws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Transonic Weapons", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "6+", "armorPen": "8+"},
        ],
        profiles=[{"M": '8"', "WS": "3+", "BS": "3+", "A": "2", "W": "4", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "10"}],
    ),
    "Sicarian Infiltrators": u(
        "Sicarian Infiltrators",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Sicarian Infiltrators"],
        [
            {"name": "Flechette Blasters", "type": "Small Arms", "range": '12"', "attacks": "x2", "skill": "8+", "armorPen": "10+"},
            {"name": "Stubcarbines", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Infiltrator Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        "Infiltrators, Terror Troops",
        profiles=[{"M": '8"', "WS": "3+", "BS": "3+", "A": "2", "W": "4", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "12"}],
        options=["Instead of Stubcarbines, this unit can be equipped with Flechette Blasters."],
    ),
    "Fulgurite Electro-Priests": u(
        "Fulgurite Electro-Priests",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "5", "Pt": "3"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Electro-Priests", "Fulgurite"],
        [{"name": "Electroleech Staves", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "7+"}],
        "Ignore Damage (5+)\nSiphoned Vigour: If an enemy unit is destroyed within 1\" of this unit, change this unit's Save characteristic to 6+ for the rest of the battle.",
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "6"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "3", "W": "3", "Ld": "6", "Sv": "10+", "N": "15", "Pt": "9"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "12"},
        ],
    ),
    "Corpuscarii Electro-Priests": u(
        "Corpuscarii Electro-Priests",
        {"M": '6"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Light", "Infantry", "Electro-Priests", "Corpuscarii"],
        [
            {"name": "Electrostatic Gauntlets (Ranged)", "type": "Small Arms", "range": '12"', "attacks": "x3", "skill": "6+", "armorPen": "8+"},
            {"name": "Electrostatic Gauntlets (Melee)", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "6+", "armorPen": "8+"},
        ],
        "Ignore Damage (5+)",
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "8"},
            {"M": '6"', "WS": "4+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "10+", "N": "15", "Pt": "12"},
            {"M": '6"', "WS": "4+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "16"},
        ],
    ),
    "Ironstrider Ballistarii": u(
        "Ironstrider Ballistarii",
        {"M": '10"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Heavy", "Vehicle", "Ironstrider Ballistarii"],
        [
            {"name": "Twin Cognis Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
            {"name": "Twin Cognis Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Broad Spectrum Data-tether: Add 1 to the Leadership characteristic of <Forge World> units whilst they are within 3\" of any friendly units with this ability.",
        profiles=[
            {"M": '10"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "8+", "N": "3", "Pt": "18"},
            {"M": '10"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "6", "Sv": "8+", "N": "6", "Pt": "36"},
        ],
        options=["For each model this unit contains, it must be equipped with one of the following: 1 Twin Cognis Autocannon; 1 Twin Cognis Lascannon."],
    ),
    "Kastelan Robots": u(
        "Kastelan Robots",
        {"M": '8"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "8", "Sv": "5+", "N": "2", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Cult Mechanicus", "<Forge World>", "Heavy", "Vehicle", "Kastelan Robots"],
        [
            {"name": "Heavy Phosphor Blaster", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Incendine Combustor", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
            {"name": "Kastelan Fists", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+"},
        ],
        "Battle Protocols: This unit has one of the abilities listed below, based on the order issued to its Detachment in the Orders phase. The ability lasts until the end of the turn. Note that even if that Detachment's order subsequently changes, the ability this unit has for that turn does not.\nAdvance: Add 1 to saving throws made for this unit.\nAimed Fire: You can re-roll hit rolls for attacks made by this unit with ranged weapons.\nAssault: You can re-roll hit rolls for attacks made by this unit with melee weapons.",
        profiles=[
            {"M": '8"', "WS": "4+", "BS": "4+", "A": "4", "W": "4", "Ld": "8", "Sv": "5+", "N": "4", "Pt": "14"},
            {"M": '8"', "WS": "4+", "BS": "4+", "A": "6", "W": "6", "Ld": "8", "Sv": "5+", "N": "6", "Pt": "21"},
        ],
        options=[
            "For each model this unit contains, it must be equipped with one of the following: 1 Heavy Phosphor Blaster; 1 Incendine Combustor.",
            "For each model this unit contains, it must be equipped with one of the following: 2 Heavy Phosphor Blasters; 1 Kastelan Fists.",
        ],
    ),
    "Onager Dunecrawler": u(
        "Onager Dunecrawler",
        {"M": '8"', "WS": "5+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "8"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Onager Dunecrawler"],
        [
            {"name": "Cognis Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Eradication Beamer", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "6+"},
            {"name": "Icarus Array", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+", "abilities": "Anti-air"},
            {"name": "Neutron Laser", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "11+", "armorPen": "3+", "abilities": "Destroyer"},
            {"name": "Twin Heavy Phosphor Blaster", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "8+"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Emanatus Force Field: Add 1 to saving throws made for this unit whilst it is within 6\" of any other friendly <Forge World> Onager Dunecrawler units.\nBroad Spectrum Data-tether: Add 1 to the Leadership characteristic of <Forge World> units whilst they are within 3\" of any friendly units with this ability.",
        options=[
            "Instead of 1 Eradication Beamer, this unit can be equipped with one of the following: 1 Icarus Array; 1 Neutron Laser and 1 Cognis Heavy Stubber; 1 Twin Heavy Phosphor Blaster.",
            "This unit can also be equipped with 1 Cognis Heavy Stubber.",
        ],
    ),
    "Skorpius Dunerider": u(
        "Skorpius Dunerider",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Transport", "Skorpius Dunerider"],
        [
            {"name": "Cognis Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Twin Cognis Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "8+", "armorPen": "10+"},
            {"name": "Armoured Bulk", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Broad Spectrum Data-tether: Add 1 to the Leadership characteristic of <Forge World> units whilst they are within 3\" of any friendly units with this ability.\nTRANSPORT: This unit can transport 10 Secutarii Infantry or <Forge World> Infantry models. It cannot transport Belisarius Cawl, Kataphron Breacher or Kataphron Destroyer units.",
    ),
    "Skorpius Disintegrator": u(
        "Skorpius Disintegrator",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "8"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Skorpius Disintegrator"],
        [
            {"name": "Belleros Energy Cannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "6+", "armorPen": "7+", "abilities": "Barrage"},
            {"name": "Cognis Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Disruptor Missile Launcher", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "8+"},
            {"name": "Ferrumite Cannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
            {"name": "Armoured Bulk", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Broad Spectrum Data-tether: Add 1 to the Leadership characteristic of <Forge World> units whilst they are within 3\" of any friendly units with this ability.",
        options=["Instead of 1 Ferrumite Cannon, this unit can be equipped with 1 Belleros Energy Cannon (Power Rating +1)."],
    ),
    "Hastarii Exterminators": u(
        "Hastarii Exterminators",
        {"M": '5"', "WS": "3+", "BS": "4+", "A": "1", "W": "2", "Ld": "7", "Sv": "7+", "N": "5", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Hastarii Exterminators"],
        [
            {"name": "Eradication Caster", "type": "Small Arms", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Hastarii Arc Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        options=[
            "Hastarii Exterminators are a unit that contains 5 models. It is equipped with: Eradication Caster; Hastarii Arc Blaster; Close Combat Weapons.",
        ],
    ),
    "Hastarii Fusiliers": u(
        "Hastarii Fusiliers",
        {"M": '5"', "WS": "3+", "BS": "4+", "A": "1", "W": "2", "Ld": "7", "Sv": "7+", "N": "5", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Infantry", "Hastarii Fusiliers"],
        [
            {"name": "Hastarii Phosphor Blaster", "type": "Small Arms", "range": '18"', "attacks": "3", "skill": "7+", "armorPen": "9+"},
            {"name": "Hastarii Arc Blaster", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        options=[
            "Hastarii Fusiliers are a unit that contains 5 models. It is equipped with: Neutron Fusil; Hastarii Phosphor Blaster; Close Combat Weapons.",
        ],
    ),
    "Serberys Sulphurhounds": u(
        "Serberys Sulphurhounds",
        {"M": '12"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "7", "Sv": "6+", "N": "5", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Light", "Cavalry", "Serberys Sulphurhounds"],
        [
            {"name": "Pistols", "type": "Small Arms", "range": '12"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Sulphur Breath", "type": "Small Arms", "range": '9"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Clawed Limbs", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        options=[
            "Serberys Sulphurhounds are a unit that contains 5 models. It is equipped with:  Pistols; Sulphur Breath; Clawed Limbs.",
        ],
    ),
    "Serberys Raiders": u(
        "Serberys Raiders",
        {"M": '12"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "7", "Sv": "6+", "N": "5", "Pt": "6"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Infiltrators", "Light", "Cavalry", "Serberys Raiders"],
        [
            {"name": "Galvanic Carbine", "type": "Small Arms", "range": '18"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Claws & Sabers", "type": "Melee", "range": "2x Melee", "attacks": "User", "skill": "7+", "armorPen": "8+"},
        ],
        options=[
            "Serberys Raiders are a unit that contains 5 models. It is equipped with: Galvanic Carbine; Claws & Sabres",
        ],
    ),
    "Pteraxii Sterylizors": u(
        "Pteraxii Sterylizors",
        {"M": '12"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "8+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Infiltrators", "Light", "Infantry", "Fly", "Pteraxii Sterylizors"],
        [
            {"name": "Phosphor Torch", "type": "Small Arms", "range": '12"', "attacks": "User x2", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Pteraxii Talons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "8+", "armorPen": "10+"},
        ],
        profiles=[{"M": '12"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "7", "Sv": "8+", "N": "10", "Pt": "8"}],
        options=[
            "Pteraxii Sterylizors are a unit that contains 5 models. It can contain 10 models (Power Rating 8). It is equipped with: Phosphor Torch; Pteraxii Talons.",
        ],
    ),
    "Pteraxii Skywalkers": u(
        "Pteraxii Skywalkers",
        {"M": '12"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "8+", "N": "5", "Pt": "4"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Infiltrators", "Light", "Infantry", "Fly", "Pteraxii Skywalkers"],
        [
            {"name": "Flechette Carbine", "type": "Small Arms", "range": '18"', "attacks": "x4", "skill": "8+", "armorPen": "12+"},
            {"name": "Close Combat Weapon", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        profiles=[{"M": '12"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "7", "Sv": "8+", "N": "10", "Pt": "8"}],
        options=[
            "Pteraxii Skywalkers are a unit that contains 5 models. It can contain 10 models (Power Rating 8). It is equipped with: Flechette Carbine; Close Combat Weapon.",
        ],
    ),
    "Archaeopter Stratoraptor": u(
        "Archaeopter Stratoraptor",
        {"M": '20"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "7", "Sv": "3+", "N": "1", "Pt": "8"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Fly", "Aircraft", "Archaeopter Stratoraptor"],
        [
            {"name": "Cognis Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Twin Cognis Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Heavy Phosphor Blaster", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Hover",
        options=["An Archaeopter Stratoraptor is a unit that contains 1 model. It is equipped with: Cognis Heavy Stubber; Hellstrike Missiles; Heavy Phosphor Blaster; Armoured Hull."],
    ),
    "Archaeopter Fusilave": u(
        "Archaeopter Fusilave",
        {"M": '20"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "7", "Sv": "3+", "N": "1", "Pt": "7"},
        ["Imperium", "Adeptus Mechanicus", "Skitarii", "<Forge World>", "Heavy", "Vehicle", "Fly", "Aircraft", "Archaeopter Fusilave"],
        [
            {"name": "Cognis Heavy Stubber Array", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Hover\nBomb Rack: Each time this unit ends a Move action, you can select one enemy unit it moved over during that Move action and roll six D6: for each 4+, that unit suffers 1 mortal wound.",
        options=["An Archaeopter Fusilave is a unit that contains 1 model. It is equipped with: Cognis Heavy Stubber Array; Armoured Hull."],
    ),
    "Mars Pattern Knight": u(
        "Mars Pattern Knight",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Imperium", "Adeptus Mechanicus", "Questor Mechanicus", "Mars", "Super-heavy", "Vehicle", "Titanic", "Questoris Class", "Knight Paladin"],
        [
            {"name": "Rapid-fire Battle Cannon", "type": "Heavy", "range": '72"', "attacks": "4", "skill": "6+", "armorPen": "6+"},
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Ironstorm Missile Pod", "type": "Heavy", "range": '72"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
            {"name": "Stormspear Rocket Pod", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
            {"name": "Twin Icarus Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Anti-air"},
            {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
        ],
        "Questor Mechanicus: This unit has the Questor Mechanicus keyword and can benefit from Adeptus Mechanicus Master of Machines abilities.",
        options=[
            "A Mars Pattern Knight is a Questoris-class Knight Paladin equipped with: Rapid-fire Battle Cannon; 2 Heavy Stubbers; Reaper Chainsword.",
            "• Instead of 1 Reaper Chainsword, this unit can be equipped with 1 Thunderstrike Gauntlet.",
            "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
        ],
    ),
    "Mars Pattern Armiger": u(
        "Mars Pattern Armiger",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Imperium", "Adeptus Mechanicus", "Questor Mechanicus", "Mars", "Heavy", "Vehicle", "Armiger Class"],
        [
            {"name": "Armiger Autocannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
            {"name": "Thermal Spear", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
            {"name": "Reaper Chain-cleaver", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        "Vehicle Squadron: Each Lord of War slot in a Detachment allows you to take up to three of this unit in your army, instead of one. Each unit taken for a single Lord of War slot must be placed at the same time and within 6\" of each other unit taken for the same slot the first time they are set up.",
        options=[
            "Select Armiger Helverin or Armiger Warglaive loadout when including this unit.",
            "Armiger Helverin: equipped with 2 Armiger Autocannons, Heavy Stubber, Armoured Feet.",
            "Armiger Warglaive: equipped with Heavy Stubber, Thermal Spear, Armoured Feet, Reaper Chain-cleaver.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
        ],
    ),
}

ADMECH_SLOTS = [
    slot(1, "HQ", ADMECH["Belisarius Cawl"]),
    slot(2, "HQ", ADMECH["Tech-Priest Dominus"]),
    slot(3, "HQ", ADMECH["Tech-Priest Manipulus"]),
    slot(4, "HQ", ADMECH["Skatarii Marshal"]),
    slot(5, "Troops", ADMECH["Skitarii Rangers"]),
    slot(6, "Troops", ADMECH["Skitarii Vanguard"]),
    slot(7, "Elites", ADMECH["Tech-Priest Enginseer"]),
    slot(8, "Elites", ADMECH["Corpuscarii Electro-Priests"]),
    slot(9, "Elites", ADMECH["Cybernetica Datasmith"]),
    slot(10, "Elites", ADMECH["Fulgurite Electro-Priests"]),
    slot(11, "Elites", ADMECH["Kataphron Breachers"]),
    slot(12, "Elites", ADMECH["Servitors"]),
    slot(13, "Elites", ADMECH["Sicarian Ruststalkers"]),
    slot(14, "Elites", ADMECH["Sicarian Infiltrators"]),
    slot(15, "Elites", ADMECH["Sydonian Dragoons"]),
    slot(16, "Elites", ADMECH["Hastarii Exterminators"]),
    slot(17, "Elites", ADMECH["Hastarii Fusiliers"]),
    slot(18, "Fast", ADMECH["Ironstrider Ballistarii"]),
    slot(19, "Fast", ADMECH["Kastelan Robots"]),
    slot(20, "Fast", ADMECH["Sicarian Infiltrators"]),
    slot(21, "Fast", ADMECH["Serberys Sulphurhounds"]),
    slot(22, "Fast", ADMECH["Serberys Raiders"]),
    slot(23, "Fast", ADMECH["Pteraxii Sterylizors"]),
    slot(24, "Fast", ADMECH["Pteraxii Skywalkers"]),
    slot(25, "Heavy", ADMECH["Ironstrider Ballistarii"]),
    slot(26, "Heavy", ADMECH["Kastelan Robots"]),
    slot(27, "Heavy", ADMECH["Kataphron Destroyers"]),
    slot(28, "Heavy", ADMECH["Onager Dunecrawler"]),
    slot(29, "Heavy", ADMECH["Skorpius Disintegrator"]),
    slot(30, "Air", ADMECH["Archaeopter Stratoraptor"]),
    slot(31, "Air", ADMECH["Archaeopter Fusilave"]),
    slot(32, "Transport", ADMECH["Skorpius Dunerider"]),
    slot(33, "Lord", ADMECH["Mars Pattern Knight"]),
    slot(34, "Lord", ADMECH["Mars Pattern Armiger"]),
]


FILE_PREFIX = "Apoc40k-Armies-1st - "

FACTION_OUTPUTS = [
    ("Drukhari", "Drukhari", DRUKHARI_SLOTS),
    ("Sisters of Battle", "Sisters of Battle", SISTERS_SLOTS),
    ("Adeptus Mechanicus", "Adeptus Mechanicus", ADMECH_SLOTS),
]


def main():
    for faction_name, file_label, slots in FACTION_OUTPUTS:
        basename = f"{FILE_PREFIX}{file_label}"
        csv_path = OUTPUT_DIR / f"{basename}.csv"
        json_path = OUTPUT_DIR / f"{basename}.json"
        write_csv(csv_path, slots)
        write_json(json_path, faction_name, f"{basename}.csv", slots)
        print(f"Wrote {csv_path.name} and {json_path.name} ({len(slots)} units)")


if __name__ == "__main__":
    main()
