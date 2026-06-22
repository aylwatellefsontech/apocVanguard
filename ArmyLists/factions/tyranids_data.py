from generate_all_faction_lists import slot, u

# ---------------------------------------------------------------------------
# Tyranids unit datasheets (Apoc_Datasheet_Tyranid_Hive_Fleets_web.pdf)
# ---------------------------------------------------------------------------

TYRANIDS = {
    "Hive Tyrant": u(
        "Hive Tyrant",
        {"M": '9"', "WS": "2+", "BS": "3+", "A": "1", "W": "2", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "9"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Psyker", "Character", "Synapse Creature", "Hive Tyrant"],
        [
            {"name": "Deathspitters with Slimer Maggots", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "5+", "armorPen": "8+"},
            {"name": "Devourers with Brainleech Worms", "type": "Heavy", "range": '18"', "attacks": "3", "skill": "6+", "armorPen": "9+"},
            {"name": "Stranglethorn Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "4+", "armorPen": "8+"},
            {"name": "Heavy Venom Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "4+"},
            {"name": "Monstrous Bio-weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "7+"},
            {"name": "Prehensile Pincer Tail", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
            {"name": "Monstrous Scything Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "6+"},
        ],
        "The Will of the Hive Mind: At the start of the Generate Command Assets step, if this unit is a Warlord "
        "and is on the battlefield, you generate one extra Command Asset.",
        options=[
            "A Hive Tyrant is a unit that contains 1 model. It is equipped with: Heavy Venom Cannon; Monstrous Scything Talons; Prehensile Pincer Tail.",
            "Instead of 1 Monstrous Scything Talons, this unit can be equipped with one of the following: Deathspitters with Slimer Maggots; Devourers with Brainleech Worms; Monstrous Bio-weapons.",
            "Instead of 1 Heavy Venom Cannon, this unit can be equipped with one of the following: Deathspitters with Slimer Maggots; Devourers with Brainleech Worms; Monstrous Bio-weapons; Monstrous Scything Talons; Stranglethorn Cannon.",
            "This unit can have Wings (Power Rating +2). If this unit has Wings, it:",
            '- Has a Move characteristic of 16".',
            "- Has the following additional abilities: Deep Strike.",
            "- Has the following additional keywords: Fly.",
        ],
    ),
    "Tyranid Prime": u(
        "Tyranid Prime",
        {"M": '6"', "WS": "2+", "BS": "3+", "A": "1", "W": "1", "Ld": "8", "Sv": "6+", "N": "1", "Pt": "6"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Character", "Synapse Creature", "Tyranid Prime"],
        [
            {"name": "Ranged Bio-weapons", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Melee Bio-weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        'Alpha Warrior: Add 1 to hit rolls for attacks made by <Hive Fleet> Tyranid Warrior units whilst they are within 6" of any friendly units with this ability.',
        options=["A Tyranid Prime is a unit that contains 1 model. It is equipped with: Ranged Bio-weapons; Melee Bio-weapons."],
    ),
    "Tervigon": u(
        "Tervigon",
        {"M": '8"', "WS": "4+", "BS": "4+", "A": "1", "W": "3", "Ld": "7", "Sv": "6+", "N": "1", "Pt": "6"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Psyker", "Character", "Synapse Creature", "Tervigon"],
        [
            {"name": "Stinger Salvo", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Massive Crushing Claws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "5+"},
            {"name": "Massive Scything Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "7+"},
        ],
        "Brood Progenitor: Re-roll hit rolls of 1 for attacks made with ranged weapons by friendly <Hive Fleet> Termagant units whilst they are within 6\" of this unit.\n"
        "Synaptic Backlash: If this unit is destroyed, place one blast marker next to every friendly <Hive Fleet> Termagant unit within 6\" of this unit before removing it from the battlefield.\n"
        "Spawn Termagants: Once per turn, at the start of the Set Up Reinforcements step of the Orders phase, this unit can spawn Termagants. If it does, add a new unit of 10 Termagant models equipped with Fleshborers to your army: it is part of this unit's Detachment and has the <Hive Fleet> keyword. Set the new unit up on the battlefield wholly within 6\" of this unit and more than 1\" from enemy units. If the unit cannot be placed in this way, it is destroyed. Then roll a D6; on a 1-3 this unit cannot use this ability again this battle.",
        options=[
            "A Tervigon is a unit that contains 1 model. It is equipped with: Stinger Salvo; Massive Scything Talons.",
            "Instead of Massive Scything Talons, this unit can be equipped with Massive Crushing Claws.",
        ],
    ),
    "The Swarmlord": u(
        "The Swarmlord",
        {"M": '9"', "WS": "2+", "BS": "3+", "A": "2", "W": "2", "Ld": "8", "Sv": "5+", "N": "1", "Pt": "12"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Psyker", "Character", "Synapse Creature", "Hive Tyrant", "The Swarmlord"],
        [
            {"name": "Bone Sabres", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Prehensile Pincer Tail", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "The Will of the Hive Mind: At the start of the Generate Command Assets step, if this unit is a Warlord "
        "and is on the battlefield, you generate one extra Command Asset.\n"
        'Hive Commander: Morale tests taken for friendly <Hive Fleet> units are automatically passed whilst they are within 18" of this unit.',
        options=[
            "The Swarmlord is a unit that contains 1 model. It is equipped with: Bone Sabres; Prehensile Pincer Tail. You can only include one of this unit in your army.",
        ],
    ),
    "Termagants": u(
        "Termagants",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "10+", "N": "10", "Pt": "2"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Termagants"],
        [
            {"name": "Fleshborers", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Spinefists", "type": "Small Arms", "range": '12"', "attacks": "x2", "skill": "8+", "armorPen": "10+"},
            {"name": "Devourers", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "7+", "armorPen": "9+"},
            {"name": "Termagant Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        "Hail of Living Ammunition: If this unit contains 30 models, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
        profiles=[
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "4", "W": "4", "Ld": "4", "Sv": "10+", "N": "20", "Pt": "4"},
            {"M": '6"', "WS": "4+", "BS": "4+", "A": "6", "W": "6", "Ld": "4", "Sv": "10+", "N": "30", "Pt": "7"},
        ],
        options=[
            "Termagants are a unit that contains 10 models. It can contain 20 models (Power Rating 4) or 30 models (Power Rating 7). It is equipped with: Fleshborers; Termagant Melee Weapons.",
            "Instead of Fleshborers, this unit can be equipped with Spinefists (Power Rating +1 for each 10 models this unit contains).",
            "Instead of Fleshborers, this unit can be equipped with Devourers (Power Rating +2 for each 10 models this unit contains).",
        ],
    ),
    "Hormagaunts": u(
        "Hormagaunts",
        {"M": '9"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "10+", "N": "10", "Pt": "2"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Hormagaunts"],
        [{"name": "Scything Talons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"}],
        "Hungering Swarm: If this unit contains 30 models, re-roll wound rolls of 1 for attacks made with melee weapons by this unit.",
        profiles=[
            {"M": '9"', "WS": "4+", "BS": "4+", "A": "4", "W": "4", "Ld": "4", "Sv": "10+", "N": "20", "Pt": "4"},
            {"M": '9"', "WS": "4+", "BS": "4+", "A": "6", "W": "6", "Ld": "4", "Sv": "10+", "N": "30", "Pt": "7"},
        ],
        options=["Hormagaunts are a unit that contains 10 models. It can contain 20 models (Power Rating 4) or 30 models (Power Rating 7). It is equipped with: Scything Talons."],
    ),
    "Ripper Swarms": u(
        "Ripper Swarms",
        {"M": '6"', "WS": "5+", "BS": "5+", "A": "2", "W": "2", "Ld": "4", "Sv": "11+", "N": "3", "Pt": "2"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Swarm", "Rippers"],
        [{"name": "Claws & Teeth", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"}],
        "Deep Strike",
        profiles=[
            {"M": '6"', "WS": "5+", "BS": "5+", "A": "4", "W": "4", "Ld": "4", "Sv": "11+", "N": "6", "Pt": "4"},
            {"M": '6"', "WS": "5+", "BS": "5+", "A": "6", "W": "6", "Ld": "4", "Sv": "11+", "N": "9", "Pt": "6"},
        ],
        options=["Ripper Swarms are a unit that contains 3 models. It can contain 6 models (Power Rating 4) or 9 models (Power Rating 6). It is equipped with: Claws & Teeth."],
    ),
    "Tyranid Warriors": u(
        "Tyranid Warriors",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "7", "Sv": "8+", "N": "3", "Pt": "4"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Synapse Creature", "Tyranid Warriors"],
        [
            {"name": "Barbed Strangler", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Venom Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "7+"},
            {"name": "Ranged Bio-weapons", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Melee Bio-weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "7", "Sv": "8+", "N": "6", "Pt": "8"},
            {"M": '6"', "WS": "3+", "BS": "4+", "A": "6", "W": "6", "Ld": "7", "Sv": "8+", "N": "9", "Pt": "12"},
        ],
        options=[
            "Tyranid Warriors are a unit that contains 3 models. It can contain 6 models (Power Rating 8) or 9 models (Power Rating 12). It is equipped with: Ranged Bio-weapons; Melee Bio-weapons.",
            "For every 3 models this unit contains, it can also be equipped with one of the following (Power Rating +1 per weapon): 1 Barbed Strangler; 1 Venom Cannon.",
        ],
    ),
    "Genestealers": u(
        "Genestealers",
        {"M": '9"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "9+", "N": "5", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Genestealers"],
        [{"name": "Genestealer Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "6+", "armorPen": "8+"}],
        "Infiltrators",
        profiles=[
            {"M": '9"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "7", "Sv": "9+", "N": "10", "Pt": "9"},
            {"M": '9"', "WS": "3+", "BS": "4+", "A": "4", "W": "3", "Ld": "7", "Sv": "9+", "N": "15", "Pt": "13"},
            {"M": '9"', "WS": "3+", "BS": "4+", "A": "5", "W": "4", "Ld": "7", "Sv": "9+", "N": "20", "Pt": "17"},
        ],
        options=[
            "Genestealers are a unit that contains 5 models. It can contain 10 models (Power Rating 9), 15 models (Power Rating 13) or 20 models (Power Rating 17). It is equipped with: Genestealer Melee Weapons.",
        ],
    ),
    "Zoanthropes": u(
        "Zoanthropes",
        {"M": '5"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "7", "Sv": "6+", "N": "3", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Fly", "Psyker", "Synapse Creature", "Zoanthropes"],
        [
            {"name": "Warp Blast", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "4+", "armorPen": "4+", "abilities": "Witchfire"},
            {"name": "Zoanthrope Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Warp Field: Roll D12s when making saving throws for this unit, irrespective of the size of the blast markers next to it.",
        profiles=[{"M": '5"', "WS": "4+", "BS": "3+", "A": "2", "W": "4", "Ld": "7", "Sv": "6+", "N": "6", "Pt": "10"}],
        options=["Zoanthropes are a unit that contains 3 models. It can contain 6 models (Power Rating 10). It is equipped with: Warp Blast; Zoanthrope Melee Weapons."],
    ),
    "Lictor": u(
        "Lictor",
        {"M": '9"', "WS": "2+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "10+", "N": "1", "Pt": "3"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Lictor"],
        [
            {"name": "Flesh Hooks", "type": "Small Arms", "range": '6"', "attacks": "User", "skill": "8+", "armorPen": "9+"},
            {"name": "Grasping Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "8+"},
        ],
        "Deep Strike, Stealth",
        options=["A Lictor is a unit that contains 1 model. It is equipped with: Flesh Hooks; Grasping Talons."],
    ),
    "Pyrovores": u(
        "Pyrovores",
        {"M": '5"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "3"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Pyrovores"],
        [
            {"name": "Flamespurt", "type": "Heavy", "range": '10"', "attacks": "User", "skill": "4+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Acid Maw", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "8+"},
        ],
        "Acid Blood: When a blast marker is placed next to this unit, if it is in base contact with any enemy units, select one of those units and roll one D6. On a 4+ place one blast marker next to that unit.",
        profiles=[
            {"M": '5"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "2", "Pt": "5"},
            {"M": '5"', "WS": "4+", "BS": "4+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "7"},
        ],
        options=[
            "Pyrovores are a unit that contains 1 model. It can contain 2 models (Power Rating 5) or 3 models (Power Rating 7). It is equipped with: Flamespurt; Acid Maw.",
        ],
    ),
    "Haruspex": u(
        "Haruspex",
        {"M": '7"', "WS": "4+", "BS": "4+", "A": "2", "W": "3", "Ld": "4", "Sv": "6+", "N": "1", "Pt": "8"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Haruspex"],
        [
            {"name": "Grasping Tongue", "type": "Small Arms", "range": '12"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Ravenous Maw", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "9+"},
            {"name": "Shovelling Claws", "type": "Melee", "range": "Melee", "attacks": "1", "skill": "5+", "armorPen": "4+"},
        ],
        "Acid Blood: When a blast marker is placed next to this unit, if it is in base contact with any enemy units, select one of those units and roll one D6. On a 4+ place one blast marker next to that unit.\n"
        "Rapacious Hunger: When an enemy Light unit is destroyed whilst in base contact with this unit, if this unit has at least one damage marker next to it, remove one damage marker from this unit.",
        options=[
            "A Haruspex is a unit that contains 1 model. It is equipped with: Grasping Tongue; Ravenous Maw; Shovelling Claws.",
        ],
    ),
    "Tyrant Guard": u(
        "Tyrant Guard",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "6+", "N": "3", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Tyrant Guard"],
        [{"name": "Tyrant Guard Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "4+", "armorPen": "8+"}],
        'Shieldwall: At the start of the Damage phase, you can select one friendly <Hive Fleet> Hive Tyrant unit that has at least one blast marker next to it and is within 6" of this unit. Remove up to D3 blast markers from that Hive Tyrant unit and place them next to this unit.',
        profiles=[{"M": '7"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "4", "Sv": "6+", "N": "6", "Pt": "10"}],
        options=["Tyrant Guard are a unit that contains 3 models. It can contain 6 models (Power Rating 10). It is equipped with: Tyrant Guard Melee Weapons."],
    ),
    "Hive Guard": u(
        "Hive Guard",
        {"M": '5"', "WS": "4+", "BS": "3+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "3", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Hive Guard"],
        [
            {"name": "Impaler Cannons", "type": "Small Arms", "range": '36"', "attacks": "User", "skill": "4+", "armorPen": "7+", "abilities": "Barrage"},
            {"name": "Shockcannons", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "5+"},
            {"name": "Forelimbs", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        profiles=[{"M": '5"', "WS": "4+", "BS": "3+", "A": "2", "W": "4", "Ld": "5", "Sv": "8+", "N": "6", "Pt": "10"}],
        options=[
            "Hive Guard are a unit that contains 3 models. It can contain 6 models (Power Rating 10). It is equipped with: Impaler Cannons; Forelimbs.",
            "Instead of Impaler Cannons, this unit can be equipped with Shockcannons.",
        ],
    ),
    "Venomthropes": u(
        "Venomthropes",
        {"M": '5"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "10+", "N": "3", "Pt": "4"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Fly", "Venomthropes"],
        [
            {"name": "Toxic Lashes (Ranged)", "type": "Small Arms", "range": '6"', "attacks": "User", "skill": "5+", "armorPen": "9+"},
            {"name": "Toxic Lashes (Melee)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "9+"},
        ],
        'Shrouding Spores: Friendly Light <Hive Fleet> and Heavy <Hive Fleet> units have the Stealth ability whilst they are within 6" of this unit. If this unit contains 6 models, the range of this ability is increased by 3".\n'
        'Toxic Miasma: At the end of the Action phase, roll one D6 for each unit within 6" of any enemy units with this ability; on a 6 place one blast marker next to the unit being rolled for.',
        profiles=[{"M": '5"', "WS": "4+", "BS": "4+", "A": "2", "W": "4", "Ld": "4", "Sv": "10+", "N": "6", "Pt": "8"}],
        options=["Venomthropes are a unit that contains 3 models. It can contain 6 models (Power Rating 8). It is equipped with: Toxic Lashes (Ranged); Toxic Lashes (Melee)."],
    ),
    "Neurothrope": u(
        "Neurothrope",
        {"M": '5"', "WS": "4+", "BS": "3+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Fly", "Psyker", "Character", "Infantry", "Zoanthrope", "Synapse Creature", "Neurothrope"],
        [
            {"name": "Spirit Leech", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "8+", "armorPen": "8+", "abilities": "Witchfire"},
            {"name": "Claws & Teeth", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "10+"},
        ],
        "Warp Field: Roll D12s when making saving throws for this unit, irrespective of the size of the blast markers next to it.",
        options=["A Neurothrope is a unit that contains 1 model. It is equipped with: Spirit Leech; Claws & Teeth."],
    ),
    "Gargoyles": u(
        "Gargoyles",
        {"M": '12"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "10+", "N": "10", "Pt": "4"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Fly", "Gargoyles"],
        [
            {"name": "Fleshborers", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Blinding Venom", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike\nHail of Living Ammunition: If this unit contains 30 models, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
        profiles=[
            {"M": '12"', "WS": "4+", "BS": "4+", "A": "4", "W": "4", "Ld": "4", "Sv": "10+", "N": "20", "Pt": "8"},
            {"M": '12"', "WS": "4+", "BS": "4+", "A": "6", "W": "6", "Ld": "4", "Sv": "10+", "N": "30", "Pt": "12"},
        ],
        options=[
            "Gargoyles are a unit that contains 10 models. It can contain 20 models (Power Rating 8) or 30 models (Power Rating 12). It is equipped with: Fleshborers; Blinding Venom.",
        ],
    ),
    "Raveners": u(
        "Raveners",
        {"M": '12"', "WS": "3+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "10+", "N": "3", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Raveners"],
        [
            {"name": "Ravener Ranged Weapons", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Ravener Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "8+"},
        ],
        "Deep Strike",
        profiles=[
            {"M": '12"', "WS": "3+", "BS": "4+", "A": "2", "W": "4", "Ld": "4", "Sv": "10+", "N": "6", "Pt": "10"},
            {"M": '12"', "WS": "3+", "BS": "4+", "A": "3", "W": "6", "Ld": "4", "Sv": "10+", "N": "9", "Pt": "15"},
        ],
        options=[
            "Raveners are a unit that contains 3 models. It can contain 6 models (Power Rating 10) or 9 models (Power Rating 15). It is equipped with: Ravener Ranged Weapons; Ravener Melee Weapons.",
        ],
    ),
    "Spore Mines": u(
        "Spore Mines",
        {"M": '3"', "WS": "-", "BS": "-", "A": "-", "W": "1", "Ld": "8", "Sv": "12+", "N": "3", "Pt": "2"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Fly", "Spore Mines"],
        [],
        "Deep Strike\nLiving Bombs: Morale tests taken for this unit are automatically passed.\n"
        'Floating Death: After a Move action (made by any unit), if this unit is within 3" of an enemy unit, roll one D6 for each model in this unit. For each 3+ place one blast marker next to the closest enemy unit. Then, this unit is destroyed.',
        profiles=[
            {"M": '3"', "WS": "-", "BS": "-", "A": "-", "W": "2", "Ld": "8", "Sv": "12+", "N": "6", "Pt": "4"},
            {"M": '3"', "WS": "-", "BS": "-", "A": "-", "W": "3", "Ld": "8", "Sv": "12+", "N": "9", "Pt": "6"},
        ],
        options=["Spore Mines are a unit that contains 3 models. It can contain 6 models (Power Rating 4) or 9 models (Power Rating 6)."],
    ),
    "Carnifex": u(
        "Carnifex",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "6+", "N": "1", "Pt": "5"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Carnifex"],
        [
            {"name": "Deathspitters with Slimer Maggots", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "5+", "armorPen": "8+"},
            {"name": "Devourers with Brainleech Worms", "type": "Heavy", "range": '18"', "attacks": "3", "skill": "6+", "armorPen": "9+"},
            {"name": "Heavy Venom Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "4+"},
            {"name": "Spine Banks", "type": "Heavy", "range": '6"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Stranglethorn Cannon", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "4+", "armorPen": "8+"},
            {"name": "Carnifex Jaws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
            {"name": "Carnifex Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "5+"},
        ],
        'Chitin Thorns: At the end of the Action phase, roll a D6 for each unit within 6" of any enemy units with Chitin Thorns; on a 6 place one blast marker next to the unit being rolled for.\n'
        "Monstrous Brood: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. "
        'Each unit taken for a single Heavy Support slot must be placed at the same time and within 6" of each other unit taken for the same slot the first time they are set up.',
        options=[
            "A Carnifex is a unit that contains 1 model. It is equipped with: Heavy Venom Cannon; Carnifex Jaws; Carnifex Melee Weapons.",
            "Instead of Carnifex Melee Weapons, this unit can be equipped with one of the following: Deathspitters with Slimer Maggots; Devourers with Brainleech Worms.",
            "Instead of 1 Heavy Venom Cannon, this unit can be equipped with one of the following: Carnifex Melee Weapons; Deathspitters with Slimer Maggots; Devourers with Brainleech Worms; Stranglethorn Cannon.",
            "This unit can also be equipped with Spine Banks (Power Rating +1).",
            "This unit can have Enhanced Senses (Power Rating +1). If this unit has Enhanced Senses, it has a Ballistic Skill of 3+.",
            "This unit can have Chitin Thorns (Power Rating +1). If this unit has Chitin Thorns, it has the following additional abilities: Chitin Thorns.",
        ],
    ),
    "Exocrine": u(
        "Exocrine",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "3", "Ld": "4", "Sv": "6+", "N": "1", "Pt": "10"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Exocrine"],
        [
            {"name": "Bio-plasmic Cannon", "type": "Heavy", "range": '36"', "attacks": "3", "skill": "4+", "armorPen": "6+"},
            {"name": "Powerful Limbs", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "Weapon Beast: When this unit makes a Shoot action, if it has remained stationary this turn, double the Attacks characteristic of its Bio-plasmic Cannon for that action.",
        options=["An Exocrine is a unit that contains 1 model. It is equipped with: Bio-plasmic Cannon; Powerful Limbs."],
    ),
    "Tyrannofex": u(
        "Tyrannofex",
        {"M": '6"', "WS": "4+", "BS": "4+", "A": "1", "W": "3", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "11"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Tyrannofex"],
        [
            {"name": "Acid Spray", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "5+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Fleshborer Hive", "type": "Heavy", "range": '18"', "attacks": "5", "skill": "4+", "armorPen": "9+"},
            {"name": "Rupture Cannon", "type": "Heavy", "range": '48"', "attacks": "3", "skill": "9+", "armorPen": "4+"},
            {"name": "Stinger Salvo", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Powerful Limbs", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        "Weapon Beast: When this unit makes a Shoot action, if it has remained stationary this turn, double the Attacks characteristic of its Acid Spray, Fleshborer Hive, Rupture Cannon and Stinger Salvo for that action.",
        options=[
            "A Tyrannofex is a unit that contains 1 model. It is equipped with: Acid Spray; Stinger Salvo; Powerful Limbs.",
            "Instead of 1 Acid Spray, this unit can be equipped with one of the following: 1 Fleshborer Hive; 1 Rupture Cannon.",
        ],
    ),
    "Biovores": u(
        "Biovores",
        {"M": '5"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "2"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Light", "Infantry", "Biovores"],
        [
            {"name": "Spore Mine Launcher", "type": "Small Arms", "range": '48"', "attacks": "User", "skill": "6+", "armorPen": "6+", "abilities": "Barrage"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '5"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "2", "Pt": "4"},
            {"M": '5"', "WS": "4+", "BS": "4+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "6"},
        ],
        options=["Biovores are a unit that contains 1 model. It can contain 2 models (Power Rating 4) or 3 models (Power Rating 6). It is equipped with: Spore Mine Launcher; Close Combat Weapons."],
    ),
    "Toxicrene": u(
        "Toxicrene",
        {"M": '8"', "WS": "3+", "BS": "4+", "A": "1", "W": "3", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "8"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Toxicrene"],
        [
            {"name": "Choking Spores", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "6+", "armorPen": "9+"},
            {"name": "Massive Toxic Lashes (Ranged)", "type": "Small Arms", "range": '8"', "attacks": "x2", "skill": "5+", "armorPen": "8+"},
            {"name": "Massive Toxic Lashes (Melee)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "8+"},
        ],
        'Hypertoxic Miasma: At the end of the Action phase, roll one D6 for each unit within 6" of any enemy units with this ability; on a 5+ place one blast marker next to the unit being rolled for.\n'
        "Acid Blood: When a blast marker is placed next to this unit, if it is in base contact with any enemy units, select one of those units and roll one D6. On a 4+ place one blast marker next to that unit.",
        options=["A Toxicrene is a unit that contains 1 model. It is equipped with: Choking Spores; Massive Toxic Lashes (Ranged); Massive Toxic Lashes (Melee)."],
    ),
    "Screamer-Killer": u(
        "Screamer-Killer",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "6+", "N": "1", "Pt": "6"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Carnifex", "Screamer-Killer"],
        [
            {"name": "Bio-plasmic Scream", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
            {"name": "Screamer-Killer Talons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "6+"},
        ],
        "Terror Troops\n"
        "Monstrous Brood: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. "
        'Each unit taken for a single Heavy Support slot must be placed at the same time and within 6" of each other unit taken for the same slot the first time they are set up.',
        options=["A Screamer-Killer is a unit that contains 1 model. It is equipped with: Bio-plasmic Scream; Screamer-Killer Talons."],
    ),
    "Trygon": u(
        "Trygon",
        {"M": '9"', "WS": "3+", "BS": "4+", "A": "3", "W": "3", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "10"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Trygon"],
        [
            {"name": "Bio-electric Pulse", "type": "Heavy", "range": '12"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Massive Scything Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "7+"},
        ],
        "Deep Strike",
        options=["A Trygon is a unit that contains 1 model. It is equipped with: Bio-electric Pulse; Massive Scything Talons."],
    ),
    "Mawloc": u(
        "Mawloc",
        {"M": '9"', "WS": "4+", "BS": "-", "A": "1", "W": "3", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "10"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Mawloc"],
        [
            {"name": "Distensible Jaws", "type": "Melee", "range": "Melee", "attacks": "1", "skill": "5+", "armorPen": "6+"},
            {"name": "Scything Talons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike\n"
        "Burrow: When this unit makes a Move action, it can burrow instead of moving. If it does, it is removed from the battlefield and placed into Tactical Reserves. When this unit arrives as reinforcements, set it up as described in the Terror from the Deep ability. A unit cannot burrow if it was set up on the battlefield this turn, if there are any enemy units in base contact with it, or if there are any blast markers next to it.\n"
        'Terror from the Deep: When this unit uses the Deep Strike ability, you can set it up anywhere on the battlefield that is more than 1" away from any enemy units, instead of 9". After setting this unit up using the Deep Strike ability, if there are any enemy units within 3" of it, select one of those units and roll one D12. On a 3-5 place one blast marker next to that unit, on a 6-9 place two blast markers next to that unit and on a 10+ place three blast markers next to that unit.',
        options=["A Mawloc is a unit that contains 1 model. It is equipped with: Distensible Jaws; Scything Talons."],
    ),
    "Tyrannocyte": u(
        "Tyrannocyte",
        {"M": '6"', "WS": "5+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "8"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Fly", "Tyrannocyte"],
        [
            {"name": "Barbed Stranglers", "type": "Heavy", "range": '36"', "attacks": "5", "skill": "7+", "armorPen": "9+"},
            {"name": "Deathspitters", "type": "Heavy", "range": '24"', "attacks": "5", "skill": "6+", "armorPen": "9+"},
            {"name": "Venom Cannons", "type": "Heavy", "range": '36"', "attacks": "5", "skill": "9+", "armorPen": "7+"},
            {"name": "Barbed Tentacles", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Deep Strike\n"
        "Transport Spore: When this unit is set up in Tactical Reserves, you can also set up a friendly <Hive Fleet> Infantry unit of up to 20 models or a <Hive Fleet> Monster unit with a Wounds "
        'characteristic of 4 or less inside it (this cannot be a Tyrannocyte or Sporocyst). When this unit uses its Deep Strike ability, set any unit inside it up on the battlefield wholly within 6" of this unit '
        'and more than 9" from enemy units. If that unit cannot be placed in this way, it is destroyed.',
        options=[
            "A Tyrannocyte is a unit that contains 1 model. It is equipped with: Deathspitters; Barbed Tentacles.",
            "Instead of Deathspitters, this unit can be equipped with one of the following: Barbed Stranglers; Venom Cannons.",
        ],
    ),
    "Harpy": u(
        "Harpy",
        {"M": '30"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "7", "Sv": "8+", "N": "1", "Pt": "9"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Fly", "Harpy"],
        [
            {"name": "Heavy Venom Cannons", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "8+", "armorPen": "4+"},
            {"name": "Stranglethorn Cannons", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "4+", "armorPen": "8+"},
            {"name": "Stinger Salvo", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Scything Wings", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        "Spore Mine Cysts: After this unit makes a Move action, you can select one enemy unit it moved over whilst making that Move action. Roll one D6; on a 3+ place one blast marker next to that unit.",
        options=[
            "A Harpy is a unit that contains 1 model. It is equipped with: Stinger Salvo; Stranglethorn Cannons; Scything Wings.",
            "Instead of Stranglethorn Cannons, this unit can be equipped with Heavy Venom Cannons.",
        ],
    ),
    "Hive Crone": u(
        "Hive Crone",
        {"M": '30"', "WS": "4+", "BS": "4+", "A": "1", "W": "2", "Ld": "7", "Sv": "8+", "N": "1", "Pt": "9"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Heavy", "Monster", "Fly", "Hive Crone"],
        [
            {"name": "Drool Cannon", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "5+", "armorPen": "8+", "abilities": "Inferno"},
            {"name": "Stinger Salvo", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Tentaclids", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "Anti-air"},
            {"name": "Scything Wings", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "9+"},
            {"name": "Wicked Spur", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "5+"},
        ],
        options=["A Hive Crone is a unit that contains 1 model. It is equipped with: Drool Cannon; Stinger Salvo; Tentaclids; Scything Wings; Wicked Spur."],
    ),
    "Hierophant": u(
        "Hierophant",
        {"M": '12"', "WS": "3+", "BS": "3+", "A": "2", "W": "7", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "45"},
        ["Tyranids", "Tyranid Hive Fleets", "<Hive Fleet>", "Super-heavy", "Monster", "Transport", "Titanic", "Hierophant Bio-titan"],
        [
            {"name": "Bio-plasma Torrent", "type": "Heavy", "range": '8"', "attacks": "4", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Dire Bio-cannon", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Gargantuan Scything Talons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Lashwhip Pods", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "9+"},
        ],
        "Transport: This unit can transport up to 20 friendly Genestealers, Termagants, Hormagaunts, Hive Guard, Tyrant Guard or Tyranid Warriors models. Each Hive Guard, Tyrant Guard or Tyranid Warrior model takes up the space of 3 other models. It can also transport 1 friendly Tyranid Prime or Broodlord.",
        options=[
            "A Hierophant Bio-titan is a unit that contains 1 model. It is equipped with: 2 Dire Bio-cannons; Lashwhip Pods; Bio-plasma Torrent; Gargantuan Scything Talons.",
        ],
    ),
}

TYRANIDS_SLOTS = [
    slot(1, "HQ", TYRANIDS["The Swarmlord"]),
    slot(2, "HQ", TYRANIDS["Tervigon"]),
    slot(3, "HQ", TYRANIDS["Hive Tyrant"]),
    slot(4, "HQ", TYRANIDS["Tyranid Prime"]),
    slot(5, "Troops", TYRANIDS["Tyranid Warriors"]),
    slot(6, "Troops", TYRANIDS["Hormagaunts"]),
    slot(7, "Troops", TYRANIDS["Ripper Swarms"]),
    slot(8, "Troops", TYRANIDS["Termagants"]),
    slot(9, "Elites", TYRANIDS["Genestealers"]),
    slot(10, "Elites", TYRANIDS["Hive Guard"]),
    slot(11, "Elites", TYRANIDS["Lictor"]),
    slot(12, "Elites", TYRANIDS["Neurothrope"]),
    slot(13, "Elites", TYRANIDS["Tyrant Guard"]),
    slot(14, "Elites", TYRANIDS["Venomthropes"]),
    slot(15, "Elites", TYRANIDS["Zoanthropes"]),
    slot(16, "Elites", TYRANIDS["Pyrovores"]),
    slot(17, "Elites", TYRANIDS["Haruspex"]),
    slot(18, "Fast", TYRANIDS["Gargoyles"]),
    slot(19, "Fast", TYRANIDS["Raveners"]),
    slot(20, "Fast", TYRANIDS["Spore Mines"]),
    slot(21, "Heavy", TYRANIDS["Biovores"]),
    slot(22, "Heavy", TYRANIDS["Carnifex"]),
    slot(23, "Heavy", TYRANIDS["Exocrine"]),
    slot(24, "Heavy", TYRANIDS["Screamer-Killer"]),
    slot(25, "Heavy", TYRANIDS["Toxicrene"]),
    slot(26, "Heavy", TYRANIDS["Trygon"]),
    slot(27, "Heavy", TYRANIDS["Tyrannofex"]),
    slot(28, "Heavy", TYRANIDS["Mawloc"]),
    slot(29, "Air", TYRANIDS["Harpy"]),
    slot(30, "Air", TYRANIDS["Hive Crone"]),
    slot(31, "Transport", TYRANIDS["Tyrannocyte"]),
    slot(32, "Lord", TYRANIDS["Hierophant"]),
]
