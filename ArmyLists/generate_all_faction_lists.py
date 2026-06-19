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
    faction_keys = {"Aeldari", "Drukhari", "T'au Empire", "Imperium", "Adeptus Ministorum",
                    "Adepta Sororitas", "Adeptus Mechanicus", "Cult Mechanicus", "Skitarii",
                    "Kroot", "Vespid", "Incubi", "Prophets of Flesh", "Cult of Strife",
                    "Farsight Enclaves", "T'au Sept", "Order of Our Martyred Lady", "Mars",
                    "Questor Mechanicus", "Chaos", "Heretic Astartes", "Astra Militarum",
                    "Adeptus Astartes", "Knights", "Imperial Knights", "Chaos Knights",
                    "Servants of the Abyss", "Legiones Daemonica", "Daemon",
                    "Cadian", "Officio Prefectus", "Militarum Tempestus", "Militarum Auxilia",
                    "Astra Telepathica", "Scholastica Psykana", "Aeronautica Imperialis",
                    "Black Legion", "Khorne", "Nurgle", "Slaanesh", "Tzeentch"}
    placeholder_keys = {"<Kabal>", "<Wych Cult>", "<Haemonculus Coven>", "<Sept>",
                        "<Order>", "<Forge World>", "<Legion>", "<Mark of Chaos>",
                        "<Chapter>", "<Regiment>", "<Questor Allegiance>", "<Questor Traitoris>",
                        "<Household>", "<Craftworld>"}
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
    "Lhamaean": u(
        "Lhamaean",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "1", "Pt": "1"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Court of the Archon", "Lhamaean"],
        [{"name": "Shaimeshi Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "12+"}],
        "Court of the Archon: You can re-roll hit rolls for attacks made by this unit whilst it is within 3\" of any friendly <Kabal> Archon units. This unit does not take up a slot in a Detachment that includes any <Kabal> Archon units.",
    ),
    "Medusae": u(
        "Medusae",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "1", "Pt": "2"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Court of the Archon", "Medusae"],
        [
            {"name": "Eyeburst Attack (Ranged)", "type": "Heavy", "range": '9"', "attacks": "1", "skill": "10+", "armorPen": "10+"},
            {"name": "Eyeburst Attack (Melee)", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "12+"},
        ],
        "Court of the Archon: You can re-roll hit rolls for attacks made by this unit whilst it is within 3\" of any friendly <Kabal> Archon units. This unit does not take up a slot in a Detachment that includes any <Kabal> Archon units.",
    ),
    "Scourges": u(
        "Scourges",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "7+", "N": "5", "Pt": "4"},
        ["Aeldari", "Drukhari", "Light", "Infantry", "Fly", "Scourges"],
        [
            {"name": "Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Dark Lance", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Haywire Blaster", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "12+", "armorPen": "4+"},
            {"name": "Heat Lance", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "9+", "armorPen": "6+"},
            {"name": "Shredder", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "6+", "armorPen": "8+"},
            {"name": "Splinter Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "5+", "armorPen": "12+", "abilities": "Rapid Fire"},
            {"name": "Shardcarbines", "type": "Small Arms", "range": '18"', "attacks": "x2", "skill": "5+", "armorPen": "12+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[{"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "10", "Pt": "10"}],
        options=[
            "This unit can also be equipped with up to four of the following in any combination (Power Rating +2 per Shredder or Splinter Cannon; Power Rating +1 per other weapon); 1 Blaster; 1 Dark Lance; 1 Haywire Blaster; 1 Heat Lance; 1 Shredder; 1 Splinter Cannon.",
            "If this unit contains 10 models or is not equipped with any Heavy weapons, it is also equipped with Shardcarbines.",
        ],
    ),
    "Sslyth": u(
        "Sslyth",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "4", "Sv": "9+", "N": "1", "Pt": "2"},
        ["Aeldari", "Drukhari", "<Kabal>", "Light", "Infantry", "Court of the Archon", "Sslyth"],
        [{"name": "Sslyth Battle-blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"}],
        "Ignore Damage (6+)\nCourt of the Archon: You can re-roll hit rolls for attacks made by this unit whilst it is within 3\" of any friendly <Kabal> Archon units. This unit does not take up a slot in a Detachment that includes any <Kabal> Archon units.\nCold-blooded Bodyguard: At the start of the Damage phase, you can select one friendly <Kabal> Archon unit that has at least one blast marker next to it and is within 3\" of this unit. Remove up to D3 blast markers from that Archon unit and place them next to this unit.",
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
    "Webway Gate": u(
        "Webway Gate",
        {"M": "-", "WS": "-", "BS": "-", "A": "-", "W": "3", "Ld": "-", "Sv": "5+", "N": "1", "Pt": "6"},
        ["Aeldari", "Heavy", "Vehicle", "Building", "Webway Gate"],
        [],
        "Shimmering Arrival: When this unit is set up on the battlefield, it can be set up anywhere that is more than 12\" away from your opponent's deployment zone and any enemy units, and more than 3\" away from any other terrain features or the centre of any objective markers.\nWebway Gate: This unit is never Out of Command: an Out of Command marker is never placed next to it. When measuring distances to and from this unit, measure to and from the closest point of this unit. This unit cannot be affected by Command Assets or other units' abilities. If a Webway Gate is destroyed, remove both pieces from the battlefield.\nWebway Strike: After this unit is set up on the battlefield, any friendly Aeldari units, other than Fortifications, that have not already been set up can be set up in a webway spar as Tactical Reserves instead of being set up on the battlefield. In the Set Up Reinforcements step, one unit in a webway spar can emerge from each friendly Webway Gate as reinforcements; a unit emerging from a Webway Gate must be set up wholly within 3\" of that Webway Gate and more than 9\" away from any enemy units. No more than half the total number of units in your army can be set up in Tactical Reserves.",
    ),
}

DRUKHARI_SLOTS = [
    slot(1, "HQ", DRUKHARI["Drazhar"]),
    slot(2, "HQ", DRUKHARI["Archon"]),
    slot(3, "HQ", DRUKHARI["Succubus"]),
    slot(4, "HQ", DRUKHARI["Haemonculus"]),
    slot(5, "Fast", DRUKHARI["Reavers"]),
    slot(6, "Troops", DRUKHARI["Kabalite Warriors"]),
    slot(7, "Troops", DRUKHARI["Wyches"]),
    slot(8, "Elites", DRUKHARI["Incubi"]),
    slot(9, "Elites", DRUKHARI["Mandrakes"]),
    slot(10, "Elites", DRUKHARI["Grotesques"]),
    slot(11, "Elites", DRUKHARI["Wracks"]),
    slot(12, "Elites", DRUKHARI["Lhamaean"]),
    slot(13, "Elites", DRUKHARI["Medusae"]),
    slot(14, "Elites", DRUKHARI["Scourges"]),
    slot(15, "Elites", DRUKHARI["Sslyth"]),
    slot(16, "Fast", DRUKHARI["Hellions"]),
    slot(17, "Fast", DRUKHARI["Khymerae"]),
    slot(18, "Fast", DRUKHARI["Clawed Fiends"]),
    slot(19, "Fast", DRUKHARI["Razorwing Flocks"]),
    slot(20, "Fast", DRUKHARI["Beastmaster"]),
    slot(21, "Heavy", DRUKHARI["Talos"]),
    slot(22, "Heavy", DRUKHARI["Cronos"]),
    slot(23, "Heavy", DRUKHARI["Ravager"]),
    slot(24, "Heavy", DRUKHARI["Hellions"]),
    slot(25, "Heavy", DRUKHARI["Scourges"]),
    slot(26, "Heavy", DRUKHARI["Talos"]),
    slot(27, "Lord", DRUKHARI["Lelith Hesperax"]),
    slot(28, "Lord", DRUKHARI["Urien Rakarth"]),
    slot(29, "Transport", DRUKHARI["Raider"]),
    slot(30, "Air", DRUKHARI["Razorwing Jetfighter"]),
    slot(31, "Transport", DRUKHARI["Venom"]),
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
    slot(1, "HQ", SISTERS["Celestine"]),
    slot(2, "HQ", SISTERS["Canoness"]),
    slot(3, "HQ", SISTERS["Imagifier"]),
    slot(4, "HQ", SISTERS["Hospitaller"]),
    slot(5, "Fast", SISTERS["Junith Eruita"]),
    slot(6, "Troops", SISTERS["Battle Sisters Squad"]),
    slot(7, "Troops", SISTERS["Dominion Squad"]),
    slot(8, "Elites", SISTERS["Celestian Squad"]),
    slot(9, "Elites", SISTERS["Retributor Squad"]),
    slot(10, "Elites", SISTERS["Repentia Superior"]),
    slot(11, "Elites", SISTERS["Sisters Repentia"]),
    slot(12, "Elites", SISTERS["Dialogus"]),
    slot(13, "Elites", SISTERS["Geminae Superia"]),
    slot(14, "Elites", SISTERS["Missionary"]),
    slot(15, "Elites", SISTERS["Preacher"]),
    slot(16, "Fast", SISTERS["Seraphim Squad"]),
    slot(17, "Fast", SISTERS["Zephyrim Squad"]),
    slot(18, "Fast", SISTERS["Crusaders"]),
    slot(19, "Fast", SISTERS["Death Cult Assassins"]),
    slot(20, "Fast", SISTERS["Arco-flagellants"]),
    slot(21, "Heavy", SISTERS["Exorcist"]),
    slot(22, "Heavy", SISTERS["Immolator"]),
    slot(23, "Heavy", SISTERS["Mortifiers"]),
    slot(24, "Heavy", SISTERS["Penitent Engines"]),
    slot(25, "Heavy", SISTERS["Exorcist"]),
    slot(26, "Heavy", SISTERS["Mortifiers"]),
    slot(27, "Lord", SISTERS["Triumph of Saint Katherine"]),
    slot(28, "Lord", SISTERS["Uriah Jacobus"]),
    slot(29, "Transport", SISTERS["Sororitas Rhino"]),
    slot(30, "Air", SISTERS["Seraphim Squad"]),
    slot(31, "Transport", SISTERS["Immolator"]),
    slot(32, "Lord", SISTERS["Penitent Engines"]),
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
}

ADMECH_SLOTS = [
    slot(1, "HQ", ADMECH["Belisarius Cawl"]),
    slot(2, "HQ", ADMECH["Tech-Priest Dominus"]),
    slot(3, "HQ", ADMECH["Tech-Priest Manipulus"]),
    slot(4, "HQ", ADMECH["Tech-Priest Enginseer"]),
    slot(5, "Fast", ADMECH["Sydonian Dragoons"]),
    slot(6, "Troops", ADMECH["Skitarii Rangers"]),
    slot(7, "Troops", ADMECH["Skitarii Vanguard"]),
    slot(8, "Elites", ADMECH["Kataphron Breachers"]),
    slot(9, "Elites", ADMECH["Kataphron Destroyers"]),
    slot(10, "Elites", ADMECH["Servitors"]),
    slot(11, "Elites", ADMECH["Cybernetica Datasmith"]),
    slot(12, "Elites", ADMECH["Sicarian Ruststalkers"]),
    slot(13, "Elites", ADMECH["Sicarian Infiltrators"]),
    slot(14, "Elites", ADMECH["Fulgurite Electro-Priests"]),
    slot(15, "Elites", ADMECH["Corpuscarii Electro-Priests"]),
    slot(16, "Fast", ADMECH["Kastelan Robots"]),
    slot(17, "Fast", ADMECH["Ironstrider Ballistarii"]),
    slot(18, "Fast", ADMECH["Sydonian Dragoons"]),
    slot(19, "Fast", ADMECH["Sicarian Infiltrators"]),
    slot(20, "Fast", ADMECH["Fulgurite Electro-Priests"]),
    slot(21, "Heavy", ADMECH["Onager Dunecrawler"]),
    slot(22, "Heavy", ADMECH["Skorpius Disintegrator"]),
    slot(23, "Heavy", ADMECH["Ironstrider Ballistarii"]),
    slot(24, "Heavy", ADMECH["Kastelan Robots"]),
    slot(25, "Heavy", ADMECH["Kataphron Breachers"]),
    slot(26, "Heavy", ADMECH["Kataphron Destroyers"]),
    slot(27, "Lord", ADMECH["Tech-Priest Dominus"]),
    slot(28, "Lord", ADMECH["Onager Dunecrawler"]),
    slot(29, "Transport", ADMECH["Skorpius Dunerider"]),
    slot(30, "Air", ADMECH["Ironstrider Ballistarii"]),
    slot(31, "Transport", ADMECH["Skorpius Disintegrator"]),
    slot(32, "Lord", ADMECH["Kastelan Robots"]),
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
