from generate_all_faction_lists import slot, u

# ---------------------------------------------------------------------------
# Orks unit datasheets (Apoc_Datasheet_Orks_web.pdf)
# Slot layout from Apoc40k-Armies-1st - Orks.csv
# ---------------------------------------------------------------------------

ORKS = {
    "Gazzghkull Thraka": u(
        "Gazzghkull Thraka",
        {"M": '5"', "WS": "2+", "BS": "5+", "A": "2", "W": "2", "Ld": "6", "Sv": "3+", "N": "1", "Pt": "10"},
        ["Orks", "Goff", "Heavy", "Infantry", "Character", "Mega Armour", "Warboss", "Ghazghkull Thraka"],
        [
            {"name": "Twin Big Shoota", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Kustom Klaw", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "5+", "armorPen": "5+"},
        ],
        'Great Waaagh!: Add 1 to the Attacks characteristic of friendly Orks Light units whilst they are making Fight actions whilst within 6" of this unit.\n'
        'Waaagh!: Re-roll hit rolls of 1 for attacks made with melee weapons by friendly Goff units whilst they are within 6" of this unit.',
        options=["Ghazghkull Thraka is a unit that contains 1 model. It is equipped with: Kustom Klaw; Twin Big Shoota. You can only include one of this unit in your army."],
    ),
    "Warboss": u(
        "Warboss",
        {"M": '5"', "WS": "2+", "BS": "5+", "A": "2", "W": "1", "Ld": "6", "Sv": "8+", "N": "1", "Pt": "3"},
        ["Orks", "<Clan>", "Light", "Infantry", "Character", "Warboss"],
        [{"name": "Boss Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "6+"}],
        'Waaagh!: Re-roll hit rolls of 1 for attacks made with melee weapons by friendly <Clan> units whilst they are within 6" of this unit.',
        options=["A Warboss is a unit that contains 1 model. It is equipped with: Boss Weapons."],
    ),
    "Big Mek": u(
        "Big Mek",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "5"},
        ["Orks", "<Clan>", "Light", "Infantry", "Character", "Big Mek"],
        [
            {"name": "Shokk Attack Gun", "type": "Heavy", "range": '60"', "attacks": "2", "skill": "6+", "armorPen": "6+", "abilities": "Destroyer"},
            {"name": "Tellyport Blasta", "type": "Heavy", "range": '12"', "attacks": "1", "skill": "9+", "armorPen": "9+", "abilities": "Destroyer"},
            {"name": "Mek Mega Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
            {"name": "Mek Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        "Big Mekaniak: At the end of the Action phase, this unit can attempt to repair one friendly <Clan> Vehicle unit in base contact with it. "
        "If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.\n"
        "Kustom Force Field: Subtract 1 from wound rolls for attacks made by ranged weapons that target <Clan> units whilst they are wholly within 9\" "
        "of any friendly <Clan> units with a Kustom Force Field.",
        options=[
            "A Big Mek is a unit that contains 1 model. It is equipped with: Shokk Attack Gun; Mek Weapons.",
            "This unit can have Mega Armour. If this unit has Mega Armour, it:",
            "- Is equipped with Mek Mega Weapons instead of 1 Shokk Attack Gun and Mek Weapons.",
            '- Has a Move characteristic of 4", and Save characteristic of 4+.',
            "- Has the following keyword: Mega Armour.",
            "- Can be equipped with a Tellyport Blasta (Power Rating +1) or can also have a Kustom Force Field (Power Rating +1). "
            "If this unit has a Kustom Force Field it has the following additional abilities: Kustom Force Field.",
        ],
    ),
    "Weirdboy": u(
        "Weirdboy",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "1", "Pt": "2"},
        ["Orks", "<Clan>", "Light", "Infantry", "Psyker", "Character", "Weirdboy"],
        [{"name": "Weirdboy Staff", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"}],
        'Waaagh! Energy: At the start of the Action phase, if this unit is within 6" of three or more friendly <Clan> units that each contain at least 10 models, '
        "you can turn over the top 3 cards of your Command Asset deck. If you reveal any Command Asset cards that are psychic powers, you can select one of "
        "those psychic powers and put in into your hand. Then put the remaining cards back in your Command Asset deck and shuffle the deck.",
        options=["A Weirdboy is a unit that contains 1 model. It is equipped with: Weirdboy Staff."],
    ),
    "Deffkilla Wartrike": u(
        "Deffkilla Wartrike",
        {"M": '14"', "WS": "2+", "BS": "5+", "A": "2", "W": "2", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "6"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Character", "Speed Freeks", "Speedboss", "Deffkilla Wartrike"],
        [
            {"name": "Killa Jet", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "6+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Snagga Klaw", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"},
        ],
        'Speedwaaagh!: If a <Clan> Speed Freeks unit starts a Move action within 6" of any friendly units with this ability, add 3" to that unit\'s Move characteristic whilst making that Move action.',
        options=["A Deffkilla Wartrike is a unit that contains 1 model. It is equipped with: Killa Jet; Snagga Klaw."],
    ),
    "Boyz": u(
        "Boyz",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "4"},
        ["Orks", "<Clan>", "Light", "Infantry", "Boyz"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Shootas", "type": "Small Arms", "range": '18"', "attacks": "x4", "skill": "7+", "armorPen": "9+"},
            {"name": "Sluggas", "type": "Small Arms", "range": '12"', "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Choppas", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "7+", "armorPen": "9+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "2", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "8"},
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "4", "W": "6", "Ld": "7", "Sv": "10+", "N": "30", "Pt": "13"},
        ],
        options=[
            "Boyz are a unit that contains 10 models. It can contain 20 models (Power Rating 8) or 30 models (Power Rating 13). It is equipped with: Sluggas; Choppas.",
            "Instead of Sluggas and Choppas, this unit can be equipped with Shootas and Close Combat Weapons (Power Rating +1).",
            "For every 10 models in the unit, it can also be equipped with one of the following: 1 Big Shoota; 1 Rokkit Launcha.",
        ],
    ),
    "Gretchin": u(
        "Gretchin",
        {"M": '5"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "11+", "N": "10", "Pt": "1"},
        ["Orks", "<Clan>", "Light", "Infantry", "Gretchin"],
        [
            {"name": "Grot Blasta", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "8+", "armorPen": "10+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "11+"},
        ],
        profiles=[
            {"M": '5"', "WS": "5+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "11+", "N": "20", "Pt": "2"},
            {"M": '5"', "WS": "5+", "BS": "4+", "A": "3", "W": "3", "Ld": "4", "Sv": "11+", "N": "30", "Pt": "3"},
        ],
        options=[
            "Gretchin are a unit that contains 10 models. It can contain 20 models (Power Rating 2) or 30 models (Power Rating 3). It is equipped with: Grot Blastas; Close Combat Weapons.",
            "This unit can include a Runtherd (Power Rating +1). If this unit includes a Runtherd, it has a Leadership characteristic of 6.",
        ],
    ),
    "Painboy": u(
        "Painboy",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "1", "Pt": "2"},
        ["Orks", "<Clan>", "Light", "Infantry", "Character", "Painboy"],
        [{"name": "Doks Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"}],
        "Sawbonez: At the end of the Action phase, this unit can attempt to heal one friendly <Clan> Light unit in base contact with it. "
        "If it does, roll one D6; on a 4+, remove one damage marker from that Light unit. Only one attempt to heal each unit can be made each turn.",
        options=["A Painboy is a unit that contains 1 model. It is equipped with: Dok's Tools."],
    ),
    "Mek": u(
        "Mek",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "1", "Pt": "2"},
        ["Orks", "<Clan>", "Light", "Infantry", "Character", "Mek"],
        [{"name": "Meks Tools", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"}],
        "Mekaniak: At the end of the Action phase, this unit can attempt to repair one friendly <Clan> Vehicle unit in base contact with it. "
        "If it does, roll one D6; on a 4+ remove one damage marker from that Vehicle unit. Only one attempt to repair each unit can be made each turn.",
        options=["A Mek is a unit that contains 1 model. It is equipped with: Mek's Tools."],
    ),
    "Burna Boyz": u(
        "Burna Boyz",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "5", "Pt": "3"},
        ["Orks", "<Clan>", "Light", "Infantry", "Burna Boyz"],
        [
            {"name": "Burna (Ranged)", "type": "Small Arms", "range": '8"', "attacks": "x3", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Burna (Melee)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "6"},
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "6", "Sv": "10+", "N": "15", "Pt": "9"},
        ],
        options=[
            "Burna Boyz are a unit that contains 5 models. It can contain 10 models (Power Rating 6), or 15 models (Power Rating 9). "
            "It is equipped with: Burnas (Ranged); Burnas (Melee).",
        ],
    ),
    "Tankbustaz": u(
        "Tankbustaz",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "5", "Pt": "4"},
        ["Orks", "<Clan>", "Light", "Infantry", "Tankbustas"],
        [
            {"name": "Tankbusta Rokkit Launchas", "type": "Small Arms", "range": '24"', "attacks": "x2", "skill": "7+", "armorPen": "7+"},
            {"name": "Tankbusta Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "7+"},
        ],
        'Bomb Squigs: Once per battle, after this unit makes a Shoot action, select one enemy Vehicle unit (other than an Aircraft) within 18" of this unit and roll one D6. On a 4+ place one blast marker next to that unit.\n'
        "Tank Hunters: You can re-roll hit rolls for attacks made by this unit that target Vehicle units.",
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "8"},
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "7", "Sv": "10+", "N": "15", "Pt": "12"},
        ],
        options=[
            "Tankbustas are a unit that contains 5 models. It can contain 10 models (Power Rating 8) or 15 models (Power Rating 12). "
            "It is equipped with: Tankbusta Rokkit Launchas; Tankbusta Weapons.",
        ],
    ),
    "Nobz": u(
        "Nobz",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "5", "Pt": "6"},
        ["Orks", "<Clan>", "Light", "Infantry", "Nobz"],
        [
            {"name": "Sluggas", "type": "Small Arms", "range": '12"', "attacks": "x2", "skill": "7+", "armorPen": "9+"},
            {"name": "Nob Choppas", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "6+", "armorPen": "6+"},
        ],
        profiles=[{"M": '5"', "WS": "3+", "BS": "5+", "A": "2", "W": "4", "Ld": "6", "Sv": "8+", "N": "10", "Pt": "12"}],
        options=["Nobz are a unit that contains 5 models. It can contain 10 models (Power Rating 12). It is equipped with: Sluggas; Nob Choppas."],
    ),
    "Nobz w Waaagh! Banner": u(
        "Nobz w Waaagh! Banner",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "3"},
        ["Orks", "<Clan>", "Light", "Infantry", "Character", "Nob"],
        [{"name": "Waaagh! Banner", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "8+"}],
        'Waaagh! Banner: Add 1 to hit rolls for attacks made with melee weapons by <Clan> units whilst they are within 6" of any friendly <Clan> units with this ability.',
        options=["A Nob with Waaagh! Banner is a unit that contains 1 model. It is equipped with: Waaagh! Banner."],
    ),
    "Meganobz": u(
        "Meganobz",
        {"M": '4"', "WS": "3+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "4+", "N": "3", "Pt": "6"},
        ["Orks", "<Clan>", "Light", "Infantry", "Mega Armour", "Nobz", "Meganobz"],
        [
            {"name": "Meganob Shootas", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "7+", "armorPen": "9+"},
            {"name": "Meganob Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "6+"},
        ],
        profiles=[
            {"M": '4"', "WS": "3+", "BS": "5+", "A": "2", "W": "4", "Ld": "6", "Sv": "4+", "N": "6", "Pt": "12"},
            {"M": '4"', "WS": "3+", "BS": "5+", "A": "3", "W": "6", "Ld": "7", "Sv": "4+", "N": "9", "Pt": "18"},
        ],
        options=[
            "Meganobz are a unit that contains 3 models. It can contain 6 models (Power Rating 12) or 9 models (Power Rating 18). "
            "It is equipped with: Meganob Shootas; Meganob Melee Weapons.",
        ],
    ),
    "Kommandos": u(
        "Kommandos",
        {"M": '6"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "5", "Pt": "3"},
        ["Orks", "<Clan>", "Light", "Infantry", "Kommandos"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Kommando Burna", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Kommando Sluggas", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Kommando Choppas", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[
            {"M": '6"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "6", "Sv": "10+", "N": "10", "Pt": "5"},
            {"M": '6"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "7", "Sv": "10+", "N": "15", "Pt": "7"},
        ],
        options=[
            "Kommandos are a unit that contains 5 models. It can contain 10 models (Power Rating 5) or 15 models (Power Rating 7). "
            "It is equipped with: Kommando Sluggas; Kommando Choppas.",
            "This unit can also be equipped with up to two of the following (Power Rating +1 per Kommando Burna): 1 Big Shoota; 1 Kommando Burna; 1 Rokkit Launcha.",
        ],
    ),
    "Nobz On Bikes": u(
        "Nobz On Bikes",
        {"M": '14"', "WS": "3+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "8+", "N": "3", "Pt": "7"},
        ["Orks", "<Clan>", "Light", "Biker", "Speed Freeks", "Nobz"],
        [
            {"name": "Dakka Guns", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "7+", "armorPen": "9+"},
            {"name": "Nob Choppas", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "6+", "armorPen": "6+"},
        ],
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "2", "W": "4", "Ld": "6", "Sv": "8+", "N": "6", "Pt": "14"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "3", "W": "6", "Ld": "7", "Sv": "8+", "N": "9", "Pt": "21"},
        ],
        options=[
            "Nobz on Warbikes are a unit that contains 3 models. It can contain 6 models (Power Rating 14) or 9 models (Power Rating 21). "
            "It is equipped with: Dakkaguns; Nob Choppas.",
        ],
    ),
    "Warbikers": u(
        "Warbikers",
        {"M": '14"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "5", "Sv": "7+", "N": "3", "Pt": "4"},
        ["Orks", "<Clan>", "Light", "Biker", "Speed Freeks", "Warbikers"],
        [
            {"name": "Dakka Guns", "type": "Small Arms", "range": '18"', "attacks": "x3", "skill": "7+", "armorPen": "9+"},
            {"name": "Warbiker Choppas", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "6", "Sv": "7+", "N": "6", "Pt": "8"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "7", "Sv": "7+", "N": "9", "Pt": "12"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "4", "W": "4", "Ld": "8", "Sv": "7+", "N": "12", "Pt": "16"},
        ],
        options=[
            "Warbikers are a unit that contains 3 models. It can contain 6 models (Power Rating 8), 9 models (Power Rating 12) or 12 models (Power Rating 16). "
            "It is equipped with: Dakkaguns; Warbiker Choppas.",
        ],
    ),
    "Warbuggies": u(
        "Warbuggies",
        {"M": '12"', "WS": "4+", "BS": "5+", "A": "1", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "5"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Speed Freeks", "Kustom Boosta-blastas"],
        [
            {"name": "Burna Exhaust", "type": "Heavy", "range": '8"', "attacks": "User", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Rivet Kannons", "type": "Heavy", "range": '36"', "attacks": "x2", "skill": "6+", "armorPen": "7+"},
            {"name": "Spiked Rams", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "10+"},
        ],
        "Ram: After this unit makes a Move action, if it is in base contact with any enemy units, select one of those units and roll one D6. On a 5+ place one blast marker next to that unit.",
        profiles=[
            {"M": '12"', "WS": "4+", "BS": "5+", "A": "2", "W": "4", "Ld": "4", "Sv": "8+", "N": "2", "Pt": "10"},
            {"M": '12"', "WS": "4+", "BS": "5+", "A": "3", "W": "6", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "15"},
        ],
        options=[
            "Kustom Boosta-blastas are a unit that contains 1 model. It can contain 2 models (Power Rating 10) or 3 models (Power Rating 15). "
            "It is equipped with: Rivet Kannons; Burna Exhausts; Spiked Rams.",
        ],
    ),
    "Stormboyz": u(
        "Stormboyz",
        {"M": '14"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "5", "Sv": "10+", "N": "5", "Pt": "4"},
        ["Orks", "<Clan>", "Light", "Infantry", "Fly", "Jump Pack", "Stormboyz"],
        [
            {"name": "Stormboy Sluggas", "type": "Small Arms", "range": '12"', "attacks": "User", "skill": "7+", "armorPen": "9+"},
            {"name": "Stormboy Choppas", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "7"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "4", "W": "4", "Ld": "6", "Sv": "10+", "N": "20", "Pt": "13"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "6", "W": "6", "Ld": "7", "Sv": "10+", "N": "30", "Pt": "19"},
        ],
        options=[
            "Stormboyz are a unit that contains 5 models. It can contain 10 models (Power Rating 7), 20 models (Power Rating 13) or 30 models (Power Rating 19). "
            "It is equipped with: Stormboy Sluggas; Stormboy Choppas.",
        ],
    ),
    "Deffkoptas": u(
        "Deffkoptas",
        {"M": '14"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "4"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Fly", "Speed Freeks", "Deffkoptas"],
        [
            {"name": "Twin Big Shoota", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Kopta Rokkits", "type": "Small Arms", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Spinnin' Blades", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        "Deep Strike",
        profiles=[
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "2", "Pt": "7"},
            {"M": '14"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "4", "Sv": "8+", "N": "3", "Pt": "10"},
        ],
        options=[
            "Deffkoptas are a unit that contains 1 model. It can contain 2 models (Power Rating 7) or 3 models (Power Rating 10). It is equipped with: Spinnin' Blades.",
            "For each model this unit contains, it must be equipped with one of the following: Kopta Rokkits; 1 Twin Big Shoota.",
        ],
    ),
    "Mek Gun": u(
        "Mek Gun",
        {"M": '3"', "WS": "5+", "BS": "4+", "A": "1", "W": "2", "Ld": "4", "Sv": "10+", "N": "6", "Pt": "2"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Artillery", "Gretchin", "Mek Gun"],
        [
            {"name": "Bubblechukka", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "6+", "armorPen": "6+"},
            {"name": "Kustom Mega-Kannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "9+", "armorPen": "5+", "abilities": "Supercharge"},
            {"name": "Smasha Gun", "type": "Heavy", "range": '48"', "attacks": "2", "skill": "7+", "armorPen": "5+"},
            {"name": "Traktor Kannon", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "10+", "armorPen": "3+", "abilities": "Anti-air"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "11+"},
        ],
        "Artillery Battery: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. "
        "Each unit taken for a single Heavy Support slot must be placed at the same time and within 6\" of each other unit taken for the same slot the first time they are set up.",
        options=[
            "A Mek Gun is a unit that contains 6 models. The unit is equipped with: Close Combat Weapons.",
            "This unit must also be equipped with one of the following: 1 Bubblechukka; 1 Kustom Mega-Kannon; 1 Smasha Gun; 1 Traktor Kannon.",
            "This unit can include a Runtherd (Power Rating +1). If this unit includes a Runtherd, it has a Leadership characteristic of 6.",
        ],
    ),
    "Battlewagon": u(
        "Battlewagon",
        {"M": '12"', "WS": "5+", "BS": "5+", "A": "1", "W": "3", "Ld": "5", "Sv": "8+", "N": "1", "Pt": "8"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Transport", "Battlewagon"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Kannon", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "7+"},
            {"name": "Killkannon", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "6+", "armorPen": "6+"},
            {"name": "Lobba", "type": "Heavy", "range": '48"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Barrage"},
            {"name": "Zzap Gun", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "9+", "armorPen": "4+"},
            {"name": "Deff Rolla", "type": "Melee", "range": "Melee", "attacks": "x3", "skill": "7+", "armorPen": "7+"},
            {"name": "Wagon Melee Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        "Open-topped",
        options=[
            "A Battlewagon is a unit that contains 1 model. It is equipped with: Wagon Melee Weapons.",
            "This unit can also be equipped with 1 Lobba (Power Rating +1).",
            "This unit can also be equipped with one of the following (Power Rating +1): 1 Kannon; 1 Killkannon; 1 Zzap Gun.",
            "This unit can also be equipped with up to 4 Big Shootas (Power Rating +1 per weapon).",
            "Instead of Wagon Melee Weapons, this unit can be equipped with 1 Deff Rolla (Power Rating +1).",
            "This unit can have an 'Ard Case. If this unit has an 'Ard Case, it: Has a Save characteristic of 6+; loses the following abilities: Open-topped.",
            "Transport: This unit can transport up to 20 friendly Flash Gitz or <Clan> Infantry models. Each Mega Armour or Jump Pack model takes the space of 2 other Infantry models. "
            "If this unit is equipped with a Killkannon, it can only transport up to 12 models.",
        ],
    ),
    "Killa Kans": u(
        "Killa Kans",
        {"M": '6"', "WS": "5+", "BS": "4+", "A": "1", "W": "1", "Ld": "4", "Sv": "6+", "N": "1", "Pt": "2"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Gretchin", "Killa Kans"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Grotzooka", "type": "Heavy", "range": '18"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Skorcha", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Killa Kan Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "7+"},
        ],
        profiles=[
            {"M": '6"', "WS": "5+", "BS": "4+", "A": "4", "W": "3", "Ld": "4", "Sv": "6+", "N": "3", "Pt": "7"},
            {"M": '6"', "WS": "5+", "BS": "4+", "A": "8", "W": "6", "Ld": "4", "Sv": "6+", "N": "6", "Pt": "13"},
        ],
        options=[
            "Killa Kans are a unit that contains 1 model. It can contain 3 models (Power Rating 7) or 6 models (Power Rating 13). It is equipped with: Killa Kan Weapons.",
            "For each model this unit contains, it must also be equipped with one of the following: 1 Big Shoota; 1 Grotzooka; 1 Rokkit Launcha; 1 Skorcha.",
        ],
    ),
    "Deff Dread": u(
        "Deff Dread",
        {"M": '6"', "WS": "3+", "BS": "5+", "A": "1", "W": "2", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "4"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Deff Dread"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Kustom Mega-blasta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "Supercharge"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Skorcha", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Armoured Feet", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "10+", "armorPen": "11+"},
            {"name": "Dread Klaws", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "6+", "armorPen": "8+"},
            {"name": "Dread Saw", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "8+", "armorPen": "6+"},
        ],
        "Dread Mob: Each Heavy Support slot in a Detachment allows you to take up to three of this unit in your army, instead of one. "
        "Each unit taken for a single Heavy Support slot must be placed at the same time and within 6\" of each other unit taken for the same slot the first time they are set up.",
        options=[
            "A Deff Dread is a unit that contains 1 model. It is equipped with: Armoured Feet; 2 Dread Klaws.",
            "Instead of 1 Dread Klaw, this unit can be equipped with one of the following: 1 Rokkit Launcha; 1 Kustom Mega-Blasta; 1 Skorcha; 1 Dread Saw.",
            "Instead of 2 Dread Klaws, this unit can be equipped with two of the following in any combination: 1 Rokkit Launcha; 1 Kustom Mega-Blasta; 1 Skorcha; 1 Dread Saw.",
            "This unit must be equipped with two of the following in any combination: 1 Big Shoota; 1 Rokkit Launcha; 1 Skorcha; 1 Kustom Mega-blasta; 1 Dread Saw.",
        ],
    ),
    "Lootas": u(
        "Lootas",
        {"M": '5"', "WS": "3+", "BS": "5+", "A": "1", "W": "1", "Ld": "4", "Sv": "10+", "N": "5", "Pt": "4"},
        ["Orks", "<Clan>", "Light", "Infantry", "Lootas"],
        [
            {"name": "Deffguns", "type": "Small Arms", "range": '48"', "attacks": "x4", "skill": "7+", "armorPen": "7+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "2", "W": "2", "Ld": "5", "Sv": "10+", "N": "10", "Pt": "8"},
            {"M": '5"', "WS": "3+", "BS": "5+", "A": "3", "W": "3", "Ld": "6", "Sv": "10+", "N": "15", "Pt": "12"},
        ],
        options=[
            "Lootas are a unit that contains 5 models. It can contain 10 models (Power Rating 8) or 15 models (Power Rating 12). "
            "It is equipped with: Deffguns; Close Combat Weapons.",
        ],
    ),
    "Flash Gits": u(
        "Flash Gits",
        {"M": '5"', "WS": "3+", "BS": "4+", "A": "2", "W": "2", "Ld": "4", "Sv": "8+", "N": "5", "Pt": "8"},
        ["Orks", "Freebooterz", "Light", "Infantry", "Flash Gitz"],
        [
            {"name": "Snazzguns", "type": "Small Arms", "range": '24"', "attacks": "x3", "skill": "6+", "armorPen": "8+"},
            {"name": "Close Combat Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "7+", "armorPen": "9+"},
        ],
        profiles=[{"M": '5"', "WS": "3+", "BS": "4+", "A": "4", "W": "4", "Ld": "5", "Sv": "8+", "N": "10", "Pt": "16"}],
        options=[
            "Flash Gitz are a unit that contains 5 models. It can contain 10 models (Power Rating 16). It is equipped with: Snazzguns; Close Combat Weapons.",
        ],
    ),
    "Morkanaut": u(
        "Morkanaut",
        {"M": '8"', "WS": "3+", "BS": "5+", "A": "1", "W": "4", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "15"},
        ["Orks", "<Clan>", "Super-heavy", "Vehicle", "Transport", "Morkanaut"],
        [
            {"name": "Kustom Mega-blasta", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "9+", "armorPen": "5+", "abilities": "Supercharge"},
            {"name": "Kustom Mega-zappa", "type": "Heavy", "range": '36"', "attacks": "3", "skill": "9+", "armorPen": "5+", "abilities": "Supercharge"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Twin Big Shoota", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Klaw of Gork (or possibly Mork)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "5+"},
        ],
        "Kustom Force Field: Subtract 1 from wound rolls for attacks made by ranged weapons that target <Clan> units whilst they are wholly within 9\" "
        "of any friendly <Clan> units with a Kustom Force Field.",
        options=[
            "A Morkanaut is a unit that contains 1 model. It is equipped with: 2 Twin Big Shootas; 2 Rokkit Launchas; Kustom Mega-zappa; Kustom Mega-blasta; Klaw of Gork (or possibly Mork).",
            "This unit can have a Kustom Force Field. If this unit has a Kustom Force Field, it has the following additional abilities: Kustom Force Field.",
            "Transport: This unit can transport up to 6 friendly Flash Gitz or <Clan> Infantry models. Each Mega Armour or Jump Pack model takes the space of 2 other Infantry models.",
        ],
    ),
    "Gorkanaut": u(
        "Gorkanaut",
        {"M": '8"', "WS": "3+", "BS": "5+", "A": "2", "W": "4", "Ld": "5", "Sv": "6+", "N": "1", "Pt": "15"},
        ["Orks", "<Clan>", "Super-heavy", "Vehicle", "Transport", "Gorkanaut"],
        [
            {"name": "Deffstorm Mega-shoota", "type": "Heavy", "range": '36"', "attacks": "8", "skill": "6+", "armorPen": "8+"},
            {"name": "Rokkit Launcha", "type": "Heavy", "range": '24"', "attacks": "1", "skill": "7+", "armorPen": "7+"},
            {"name": "Skorcha", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Twin Big Shoota", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Klaw of Gork (or possibly Mork)", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "5+", "armorPen": "5+"},
        ],
        options=[
            "A Gorkanaut is a unit that contains 1 model. It is equipped with: 2 Twin Big Shootas; 2 Rokkit Launchas; Deffstorm Mega-shoota; Skorcha; Klaw of Gork (or possibly Mork).",
            "Transport: This unit can transport up to 6 friendly Flash Gitz or <Clan> Infantry models. Each Mega Armour or Jump Pack model takes the space of 2 other Infantry models.",
        ],
    ),
    "Trukk": u(
        "Trukk",
        {"M": '12"', "WS": "5+", "BS": "5+", "A": "1", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "4"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Transport", "Trukk"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Trukk Weapons", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "9+", "armorPen": "9+"},
        ],
        "Open-topped, Ignore Damage (6+)",
        options=[
            "A Trukk is a unit that contains 1 model. It is equipped with: Big Shoota; Trukk Weapons.",
            "Transport: This unit can transport up to 12 friendly Flash Gitz or <Clan> Infantry models. Each Mega Armour or Jump Pack model takes the space of 2 other Infantry models.",
        ],
    ),
    "Dakka Jet": u(
        "Dakka Jet",
        {"M": '20-60"', "WS": "5+", "BS": "5+", "A": "1", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "5"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Fly", "Aircraft", "Dakkajet"],
        [
            {"name": "Supa-shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Armoured Bulk", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Supersonic\nAll da Dakka: Add 1 to hit rolls for attacks made by this unit with ranged weapons.",
        options=[
            "A Dakkajet is a unit that contains 1 model. It is equipped with: 4 Supa-shootas; Armoured Bulk.",
            "This unit can also be equipped with 2 Supa-shootas (Power Rating +1).",
        ],
    ),
    "Bomba": u(
        "Bomba",
        {"M": '20-50"', "WS": "5+", "BS": "5+", "A": "1", "W": "2", "Ld": "4", "Sv": "8+", "N": "1", "Pt": "6"},
        ["Orks", "<Clan>", "Heavy", "Vehicle", "Fly", "Aircraft", "Burna-Bommer"],
        [
            {"name": "Skorcha Missiles", "type": "Heavy", "range": '24"', "attacks": "2", "skill": "5+", "armorPen": "9+"},
            {"name": "Supa-shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "6+", "armorPen": "8+"},
            {"name": "Twin Big Shoota", "type": "Heavy", "range": '36"', "attacks": "2", "skill": "7+", "armorPen": "9+"},
            {"name": "Armoured Bulk", "type": "Melee", "range": "Melee", "attacks": "User", "skill": "11+", "armorPen": "11+"},
        ],
        "Supersonic\n"
        "Burna Bombs: After this unit makes a Move action, select one enemy unit it moved over whilst making that Move action. "
        "Roll three D6, subtracting 1 from each result if that unit is a Character and adding 1 to each result if that unit is garrisoning a Defensible Terrain feature; "
        "for each result of 4+ place one blast marker next to that unit.",
        options=[
            "A Burna-bommer is a unit that contains 1 model. It is equipped with: Twin Big Shoota; 2 Supa-shootas; Armoured Bulk.",
            "This unit can also be equipped with Skorcha Missiles (Power Rating +1).",
        ],
    ),
    "Stompa": u(
        "Stompa",
        {"M": '12"', "WS": "3+", "BS": "5+", "A": "2", "W": "8", "Ld": "6", "Sv": "6+", "N": "1", "Pt": "49"},
        ["Orks", "<Clan>", "Super-heavy", "Vehicle", "Titanic", "Transport", "Stompa"],
        [
            {"name": "Big Shoota", "type": "Heavy", "range": '36"', "attacks": "1", "skill": "7+", "armorPen": "9+"},
            {"name": "Deffkannon", "type": "Heavy", "range": '72"', "attacks": "6", "skill": "5+", "armorPen": "5+"},
            {"name": "Skorcha", "type": "Heavy", "range": '8"', "attacks": "1", "skill": "7+", "armorPen": "9+", "abilities": "Inferno"},
            {"name": "Supa-gatler", "type": "Heavy", "range": '48"', "attacks": "12", "skill": "6+", "armorPen": "8+"},
            {"name": "Supa-rokkit", "type": "Heavy", "range": '100"', "attacks": "2", "skill": "7+", "armorPen": "4+", "abilities": "One Use Only"},
            {"name": "Mega-choppa", "type": "Melee", "range": "Melee", "attacks": "x2", "skill": "4+", "armorPen": "3+", "abilities": "Destroyer"},
        ],
        "Effigy: You can re-roll Morale tests taken for friendly Orks units whilst they are within 6\" of this unit.\n"
        "Stompa Rigger Crew: At the end of the Action phase, this unit can attempt to repair itself. If it does, roll one D6; on a 4+, remove one damage marker from this unit. "
        "Only one attempt to repair each unit can be made each turn.",
        options=[
            "A Stompa is a unit that contains 1 model. It is equipped with: Deffkannon; Supa-gatler; 3 Big Shootas; 3 Supa-rokkits; Skorcha; Mega-choppa.",
            "This unit can also be equipped with 2 Supa-rokkits (Power Rating +2).",
            "Transport: This unit can transport up to 20 friendly Flash Gitz or <Clan> Infantry models. Each Mega Armour or Jump Pack model takes the space of 2 other Infantry models.",
        ],
    ),
}

ORKS_SLOTS = [
    slot(1, "HQ", ORKS["Gazzghkull Thraka"]),
    slot(2, "HQ", ORKS["Warboss"]),
    slot(3, "HQ", ORKS["Big Mek"]),
    slot(4, "HQ", ORKS["Weirdboy"]),
    slot(5, "HQ", ORKS["Deffkilla Wartrike"]),
    slot(6, "Troops", ORKS["Boyz"]),
    slot(7, "Troops", ORKS["Gretchin"]),
    slot(8, "Elites", ORKS["Painboy"]),
    slot(9, "Elites", ORKS["Mek"]),
    slot(10, "Elites", ORKS["Burna Boyz"]),
    slot(11, "Elites", ORKS["Tankbustaz"]),
    slot(12, "Elites", ORKS["Nobz"]),
    slot(13, "Elites", ORKS["Nobz w Waaagh! Banner"]),
    slot(14, "Elites", ORKS["Meganobz"]),
    slot(15, "Elites", ORKS["Kommandos"]),
    slot(16, "Fast", ORKS["Nobz On Bikes"]),
    slot(17, "Fast", ORKS["Warbikers"]),
    slot(18, "Fast", ORKS["Warbuggies"]),
    slot(19, "Fast", ORKS["Stormboyz"]),
    slot(20, "Fast", ORKS["Deffkoptas"]),
    slot(21, "Heavy", ORKS["Mek Gun"]),
    slot(22, "Heavy", ORKS["Battlewagon"]),
    slot(23, "Heavy", ORKS["Killa Kans"]),
    slot(24, "Heavy", ORKS["Deff Dread"]),
    slot(25, "Heavy", ORKS["Lootas"]),
    slot(26, "Heavy", ORKS["Flash Gits"]),
    slot(27, "Lord", ORKS["Morkanaut"]),
    slot(28, "Lord", ORKS["Gorkanaut"]),
    slot(29, "Transport", ORKS["Trukk"]),
    slot(30, "Air", ORKS["Dakka Jet"]),
    slot(31, "Air", ORKS["Bomba"]),
    slot(32, "Lord", ORKS["Stompa"]),
]
