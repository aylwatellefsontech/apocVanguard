from generate_all_faction_lists import slot, u

# ---------------------------------------------------------------------------
# Chaos Marines unit datasheets
# Sources: Apoc_Datasheet_Heretic_Astartes_web.pdf,
#          Apoc_Datasheet_Legiones_Daemonica_web.pdf (Greater Daemon)
# ---------------------------------------------------------------------------

CHAOS_MARINES = {
    "Abaddon The Despoiler": u(
        "Abaddon The Despoiler",
        {"M": '6"', "WS": "2+", "BS": "2+", "A": "2", "W": "2", "Ld": "8", "Sv": "3+", "N": "1", "Pt": "15"},
        ["Chaos", "Khorne", "Nurgle", "Slaanesh", "Tzeentch", "Heretic Astartes", "Black Legion",
         "Light", "Infantry", "Character", "Chaos Lord", "Terminator", "Abaddon the Despoiler"],
        [{"name": "Talon of Horus & Drach'nyen", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+"}],
        abilities=(
            "You can only include one of this unit in your army.\n"
            "Deep Strike\n"
            "Lord of the Black Legion: You can re-roll hit rolls for attacks made by friendly Black Legion units whilst they are within 6\" of this unit.\n"
            "Mark of Chaos Ascendant: Morale tests taken for friendly Heretic Astartes units are automatically passed whilst they are within 6\" of this unit.\n"
            "Dark Destiny: Roll D12s when making saving throws for this unit, irrespective of the size of the blast markers next to it."
        ),
    ),

    "Lord": u(
        "Lord",
        {"M": '6"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "5"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Character", "Chaos Lord"],
        [{"name": "Helwrought Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"}],
        abilities="Lord of Chaos: Re-roll hit rolls of 1 for attacks made by friendly <Legion> units whilst they are within 6\" of this unit.",
        options=[
            "This unit can have one of the following:",
            "Jump Pack (Power Rating +2). If this unit has a Jump Pack, it: Has Move 12\"; Deep Strike; keywords Jump Pack, Fly.",
            "Terminator Armour (Power Rating +2). If this unit has Terminator Armour, it: Has Move 5\", Save 4+; Deep Strike; keyword Terminator.",
            "Bike (Power Rating +1). If this unit has a Bike, it: Has Move 14\"; keyword Biker; loses keyword Infantry.",
        ],
    ),

    "Sorcerer": u(
        "Sorcerer",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "1", "Pt": "3"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Psyker", "Character", "Infantry", "Sorcerer"],
        [{"name": "Force Weapon", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"}],
        options=[
            "This unit can have one of the following:",
            "Jump Pack (Power Rating +2). If this unit has a Jump Pack, it: Has Move 12\"; Deep Strike; keywords Jump Pack, Fly.",
            "Terminator Armour (Power Rating +2). If this unit has Terminator Armour, it: Has Move 5\", Save 4+; Deep Strike; keyword Terminator.",
            "Bike (Power Rating +1). If this unit has a Bike, it: Has Move 14\"; keyword Biker; loses keyword Infantry.",
        ],
    ),

    "Demon Prince": u(
        "Demon Prince",
        {"M": '8"', "WS": "2+", "BS": "2+", "A": "2", "W": "2", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Chaos", "Heretic Astartes", "<Legion>",
         "Heavy", "Monster", "Character", "Daemon", "Daemon Prince"],
        [{"name": "Daemonic Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"}],
        abilities=(
            "Prince of Chaos: Re-roll hit rolls of 1 for attacks made by friendly <Legion> units whilst they are within 6\" of this unit.\n"
            "Might Over Magic: If this unit has the Khorne keyword, add 1 to wound rolls for attacks made with melee weapons by this unit."
        ),
        options=[
            "This unit can have Wings (Power Rating +1). If this unit has Wings, it: Has Move 12\"; keyword Fly.",
            "When you include this unit in your army, you must choose one of the following additional keywords: Khorne, Tzeentch, Nurgle or Slaanesh.",
            "If you choose Khorne, this unit has the additional ability: Might Over Magic.",
            "If you choose Tzeentch, Nurgle or Slaanesh, this unit has the additional keyword: Psyker.",
        ],
    ),

    "Exalted Champion": u(
        "Exalted Champion",
        {"M": '6"', "WS": "2+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "3"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Character", "Exalted Champion"],
        [{"name": "Exalted Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"}],
        abilities="Aspire to Glory: You can re-roll wound rolls for attacks made with melee weapons by friendly <Legion> units whilst they are within 6\" of this unit.",
    ),

    "Traitor Marines": u(
        "Traitor Marines",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Chaos Space Marines"],
        [
            {"name": "Autocannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "8+", "armorPen": "8+"},
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Lascannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Missile Launcher", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Reaper Chaincannon", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "6+", "armorPen": "10+"},
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Chainswords", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        options=[
            "This unit can also be equipped with one of the following (Power Rating +1): 1 Autocannon; 1 Heavy Bolter; 1 Lascannon; 1 Missile Launcher; 1 Reaper Chaincannon.",
            "Instead of Boltguns and Close Combat Weapons, this unit can be equipped with Bolt Pistols and Chainswords.",
            "If this unit contains 10 or more models, it can also be equipped with one of the following (Power Rating +1): 1 Autocannon; 1 Heavy Bolter; 1 Lascannon; 1 Missile Launcher; 1 Reaper Chaincannon.",
        ],
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "8"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "12"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "6+", "N": "20", "Pt": "16"},
        ],
    ),

    "Cultists": u(
        "Cultists",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "10+", "N": "10", "Pt": "2"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Chaos Cultists"],
        [
            {"name": "Heavy Stubber", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "10+"},
            {"name": "Auto Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "8+", "armorPen": "10+"},
            {"name": "Autoguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "8+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Brutal Assault Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        options=[
            "For every 10 models this unit contains, it can also be equipped with 1 Heavy Stubber (Power Rating +1 per weapon).",
            "Instead of Autoguns and Close Combat Weapons, this unit can be equipped with Auto Pistols and Brutal Assault Weapons.",
        ],
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "4", "W": "4", "Ld": "4", "Sv": "10+", "N": "20", "Pt": "6"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "6", "W": "6", "Ld": "4", "Sv": "10+", "N": "30", "Pt": "9"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "8", "W": "8", "Ld": "4", "Sv": "10+", "N": "40", "Pt": "12"},
        ],
    ),

    "Chaos Chosen": u(
        "Chaos Chosen",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Chosen"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Chosen Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "7+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        options=[
            "Instead of Boltguns and Close Combat Weapons, this unit can be equipped with Bolt Pistols and Chosen Combat Weapons.",
        ],
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "6+", "N": "10", "Pt": "8"},
        ],
    ),

    "Cult Marines": u(
        "Cult Marines",
        {"M": '5"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Cult Marines"],
        [
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Blight Launcher", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "8+"},
            {"name": "Plague Spewer", "type": "Heavy", "range": '9"', "attacks": "1", "skill": "6+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Plague Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "8+"},
            {"name": "Soulreaper Cannon", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Inferno Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "6+", "armorPen": "8+", "abilities": "Rapid Fire"},
            {"name": "Warpflamers", "type": "Small Arms", "range": '8"', "attacks": "User", "skill": "5+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "9+"},
        ],
        abilities=(
            "Select one cult marine variant. Use the datasheet for the chosen variant.\n"
            "Plague Marines (Nurgle, Pt 4/7/10/13 for 5/10/15/20 models, M 5\", Sv 6+) - Ignore Damage (6+). "
            "Can equip up to two of: Blight Launcher, Plague Spewer (Power Rating +1 each).\n"
            "Rubric Marines (Tzeentch, Pt 5/9/13/17 for 5/10/15/20 models, M 5\", Sv 5+, Psyker). "
            "For every 10 models, can equip 1 Soulreaper Cannon (Power Rating +1). "
            "Can swap Inferno Boltguns for Warpflamers."
        ),
        options=[
            "Select one Cult Marine variant (Plague Marines or Rubric Marines). Each has unique stats, keywords and wargear as listed in the Abilities column.",
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "7"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "10"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "6+", "N": "20", "Pt": "13"},
        ],
    ),

    "Terminators": u(
        "Terminators",
        {"M": '5"', "WS": "3+", "BS": "3+", "A": "1", "W": "2", "Ld": "7", "Sv": "4+", "N": "5", "Pt": "11"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Terminators"],
        [
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Reaper Autocannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
            {"name": "Combi-bolters", "type": "Small Arms", "range": '24"', "attacks": "x2", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Terminator Power Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "7+"},
        ],
        abilities="Deep Strike",
        options=[
            "For every 5 models this unit contains, it can also be equipped with one of the following (Power Rating +1 per weapon): 1 Heavy Flamer; 1 Reaper Autocannon.",
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "4", "Ld": "7", "Sv": "4+", "N": "10", "Pt": "21"},
        ],
    ),

    "Greater Possessed": u(
        "Greater Possessed",
        {"M": '7"', "WS": "2+", "BS": "3+", "A": "2", "W": "1", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "6"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Daemon", "Character", "Greater Possessed"],
        [{"name": "Daemonic Mutations", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "8+"}],
        abilities=(
            "Champions of the Host: Each Elites slot in a Detachment allows you to take up to two of this unit "
            "in your army, instead of one. Each unit taken for a single Elites slot must be placed at the same time "
            "and within 6\" of each other unit taken for the same slot the first time they are set up.\n"
            "Locus of Power: Add 1 to wound rolls for attacks made with melee weapons by <Legion> Daemon units whilst they are within 6\" of any units with this ability."
        ),
    ),

    "Possessed": u(
        "Possessed",
        {"M": '7"', "WS": "3+", "BS": "3+", "A": "D3", "W": "2", "Ld": "6", "Sv": "5+", "N": "5", "Pt": "4"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Daemon", "Possessed"],
        [{"name": "Horrifying Mutations", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "8+"}],
        abilities="Writhing Tentacles: Each time this unit fights with a melee weapon, roll one D3 for every 5 models this unit contains to determine the number of attacks it makes.",
        profiles=[
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "2D3", "W": "4", "Ld": "6", "Sv": "5+", "N": "10", "Pt": "11"},
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "3D3", "W": "6", "Ld": "6", "Sv": "5+", "N": "15", "Pt": "16"},
            {"M": '7"', "WS": "3+", "BS": "3+", "A": "4D3", "W": "8", "Ld": "6", "Sv": "5+", "N": "20", "Pt": "21"},
        ],
    ),

    "Chaos Spawn": u(
        "Chaos Spawn",
        {"M": '7"', "WS": "4+", "BS": "-", "A": "1", "W": "1", "Ld": "7", "Sv": "10+", "N": "1", "Pt": "3"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Beast", "Chaos Spawn"],
        [{"name": "Hideous Mutations", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "7+"}],
        abilities=(
            "Terror Troops\n"
            "Mutated Beyond Reason: When this unit makes a Fight action, before picking targets, roll one D3 on the table below to determine what mutation it gains until the end of that action.\n"
            "1 Razor Claws: Add 1 to wound rolls for attacks made by this unit with melee weapons.\n"
            "2 Grasping Pseudopods: Add 1 to this unit's Attacks characteristic.\n"
            "3 Toxic Haemorrhage: Re-roll wound rolls of 1 for attacks made by this unit with melee weapons."
        ),
        profiles=[
            {"M": '7"', "WS": "4+", "BS": "-", "A": "2", "W": "2", "Ld": "7", "Sv": "10+", "N": "2", "Pt": "4"},
            {"M": '7"', "WS": "4+", "BS": "-", "A": "3", "W": "3", "Ld": "8", "Sv": "10+", "N": "3", "Pt": "7"},
            {"M": '7"', "WS": "4+", "BS": "-", "A": "4", "W": "4", "Ld": "8", "Sv": "10+", "N": "4", "Pt": "9"},
            {"M": '7"', "WS": "4+", "BS": "-", "A": "5", "W": "5", "Ld": "8", "Sv": "10+", "N": "5", "Pt": "11"},
        ],
    ),

    "Bikers": u(
        "Bikers",
        {"M": '14"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "3", "Pt": "8"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Biker", "Bikers"],
        [
            {"name": "Twin Boltguns", "type": "Small Arms", "range": '24"', "attacks": "x2", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "6", "Pt": "10"},
            {"M": '14"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "5+", "N": "9", "Pt": "15"},
        ],
    ),

    "Raptors": u(
        "Raptors",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "5"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Fly", "Jump Pack", "Raptors"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Chainswords", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        abilities="Deep Strike, Terror Troops",
        profiles=[
            {"M": '12"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "8"},
            {"M": '12"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "11"},
        ],
    ),

    "Havocs": u(
        "Havocs",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "5", "Pt": "7"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Havocs"],
        [
            {"name": "Autocannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "8+", "armorPen": "8+"},
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Lascannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Missile Launcher", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Reaper Chaincannon", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "6+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        options=[
            "This unit must also be equipped with four of the following in any combination: 1 Autocannon; 1 Heavy Bolter; 1 Lascannon; 1 Missile Launcher; 1 Reaper Chaincannon.",
        ],
    ),

    "Defiler": u(
        "Defiler",
        {"M": '8"', "WS": "4+", "BS": "4+", "A": "3", "W": "3", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "11"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Daemon", "Daemon Engine", "Defiler"],
        [
            {"name": "Battle Cannon", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "6+", "armorPen": "6+"},
            {"name": "Reaper Autocannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
            {"name": "Twin Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Twin Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "2", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Twin Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Defiler Claws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+"},
            {"name": "Defiler Scourge", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "5+"},
        ],
        abilities="Infernal Regeneration: At the start of the Action phase, you can remove one damage marker from this unit.",
        options=[
            "Instead of 1 Twin Heavy Flamer, this unit can be equipped with 1 Defiler Scourge.",
            "Instead of 1 Reaper Autocannon, this unit can be equipped with one of the following: 1 Twin Heavy Bolter; 1 Twin Lascannon.",
        ],
    ),

    "Hellbrute": u(
        "Hellbrute",
        {"M": '8"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "7"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Helbrute"],
        [
            {"name": "Heavy Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Helbrute Plasma Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "6+"},
            {"name": "Missile Launcher", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Multi-melta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Reaper Autocannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
            {"name": "Twin Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Twin Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
            {"name": "Helbrute Fist", "type": "Melee", "range": "Melee", "attacks": "2", "skill": "6+", "armorPen": "6+"},
            {"name": "Helbrute Hammer", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "5+"},
            {"name": "Power Scourge", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "9+"},
        ],
        abilities="Crazed: At the end of the Action phase, roll one D6 for each blast marker placed next to this unit that phase; if any of those dice results are a 6, you can make one Shoot action or one Fight action with this unit.",
        options=[
            "Instead of 1 Multi-melta, this unit can be equipped with one of the following: 1 Helbrute Plasma Cannon; 1 Reaper Autocannon; 1 Twin Heavy Bolter; 1 Twin Lascannon; 1 Helbrute Fist.",
            "Instead of 1 Helbrute Fist, this unit can be equipped with one of the following: 1 Helbrute Hammer; 1 Power Scourge.",
            "Instead of 1 Helbrute Fist, this unit can be equipped with 1 Missile Launcher and Armoured Feet.",
            "For each Helbrute Fist this unit is equipped with, it can also be equipped with 1 Heavy Flamer.",
        ],
    ),

    "Predator": u(
        "Predator",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "7"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Chaos Predator"],
        [
            {"name": "Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Lascannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "10+", "armorPen": "5+"},
            {"name": "Twin Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Predator Autocannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        options=[
            "Instead of 1 Predator Autocannon, this unit can be equipped with 1 Twin Lascannon.",
            "This unit can also be equipped with one of the following (Power Rating +2): 2 Heavy Bolters; 2 Lascannons.",
        ],
    ),

    "Forgefiend": u(
        "Forgefiend",
        {"M": '8"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "6"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Daemon", "Daemon Engine", "Forgefiend"],
        [
            {"name": "Ectoplasma Cannon", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "5+", "armorPen": "5+"},
            {"name": "Hades Autocannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "5+", "armorPen": "7+"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
            {"name": "Daemon Jaws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"},
        ],
        abilities="Infernal Regeneration: At the start of the Action phase, you can remove one damage marker from this unit.",
        options=[
            "Instead of Daemon Jaws, this unit can be equipped with Armoured Feet and 1 Ectoplasma Cannon (Power Rating +1).",
            "Instead of 2 Ectoplasma Cannons, this unit can be equipped with 2 Hades Autocannons (Power Rating +1).",
        ],
    ),

    "Vindicator": u(
        "Vindicator",
        {"M": '10"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Chaos Vindicator"],
        [
            {"name": "Demolisher Cannon", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        options=[
            "This unit can have a Siege Shield (Power Rating +1). If this unit has a Siege Shield, it has a Save characteristic of 4+.",
        ],
    ),

    "Obliterators": u(
        "Obliterators",
        {"M": '4"', "WS": "3+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "4+", "N": "1", "Pt": "9"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Daemon", "Cult of Destruction", "Obliterators"],
        [
            {"name": "Fleshmetal Guns", "type": "Small Arms", "range": '24"', "attacks": "x2", "skill": "5+", "armorPen": "5+"},
            {"name": "Crushing Fists", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        abilities="Deep Strike",
        profiles=[
            {"M": '4"', "WS": "3+", "BS": "3+", "A": "2", "W": "4", "Ld": "6", "Sv": "4+", "N": "2", "Pt": "17"},
            {"M": '4"', "WS": "3+", "BS": "3+", "A": "3", "W": "6", "Ld": "6", "Sv": "4+", "N": "3", "Pt": "25"},
        ],
    ),

    "Land Raider": u(
        "Land Raider",
        {"M": '10"', "WS": "5+", "BS": "3+", "A": "2", "W": "3", "Ld": "7", "Sv": "4+", "N": "1", "Pt": "13"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Transport", "Chaos Land Raider"],
        [
            {"name": "Twin Heavy Bolter", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Twin Lascannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "10+", "armorPen": "5+"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        abilities=(
            "TRANSPORT: This unit can transport up to 10 friendly <Legion> Infantry models. "
            "Each Terminator and Jump Pack model takes up the space of two other models, and each Cult of Destruction model takes up the space of three other models."
        ),
    ),

    "Rhino": u(
        "Rhino",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Transport", "Chaos Rhino"],
        [
            {"name": "Combi-bolter", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Armoured Tracks", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        abilities=(
            "TRANSPORT: This unit can transport up to 10 friendly <Legion> Infantry models. "
            "It cannot transport Terminators, Cult of Destruction or Jump Pack units."
        ),
    ),

    "Helldrake": u(
        "Helldrake",
        {"M": '30"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "10"},
        ["Chaos", "<Mark of Chaos>", "Heretic Astartes", "<Legion>",
         "Heavy", "Vehicle", "Fly", "Daemon", "Daemon Engine", "Helldrake"],
        [
            {"name": "Hades Autocannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "5+", "armorPen": "7+"},
            {"name": "Baleflamer", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "6+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Heldrake Claws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+", "abilities": "Anti-air"},
        ],
        abilities="Infernal Regeneration: At the start of the Action phase, you can remove one damage marker from this unit.",
        options=[
            "Instead of 1 Hades Autocannon, this unit can be equipped with 1 Baleflamer (Power Rating +1).",
        ],
    ),

    "Plague Marines": u(
        "Plague Marines",
        {"M": '5"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "Nurgle", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Plague Marines"],
        [
            {"name": "Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Blight Launcher", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "8+"},
            {"name": "Plague Spewer", "type": "Heavy", "range": '9"', "attacks": "1", "skill": "6+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Plague Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "8+"},
        ],
        abilities="Ignore Damage (6+)",
        options=[
            "This unit can also be equipped with up to two of the following in any combination (Power Rating +1 per weapon): 1 Blight Launcher; 1 Plague Spewer.",
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "7"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "10"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "6+", "N": "20", "Pt": "13"},
        ],
    ),

    "Khorne Berzerkers": u(
        "Khorne Berzerkers",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "Khorne", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Khorne Berzerkers"],
        [
            {"name": "Bolt Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Chain Weapons", "type": "Melee", "range": "Melee", "attacks": "x4", "skill": "6+", "armorPen": "9+"},
        ],
        abilities="Berzerker Horde: If this unit is in a Detachment that contains only World Eaters units, its Battlefield Role is Troops instead of Elites.",
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "8"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "12"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "6+", "N": "20", "Pt": "16"},
        ],
    ),

    "Noise Marines": u(
        "Noise Marines",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "5", "Pt": "4"},
        ["Chaos", "Slaanesh", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Noise Marines"],
        [
            {"name": "Blastmaster", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Noise Marine Weapons", "type": "Small Arms", "range": '24"', "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        abilities="Masters of the Kakophoni: If this unit is in a Detachment that contains only Emperor's Children units, its Battlefield Role is Troops instead of Elites.",
        options=[
            "This unit can also be equipped with 1 Blastmaster (Power Rating +1).",
            "If the unit contains 10 or more models, it can also be equipped with 1 Blastmaster (Power Rating +1).",
        ],
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "10", "Pt": "8"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "6+", "N": "15", "Pt": "12"},
            {"M": '6"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "6+", "N": "20", "Pt": "16"},
        ],
    ),

    "Rubric Marines": u(
        "Rubric Marines",
        {"M": '5"', "WS": "3+", "BS": "3+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "5", "Pt": "5"},
        ["Chaos", "Tzeentch", "Heretic Astartes", "<Legion>",
         "Light", "Infantry", "Psyker", "Rubric Marines"],
        [
            {"name": "Soulreaper Cannon", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Inferno Boltguns", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "6+", "armorPen": "8+", "abilities": "Rapid Fire"},
            {"name": "Warpflamers", "type": "Small Arms", "range": '8"', "attacks": "User", "skill": "5+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "9+"},
        ],
        options=[
            "For every 10 models this unit contains, it can also be equipped with 1 Soulreaper Cannon (Power Rating +1 per weapon).",
            "Instead of Inferno Boltguns, this unit can be equipped with Warpflamers.",
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "10", "Pt": "9"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "3", "W": "3", "Ld": "6", "Sv": "5+", "N": "15", "Pt": "13"},
            {"M": '5"', "WS": "3+", "BS": "3+", "A": "4", "W": "4", "Ld": "6", "Sv": "5+", "N": "20", "Pt": "17"},
        ],
    ),

    "Traitor Guard": u(
        "Traitor Guard",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "7", "Pt": "2"},
        ["Chaos", "Servants of the Abyss",
         "Light", "Infantry", "Traitor Guardsmen"],
        [
            {"name": "Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Las Weapons", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "8+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
    ),

    "Chaos Beastmen": u(
        "Chaos Beastmen",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "4", "Pt": "1"},
        ["Chaos", "Servants of the Abyss",
         "Light", "Infantry", "Chaos Beastmen"],
        [
            {"name": "Pistols", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "8+", "armorPen": "10+"},
            {"name": "Brutal Assault Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        abilities="Slaves to Mallex: This unit does not take up slots in a Detachment that contains Obsidius Mallex.",
    ),

    "Greater Daemon": u(
        "Greater Daemon",
        {"M": '12"', "WS": "2+", "BS": "2+", "A": "2", "W": "3", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "14"},
        ["Chaos", "Daemon", "Legiones Daemonica",
         "Heavy", "Monster", "Fly", "Character", "Greater Daemon"],
        [
            {"name": "Great Axe of Khorne", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "4+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Orange Fires of Tzeentch", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "8+", "armorPen": "8+", "abilities": "Witchfire"},
            {"name": "Staff of Tzeentch", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "7+"},
            {"name": "Baleful Sword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "8+"},
            {"name": "Plague Flail (Ranged)", "type": "Small Arms", "range": '7"', "attacks": "x2", "skill": "7+", "armorPen": "7+"},
            {"name": "Bilesword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+"},
            {"name": "Bileblade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
            {"name": "Doomsday Bell", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
            {"name": "Nurgling Claws & Teeth", "type": "Melee", "range": "Melee", "attacks": "1", "skill": "10+", "armorPen": "10+"},
            {"name": "Plague Flail (Melee)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "7+"},
            {"name": "Ritual Knife", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
            {"name": "Snapping Claws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"},
            {"name": "Witstealer Sword", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
            {"name": "Living Whip (Ranged)", "type": "Small Arms", "range": '6"', "attacks": "2", "skill": "7+", "armorPen": "8+"},
            {"name": "Living Whip (Melee)", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "8+"},
        ],
        abilities=(
            "Select one Greater Daemon. Use the datasheet for the chosen god.\n"
            "Bloodthirster of Insensate Rage (Khorne, Pt 14, M 12\", Fly) - "
            "Greater Daemon of Khorne: Friendly Khorne Daemon units can use this unit's Leadership characteristic instead of their own whilst they are within 6\" of this unit.\n"
            "Lord of Change (Tzeentch, Pt 12, M 12\", Sv 8+, Fly, Psyker) - "
            "Greater Daemon of Tzeentch: Friendly Tzeentch Daemon units can use this unit's Leadership characteristic instead of their own whilst they are within 6\" of this unit. "
            "Rod of Sorcery (Power Rating +1): Add 6\" to the Range of Orange Fires of Tzeentch.\n"
            "Great Unclean One (Nurgle, Pt 14, M 7\", W 4, Sv 9+, Psyker) - Ignore Damage (6+). "
            "Greater Daemon of Nurgle: Friendly Nurgle Daemon units can use this unit's Leadership characteristic instead of their own whilst they are within 6\" of this unit. "
            "Putrid Offering (Bileblade): At the start of the Generate Command Assets step, if equipped with a Bileblade, is a Warlord and is on the battlefield, generate one extra Command Asset. "
            "Reverberating Summons (Doomsday Bell): At the start of the Action phase, roll one D6 for each friendly Light Nurgle Daemon unit within 7\" of any units equipped with a Doomsday Bell; on a 6+ remove one damage marker from that unit.\n"
            "Keeper of Secrets (Slaanesh, Pt 14, M 15\", Sv 9+, Psyker) - "
            "Greater Daemon of Slaanesh: Friendly Slaanesh Daemon units can use this unit's Leadership characteristic instead of their own whilst they are within 6\" of this unit. "
            "Mesmerising Aura: Subtract 1 from hit rolls for attacks made with melee weapons by enemy units that target this unit. "
            "Sinistrous Hand: Each time a blast marker is placed next to an enemy unit as a result of an attack made by this unit with a melee weapon, you can remove one blast marker from this unit."
        ),
        options=[
            "Select one Greater Daemon (Bloodthirster of Insensate Rage, Lord of Change, Great Unclean One, or Keeper of Secrets). Each has unique Move, Save, abilities and wargear as listed in the Abilities column.",
            "Lord of Change: Can equip 1 Baleful Sword (Power Rating +1) or have a Rod of Sorcery (Power Rating +1).",
            "Great Unclean One: Instead of 1 Bilesword, can equip 1 Doomsday Bell (Power Rating +1). Instead of 1 Plague Flail, can equip 1 Bileblade.",
            "Keeper of Secrets: Instead of 1 Ritual Knife, can equip Living Whip (Ranged) and Living Whip (Melee) (Power Rating +2), or have Shining Aegis (Ignore Damage 6+) or Sinistrous Hand.",
        ],
        profiles=[
            {"M": '12"', "WS": "2+", "BS": "2+", "A": "2", "W": "3", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "14"},
            {"M": '12"', "WS": "2+", "BS": "2+", "A": "2", "W": "3", "Ld": "8", "Sv": "8+", "N": "1", "Pt": "12"},
            {"M": '7"', "WS": "2+", "BS": "2+", "A": "2", "W": "4", "Ld": "8", "Sv": "9+", "N": "1", "Pt": "14"},
            {"M": '15"', "WS": "2+", "BS": "2+", "A": "2", "W": "3", "Ld": "8", "Sv": "9+", "N": "1", "Pt": "14"},
        ],
    ),
}

CHAOS_MARINES_SLOTS = [
    slot(1, "HQ", CHAOS_MARINES["Abaddon The Despoiler"]),
    slot(2, "HQ", CHAOS_MARINES["Lord"]),
    slot(3, "HQ", CHAOS_MARINES["Sorcerer"]),
    slot(4, "HQ", CHAOS_MARINES["Demon Prince"]),
    slot(5, "HQ", CHAOS_MARINES["Exalted Champion"]),
    slot(6, "Troops", CHAOS_MARINES["Traitor Marines"]),
    slot(7, "Troops", CHAOS_MARINES["Cultists"]),
    slot(8, "Elites", CHAOS_MARINES["Chaos Chosen"]),
    slot(9, "Elites", CHAOS_MARINES["Cult Marines"]),
    slot(10, "Elites", CHAOS_MARINES["Terminators"]),
    slot(11, "Elites", CHAOS_MARINES["Greater Possessed"]),
    slot(12, "Elites", CHAOS_MARINES["Possessed"]),
    slot(13, "Fast", CHAOS_MARINES["Chaos Spawn"]),
    slot(14, "Fast", CHAOS_MARINES["Bikers"]),
    slot(15, "Fast", CHAOS_MARINES["Raptors"]),
    slot(16, "Heavy", CHAOS_MARINES["Havocs"]),
    slot(17, "Heavy", CHAOS_MARINES["Defiler"]),
    slot(18, "Heavy", CHAOS_MARINES["Hellbrute"]),
    slot(19, "Heavy", CHAOS_MARINES["Predator"]),
    slot(20, "Heavy", CHAOS_MARINES["Forgefiend"]),
    slot(21, "Heavy", CHAOS_MARINES["Vindicator"]),
    slot(22, "Heavy", CHAOS_MARINES["Obliterators"]),
    slot(23, "Heavy", CHAOS_MARINES["Land Raider"]),
    slot(24, "Transport", CHAOS_MARINES["Rhino"]),
    slot(25, "Air", CHAOS_MARINES["Helldrake"]),
    slot(26, "Elites", CHAOS_MARINES["Plague Marines"]),
    slot(27, "Elites", CHAOS_MARINES["Khorne Berzerkers"]),
    slot(28, "Heavy", CHAOS_MARINES["Noise Marines"]),
    slot(29, "Elites", CHAOS_MARINES["Rubric Marines"]),
    slot(30, "HQ", CHAOS_MARINES["Traitor Guard"]),
    slot(31, "Elites", CHAOS_MARINES["Chaos Beastmen"]),
    slot(32, "Lord", CHAOS_MARINES["Greater Daemon"]),
]
