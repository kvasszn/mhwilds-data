import os
import sys

from icon_map import *
from colors import *
from images import *
import gen_items
import gen_skills
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json

base = os.environ["BASE"]

MSG_FILES = [
        "combined_msgs.json"
]

"""
Three food selections
- first selection is in mealdata.user, called rations
    contains the base food choice for the meal
    provides baseline stats to be added onto for the other food choices
the next two types of food are in fooddata.user
    ismain determines if its a primary or subtype selection
2nd is called additional
3rd is finishing touches

Eating inside villages also seems to give some certain boosts
There's also random skills that can be activated based on the random tables
"""

RATION_TYPE_MAP = {
    "TYPE_00": "Meat",
    "TYPE_01": "Fish",
    "TYPE_02": "Veggies",
}

def parse_meals(self):
    f = open(os.path.join(base, "natives/STM/GameDesign/Facility/MealData.user.3.json"))
    mealdata = json.load(f)[0]["rsz"]["_Values"]
    f = open(os.path.join(base, "natives/STM/GameDesign/Facility/FoodData.user.3.json"))
    fooddata = json.load(f)[0]["rsz"]["_Values"]
    meals = {
        "rations": [],
        "additional": {},
        "finishing": {},
    }
    for meal in mealdata:
        icon = meal["_ItemIcon"]
        icon_idx = int(icon.strip("ITEM_"))
        out_dir = "wilds/data/item_icons"
        color = meal["_IconColor"]
        color_name = color.strip("I_").lower().capitalize()
        if icon != "INVALID":
            icon_idx = int(icon.replace("ITEM_", ""))
            tex_name = f"MHWilds-{ICONS_WILDS[icon_idx]} Icon {color_name}.png"
            icon_path = os.path.join(out_dir, tex_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            icon_tex_base = ICONS_TEX[icon_idx].copy()
            color = COLORS[WILDS_COLOR_IDX_MAP[color]]
            icon_tex = multiply_image_by_color(icon_tex_base, color[:3])
            icon_tex.save(icon_path)
            icon = ICONS_WILDS[icon_idx]

        meal_type =  RATION_TYPE_MAP[meal["_PortableFoodType"]]
        meals["rations"].append({
                "type": meal_type,
                "icon": icon,
                "color": color_name,
                "time": meal["_Time"],
                "health": meal["_Health"],
                "stamina": meal["_Stamina"],
                "attack": meal["_Attack"],
                "defence": meal["_Defence"],
                "attr_resist": meal["_AttrResist"],
                "meal_skills": [skill for skill in meal["_MealSkill"] if skill != "NONE"],
                "random_table": [tbl for tbl in meal["_RandomTable"] if tbl != "INVALID"],
        })

    for food in fooddata:
        id = food["_ItemId"]
        if food["_IsMain"]:
            category = "additional"
        else:
            category = "finishing"

        name = None
        if item := gen_items.item_data.get(id):
            name = item["name"]

        meal_skill = food["_MealSkill"]
        meal_skill_name = None
        if skill := gen_skills.meal_skills.get(meal_skill):
            meal_skill_name = skill["name"]
        meals[category][id] = {
                "item": name,
                "time": food["_Time"],
                "health": food["_Health"],
                "stamina": food["_Stamina"],
                "attack": food["_Attack"],
                "defence": food["_Defence"],
                "attr_resist": food["_AttrResist"],
                "meal_skills": food["_MealSkill"],
                "meal_skill_name": meal_skill_name,
                "random_table": [tbl for tbl in food["_RandomTable"] if tbl != "INVALID"],
        }

    return meals

meals = Parser2(parse_meals, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/fooddata.json', 'w') as f:
    json.dump(meals, f, ensure_ascii=False, indent=4)
