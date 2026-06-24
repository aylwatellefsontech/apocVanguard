#!/usr/bin/env python3
"""Apply batch unit stat updates to Apoc40k army list CSVs."""

import csv
import re
import shutil
from pathlib import Path

ARMY_LISTS_DIR = Path(__file__).resolve().parent
WEB_ARMY_LISTS_DIR = ARMY_LISTS_DIR.parent / "web" / "src" / "ArmyLists"

CSV_HEADER = [
    "No", "Type", "Name",
    "M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt",
    "Weapon", "Type", "Rng", "A", "SAP", "SAT", "Abilties", "Keywords", "Options",
]

FIELDNAMES = [
    "No", "Type", "Name",
    "M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt",
    "Weapon", "WeaponType", "Rng", "WeaponA", "SAP", "SAT", "Abilities",
    "Keywords", "Options",
]

STAT_COLS = ["M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt"]
WEAPON_COLS = ["Weapon", "WeaponType", "Rng", "WeaponA", "SAP", "SAT", "Abilities"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        next(reader, None)
        rows = [dict(zip(FIELDNAMES, row + [""] * (len(FIELDNAMES) - len(row)))) for row in reader]
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        writer.writerow([""] * len(CSV_HEADER))
        for row in rows:
            writer.writerow([row.get(col, "") for col in FIELDNAMES])


def unit_rows(rows, no):
    return [r for r in rows if r["No"].strip() == str(no)]


CANONICAL_TYPES = {
    "hq": "HQ", "troops": "Troops", "elites": "Elites", "elite": "Elites",
    "fast": "Fast", "heavy": "Heavy", "lord": "Lord", "transport": "Transport", "air": "Air",
}
UNIT_TYPES = set(CANONICAL_TYPES.values())


def norm_type(value):
    return CANONICAL_TYPES.get(value.strip().lower(), value.strip())


def header_row(rows, no):
    for r in rows:
        if r["No"].strip() == str(no) and norm_type(r.get("Type", "")) in UNIT_TYPES:
            return r
    return None


def profile_rows(rows, no):
    return [r for r in rows if r["No"].strip() == str(no) and not r["Type"].strip() and r["M"].strip()]


def weapon_rows(rows, no, weapon_name=None):
    result = []
    for r in rows:
        if r["No"].strip() != str(no):
            continue
        if not r["Weapon"].strip():
            continue
        if weapon_name and r["Weapon"].strip() != weapon_name:
            continue
        result.append(r)
    return result


def set_stats(row, **kwargs):
    for k, v in kwargs.items():
        row[k] = v


def remove_profiles(rows, no, keep_ns):
    keep = {str(n) for n in keep_ns}
    return [
        r for r in rows
        if not (r["No"].strip() == str(no) and not r["Type"].strip() and r["M"].strip() and r["N"].strip() not in keep)
    ]


def remove_unit(rows, no):
    return [r for r in rows if r["No"].strip() != str(no)]


def update_weapon(rows, no, weapon, **kwargs):
    if "A" in kwargs:
        kwargs["WeaponA"] = kwargs.pop("A")
    for r in weapon_rows(rows, no, weapon):
        for k, v in kwargs.items():
            r[k] = v


def set_profiles(rows, no, profiles):
    """Replace profile rows for a unit, keeping non-profile continuation rows."""
    new_rows = []
    inserted = False
    for r in rows:
        if r["No"].strip() == str(no) and not r["Type"].strip() and r["M"].strip():
            if not inserted:
                for p in profiles:
                    nr = {col: "" for col in FIELDNAMES}
                    nr["No"] = str(no)
                    for k, v in p.items():
                        nr[k] = v
                    new_rows.append(nr)
                inserted = True
            continue
        new_rows.append(r)
    return new_rows


def add_ability(row, ability):
    existing = row.get("Abilities", "").strip()
    if ability in existing:
        return
    row["Abilities"] = f"{existing}\n{ability}".strip() if existing else ability


def apply_imperial_guard(rows):
    set_stats(header_row(rows, 2), Type="Elites")
    set_stats(header_row(rows, 6), WS="4+", BS="4+")
    set_stats(header_row(rows, 11), M='6"', WS="4+", BS="4+", A="1", W="1", Ld="5", Sv="10+", N="5", Pt="2")
    rows[:] = set_profiles(rows, 11, [{"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "3"}])
    rows[:] = remove_profiles(rows, 8, ["20"])
    for r in rows:
        if r["No"].strip() == "8" and "30 models" in r.get("Abilities", ""):
            r["Abilities"] = "Conscripts is a unit that contains 20 models."
        if r["No"].strip() == "8" and "per 30 models" in r.get("Options", ""):
            r["Options"] = ""
    update_weapon(rows, 32, "Commissar Weapons", SAP="10+", SAT="11+")
    set_stats(header_row(rows, 27), A="1", W="2", N="5", Pt="3")
    rows[:] = set_profiles(rows, 27, [{"M": '10"', "WS": "4+", "BS": "4+", "A": "2", "W": "4", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "6"}])
    for no in (15, 16, 24):
        set_stats(header_row(rows, no), Sv="7+", Pt=str(int(header_row(rows, no)["Pt"]) - 1))
    set_stats(header_row(rows, 21), W="3", Pt="11")
    update_weapon(rows, 12, "Ripper Guns", SAP="7+", SAT="9+")
    update_weapon(rows, 12, "Ripper Gun Stocks", SAP="7+", SAT="9+")

    # Aquilons -> Tempestus infantry
    aquilon_rows = unit_rows(rows, 31)
    idx = rows.index(aquilon_rows[0])
    new_aquilon = [
        {**{c: "" for c in FIELDNAMES}, "No": "31", "Type": "Fast", "Name": "Aquilons",
         "M": '10"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "4",
         "Abilities": "Infiltrators", "Keywords": "Imperium, Astra Militarum, Militarum Tempestus\nLight, Infantry, Militarum Tempestus Scions, Aquilons",
         "Options": "per 10 models (Power Rating 6): It can contain 10 models (Power Rating 6)."},
        {**{c: "" for c in FIELDNAMES}, "No": "31", "M": '10"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "6"},
        {**{c: "" for c in FIELDNAMES}, "No": "31", "Abilities": "Aquilons are Tempestus Scions with Move 10\" and Infiltrators. It can contain 10 models (Power Rating 6)."},
        {**{c: "" for c in FIELDNAMES}, "No": "31", "Weapon": "Hot-shot Lasguns", "WeaponType": "Small Arms", "Rng": '18"', "WeaponA": "User", "SAP": "6+", "SAT": "8+", "Abilities": "Rapid Fire"},
        {**{c: "" for c in FIELDNAMES}, "No": "31", "Weapon": "Close Combat Weapons", "WeaponType": "Melee", "Rng": "Melee", "WeaponA": "User", "SAP": "8+", "SAT": "10+"},
    ]
    rows[idx:idx + len(aquilon_rows)] = new_aquilon
    return rows


def apply_sisters(rows):
    base = {"M": '6"', "WS": "4+", "BS": "3+", "Ld": "7", "Sv": "6+"}
    set_stats(header_row(rows, 5), **base, A="1", W="1", N="5", Pt="3")
    rows[:] = set_profiles(rows, 5, [{"M": '6"', "WS": "4+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "10", "Pt": "6"}])
    rows[:] = remove_profiles(rows, 5, ["5", "10"])
    set_stats(header_row(rows, 6), Sv="11+")
    for r in profile_rows(rows, 6):
        r["Sv"] = "11+"
    update_weapon(rows, 9, "Anointed Halberds", SAP="6+", SAT="8+")
    set_stats(header_row(rows, 9), Sv="6+")
    for r in profile_rows(rows, 9):
        r["Sv"] = "6+"
    rows[:] = remove_profiles(rows, 14, ["4", "8"])
    rows[:] = set_profiles(rows, 14, [{"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "6+", "N": "4", "Pt": "1"},
                                      {"M": '6"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "6+", "N": "8", "Pt": "2"}])
    rows[:] = remove_profiles(rows, 15, ["2", "4"])
    rows[:] = set_profiles(rows, 15, [{"M": '7"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "9+", "N": "2", "Pt": "1"},
                                      {"M": '7"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "9+", "N": "4", "Pt": "2"}])
    rows[:] = remove_profiles(rows, 16, ["5", "10"])
    rows[:] = set_profiles(rows, 16, [{"M": '6"', "WS": "4+", "BS": "-", "A": "1", "W": "1", "Ld": "5", "Sv": "11+", "N": "5", "Pt": "2"},
                                      {"M": '6"', "WS": "4+", "BS": "-", "A": "2", "W": "2", "Ld": "5", "Sv": "11+", "N": "10", "Pt": "3"}])
    update_weapon(rows, 16, "Arco-flails", A="x3")
    for no in (20, 21):
        set_stats(header_row(rows, no), Sv="6+")
        for r in profile_rows(rows, no):
            r["Sv"] = "6+"
    update_weapon(rows, 21, "Zephyrim Power Swords", A="x2")
    update_weapon(rows, 28, "Paragon War Blade", SAP="6+", SAT="6+")
    for r in rows:
        if r["No"].strip() == "28" and "Paragon War Mace" in r.get("Abilities", ""):
            r["Abilities"] = ""
        if r["No"].strip() == "28" and "Paragon War Mace" in r.get("Options", ""):
            r["Options"] = re.sub(r";?\s*per Unit: Any model can have its Paragon War Blade replaced with 1 Paragon War Mace\.?", "", r["Options"])
    rows[:] = [r for r in rows if not (r["No"].strip() == "28" and r.get("Weapon", "").strip() == "Paragon War Mace")]
    return rows


def sm_profile(n5_pt, n10_pt):
    return [
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "5", "Pt": str(n5_pt)},
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "10", "Pt": str(n10_pt)},
    ]


def apply_space_marines(rows):
    for no, pts in ((6, (6, 12)), (7, (6, 12)), (8, (6, 12)), (9, (10, 20)), (10, (5, 10)),
                    (11, (11, 21)), (12, (9, 18)), (15, (6, 12)), (20, (6, 12)), (21, (12, 24))):
        h = header_row(rows, no)
        if h:
            move = '5"' if no in (11, 12) else '6"'
            set_stats(h, M=move, WS="3+", BS="3+", A="2", W="2", Ld="7", Sv="6+", N="5", Pt=str(pts[0]))
            profiles = sm_profile(*pts)
            for p in profiles:
                p["M"] = move
            rows[:] = set_profiles(rows, no, profiles)
    set_stats(header_row(rows, 14), A="2", W="2", N="5", Pt="5")
    update_weapon(rows, 8, "Close Combat Weapons", A="User")
    update_weapon(rows, 3, "Force Weapon", SAP="7+", SAT="8+")
    update_weapon(rows, 4, "Crozius Arcanum", SAP="7+", SAT="8+")
    update_weapon(rows, 5, "Servo-arm & Power Weapon", SAP="9+", SAT="8+")
    update_weapon(rows, 11, "Terminator Power Weapons", A="User", SAP="6+", SAT="6+")
    update_weapon(rows, 11, "Storm Bolters", A="User")
    update_weapon(rows, 12, "Lightning Claws", A="x2", SAP="7+", SAT="8+")
    update_weapon(rows, 12, "Thunder Hammers", A="User")
    update_weapon(rows, 21, "Close Combat Weapons", A="User")
    set_stats(header_row(rows, 16), A="2", W="2", N="3", Pt="11")
    rows[:] = set_profiles(rows, 16, [
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "6", "Pt": "22"},
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "7", "Sv": "6+", "N": "9", "Pt": "33"},
    ])
    set_stats(header_row(rows, 18), A="2", W="2", N="3", Pt="10")
    rows[:] = set_profiles(rows, 18, [
        {"M": '16"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "6", "Pt": "20"},
        {"M": '16"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "7", "Sv": "6+", "N": "9", "Pt": "30"},
    ])
    set_stats(header_row(rows, 19), A="2", W="2", N="3", Pt="12")
    rows[:] = set_profiles(rows, 19, [{"M": '10"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "6", "Pt": "24"}])
    update_weapon(rows, 19, "Close Combat Weapons", A="User")
    update_weapon(rows, 19, "Plasma Exterminators", A="User")
    update_weapon(rows, 19, "Assault Bolters", A="x2")
    set_stats(header_row(rows, 29), Pt="20", W="5", WS="4+", BS="2+")
    return rows


def apply_eldar(rows):
    rows[:] = remove_profiles(rows, 8, ["8", "16"])
    rows[:] = set_profiles(rows, 8, [
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "8", "Pt": "3"},
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "5", "Sv": "10+", "N": "16", "Pt": "6"},
    ])
    update_weapon(rows, 8, "Aeldari Blades", A="User")
    update_weapon(rows, 9, "Power Swords", A="x3")
    update_weapon(rows, 12, "Ghostswords", A="x3")
    set_stats(header_row(rows, 12), N="6", Pt="8")
    rows[:] = set_profiles(rows, 12, [{"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "6", "Ld": "7", "Sv": "5+", "N": "10", "Pt": "16"}])
    set_stats(header_row(rows, 14), N="5", Pt="9")
    rows[:] = set_profiles(rows, 14, [{"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "6", "Ld": "7", "Sv": "5+", "N": "10", "Pt": "18"}])
    for no in (17, 25, 26, 27):
        h = header_row(rows, no)
        if h:
            add_ability(h, "Harrier")
    return rows


def apply_orks(rows):
    set_stats(header_row(rows, 1), A="3")
    update_weapon(rows, 1, "Twin Big Shoota", A="User")
    for r in rows:
        if r["No"].strip() == "1" and "Great Waaagh!" in r.get("Abilities", ""):
            r["Abilities"] = r["Abilities"].replace("friendly Orks Light units", "other friendly Ork Light units")
    add_ability(header_row(rows, 2), "Ignore Damage (+6)")
    update_weapon(rows, 5, "Snagga Klaw", SAP="7+", SAT="7+")
    update_weapon(rows, 3, "Mek Weapons", SAP="8+", SAT="8+")
    update_weapon(rows, 3, "Mek Mega Weapons", SAP="7+", SAT="7+")
    set_stats(header_row(rows, 4), Sv="9+")
    update_weapon(rows, 4, "Weirdboy Staff", SAP="7+", SAT="9+")
    update_weapon(rows, 7, "Close Combat Weapons", SAP="10+", SAT="11+")
    set_stats(header_row(rows, 6), A="2", W="2", N="10", Sv="9+", Pt="5")
    rows[:] = set_profiles(rows, 6, [
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "4", "W": "4", "Ld": "5", "Sv": "9+", "N": "20", "Pt": "10"},
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "6", "W": "6", "Ld": "5", "Sv": "9+", "N": "30", "Pt": "15"},
    ])
    update_weapon(rows, 6, "Choppas", A="x2")
    update_weapon(rows, 6, "Close Combat Weapons", A="User")
    update_weapon(rows, 6, "Shootas", A="x2")
    for r in rows:
        if r["No"].strip() == "6" and "Power Rating +1" in r.get("Options", "") and "Shootas" in r.get("Options", ""):
            r["Options"] = re.sub(r";\s*per Unit \(Power Rating \+1\): Instead of Sluggas and Choppas.*", "", r["Options"])
        if r["No"].strip() == "6" and "Shootas and Close Combat Weapons" in r.get("Abilities", ""):
            r["Abilities"] = r["Abilities"].replace(
                "Instead of Sluggas and Choppas, this unit can be equipped with Shootas and Close Combat Weapons (Power Rating +1).", ""
            ).strip()
    update_weapon(rows, 8, "Doks Tools", SAP="8+", SAT="9+")
    update_weapon(rows, 9, "Meks Tools", SAP="9+", SAT="8+")
    set_stats(header_row(rows, 12), A="3", Sv="7+", N="5", Pt="6")
    rows[:] = set_profiles(rows, 12, [{"M": '5"', "WS": "3+", "BS": "5+", "A": "6", "W": "4", "Ld": "6", "Sv": "7+", "N": "10", "Pt": "12"}])
    update_weapon(rows, 12, "Nob Choppas", A="User")
    update_weapon(rows, 12, "Sluggas", A="User")
    set_stats(header_row(rows, 13), Sv="9+")
    for no in (14, 16):
        set_stats(header_row(rows, no), A="2", W="2", N="3", Pt=str(6 if no == 14 else 7))
        rows[:] = set_profiles(rows, no, [
            {"M": '4"' if no == 14 else '14"', "WS": "3+", "BS": "5+", "A": "4", "W": "4", "Ld": "6" if no == 14 else "5", "Sv": "4+" if no == 14 else "8+", "N": "6", "Pt": "12" if no == 14 else "14"},
            {"M": '4"' if no == 14 else '14"', "WS": "3+", "BS": "5+", "A": "6", "W": "6", "Ld": "7" if no == 14 else "5", "Sv": "4+" if no == 14 else "8+", "N": "9", "Pt": "18" if no == 14 else "21"},
        ])
        update_weapon(rows, no, "Meganob Melee Weapons", A="User")
        update_weapon(rows, no, "Meganob Shootas", A="x2")
        update_weapon(rows, no, "Nob Choppas", A="User")
    for no in (10, 11, 15, 19, 25):
        h = header_row(rows, no)
        if h:
            h["Sv"] = "9+"
    set_stats(header_row(rows, 26), Sv="7+")
    set_stats(header_row(rows, 32), Pt="40", A="4")
    update_weapon(rows, 32, "Mega-choppa", A="User")
    stomp = {c: "" for c in FIELDNAMES}
    stomp.update({"No": "32", "Weapon": "Stomp", "WeaponType": "Melee", "Rng": "Melee", "WeaponA": "User", "SAP": "7+", "SAT": "9+"})
    insert_at = next(i for i, r in enumerate(rows) if r["No"].strip() == "32" and r.get("Weapon") == "Mega-choppa") + 1
    rows.insert(insert_at, stomp)
    return rows


def chaos_marine_profile(n5_pt, n10_pt, n15_pt=None):
    profiles = [
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "5", "Pt": str(n5_pt)},
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "10", "Pt": str(n10_pt)},
    ]
    if n15_pt is not None:
        profiles.append({"M": '6"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "7", "Sv": "6+", "N": "15", "Pt": str(n15_pt)})
    return profiles


def apply_chaos_marines(rows):
    set_stats(header_row(rows, 7), M='6"', WS="5+", BS="5+", A="1", W="1", Ld="5", Sv="10+", N="10", Pt="2")
    rows[:] = set_profiles(rows, 7, [
        {"M": '6"', "WS": "5+", "BS": "5+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "20", "Pt": "4"},
        {"M": '6"', "WS": "5+", "BS": "5+", "A": "3", "W": "3", "Ld": "5", "Sv": "10+", "N": "30", "Pt": "6"},
    ])

    pts_by_no = {
        6: (8, 16, 24), 8: (8, 16, 24), 9: (8, 16, 24),
        10: (11, 21, None),
        26: (7, 14, 20), 27: (7, 14, 20), 28: (7, 14, 20), 29: (7, 14, 20),
    }
    move_by_no = {10: '5"'}
    for no, pts in pts_by_no.items():
        h = header_row(rows, no)
        if not h:
            continue
        move = move_by_no.get(no, '6"')
        set_stats(h, M=move, WS="3+", BS="3+", A="2", W="2", Ld="7", Sv="6+", N="5", Pt=str(pts[0]))
        profiles = chaos_marine_profile(pts[0], pts[1], pts[2])
        for p in profiles:
            p["M"] = move
        rows[:] = set_profiles(rows, no, profiles)

    # Possessed special attacks/points
    set_stats(header_row(rows, 12), M='7"', A="D3+1", W="2", N="5", Pt="10")
    rows[:] = set_profiles(rows, 12, [
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "2D3+2", "W": "4", "Ld": "6", "Sv": "5+", "N": "10", "Pt": "20"},
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "3D3+3", "W": "6", "Ld": "6", "Sv": "5+", "N": "15", "Pt": "30"},
    ])

    set_stats(header_row(rows, 15), N="5", Pt="8")
    rows[:] = set_profiles(rows, 15, [
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "10", "Pt": "20"},
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "6", "W": "6", "Ld": "7", "Sv": "6+", "N": "15", "Pt": "25"},
    ])
    set_stats(header_row(rows, 16), A="2", N="5", Pt="7")
    update_weapon(rows, 22, "Crushing Fists", SAP="7+", SAT="9+")
    set_stats(header_row(rows, 14), A="2", W="2", N="3", Pt="10")
    rows[:] = set_profiles(rows, 14, [{"M": '14"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "7", "Sv": "6+", "N": "6", "Pt": "18"}])
    return rows


def apply_drukhari(rows):
    rows[:] = remove_profiles(rows, 6, ["15", "20"])
    set_stats(header_row(rows, 5), N="10", Pt="4", A="2", W="2")
    rows[:] = remove_profiles(rows, 5, ["10", "15", "20"])
    rows[:] = set_profiles(rows, 5, [{"M": '7"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "8"}])
    set_stats(header_row(rows, 17), N="4", Pt="1", A="1", W="1")
    rows[:] = remove_profiles(rows, 17, ["4", "8", "12"])
    rows[:] = set_profiles(rows, 17, [
        {"M": '10"', "WS": "3+", "BS": "-", "A": "2", "W": "2", "Ld": "4", "Sv": "9+", "N": "8", "Pt": "2"},
        {"M": '10"', "WS": "3+", "BS": "-", "A": "3", "W": "3", "Ld": "4", "Sv": "9+", "N": "12", "Pt": "3"},
    ])
    set_stats(header_row(rows, 23), N="5", Pt="6")
    rows[:] = set_profiles(rows, 23, [{"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "10", "Pt": "12"}])
    for r in rows:
        if r["No"].strip() == "23":
            if "Power Rating +2" in r.get("Options", ""):
                r["Options"] = re.sub(
                    r"per Unit \(Power Rating \+2 per Shredder or Splinter Cannon; Power Rating \+1 per other weapon\):",
                    "per Unit:",
                    r["Options"],
                )
            if "Power Rating +2 per Shredder" in r.get("Abilities", ""):
                r["Abilities"] = re.sub(
                    r"\(Power Rating \+2 per Shredder or Splinter Cannon; Power Rating \+1 per other weapon\)",
                    "(no additional points)",
                    r["Abilities"],
                )
    splinter = {c: "" for c in FIELDNAMES}
    splinter.update({"No": "14", "Weapon": "Splinter Rifles", "WeaponType": "Small Arms", "Rng": '24"', "WeaponA": "1", "SAP": "5+", "SAT": "12+", "Abilities": "Rapid Fire"})
    if not weapon_rows(rows, 14, "Splinter Rifles"):
        idx = next(i for i, r in enumerate(rows) if r["No"].strip() == "14" and r.get("Weapon") == "Close Combat Weapons")
        rows.insert(idx + 1, splinter)
    return rows


def apply_tyranids(rows):
    update_weapon(rows, 6, "Scything Talons", A="User", SAP="6+", SAT="9+")
    for r in rows:
        if r["No"].strip() == "6" and "Hungering Swarm" in r.get("Abilities", ""):
            r["Abilities"] = r["Abilities"].replace("contains 30 models", "contains 20 or 30 models")
    set_stats(profile_rows(rows, 6)[0], Pt="5") if profile_rows(rows, 6) else None
    for r in profile_rows(rows, 6):
        if r["N"] == "20":
            r["Pt"] = "5"
    return rows


def apply_tau(rows):
    set_stats(header_row(rows, 6), M='6"', WS="3+", BS="4+", A="2", W="2", Ld="5", Sv="10+", N="10", Pt="4")
    rows[:] = set_profiles(rows, 6, [{"M": '6"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "5", "Sv": "10+", "N": "20", "Pt": "7"}])
    update_weapon(rows, 6, "Kroot Rifles (Melee)", A="User", SAP="7+", SAT="9+")
    update_weapon(rows, 6, "Kroot Rifles (Ranged)", A="User", SAP="8+", SAT="10+")
    update_weapon(rows, 19, "Ripping Fangs", SAP="8+", SAT="10+")
    return rows


def apply_genestealer_cults(rows):
    rows[:] = remove_unit(rows, 29)
    rows[:] = remove_unit(rows, 30)
    kel = header_row(rows, 15)
    if kel:
        kel["Type"] = "HQ"
    hydra = [
        {**{c: "" for c in FIELDNAMES}, "No": "29", "Type": "Heavy", "Name": "Cult Hydra",
         "M": '12"', "WS": "6+", "BS": "4+", "A": "1", "W": "2", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "7",
         "Abilities": "Tank Squadron: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one.",
         "Keywords": "Tyranids, Genestealer Cults, Brood Brothers\nHeavy, Vehicle, Hydra, Cult Hydra",
         "Options": "per Unit: Instead of 1 Heavy Bolter, this unit can be equipped with 1 Heavy Flamer.; per Unit (Power Rating +1): This unit can also be equipped with one of the following (Power Rating +1): 1 Heavy Stubber; 1 Storm Bolter."},
        {**{c: "" for c in FIELDNAMES}, "No": "29", "Abilities": "A Cult Hydra is a unit that contains 1 model. It is equipped with: Hydra Quad Autocannon; Heavy Bolter; Armoured Tracks."},
        {**{c: "" for c in FIELDNAMES}, "No": "29", "Weapon": "Hydra Quad Autocannon", "WeaponType": "Heavy", "Rng": '72"', "WeaponA": "2", "SAP": "8+", "SAT": "6+", "Abilities": "Anti-air"},
        {**{c: "" for c in FIELDNAMES}, "No": "29", "Weapon": "Heavy Bolter", "WeaponType": "Heavy", "Rng": '36"', "WeaponA": "1", "SAP": "7+", "SAT": "9+"},
        {**{c: "" for c in FIELDNAMES}, "No": "29", "Weapon": "Armoured Tracks", "WeaponType": "Melee", "Rng": "Melee", "WeaponA": "User", "SAP": "10+", "SAT": "10+"},
    ]
    engineers = [
        {**{c: "" for c in FIELDNAMES}, "No": "30", "Type": "Troops", "Name": "Cult Combat Engineers",
         "M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "4",
         "Keywords": "Tyranids, Genestealer Cults, <Cult>\nLight, Infantry, Cult Combat Engineers",
         "Options": "per 20 models (Power Rating 8): It can contain 20 models (Power Rating 8)."},
        {**{c: "" for c in FIELDNAMES}, "No": "30", "M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "8"},
        {**{c: "" for c in FIELDNAMES}, "No": "30", "Abilities": "Cult Combat Engineers is a unit that contains 10 models. It can contain 20 models (Power Rating 8)."},
        {**{c: "" for c in FIELDNAMES}, "No": "30", "Weapon": "Trench Clubs", "WeaponType": "Melee", "Rng": '12"', "WeaponA": "User", "SAP": "8+", "SAT": "10+"},
        {**{c: "" for c in FIELDNAMES}, "No": "30", "Weapon": "Flamers", "WeaponType": "Small Arms", "Rng": '12"', "WeaponA": "User", "SAP": "8+", "SAT": "10+", "Abilities": "Inferno"},
        {**{c: "" for c in FIELDNAMES}, "No": "30", "Abilities": 'Remote Mines: Once per battle, select a unit within 9" and roll a d6. On a 3+, the unit suffers a blast marker, or 2 blast markers for vehicle or fortification unit.'},
    ]
    rows.extend(hydra)
    rows.extend(engineers)
    return rows


def main():
    updates = {
        "Imperial Guard": apply_imperial_guard,
        "Sisters of Battle": apply_sisters,
        "Space Marines": apply_space_marines,
        "Eldar": apply_eldar,
        "Orks": apply_orks,
        "Chaos Marines": apply_chaos_marines,
        "Drukhari": apply_drukhari,
        "Tyranids": apply_tyranids,
        "Tau": apply_tau,
        "Genestealer Cults": apply_genestealer_cults,
    }
    for faction, fn in updates.items():
        path = ARMY_LISTS_DIR / f"Apoc40k-Armies-1st - {faction}.csv"
        rows = read_csv(path)
        fn(rows)
        write_csv(path, rows)
        print(f"Updated {path.name}")

    from csv_to_json import write_json
    for csv_path in sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv")):
        json_path, _ = write_json(csv_path)
        dest = WEB_ARMY_LISTS_DIR / json_path.name
        shutil.copy2(json_path, dest)
        print(f"Synced {json_path.name}")


if __name__ == "__main__":
    main()
