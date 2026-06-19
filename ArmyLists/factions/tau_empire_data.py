from generate_all_faction_lists import slot, u

# ---------------------------------------------------------------------------
# T'au Empire unit datasheets (Apoc_Datasheet_Tau_Empire_web.pdf)
# Slot layout from Apoc40k-Armies-1st - Tau Empire.csv
# ---------------------------------------------------------------------------

_COMMANDER_WEAPONS = [
    {"name": "Airbursting Fragmentation Projector", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "8+", "armorPen": "10+", "abilities": "Barrage"},
    {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
    {"name": "Cyclic Ion Blaster", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
    {"name": "Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
    {"name": "Fusion Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
    {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
    {"name": "Plasma Rifle", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+", "abilities": "Rapid Fire"},
    {"name": "High-output Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "4", "skill": "8+", "armorPen": "9+"},
]

_CRISIS_WEAPONS = [
    {"name": "Airbursting Fragmentation Projector", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "8+", "armorPen": "10+", "abilities": "Barrage"},
    {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
    {"name": "Cyclic Ion Blaster", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
    {"name": "Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
    {"name": "Fusion Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
    {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
    {"name": "Plasma Rifle", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+", "abilities": "Rapid Fire"},
    {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
]

TAU_EMPIRE = {
    "Commander Shadowsun": u(
        "Commander Shadowsun",
        {"M": '8"', "WS": "3+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "11"},
        ["T'au Empire", "T'au Sept", "Light", "Infantry", "Fly", "Battlesuit", "Character", "Commander", "XV22 Stalker", "Jet Pack", "Shadowsun"],
        [
            {"name": "Fusion Blasters", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "10+", "armorPen": "4+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Infiltrators, Stealth, Master of War\n"
        "Genius of Kauyon: Once per battle, at the start of the Action phase, this unit can declare Kauyon even if Kauyon or Mont'ka has already been declared. "
        "Mont'ka and Kauyon cannot be both declared in the same turn.\n"
        'Command-link: If this unit has a Command-link Drone, then after this unit makes a Move action, you can select one friendly T\'au Empire unit within 6" of this unit. '
        "Until the end of the phase, re-roll hit rolls of 1 for attacks made with ranged weapons by that unit.",
        options=[
            "Commander Shadowsun is a unit that contains 1 model. It is equipped with: Fusion Blasters; Close Combat Weapons. You can only include one of this unit in your army.",
            "This unit may have a Command-link Drone (Power Rating +1). If this unit has a Command-link Drone, it has the following additional abilities: Command-link.",
            "This unit may have Shield Drones (Power Rating +1). If this unit has Shield Drones, improve its Save characteristic by 1.",
        ],
    ),
    "Commander Farsight": u(
        "Commander Farsight",
        {"M": '8"', "WS": "2+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "5+", "N": "1", "Pt": "13"},
        ["T'au Empire", "Farsight Enclaves", "Light", "Battlesuit", "Fly", "Character", "Commander", "Jet Pack", "Farsight"],
        [
            {"name": "High-intensity Plasma Rifle", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "6+", "armorPen": "6+", "abilities": "Rapid Fire"},
            {"name": "The Dawn Blade", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "7+"},
        ],
        "Deep Strike, Master of War\n"
        "Genius of Mont'ka: Once per battle, at the start of the Action phase, this unit can declare Mont'ka even if Kauyon or Mont'ka has already been declared. "
        "Mont'ka and Kauyon cannot be both declared in the same turn.\n"
        'Way of the Short Blade: Re-roll hit rolls of 1 made for friendly Farsight Enclave units when using melee weapons whilst they are within 6" of this unit '
        "(and ranged weapons, if the target is an Orks unit).",
        options=[
            "Commander Farsight is a unit that contains 1 model. It is equipped with: High-intensity Plasma Rifle; The Dawn Blade. You can only include one of this unit in your army.",
        ],
    ),
    "Commander": u(
        "Commander",
        {"M": '8"', "WS": "3+", "BS": "2+", "A": "1", "W": "1", "Ld": "7", "Sv": "6+", "N": "1", "Pt": "5"},
        ["T'au Empire", "<Sept>", "Light", "Battlesuit", "Fly", "Character", "XV8 Crisis", "Jet Pack", "Commander"],
        _COMMANDER_WEAPONS + [
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Deep Strike, Master of War\n"
        "Enforcer Battlesuit: At the start of the Damage phase, if this unit has an XV85 Enforcer Battlesuit, you can remove one blast marker from this unit. "
        "Small blast markers must be removed before large blast markers.",
        options=[
            "A Commander is a unit that contains 1 model. It is equipped with: Close Combat Weapons.",
            "This unit must be equipped with two items from the Commander Weapons list.",
            "This unit can also be equipped with two items from the Commander Weapons list.",
            "Commander Weapons list: Add 1 to the Power Rating for each Airbursting Fragmentation Projector, Fusion Blaster and Missile Pod, "
            "and 2 for each Burst Cannon, Cyclic Ion Blaster, Flamer and Plasma Rifle. Cyclic Ion Blaster cannot be taken by a Commander that has an XV86 Coldstar Battlesuit.",
            "This model can have one of the following (Power Rating +1):",
            "- XV8-02 Crisis Iridium Battlesuit. If this unit has an XV8-02 Crisis Iridium Battlesuit, improve its Save characteristic by 1.",
            "- XV85 Enforcer Battlesuit. If this unit has an XV85 Enforcer Battlesuit, it has the following additional abilities: Enforcer Battlesuit; "
            "has the XV85 Enforcer keyword instead of the XV8 Crisis keyword.",
            '- XV86 Coldstar Battlesuit. If this unit has an XV86 Coldstar Battlesuit, it has a Move characteristic of 20"; '
            "is equipped with 1 High-output Burst Cannon instead of one item from the Commander Weapons list; "
            "has the XV86 Coldstar keyword instead of the XV8 Crisis keyword.",
            "This unit can have up to two of the following (Power Rating +1): Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
        ],
    ),
    "Aun'Va": u(
        "Aun'Va",
        {"M": '6"', "WS": "3+", "BS": "3+", "A": "2", "W": "2", "Ld": "7", "Sv": "10+", "N": "3", "Pt": "5"},
        ["T'au Empire", "T'au Sept", "Light", "Infantry", "Character", "Ethereal", "Ethereal Guard", "Aun'Va"],
        [{"name": "Honour Blades", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"}],
        'Failure Is Not an Option: Friendly T\'au Empire units can use this unit\'s Leadership characteristic instead of their own whilst they are within 6" of this unit.\n'
        "Supreme Loyalty: You can re-roll Morale tests taken for T'au Empire units in this unit's Detachment whilst this unit is on the battlefield.\n"
        "Paradox of Duality: Subtract 1 from wound rolls for attacks that target this unit.",
        options=["Aun'Va is a unit that contains 3 models. It is equipped with: Honour Blades. You can only include one of this unit in your army."],
    ),
    "Ethereal": u(
        "Ethereal",
        {"M": '6"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "7", "Sv": "10+", "N": "1", "Pt": "2"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Character", "Ethereal"],
        [
            {"name": "Honour Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        'Failure Is Not an Option: Friendly T\'au Empire units can use this unit\'s Leadership characteristic instead of their own whilst they are within 6" of this unit.',
        options=[
            "An Ethereal is a unit that contains 1 model. It is equipped with: Honour Blade.",
            "This unit can have up to two of the following (Power Rating +1): Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Gun Drone, it is also equipped with 1 Pulse Carbine.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
            "This unit can have a Hover Drone (Power Rating +1). If this unit has a Hover Drone, it has a Move characteristic of 8\" and gains the following additional keywords: Jet Pack, Fly.",
        ],
    ),
    "Strike Team": u(
        "Strike Team",
        {"M": '6"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Strike Team"],
        [
            {"name": "Pulse Rifles", "type": "Small Arms", "range": '30"', "attacks": "User", "skill": "6+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        profiles=[
            {"M": '6"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "6"},
            {"M": '6"', "WS": "5+", "BS": "4+", "A": "3", "W": "2", "Ld": "5", "Sv": "8+", "N": "12", "Pt": "7"},
        ],
        options=[
            "A Strike Team is a unit that contains 5 models. It can contain 10 models (Power Rating 6) or 12 models (Power Rating 7). "
            "It is equipped with: Pulse Rifles; Close Combat Weapons.",
            "This unit can have up to two of the following (Power Rating +1): Guardian Drone, Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Guardian Drone, this unit has the following abilities: Ignore Damage (6+).",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
        ],
    ),
    "Breacher Team": u(
        "Breacher Team",
        {"M": '6"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Breacher Team"],
        [
            {"name": "Pulse Blasters", "type": "Small Arms", "range": '15"', "attacks": "x2", "skill": "5+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        profiles=[{"M": '6"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "6"}],
        options=[
            "A Breacher Team is a unit that contains 5 models. It can contain 10 models (Power Rating 6). It is equipped with: Pulse Blasters; Close Combat Weapons.",
            "This unit can have up to two of the following (Power Rating +1): Guardian Drone, Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Guardian Drone, this unit has the following abilities: Ignore Damage (6+).",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
        ],
    ),
    "Kroot Carnivores": u(
        "Kroot Carnivores",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "10+", "N": "10", "Pt": "4"},
        ["T'au Empire", "Kroot", "Light", "Infantry", "Kroot Carnivores"],
        [
            {"name": "Kroot Rifles (Ranged)", "type": "Small Arms", "range": '24"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Rapid Fire"},
            {"name": "Kroot Rifles (Melee)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        "Infiltrators",
        profiles=[{"M": '7"', "WS": "3+", "BS": "4+", "A": "2", "W": "4", "Ld": "4", "Sv": "10+", "N": "20", "Pt": "7"}],
        options=[
            "Kroot Carnivores are a unit that contains 10 models. It can contain 20 models (Power Rating 7). "
            "It is equipped with: Kroot Rifles (Ranged); Kroot Rifles (Melee).",
        ],
    ),
    "XV25 Stealth Battlesuits": u(
        "XV25 Stealth Battlesuits",
        {"M": '8"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "6+", "N": "3", "Pt": "6"},
        ["T'au Empire", "<Sept>", "Light", "Battlesuit", "Fly", "Infantry", "Jet Pack", "XV25 Stealth Battlesuits"],
        [
            {"name": "Burst Cannons", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "8+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Infiltrators, Stealth",
        profiles=[{"M": '8"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "6+", "N": "6", "Pt": "10"}],
        options=[
            "XV25 Stealth Battlesuits are a unit that contains 3 models. It can contain 6 models (Power Rating 10). "
            "It is equipped with: Burst Cannons; Close Combat Weapons.",
            "This unit can have up to two of the following (Power Rating +1): Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
        ],
    ),
    "XV8 Crisis Battlesuits": u(
        "XV8 Crisis Battlesuits",
        {"M": '8"', "WS": "5+", "BS": "4+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "3", "Pt": "7"},
        ["T'au Empire", "<Sept>", "Light", "Battlesuit", "Fly", "Jet Pack", "XV8 Crisis Battlesuits"],
        _CRISIS_WEAPONS,
        "Deep Strike",
        profiles=[
            {"M": '8"', "WS": "5+", "BS": "4+", "A": "2", "W": "4", "Ld": "6", "Sv": "6+", "N": "6", "Pt": "13"},
            {"M": '8"', "WS": "5+", "BS": "4+", "A": "3", "W": "6", "Ld": "6", "Sv": "6+", "N": "9", "Pt": "19"},
        ],
        options=[
            "XV8 Crisis Battlesuits are a unit that contains 3 models. It can contain 6 models (Power Rating 13) or 9 models (Power Rating 19). "
            "It is equipped with: Close Combat Weapons.",
            "For each 3 models this unit contains, it must be equipped with one of the following (Power Rating +1 per Burst Cannon, Cyclic Ion Blaster, Flamer and Plasma Rifle): "
            "3 Airbursting Fragmentation Projectors; 3 Burst Cannons; 3 Cyclic Ion Blasters; 3 Flamers; 3 Fusion Blasters; 3 Missile Pods; 3 Plasma Rifles.",
            "This unit can have up to two of the following (Power Rating +1 for each 3 models this unit contains): Gun Drones, Marker Drones, Shield Drones.",
            "- If this unit has Gun Drones, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Marker Drones, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Shield Drones, improve its Save characteristic by 1.",
        ],
    ),
    "XV8 Crisis Bodyguards": u(
        "XV8 Crisis Bodyguards",
        {"M": '8"', "WS": "5+", "BS": "4+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "3", "Pt": "8"},
        ["T'au Empire", "<Sept>", "Light", "Battlesuit", "Fly", "Jet Pack", "XV8 Crisis Bodyguards"],
        [
            {"name": "Airbursting Fragmentation Projector", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "8+", "armorPen": "10+", "abilities": "Barrage"},
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Cyclic Ion Blaster", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "8+"},
            {"name": "Flamer", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Fusion Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "11+", "armorPen": "4+"},
            {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Plasma Rifle", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Deep Strike\n"
        'Sworn Protectors: At the start of the Damage phase, you can select one friendly <Sept> Character unit that has at least one blast marker next to it and is within 6" of this unit. '
        "Remove up to D3 blast markers from that Character unit and place them next to this unit.",
        profiles=[
            {"M": '8"', "WS": "5+", "BS": "4+", "A": "2", "W": "4", "Ld": "6", "Sv": "6+", "N": "6", "Pt": "15"},
            {"M": '8"', "WS": "5+", "BS": "4+", "A": "3", "W": "6", "Ld": "6", "Sv": "6+", "N": "9", "Pt": "22"},
        ],
        options=[
            "XV8 Crisis Bodyguards are a unit that contains 3 models. It can contain 6 models (Power Rating 15) or 9 models (Power Rating 22). "
            "It is equipped with: Close Combat Weapons.",
            "For each 3 models this unit contains, it must be equipped with one of the following (Power Rating +1 per Burst Cannon, Cyclic Ion Blaster, Flamer and Plasma Rifle): "
            "3 Airbursting Fragmentation Projectors; 3 Burst Cannons; 3 Cyclic Ion Blasters; 3 Flamers; 3 Fusion Blasters; 3 Missile Pods; 3 Plasma Rifles.",
            "This unit can have up to two of the following (Power Rating +1 for each 3 models this unit contains): Gun Drones, Marker Drones, Shield Drones.",
            "- If this unit has Gun Drones, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Marker Drones, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Shield Drones, improve its Save characteristic by 1.",
        ],
    ),
    "Pathfinder Team": u(
        "Pathfinder Team",
        {"M": '7"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "5"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Pathfinder Team"],
        [
            {"name": "Ion Rifle", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "6+", "armorPen": "8+", "abilities": "Supercharge"},
            {"name": "Pulse Carbines", "type": "Heavy", "range": '18"', "attacks": "x2", "skill": "6+", "armorPen": "8+"},
            {"name": "Rail Rifle", "type": "Heavy", "range": '30"', "attacks": "1", "skill": "8+", "armorPen": "6+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Infiltrators",
        profiles=[{"M": '7"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "9"}],
        options=[
            "A Pathfinder Team is a unit that contains 5 models. It can contain 10 models (Power Rating 9). It is equipped with: Pulse Carbines; Close Combat Weapons.",
            "This unit can also be equipped with up to three of the following in any combination (Power Rating +1 per weapon): 1 Ion Rifle; 1 Rail Rifle.",
            "This unit can have up to two of the following (Power Rating +1): Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
            "This unit can have a Recon Drone (Power Rating +1). If this unit has a Recon Drone, it does not suffer the penalty for attacks made with ranged weapons that target obscured targets.",
            "This unit can take up to two of the following (Power Rating +1): Grav-inhibitor Drone, Pulse Accelerator Drone.",
            "- If an enemy unit starts a Move action within 3\" of any units accompanied by a Grav-inhibitor Drone, reduce its Movement characteristic by 2\" until that Move action is completed.",
            "- If this unit has a Pulse Accelerator Drone, add 6\" to the range of its Pulse carbines.",
        ],
    ),
    "Firesight Marksman": u(
        "Firesight Marksman",
        {"M": '5"', "WS": "5+", "BS": "3+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Character", "Firesight Marksman"],
        [{"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"}],
        "Stealth\n"
        'Drone Uplink: Add 1 to hit rolls for attacks made with ranged weapons by <Sept> MV71 Sniper Drones whilst they are within 6" of any friendly units with this ability.',
        options=["A Firesight Marksman is a unit that contains 1 model. It is equipped with: Close Combat Weapons."],
    ),
    "Darkstrider": u(
        "Darkstrider",
        {"M": '7"', "WS": "3+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "5"},
        ["T'au Empire", "T'au Sept", "Light", "Infantry", "Character", "Darkstrider"],
        [
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Infiltrators\n"
        'Structural Analyser: Once per turn, after this unit makes a Shoot action, you can select one friendly Light T\'au Sept unit within 6" of this unit. '
        "Add 1 to wound rolls for attacks made with ranged weapons by that unit that target a unit targeted by this unit this turn.",
        options=[
            "Darkstrider is a unit that contains 1 model. It is equipped with: Pulse Carbine; Close Combat Weapons. You can only include one of this unit in your army.",
        ],
    ),
    "Cadre Fireblade": u(
        "Cadre Fireblade",
        {"M": '6"', "WS": "3+", "BS": "2+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "4"},
        ["T'au Empire", "<Sept>", "Light", "Infantry", "Character", "Cadre Fireblade"],
        [
            {"name": "Pulse Rifle", "type": "Small Arms", "range": '30"', "attacks": "User", "skill": "9+", "armorPen": "10+", "abilities": "Rapid Fire"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        'Volley Fire: Add 1 to the Attacks characteristic of <Sept> units within 6" of any friendly <Sept> Cadre Fireblades whilst they are making attacks with Pulse Carbines and Pulse Rifles '
        "that target a unit within half range of the weapon being used for that attack.",
        options=[
            "A Cadre Fireblade is a unit that contains 1 model. It is equipped with: Pulse Rifle; Close Combat Weapons.",
            "This unit can have up to two of the following (Power Rating +1): Gun Drone, Marker Drone, Shield Drone.",
            "- If this unit has a Gun Drone, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Marker Drone, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has a Shield Drone, improve its Save characteristic by 1.",
        ],
    ),
    "Kroot Shaper": u(
        "Kroot Shaper",
        {"M": '7"', "WS": "3+", "BS": "4+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "1", "Pt": "3"},
        ["T'au Empire", "Kroot", "Light", "Infantry", "Character", "Kroot Shaper"],
        [{"name": "Ritual Blade", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"}],
        'Wisest of their Kind: Friendly Kroot units can use this unit\'s Leadership characteristic instead of their own whilst they are within 6" of this unit.\n'
        'The Shaper Commands: Re-roll wound rolls of 1 for attacks made by friendly Kroot units whilst they are within 6" of this unit.',
        options=["A Kroot Shaper is a unit that contains 1 model. It is equipped with: Ritual Blade."],
    ),
    "TX4 Piranhas": u(
        "TX4 Piranhas",
        {"M": '16"', "WS": "6+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Heavy", "Vehicle", "Fly", "TX4 Piranhas"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Fusion Blaster", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "10+", "armorPen": "4+"},
            {"name": "Pulse Carbines", "type": "Heavy", "range": '18"', "attacks": "x2", "skill": "6+", "armorPen": "8+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        profiles=[
            {"M": '16"', "WS": "6+", "BS": "4+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "9"},
            {"M": '16"', "WS": "6+", "BS": "4+", "A": "5", "W": "5", "Ld": "4", "Sv": "8+", "N": "5", "Pt": "15"},
        ],
        options=[
            "TX4 Piranhas are a unit that contains 1 model. It can contain 3 models (Power Rating 9) or 5 models (Power Rating 15). "
            "It is equipped with: Pulse Carbines; Close Combat Weapons.",
            "For each model this unit contains, it must be equipped with one of the following: 1 Fusion Blaster; 1 Burst Cannon.",
        ],
    ),
    "Vespid Stingwings": u(
        "Vespid Stingwings",
        {"M": '14"', "WS": "4+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "8+", "N": "4", "Pt": "5"},
        ["T'au Empire", "Vespid", "Light", "Infantry", "Fly", "Vespid Stingwings"],
        [
            {"name": "Neutron Blasters", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "6+", "armorPen": "6+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[
            {"M": '14"', "WS": "4+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "8+", "N": "8", "Pt": "11"},
            {"M": '14"', "WS": "4+", "BS": "4+", "A": "3", "W": "3", "Ld": "6", "Sv": "8+", "N": "12", "Pt": "16"},
        ],
        options=[
            "Vespid Stingwings are a unit that contains 4 models. It can contain 8 models (Power Rating 11) or 12 models (Power Rating 16). "
            "It is equipped with: Neutron Blasters; Close Combat Weapons.",
        ],
    ),
    "Kroot Hounds": u(
        "Kroot Hounds",
        {"M": '12"', "WS": "3+", "BS": "-", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "4", "Pt": "2"},
        ["T'au Empire", "Kroot", "Light", "Beasts", "Kroot Hounds"],
        [{"name": "Ripping Fangs", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"}],
        "Voracious Predators: Add 1 to wound rolls for attacks made by this unit that target units that are not Vehicles and have any damage markers next to them.",
        profiles=[
            {"M": '12"', "WS": "3+", "BS": "-", "A": "2", "W": "2", "Ld": "4", "Sv": "10+", "N": "8", "Pt": "4"},
            {"M": '12"', "WS": "3+", "BS": "-", "A": "3", "W": "3", "Ld": "4", "Sv": "10+", "N": "12", "Pt": "6"},
        ],
        options=[
            "Kroot Hounds are a unit that contains 4 models. It can contain 8 models (Power Rating 4) or 12 models (Power Rating 6). "
            "It is equipped with: Ripping Fangs.",
        ],
    ),
    "Tactical Drones": u(
        "Tactical Drones",
        {"M": '8"', "WS": "5+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "4", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Light", "Drone", "Fly", "Tactical Drones"],
        [
            {"name": "Pulse Carbines", "type": "Heavy", "range": '18"', "attacks": "x2", "skill": "6+", "armorPen": "8+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Deep Strike\n"
        "Threat Identification Protocols: This unit must target the closest enemy unit when it makes a Shoot action. "
        "If more than one unit is equally close, select one of those units to target.",
        profiles=[
            {"M": '8"', "WS": "5+", "BS": "5+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "8", "Pt": "5"},
            {"M": '8"', "WS": "5+", "BS": "5+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "12", "Pt": "7"},
        ],
        options=[
            "Tactical Drones are a unit that contains 4 models. It can contain 8 models (Power Rating 5) or 12 models (Power Rating 7). "
            "It is equipped with: Pulse Carbines; Close Combat Weapons.",
            "This unit can have up to two of the following (Power Rating +1 for each 4 models this unit contains): Gun Drones, Marker Drones, Shield Drones.",
            "- If this unit has Gun Drones, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Marker Drones, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Shield Drones, improve its Save characteristic by 1.",
        ],
    ),
    "XV88 Broadside Battlesuits": u(
        "XV88 Broadside Battlesuits",
        {"M": '5"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "6"},
        ["T'au Empire", "<Sept>", "Light", "Battlesuit", "XV88 Broadside Battlesuits"],
        [
            {"name": "Heavy Rail Rifle", "type": "Heavy", "range": '60"', "attacks": "1", "skill": "9+", "armorPen": "5+"},
            {"name": "High-yield Missile Pod", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Plasma Rifles", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "7+", "armorPen": "7+", "abilities": "Rapid Fire"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        profiles=[
            {"M": '5"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "6", "Sv": "5+", "N": "2", "Pt": "11"},
            {"M": '5"', "WS": "5+", "BS": "4+", "A": "3", "W": "3", "Ld": "6", "Sv": "5+", "N": "3", "Pt": "16"},
        ],
        options=[
            "XV88 Broadside Battlesuits are a unit that contains 1 model. It can contain 2 models (Power Rating 11) or 3 models (Power Rating 16). "
            "It is equipped with: Close Combat Weapons.",
            "For each model this unit contains, it must be equipped with one of the following: 1 Heavy Rail Rifle; 2 High-yield Missile Pods (Power Rating +1).",
            "For each model this unit contains, it must be equipped with one of the following: Smart Missile Systems; Plasma Rifles.",
            "This unit can have up to two of the following (Power Rating +1 for each model this unit contains): Gun Drones, Marker Drones, Shield Drones.",
            "- If this unit has Gun Drones, re-roll wound rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Marker Drones, re-roll hit rolls of 1 for attacks made with ranged weapons by this unit.",
            "- If this unit has Shield Drones, improve its Save characteristic by 1.",
            "For each model this unit contains, it can have up to two Missile Drones (Power Rating +1 per drone). "
            "For each Missile Drone this unit has, it is also equipped with 1 Missile Pod.",
        ],
    ),
    "TX7 Hammerhead Gunship": u(
        "TX7 Hammerhead Gunship",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "10"},
        ["T'au Empire", "<Sept>", "Heavy", "Vehicle", "Fly", "TX7 Hammerhead Gunship"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Ion Cannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
            {"name": "Railgun", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.",
        options=[
            "A TX7 Hammerhead Gunship is a unit that contains 1 model. It is equipped with: Railgun; 2 Pulse Carbines; Armoured Hull.",
            "Instead of 1 Railgun, this unit can be equipped with 1 Ion Cannon.",
            "Instead of 2 Pulse Carbines, this unit can be equipped with one of the following (Power Rating +1): 2 Burst Cannons; Smart Missile Systems.",
        ],
    ),
    "TX78 Sky Ray Gunship": u(
        "TX78 Sky Ray Gunship",
        {"M": '12"', "WS": "6+", "BS": "3+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "9"},
        ["T'au Empire", "<Sept>", "Heavy", "Vehicle", "Fly", "TX78 Sky Ray Gunship"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
            {"name": "Seeker Missiles", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "8+", "armorPen": "6+", "abilities": "Barrage"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.\n"
        "Velocity Tracker: Add 2 to hit rolls for attacks made with ranged weapons by this unit that target Aircraft units.",
        options=[
            "A TX78 Sky Ray Gunship is a unit that contains 1 model. It is equipped with: Seeker Missiles; 2 Pulse Carbines; Armoured Hull.",
            "Instead of 2 Pulse Carbines, this unit can be equipped with one of the following (Power Rating +1): 2 Burst Cannons; Smart Missile Systems.",
        ],
    ),
    "XV95 Ghostkeel Battlesuit": u(
        "XV95 Ghostkeel Battlesuit",
        {"M": '12"', "WS": "5+", "BS": "4+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "12"},
        ["T'au Empire", "<Sept>", "Heavy", "Battlesuit", "Fly", "Monster", "Jet Pack", "XV95 Ghostkeel Battlesuit"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Cyclic Ion Raker", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "8+", "armorPen": "8+", "abilities": "Supercharge"},
            {"name": "Flamers", "type": "Heavy", "range": '8"', "attacks": "2", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Fusion Blasters", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "10+", "armorPen": "4+"},
            {"name": "Fusion Collider", "type": "Heavy", "range": '18"', "attacks": "1", "skill": "8+", "armorPen": "3+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "10+"},
        ],
        "Infiltrators, Stealth",
        options=[
            "An XV95 Ghostkeel Battlesuit is a unit that contains 1 model. It is equipped with: Flamers; Fusion Collider; Close Combat Weapons.",
            "Instead of 1 Fusion Collider, this unit can be equipped with 1 Cyclic Ion Raker.",
            "Instead of Flamers, this unit can be equipped with one of the following: 2 Burst Cannons; Fusion Blasters.",
        ],
    ),
    "XV104 Riptide Battlesuit": u(
        "XV104 Riptide Battlesuit",
        {"M": '12"', "WS": "5+", "BS": "4+", "A": "2", "W": "3", "Ld": "6", "Sv": "4+", "N": "1", "Pt": "13"},
        ["T'au Empire", "<Sept>", "Heavy", "Battlesuit", "Fly", "Monster", "Jet Pack", "XV104 Riptide Battlesuit"],
        [
            {"name": "Fusion Blasters", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "10+", "armorPen": "4+"},
            {"name": "Heavy Burst Cannon", "type": "Heavy", "range": '36"', "attacks": "6", "skill": "7+", "armorPen": "8+"},
            {"name": "Ion Accelerator", "type": "Heavy", "range": '72"', "attacks": "4", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
            {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Plasma Rifles", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "7+", "armorPen": "7+", "abilities": "Rapid Fire"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        options=[
            "An XV104 Riptide Battlesuit is a unit that contains 1 model. It is equipped with: Heavy Burst Cannon; Smart Missile Systems; Close Combat Weapons.",
            "Instead of Smart Missile Systems, this unit can be equipped with one of the following: Fusion Blasters; Plasma Rifles.",
            "Instead of 1 Heavy Burst Cannon, this unit can be equipped with 1 Ion Accelerator.",
            "This unit can have up to two Shielded Missile Drones (Power Rating +1 per drone). "
            "For each Shielded Missile Drone this unit has, it is also equipped with 1 Missile Pod.",
        ],
    ),
    "MV71 Sniper Drones": u(
        "MV71 Sniper Drones",
        {"M": '8"', "WS": "5+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "3"},
        ["T'au Empire", "<Sept>", "Light", "Drone", "Fly", "MV71 Sniper Drones"],
        [
            {"name": "Longshot Pulse Rifles", "type": "Small Arms", "range": '48"', "attacks": "User", "skill": "6+", "armorPen": "8+", "abilities": "Sniper"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Stealth",
        profiles=[
            {"M": '8"', "WS": "5+", "BS": "5+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "6", "Pt": "5"},
            {"M": '8"', "WS": "5+", "BS": "5+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "9", "Pt": "7"},
        ],
        options=[
            "MV71 Sniper Drones are a unit that contains 3 models. It can contain 6 models (Power Rating 5) or 9 models (Power Rating 7). "
            "It is equipped with: Longshot Pulse Rifles; Close Combat Weapons.",
        ],
    ),
    "Longstrike": u(
        "Longstrike",
        {"M": '12"', "WS": "6+", "BS": "2+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "12"},
        ["T'au Empire", "T'au Sept", "Heavy", "Vehicle", "Fly", "Character", "TX7 Hammerhead Gunship", "Longstrike"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Ion Cannon", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Supercharge"},
            {"name": "Railgun", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Tank Ace: Add 1 to wound rolls for attacks made by this unit with ranged weapons that target Heavy or Super-heavy units.\n"
        'Fire Caste Exemplar: Add 1 to hit rolls for attacks made with ranged weapons by friendly T\'au Sept TX7 Hammerhead Gunship units whilst they are within 6" of this unit.\n'
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.",
        options=[
            "Longstrike is a unit that contains 1 model. It is equipped with: 2 Pulse Carbines; Railgun; Armoured Hull. You can only include one of this unit in your army.",
            "Instead of 1 Railgun, this unit can be equipped with 1 Ion Cannon.",
            "Instead of 2 Pulse Carbines, this unit can be equipped with one of the following: 2 Burst Cannons; Smart Missile Systems.",
        ],
    ),
    "KV128 Stormsurge": u(
        "KV128 Stormsurge",
        {"M": '6"', "WS": "5+", "BS": "4+", "A": "1", "W": "5", "Ld": "6", "Sv": "5+", "N": "1", "Pt": "20"},
        ["T'au Empire", "<Sept>", "Super-heavy", "Titanic", "Vehicle", "KV128 Stormsurge"],
        [
            {"name": "Airbursting Fragmentation Launchers", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "10+", "abilities": "Barrage"},
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Cluster Rocket System", "type": "Heavy", "range": '48"', "attacks": "8", "skill": "8+", "armorPen": "10+"},
            {"name": "Destroyer Missile", "type": "Heavy", "range": '60"', "attacks": "1", "skill": "5+", "armorPen": "5+", "abilities": "Destroyer, One Use Only"},
            {"name": "Flamers", "type": "Heavy", "range": '8"', "attacks": "2", "skill": "7+", "armorPen": "10+", "abilities": "Inferno"},
            {"name": "Pulse Blastcannon", "type": "Heavy", "range": '30"', "attacks": "4", "skill": "6+", "armorPen": "5+"},
            {"name": "Pulse Driver Cannon", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Crushing Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "9+"},
        ],
        "Stabilising Anchors: Re-roll hit rolls of 1 for attacks made with ranged weapons by this unit if it did not make a Move action this turn.",
        options=[
            "A KV128 Stormsurge is a unit that contains 1 model. It is equipped with: Cluster Rocket System; 4 Destroyer Missiles; Flamers; Pulse Blastcannon; Smart Missile Systems; Crushing Feet.",
            "Instead of Flamers, this unit can be equipped with one of the following: Airbursting Fragmentation Projectors; 2 Burst Cannons.",
            "Instead of 1 Pulse Blastcannon, this unit can be equipped with 1 Pulse Driver Cannon.",
        ],
    ),
    "TY7 Devilfish": u(
        "TY7 Devilfish",
        {"M": '12"', "WS": "6+", "BS": "4+", "A": "1", "W": "2", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "7"},
        ["T'au Empire", "<Sept>", "Heavy", "Vehicle", "Fly", "Transport", "TY7 Devilfish"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Pulse Carbine", "type": "Small Arms", "range": '18"', "attacks": "User", "skill": "9+", "armorPen": "9+"},
            {"name": "Smart Missile Systems", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Hover: Distances are measured to and from this unit's hull, even though it has a base.\n"
        "TRANSPORT: This unit can transport up to 12 <Sept> Infantry or Drone models. It cannot transport Battlesuits.",
        options=[
            "A TY7 Devilfish is a unit that contains 1 model. It is equipped with: Burst Cannon; 2 Pulse Carbines; Armoured Hull.",
            "Instead of 2 Pulse Carbines, this unit can be equipped with Smart Missile Systems.",
        ],
    ),
    "AX3 Razorshark Strike Fighter": u(
        "AX3 Razorshark Strike Fighter",
        {"M": '20-50"', "WS": "6+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "11"},
        ["T'au Empire", "<Sept>", "Heavy", "Aircraft", "Vehicle", "Fly", "AX3 Razorshark Strike Fighter"],
        [
            {"name": "Burst Cannon", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "8+", "armorPen": "9+"},
            {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Quad Ion Turret", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "7+", "armorPen": "7+", "abilities": "Supercharge"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Supersonic",
        options=[
            "An AX3 Razorshark Strike Fighter is a unit that contains 1 model. It is equipped with: Burst Cannon; Quad Ion Turret; Armoured Hull.",
            "Instead of 1 Burst Cannon, this unit can be equipped with 1 Missile Pod.",
        ],
    ),
    "AX39 Sun Shark Bomber": u(
        "AX39 Sun Shark Bomber",
        {"M": '20-50"', "WS": "6+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "7+", "N": "1", "Pt": "10"},
        ["T'au Empire", "<Sept>", "Heavy", "Aircraft", "Vehicle", "Fly", "AX39 Sun Shark Bomber"],
        [
            {"name": "Ion Rifles", "type": "Heavy", "range": '30"', "attacks": "2", "skill": "6+", "armorPen": "8+", "abilities": "Supercharge"},
            {"name": "Missile Pod", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Armoured Hull", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Supersonic\n"
        "Bombing Run: When this unit finishes making a Move action, select one enemy unit it moved over whilst making that Move action. "
        "Roll three D6, subtracting 1 from each result if that unit is a Character and adding 1 to each result if that unit is Infantry; "
        "for each result of 4+ place one blast marker next to that unit.",
        options=[
            "An AX39 Sun Shark Bomber is a unit that contains 1 model. It is equipped with: Ion Rifles; Missile Pod; Armoured Hull.",
            "This unit can also be equipped with 1 Missile Pod (Power Rating +1).",
        ],
    ),
    "Tidewall Gunrig": u(
        "Tidewall Gunrig",
        {"M": '6"', "WS": "-", "BS": "5+", "A": "-", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "6"},
        ["T'au Empire", "<Sept>", "Building", "Vehicle", "Transport", "Tidewall Gunrig"],
        [{"name": "Supremacy Railgun", "type": "Heavy", "range": '72"', "attacks": "1", "skill": "8+", "armorPen": "4+", "abilities": "Destroyer"}],
        "Open-topped\n"
        "Automated Fire Control Systems: This unit will always target the closest enemy unit with its Supremacy Railgun unless a friendly <Sept> unit is embarked aboard it. "
        "If two enemy units are equally close, you can choose which one this unit targets.\n"
        "Mobile Defence Platform: This unit can only make a Move action if any models are embarked aboard it.\n"
        "TRANSPORT: This unit can transport up to 10 T'au Empire Infantry models.",
        options=["A Tidewall Gunrig is a unit that contains 1 model. It is equipped with: Supremacy Railgun."],
    ),
}

TAU_EMPIRE_SLOTS = [
    slot(1, "HQ", TAU_EMPIRE["Commander Shadowsun"]),
    slot(2, "HQ", TAU_EMPIRE["Commander Farsight"]),
    slot(3, "HQ", TAU_EMPIRE["Commander"]),
    slot(4, "Lord", TAU_EMPIRE["Aun'Va"]),
    slot(5, "HQ", TAU_EMPIRE["Ethereal"]),
    slot(6, "Troops", TAU_EMPIRE["Strike Team"]),
    slot(7, "Troops", TAU_EMPIRE["Breacher Team"]),
    slot(8, "Troops", TAU_EMPIRE["Kroot Carnivores"]),
    slot(9, "Elites", TAU_EMPIRE["XV25 Stealth Battlesuits"]),
    slot(10, "Elites", TAU_EMPIRE["XV8 Crisis Battlesuits"]),
    slot(11, "Elites", TAU_EMPIRE["XV8 Crisis Bodyguards"]),
    slot(12, "Elites", TAU_EMPIRE["Pathfinder Team"]),
    slot(13, "Elites", TAU_EMPIRE["Firesight Marksman"]),
    slot(14, "Elites", TAU_EMPIRE["Darkstrider"]),
    slot(15, "Elites", TAU_EMPIRE["Cadre Fireblade"]),
    slot(16, "Elites", TAU_EMPIRE["Kroot Shaper"]),
    slot(17, "Fast", TAU_EMPIRE["TX4 Piranhas"]),
    slot(18, "Fast", TAU_EMPIRE["Vespid Stingwings"]),
    slot(19, "Fast", TAU_EMPIRE["Kroot Hounds"]),
    slot(20, "Fast", TAU_EMPIRE["Tactical Drones"]),
    slot(21, "Heavy", TAU_EMPIRE["XV88 Broadside Battlesuits"]),
    slot(22, "Heavy", TAU_EMPIRE["TX7 Hammerhead Gunship"]),
    slot(23, "Heavy", TAU_EMPIRE["TX78 Sky Ray Gunship"]),
    slot(24, "Heavy", TAU_EMPIRE["XV95 Ghostkeel Battlesuit"]),
    slot(25, "Heavy", TAU_EMPIRE["XV104 Riptide Battlesuit"]),
    slot(26, "Heavy", TAU_EMPIRE["MV71 Sniper Drones"]),
    slot(27, "Heavy", TAU_EMPIRE["Longstrike"]),
    slot(28, "Lord", TAU_EMPIRE["KV128 Stormsurge"]),
    slot(29, "Transport", TAU_EMPIRE["TY7 Devilfish"]),
    slot(30, "Air", TAU_EMPIRE["AX3 Razorshark Strike Fighter"]),
    slot(31, "Air", TAU_EMPIRE["AX39 Sun Shark Bomber"]),
    slot(32, "Lord", TAU_EMPIRE["Tidewall Gunrig"]),
]
