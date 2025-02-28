import os
import sys

from numpy import pi

from icon_map import *
from colors import *
from images import *
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json

base = os.environ["BASE"]

MSG_FILES = [
        "combined_msgs.json",
]

def parse_armor(self):
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Equip/ArmorSeriesData.user.3.json"))
    seriesdata = json.load(f)[0]["rsz"]["_Values"]
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Equip/ArmorData.user.3.json"))
    piecesdata = json.load(f)[0]["rsz"]["_Values"]
    
    armor_series = {}
    for series in seriesdata:
        id = series["_Series"]
        armor_series[id] = {
                "name": self.get_msg_by_guid(series["_Name"]),
                "variety": series["_ModelVariety"],
                "mod_id": series["_ModId"],
                "mod_sub_male_id": series["_ModSubMaleId"],
                "mod_sub_female_id": series["_ModSubFemaleId"],
                "rarity": series["_Rare"],
                "price": series["_Price"],
                "color": series["_Color"],
                "pieces": {},
        }

    for piece in piecesdata:
        id = piece["_Series"]
        piece_type = piece["_PartsType"]
        if armor_series.get(id) is None:
            continue
        armor_series[id]["pieces"][piece_type] = {
            "type": piece_type,
            "name": self.get_msg_by_guid(piece["_Name"]),
            "explain": self.get_msg_by_guid(piece["_Explain"]),
            "defense": piece["_Defense"],
            "resistance": piece["_Resistance"],
            "slot_level": [slot for slot in piece["_SlotLevel"] if slot != "NONE"],
            "skills": [skill for skill in piece["_Skill"] if skill != "NONE"],
            "skill_levels": [lvl for lvl in piece["_SkillLevel"] if lvl != 0],
        }

    return armor_series

armor_series = Parser2(parse_armor, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/armor.json', 'w') as f:
    json.dump(armor_series, f, ensure_ascii=False, indent=4)

