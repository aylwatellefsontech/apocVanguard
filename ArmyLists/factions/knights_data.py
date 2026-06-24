from generate_all_faction_lists import slot, u

_QUESTORIS_WEAPONS = [
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Ironstorm Missile Pod", "type": "Heavy", "range": '72"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Barrage"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Stormspear Rocket Pod", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "6+", "armorPen": "5+"},
    {"name": "Twin Icarus Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Anti-air"},
    {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
    {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
]

_QUESTORIS_OPTIONS = [
    "• Instead of 1 Reaper Chainsword, this unit can be equipped with 1 Thunderstrike Gauntlet.",
    "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
    "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
]

_GALLANT_OPTIONS = [
    "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
    "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
]

_CASTELLAN_WEAPONS = [
    {"name": "Plasma Decimator", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
    {"name": "Shieldbreaker Missile", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "One Use Only"},
    {"name": "Twin Meltagun", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "11+", "armorPen": "4+"},
    {"name": "Twin Siegebreaker Cannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "Volcano Lance", "type": "Heavy", "range": '80"', "attacks": "2", "skill": "10+", "armorPen": "3+", "abilities": "Destroyer"},
    {"name": "Titanic Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

_CASTELLAN_ABILITIES = (
    "Dual Plasma Core Explosion: When this unit is destroyed, roll two D12 instead of one D12 to determine if it "
    "explodes, and it does so on any result of a 10+. When this unit explodes, place one blast marker next to every "
    "unit (excluding Super-heavy units) that is within 12\" of this unit instead of 6\"."
)

_TYRANT_WEAPONS = [
    {"name": "Plasma Decimator", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
    {"name": "Conflagration Cannon", "type": "Heavy", "range": '18"', "attacks": "4", "skill": "4+", "armorPen": "8+", "abilities": "Inferno"},
    {"name": "Shieldbreaker Missile", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "One Use Only"},
    {"name": "Thundercoil Harpoon", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "8+", "armorPen": "2+", "abilities": "Apocalyptic Destroyer"},
    {"name": "Twin Meltagun", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "11+", "armorPen": "4+"},
    {"name": "Twin Siegebreaker Cannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "Volcano Lance", "type": "Heavy", "range": '80"', "attacks": "2", "skill": "10+", "armorPen": "3+", "abilities": "Destroyer"},
    {"name": "Titanic Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

_TYRANT_ABILITIES = (
    "Apocalyptic Destroyer: If a wound roll for an attack made with a weapon with this ability is successful, "
    "place four blast markers next to the target unit instead of one.\n"
    + _CASTELLAN_ABILITIES
)

_VEHICLE_SQUADRON = (
    "Vehicle Squadron: Each Lord of War slot in a Detachment allows you to take up to three of this unit in your "
    "army, instead of one. Each unit taken for a single Lord of War slot must be placed at the same time and within "
    "6\" of each other unit taken for the same slot the first time they are set up."
)

_HELVERIN_WEAPONS = [
    {"name": "Armiger Autocannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
]

_WARGLAIVE_WEAPONS = [
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Thermal Spear", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
    {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
    {"name": "Reaper Chain-cleaver", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
]

_WAR_DOG_WEAPONS = [
    {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
    {"name": "Meltagun", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "11+", "armorPen": "7+"},
    {"name": "Thermal Spear", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
    {"name": "War Dog Autocannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
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
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Super-heavy", "Vehicle", "Titanic", "Questoris Class", "Knight Paladin"],
        [{"name": "Rapid-fire Battle Cannon", "type": "Heavy", "range": '72"', "attacks": "4", "skill": "6+", "armorPen": "6+"}]
        + _QUESTORIS_WEAPONS,
        options=_QUESTORIS_OPTIONS,
    ),
    "Knight Errant": u(
        "Knight Errant",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Super-heavy", "Vehicle", "Titanic", "Questoris Class", "Knight Errant"],
        [{"name": "Thermal Cannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "6+", "armorPen": "4+", "abilities": "Destroyer"}]
        + _QUESTORIS_WEAPONS,
        options=_QUESTORIS_OPTIONS,
    ),
    "Knight Castellan": u(
        "Knight Castellan",
        {"M": '10"', "WS": "4+", "BS": "3+", "A": "4", "W": "6", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "30"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Super-heavy", "Vehicle", "Titanic", "Dominus Class", "Knight Castellan"],
        _CASTELLAN_WEAPONS,
        abilities=_CASTELLAN_ABILITIES,
        options=[
            "• Instead of 1 Twin Siegebreaker Cannon, this unit can be equipped with 2 Shieldbreaker Missiles.",
        ],
    ),
    "Knight Gallant": u(
        "Knight Gallant",
        {"M": '12"', "WS": "2+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "24"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Super-heavy", "Titanic", "Vehicle", "Questoris Class", "Knight Gallant"],
        _QUESTORIS_WEAPONS,
        options=_GALLANT_OPTIONS,
    ),
    "Canis Rex": u(
        "Canis Rex",
        {"M": '12"', "WS": "2+", "BS": "2+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "30"},
        ["Imperium", "Imperial Knights", "Questor Imperialis", "Freeblade",
         "Super-heavy", "Character", "Vehicle", "Titanic", "Questoris Class", "Knight Preceptor", "Canis Rex"],
        [
            {"name": "Las-impulsor", "type": "Heavy", "range": '36"', "attacks": "4", "skill": "5+", "armorPen": "5+"},
            {"name": "Multi-laser", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "10+"},
            {"name": "Freedom's Hand", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "4+", "abilities": "Destroyer"},
        ],
        abilities=(
            "Chainbreaker: Add 1 to the Leadership characteristic of friendly Imperium units whilst they are "
            "within 6\" of this unit.\n"
            "You can only have one of this unit in your army."
        ),
    ),
    "Armiger Helverin": u(
        "Armiger Helverin",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>", "<Household>",
         "Heavy", "Vehicle", "Armiger Class", "Armiger Helverin"],
        _HELVERIN_WEAPONS,
        abilities=_VEHICLE_SQUADRON,
        options=["• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun."],
    ),
    "Armiger Warglaive": u(
        "Armiger Warglaive",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Imperium", "Imperial Knights", "<Questor Allegiance>",
         "Heavy", "Vehicle", "Armiger Class", "Armiger Warglaive"],
        _WARGLAIVE_WEAPONS,
        abilities=_VEHICLE_SQUADRON,
        options=["• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun."],
    ),
    "War Dog": u(
        "War Dog",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Chaos", "Chaos Knights", "<Questor Traitoris>", "Heavy", "Vehicle", "War Dog"],
        _WAR_DOG_WEAPONS,
        abilities=_VEHICLE_SQUADRON,
        options=[
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
            "• Instead of 2 War Dog Autocannons, this unit can be equipped with 1 Thermal Spear and 1 Reaper Chain-cleaver.",
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
            "• This unit can also be equipped with one of the following (Power Rating +1): 1 Ironstorm Missile Pod; 1 Stormspear Rocket Pod; 1 Twin Icarus Autocannon.",
            "• Instead of 1 Thunderstrike Gauntlet, this unit can be equipped with one of the following: 1 Avenger Gatling Cannon and 1 Heavy Flamer; 1 Rapid-fire Battle Cannon and 1 Heavy Stubber; 1 Thermal Cannon.",
            "• Instead of 1 Reaper Chainsword, this unit can be equipped with one of the following: 1 Avenger Gatling Cannon and 1 Heavy Flamer; 1 Rapid-fire Battle Cannon and 1 Heavy Stubber; 1 Thermal Cannon.",
            "• Instead of 1 Heavy Stubber, this unit can be equipped with 1 Meltagun.",
            "• If this unit is not equipped with any other melee weapons, it is also equipped with Titanic Feet.",
        ],
    ),
    "Knight Tyrant": u(
        "Knight Tyrant",
        {"M": '10"', "WS": "4+", "BS": "3+", "A": "4", "W": "6", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "30"},
        ["Chaos", "Chaos Knights", "<Questor Traitoris>",
         "Super-heavy", "Titanic", "Vehicle", "Knight Tyrant"],
        _TYRANT_WEAPONS,
        abilities=_TYRANT_ABILITIES,
        options=[
            "• Instead of 1 Twin Siegebreaker Cannon, this unit can be equipped with 2 Shieldbreaker Missiles.",
            "• Instead of 1 Volcano Lance and 1 Plasma Decimator, this unit can be equipped with 1 Conflagration Cannon and 1 Thundercoil Harpoon.",
        ],
    ),
    "Knight Desecrator": u(
        "Knight Desecrator",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "21"},
        ["Chaos", "Chaos Knights", "<Questor Traitoris>",
         "Super-heavy", "Titanic", "Vehicle", "Abhorrent Class", "Knight Desecrator"],
        [
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Laser Destructor", "type": "Heavy", "range": '60"', "attacks": "1", "skill": "10+", "armorPen": "3+", "abilities": "Destroyer"},
            {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
        ],
        abilities=(
            "Taskmaster: Re-roll hit rolls of 1 for attacks made by friendly <Questor Traitoris> War Dog units "
            "whilst they are within 6\" of this unit."
        ),
        options=["• Instead of 1 Reaper Chainsword, this unit can be equipped with 1 Thunderstrike Gauntlet."],
    ),
    "Knight Rampager": u(
        "Knight Rampager",
        {"M": '12"', "WS": "2+", "BS": "3+", "A": "4", "W": "5", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "19"},
        ["Chaos", "Chaos Knights", "<Questor Traitoris>",
         "Super-heavy", "Titanic", "Vehicle", "Abhorrent Class", "Knight Rampager"],
        [
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Reaper Chainsword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Thunderstrike Gauntlet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+", "abilities": "Destroyer"},
        ],
    ),
}

KNIGHTS_SLOTS = [
    slot(1, "HQ", KNIGHTS["Knight Paladin"]),
    slot(2, "HQ", KNIGHTS["Knight Errant"]),
    slot(3, "HQ", KNIGHTS["Knight Castellan"]),
    slot(4, "HQ", KNIGHTS["Knight Gallant"]),
    slot(5, "Lord", KNIGHTS["Canis Rex"]),
    slot(6, "Lord", KNIGHTS["Armiger Helverin"]),
    slot(7, "Lord", KNIGHTS["Armiger Warglaive"]),
    slot(8, "Lord", KNIGHTS["War Dog"]),
    slot(9, "HQ", KNIGHTS["Knight Despoiler"]),
    slot(10, "HQ", KNIGHTS["Knight Tyrant"]),
    slot(11, "HQ", KNIGHTS["Knight Desecrator"]),
    slot(12, "HQ", KNIGHTS["Knight Rampager"]),
]
