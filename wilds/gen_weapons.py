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

WP_TO_KEY = {
    "LONG_SWORD": "_LongSword",
    "SHORT_SWORD": "_ShortSword",
    "TWIN_SWORD": "_TwinSword",
    "TACHI": "_Tachi",
    "HAMMER": "_Hammer",
    "WHISTLE": "_Whistle",
    "LANCE": "_Lance",
    "GUN_LANCE": "_GunLance",
    "SLASH_AXE": "_SlashAxe",
    "CHARGE_AXE": "_ChargeAxe",
    "ROD": "_Rod",
    "BOW": "_Bow",
    "HEAVY_BOWGUN": "_HeavyBowgun",
    "LIGHT_BOWGUN": "_LightBowgun",
}

WEAPON_DATA = [
    "LONGSWORD",
    "SHORTSWORD",
    "TWINSWORD",
    "TACHI",
    "HAMMER",
    "WHISTLE",
    "LANCE",
    "GUNLANCE",
    "SLASHAXE",
    "CHARGEAXE",
    "ROD",
    "BOW",
    "HEAVYBOWGUN",
    "LIGHTBOWGUN",
]


WEAPON_DATA = [
    "LongSword",
    "ShortSword",
    "TwinSword",
    "Tachi",
    "Hammer",
    "Whistle",
    "Lance",
    "GunLance",
    "SlashAxe",
    "ChargeAxe",
    "Rod",
    "Bow",
    "HeavyBowgun",
    "LightBowgun",
]

def parse_weapons(self):
    weapondata = []
    for key in WEAPON_DATA:
        f = open(os.path.join(base, f"natives/STM/GameDesign/Common/Weapon/{key}.user.3.json"))
        weapondata += json.load(f)[0]["rsz"]["_Values"]
    weapons = {
        "LONG_SWORD": {},
        "SHORT_SWORD": {},
        "TWIN_SWORD": {},
        "TACHI": {},
        "HAMMER": {},
        "WHISTLE": {},
        "LANCE": {},
        "GUN_LANCE": {},
        "SLASH_AXE": {},
        "CHARGE_AXE": {},
        "ROD": {},
        "BOW": {},
        "HEAVY_BOWGUN": {},
        "LIGHT_BOWGUN": {},
    }
    for wp in weapondata:
        wp_type = wp["_Type"]
        id = wp[WP_TO_KEY[wp_type]]
        weapons[wp_type][id] = {
                "name": self.get_msg_by_guid(wp["_Name"]),
                "explain": self.get_msg_by_guid(wp["_Explain"]),
                "model_id": wp["_ModelId"],
                "custom_model_id": wp["_CustomModelId"],
                "price": wp["_Price"],
                "rarity": wp["_Rare"],
                "attack": wp["_Attack"],
                "defense": wp["_Defense"],
                "affinity": wp["_Critical"],
                "attribute": wp["_Attribute"],
                "attribute_value": wp["_AttributeValue"],
                "sub_attribute": wp["_SubAttribute"],
                "sub_attribute_value": wp["_SubAttributeValue"],
                "slots": [slot for slot in wp["_SlotLevel"] if slot != "NONE"],
                "skills": [skill for skill in wp["_Skill"] if skill != "NONE"],
                "skill_levels": [lvl for lvl in wp["_SkillLevel"] if lvl != 0],
        }

        if wp_type not in ["BOW", "HEAVYBOWGUN", "LIGHTBOWGUN"]:
            weapons[wp_type][id]["sharpness"] = wp["_SharpnessValList"],
            weapons[wp_type][id]["handicraft_values"] = wp["_TakumiValList"]

    return weapons

weapons = Parser2(parse_weapons, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/weapons.json', 'w') as f:
    json.dump(weapons, f, ensure_ascii=False, indent=4)


