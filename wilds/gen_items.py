import os
import sys

from icon_map import *
from colors import *
from images import *
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json

base = os.environ["BASE"]

#ic = icons[9].convert("RGBA")
#ic = add_padding(ic, 16)  # White padding
#add_icon = add_icons[0].convert("RGBA").resize((32, 32))
#ic.paste(add_icon, (100 - 32, 0), add_icon)
#ic = multiply_image_by_color(ic, (255, 0, 0, 255))
#ic.show()

def parse_add_icons():
    path = "natives/STM/GameDesign/GUI/Common/_UserData/AddIconData.user.3.json"
    f = open(os.path.join(base, path))
    add_icons_data = json.load(f)[0]["rsz"]["Values"]
    add_icons = {}
    for add_icon in add_icons_data:
        id = add_icon["_AddIcon"]
        add_icons[id] = {
                "pos": add_icon["_AddPosition"],
                "pattern": add_icon["_PatternNo"],
        }
    return add_icons

ADD_ICONS_DATA = parse_add_icons()

ITEM_MSG_FILES = ["natives/STM/GameDesign/Text/Excel_Data/Item.msg"]

def parse_items(self):
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Item/itemData.user.3.json"))
    itemdata = json.load(f)[0]["rsz"]["_Values"]

    items = {}
    for item in itemdata:
        id = item["_ItemId"]
        name = self.get_msg_by_guid(item["_RawName"])
        expl = self.get_msg_by_guid(item["_RawExplain"])
        icon = item["_IconType"]
        icon_idx = 0
        if "INVALID" not in icon:
            icon_idx = int(icon.strip("ITEM_"))
            icon = ICONS_WILDS[icon_idx]
        color_id = item["_IconColor"]
        color = color_id.replace("I_", "").lower().capitalize()
        add_icon = item["_AddIconType"]
        add_icon_name = add_icon.lower().capitalize().replace("_item", "")
        # check if the icon for that item exists and then generate it if needed
        tex_name = f"MHWilds-{icon} Icon {color}.png"
        if "INVALID" not in add_icon:
            tex_name = f"MHWilds-{icon} {add_icon_name} {color}.png"
        items[id] = {
            "name": name,
            "expl": expl,
            "type": item["_Type"],
            "icon": icon,
            "color": color,
            "add_icon": add_icon_name,
            "rarity": item["_Rare"],
            "max_count": item["_MaxCount"],
            "otomo_max": item["_OtomoMax"],
            "sell": item["_SellPrice"],
            "buy": item["_BuyPrice"],
            #"formoney": item["_ForMoney"],
            #"tex_name": tex_name,
        }
        out_dir = "wilds/data/item_icons"
        icon_path = os.path.join(out_dir, tex_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        #if not os.path.exists(icon_path):
        icon_tex_base = ICONS_TEX[icon_idx].copy()
        color = COLORS[WILDS_COLOR_IDX_MAP[color_id]]
        icon_tex = multiply_image_by_color(icon_tex_base, color[:3])
        if "INVALID" not in add_icon:
            add_icon = ADD_ICONS_DATA[add_icon]
            pos = ADD_ICON_POS[add_icon["pos"]]
            add_icon_idx = add_icon["pattern"]
            add_icon = ADD_ICONS_TEX[add_icon_idx].resize((32, 32))
            icon_tex.paste(add_icon, pos, add_icon)
        icon_tex.save(icon_path)

    return items

def parse_item_recipes(self, items):
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Item/ItemRecipe.user.3.json"))
    itemdata = json.load(f)[0]["rsz"]["_Values"]

    recipes = {}
    for recipe in itemdata:
        id = recipe["_ItemRecipeId"]
        result = items[recipe["_ResultItem"]]["name"]
        materials = [items[mat]["name"] for mat in recipe["_Item"]]
        recipes[id] = {
            "idx": recipe["_Index"],
            "result": result,
            "materials": materials,
            "result_id": recipe["_ResultItem"],
            "materials_id": recipe["_Item"],
        }

    return recipes


item_data = Parser2(parse_items, ITEM_MSG_FILES, base, msg_ext=".23.json").parse()
with open('wilds/data/itemdata.json', 'w') as f:
    json.dump(item_data, f, ensure_ascii=False, indent=4)

item_recipes = Parser2(parse_item_recipes, [], base, msg_ext=".23.json").parse(item_data)
with open('wilds/data/itemrecipe.json', 'w') as f:
    json.dump(item_recipes, f, ensure_ascii=False, indent=4)

