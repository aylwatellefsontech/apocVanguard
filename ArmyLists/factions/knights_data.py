from generate_all_faction_lists import slot, u


def _named(unit, name):
    out = dict(unit)
    out["name"] = name
    return out


_QUESTORIS_COMMON_WEAPONS = [
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Ironstorm Missile Pod", "type": "Heavy", "range": '72"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Barrage"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Stormspear Rocket Pod", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
    {"name": "Twin Icarus Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Anti-air"},
    {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
    {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
]

_QUESTORIS_OPTIONS = [
    "Select allegiance and variant when including this unit (see Abilities).",
    "Knight Paladin (Imperial, Pt 24): equipped with Rapid-fire Battle Cannon, 2 Heavy Stubbers, Reaper Chainsword.",
    "Knight Desecrator (Chaos, Pt 21): equipped with Heavy Stubber, Laser Destructor, Reaper Chainsword.",
    "• Instead of 1 Reaper Chainsword, this unit can be equipped with 1 Thunderstrike Gauntlet (Paladin/Desecrator).",
    "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon (Paladin only).",
    "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
]

_DOMINUS_WEAPONS = [
    {"name": "Plasma Decimator", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
    {"name": "Conflagration Cannon", "type": "Heavy", "range": '18"', "attacks": "4", "skill": "4+", "armorPen": "8+", "abilities": "Inferno"},
    {"name": "Shieldbreaker Missile", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "One Use Only"},
    {"name": "Thundercoil Harpoon", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "8+", "armorPen": "2+", "abilities": "Apocalyptic Destroyer"},
    {"name": "Twin Meltagun", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "11+", "armorPen": "4+"},
    {"name": "Twin Siegebreaker Cannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "Volcano Lance", "type": "Heavy", "range": '80"', "attacks": "2", "skill": "10+", "armorPen": "3+", "abilities": "Destroyer"},
    {"name": "Titanic Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

_DOMINUS_ABILITIES = (
    "Knight Castellan (Imperial, Pt 30): Dual Plasma Core Explosion: When this unit is destroyed, roll two D12 "
    "instead of one D12 to determine if it explodes, and it does so on any result of a 10+. When this unit explodes, "
    "place one blast marker next to every unit (excluding Super-heavy units) that is within 12\" of this unit instead of 6\".\n"
    "Knight Tyrant (Chaos, Pt 30): Apocalyptic Destroyer: If a wound roll for an attack made with a weapon with this "
    "ability is successful, place four blast markers next to the target unit instead of one. "
    "Dual Plasma Core Explosion: When this unit is destroyed, roll two D12 instead of one D12 to determine if it explodes, "
    "and it does so on any result of a 10+. When this unit explodes, place one blast marker next to every unit "
    "(excluding Super-heavy units) that is within 12\" of this unit instead of 6\"."
)

_DOMINUS_OPTIONS = [
    "Select allegiance and variant when including this unit (see Abilities).",
    "Knight Castellan (Imperial): equipped with Plasma Decimator, 2 Shieldbreaker Missiles, 2 Twin Meltaguns, "
    "2 Twin Siegebreaker Cannons, Volcano Lance, Titanic Feet.",
    "Knight Tyrant (Chaos, default): same as Castellan loadout.",
    "• Instead of 1 Twin Siegebreaker Cannon, this unit can be equipped with 2 Shieldbreaker Missiles.",
    "• Instead of 1 Volcano Lance and 1 Plasma Decimator, this unit can be equipped with "
    "1 Conflagration Cannon and 1 Thundercoil Harpoon (Tyrant / Valiant-style loadout).",
]

_SMALL_KNIGHT_ABILITIES = (
    "Vehicle Squadron: Each Lord of War slot in a Detachment allows you to take up to three of this unit "
    "in your army, instead of one. Each unit taken for a single Lord of War slot must be placed at the same "
    "time and within 6\" of each other unit taken for the same slot the first time they are set up."
)

_SMALL_KNIGHT_WEAPONS = [
    {"name": "Armiger Autocannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "War Dog Autocannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Thermal Spear", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
    {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
    {"name": "Reaper Chain-cleaver", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

_DESPOILER_WEAPONS = [
    {"name": "Avenger Gatling Cannon", "type": "Heavy", "range": '36"', "attacks": "4", "skill": "4+", "armorPen": "8+"},
    {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Ironstorm Missile Pod", "type": "Heavy", "range": '72"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Barrage"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Rapid-fire Battle Cannon", "type": "Heavy", "range": '72"', "attacks": "4", "skill": "6+", "armorPen": "6+"},
    {"name": "Stormspear Rocket Pod", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
    {"name": "Thermal Cannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "4+", "abilities": "Destroyer"},
    {"name": "Twin Icarus Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Anti-air"},
    {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
    {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
    {"name": "Titanic Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

KNIGHTS = {
    "Knight Paladin": u(
        "Knight Paladin",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Knights", "Super-heavy", "Vehicle", "Titanic", "Questoris Class"],
        [
            {"name": "Rapid-fire Battle Cannon", "type": "Heavy", "range": '72"', "attacks": "4", "skill": "6+", "armorPen": "6+"},
            {"name": "Laser Destructor", "type": "Heavy", "range": '60"', "attacks": "1", "skill": "10+", "armorPen": "3+", "abilities": "Destroyer"},
        ] + _QUESTORIS_COMMON_WEAPONS,
        abilities=(
            "Knight Desecrator (Chaos, Pt 21) - Taskmaster: Re-roll hit rolls of 1 for attacks made by friendly "
            "<Questor Traitoris> War Dog units whilst they are within 6\" of this unit."
        ),
        profiles=[{"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "21"}],
        options=_QUESTORIS_OPTIONS,
    ),
    "Knight Errant": u(
        "Knight Errant",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Super-heavy", "Vehicle", "Titanic", "Questoris Class", "Knight Errant"],
        [{"name": "Thermal Cannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "4+", "abilities": "Destroyer"}]
        + _QUESTORIS_COMMON_WEAPONS,
        options=[
            "Chaos players: field a Knight Despoiler (slot 7) with Thermal Cannon loadout as the equivalent.",
            "• Instead of 1 Reaper Chainsword, this unit can be equipped with 1 Thunderstrike Gauntlet.",
            "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
        ],
    ),
    "Dominus Knight": u(
        "Dominus Knight",
        {"M": '10"', "WS": "4+", "BS": "3+", "A": "4", "W": "6", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "30"},
        ["Knights", "Super-heavy", "Vehicle", "Titanic", "Dominus Class"],
        _DOMINUS_WEAPONS,
        abilities=_DOMINUS_ABILITIES,
        options=_DOMINUS_OPTIONS,
    ),
    "Armiger Helverin": u(
        "Armiger Helverin",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Knights", "Heavy", "Vehicle", "Armiger Class"],
        _SMALL_KNIGHT_WEAPONS,
        abilities=_SMALL_KNIGHT_ABILITIES,
        options=[
            "Select allegiance when including this unit.",
            "Armiger Helverin (Imperial): equipped with 2 Armiger Autocannons, Heavy Stubber, Armoured Feet.",
            "War Dog (Chaos, autocannon): equipped with 2 War Dog Autocannons, Heavy Stubber, Armoured Feet.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
        ],
    ),
    "Armiger Warglaive": u(
        "Armiger Warglaive",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Knights", "Heavy", "Vehicle", "Armiger Class"],
        _SMALL_KNIGHT_WEAPONS,
        abilities=_SMALL_KNIGHT_ABILITIES,
        options=[
            "Select allegiance when including this unit.",
            "Armiger Warglaive (Imperial): equipped with Heavy Stubber, Thermal Spear, Armoured Feet, Reaper Chain-cleaver.",
            "War Dog (Chaos, melee): instead of 2 War Dog Autocannons, equipped with 1 Thermal Spear and 1 Reaper Chain-cleaver.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
        ],
    ),
    "War Dog": u(
        "War Dog",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Knights", "Heavy", "Vehicle"],
        _SMALL_KNIGHT_WEAPONS,
        abilities=_SMALL_KNIGHT_ABILITIES,
        options=[
            "Select allegiance and loadout when including this unit.",
            "Imperial Armiger Helverin: 2 Armiger Autocannons, Heavy Stubber, Armoured Feet.",
            "Imperial Armiger Warglaive: Thermal Spear, Reaper Chain-cleaver, Heavy Stubber, Armoured Feet.",
            "Chaos War Dog (autocannon): 2 War Dog Autocannons, Heavy Stubber, Armoured Feet.",
            "Chaos War Dog (melee): 1 Thermal Spear, 1 Reaper Chain-cleaver, Heavy Stubber, Armoured Feet.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
            "• Instead of 2 War Dog Autocannons / Armiger Autocannons, this unit can be equipped with 1 Thermal Spear and 1 Reaper Chain-cleaver.",
        ],
    ),
    "Knight Despoiler": u(
        "Knight Despoiler",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Chaos", "Chaos Knights", "<Questor Traitoris>",
         "Super-heavy", "Titanic", "Vehicle", "Knight Despoiler"],
        _DESPOILER_WEAPONS,
        abilities=(
            "Engine of Destruction: If this unit is equipped with 1 Reaper Chainsword and 1 Thunderstrike Gauntlet, "
            "change its Weapon Skill characteristic to 2+."
        ),
        options=[
            "Default: Heavy Stubber, Thunderstrike Gauntlet, Reaper Chainsword.",
            "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
            "• Instead of 1 Thunderstrike Gauntlet, this unit can be equipped with one of the following: "
            "1 Avenger Gatling Cannon and 1 Heavy Flamer; 1 Rapid-fire Battle Cannon and 1 Heavy Stubber; 1 Thermal Cannon.",
            "• Instead of 1 Reaper Chainsword, this unit can be equipped with one of the following: "
            "1 Avenger Gatling Cannon and 1 Heavy Flamer; 1 Rapid-fire Battle Cannon and 1 Heavy Stubber; 1 Thermal Cannon.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
            "• If this unit is not equipped with any other melee weapons, it is also equipped with Titanic Feet.",
        ],
    ),
    "Knight Rampager": u(
        "Knight Rampager",
        {"M": '12"', "WS": "2+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "19"},
        ["Knights", "Super-heavy", "Titanic", "Vehicle"],
        [
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Ironstorm Missile Pod", "type": "Heavy", "range": '72"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
            {"name": "Stormspear Rocket Pod", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
            {"name": "Twin Icarus Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Anti-air"},
            {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
        ],
        profiles=[{"M": '12"', "WS": "2+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"}],
        options=[
            "Select allegiance and variant when including this unit.",
            "Knight Rampager (Chaos, Pt 19): equipped with Heavy Stubber, Reaper Chainsword, Thunderstrike Gauntlet.",
            "Knight Gallant (Imperial, Pt 24): equipped with Heavy Stubber, Thunderstrike Gauntlet, Reaper Chainsword.",
            "• Knight Gallant can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
            "• Instead of 1 Heavy Stubber, Knight Gallant can be equipped with 1 Meltagun.",
        ],
    ),
}

KNIGHTS_SLOTS = [
    slot(1, "HQ", KNIGHTS["Knight Paladin"]),
    slot(2, "HQ", KNIGHTS["Knight Errant"]),
    slot(3, "HQ", _named(KNIGHTS["Dominus Knight"], "Knight Castellan")),
    slot(4, "HQ", _named(KNIGHTS["Armiger Helverin"], "Armiger Helveren")),
    slot(5, "HQ", KNIGHTS["Armiger Warglaive"]),
    slot(6, "Troops", _named(KNIGHTS["War Dog"], "Wardog")),
    slot(7, "Troops", KNIGHTS["Knight Despoiler"]),
    slot(8, "Elites", _named(KNIGHTS["Dominus Knight"], "Knight Tyrant")),
    slot(9, "Elites", KNIGHTS["Knight Rampager"]),
]
