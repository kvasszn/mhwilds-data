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
PARTS_FILE_EXT = "_Param_Parts.user.3.json"

def parse_enemies(self):
    base_path = os.path.join(base, "natives/STM/GameDesign/Enemy")
    enemies = {}
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Enemy/EnemyData.user.3.json"))
    enemydata = json.load(f)[0]["rsz"]["_Values"]
    
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Enemy/EnemySpecies.user.3.json"))
    speciesdata = json.load(f)[0]["rsz"]["_Values"]
    species = {s["_EmSpecies"]: self.get_msg_by_guid(s["_EmSpeciesName"]) for s in speciesdata}

    for enemy in enemydata:
        id = enemy["_enemyId"] 
        if id == "INVALID":
            continue
        emid, subid, idk = id.split("_")
        emid = emid.removeprefix("EM")

        reward_path = os.path.join(base, f"natives/STM/GameDesign/Common/Enemy/{id}.user.3.json")
        reward_data = []
        if os.path.exists(reward_path):
            f = open(reward_path)
            reward_raw = json.load(f)[0]["rsz"]["_Values"]
            for reward in reward_raw:
                item_ids = [i for i in reward["_IdEx"] if i != "INVALID"]
                reward_data.append({
                        "story": {
                            "item_id": reward["_IdStory"],
                            "num": reward["_RewardNumStory"],
                            "probability": reward["_probabilityStory"],
                        },
                        "ex": {
                            "item_ids": item_ids,
                            "nums": reward["_RewardNumEx"][:len(item_ids)],
                            "probabilities": reward["_probabilityEx"][:len(item_ids)],
                        },
                    })

        icon_color = enemy["_IconColor"]
        boss_icon_id = enemy["_BossIconType"]
        zako_icon_id = enemy["_ZakoIconType"]
        item_icon_id = enemy["_ItemIconType"]
        map_icon_id = enemy["_MapIconType"]
        animal_icon_id = enemy["_AnimalIconType"]
        icon_idx = None
        if boss_icon_id != "INVALID":
            icon_idx = int(boss_icon_id[1:]) + 20
        elif zako_icon_id != "INVALID":
            icon_idx = int(zako_icon_id[1:]) + 100
        elif animal_icon_id != "INVALID":
            icon_idx = int(animal_icon_id[1:]) + 12 * 20

        item_icon_idx = None
        if item_icon_id != "INVALID":
            item_icon_idx = int(item_icon_id.split("_")[-1])

        map_icon_idx = None
        if map_icon_id != "INVALID":
            map_icon_idx = int(map_icon_id.split("_")[-1]) + 16 * 20

        out_dir = "wilds/data/enemy_icons"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if icon_idx is not None:
            tex_icon_name = f"MHWilds-{id} Icon.png"
            icon_path = os.path.join(out_dir, tex_icon_name)
            color = COLORS[WILDS_COLOR_IDX_MAP[icon_color]]
            icon_tex = COL_ICONS[icon_idx].copy()
            icon_tex.save(icon_path)

        if item_icon_idx is not None:
            tex_item_name = f"MHWilds-{id} Item Icon.png"
            item_icon_path = os.path.join(out_dir, tex_item_name)
            color = COLORS[WILDS_COLOR_IDX_MAP[icon_color]]
            item_tex = ICONS_TEX[item_icon_idx].copy()
            item_tex = multiply_image_by_color(item_tex, color[:3])
            item_tex.save(item_icon_path)

        if map_icon_idx is not None:
            map_tex_name = f"MHWilds-{id} Map Icon.png"
            map_icon_path = os.path.join(out_dir, map_tex_name)
            color = COLORS[WILDS_COLOR_IDX_MAP[icon_color]]
            map_tex = ICONS_TEX[map_icon_idx].copy()
            map_tex = multiply_image_by_color(map_tex, color[:3])
            map_tex.save(map_icon_path)

        enemies[id] = {
            "name": self.get_msg_by_guid(enemy["_EnemyName"]),
            "explain": self.get_msg_by_guid(enemy["_EnemyExp"]),
            "extraname": self.get_msg_by_guid(enemy["_EnemyExtraName"]),
            "boss_explain": self.get_msg_by_guid(enemy["_EnemyBossExp"]),
            "features": self.get_msg_by_guid(enemy["_EnemyFeatures"]),
            "tips": self.get_msg_by_guid(enemy["_EnemyTips"]),
            "memo": self.get_msg_by_guid(enemy["_Memo"]),
            "grammar": self.get_msg_by_guid(enemy["_Grammar"]),
            "name_langs": self.get_msg_by_guid_all_langs(enemy["_EnemyName"]),
            "explain_langs": self.get_msg_by_guid_all_langs(enemy["_EnemyExp"]),
            "memo_langs": self.get_msg_by_guid_all_langs(enemy["_Memo"]),
            "species_id": enemy["_Species"],
            "species": species.get(enemy["_Species"]),
            "reward_data": reward_data,
        }

        enemies[id]['color'] = icon_color
        enemies[id]['item_icon'] = item_icon_id 
        enemies[id]['map_icon'] = map_icon_id
        enemies[id]['animal_icon'] = animal_icon_id
        enemies[id]['zako_icon'] = zako_icon_id
        enemies[id]['boss_icon'] = boss_icon_id
        #
        # FIX MULTI PARTS STUFF
        # FIX MULTI PARTS STUFF
        # FIX MULTI PARTS STUFF
        # FIX MULTI PARTS STUFF
        #
        if not enemies.get(id):
            enemies[id] = {"parts_data": {}}
        file_path = os.path.join(base_path, f"Em{emid}", subid, f"Data/Em{emid}_{subid}{PARTS_FILE_EXT}") 

        if os.path.exists(file_path):
            f = open(file_path)
            parts_raw = json.load(f)[0]["rsz"]
            base_health = parts_raw["_BaseHealth"]
            meat_vals = {}
            for meat in parts_raw["_MeatArray"]["_DataArray"]:
                meat_vals[meat["_InstanceGuid"]] = {
                        "slash": meat["_Slash"],
                        "blow": meat["_Blow"],
                        "shot": meat["_Shot"],
                        "fire": meat["_Fire"],
                        "water": meat["_Water"],
                        "thunder": meat["_Thunder"],
                        "ice": meat["_Ice"],
                        "dragon": meat["_Dragon"],
                        "stun": meat["_Stun"],
                        "lightplant": meat["_LightPlant"],
                }

            parts = {}
            for part in parts_raw["_PartsArray"]["_DataArray"]:
                parts[part["_InstanceGuid"]] = {
                        "vital": part["_Vital"][0]["_Value"], # they're arrays of value objects like wtf
                        "extract": part["_RodExtract"],
                        "hzv_normal": meat_vals.get(part["_MeatGuidNormal"]),
                        "hzv_break": meat_vals.get(part["_MeatGuidBreak"]),
                        "hzv_misc1": meat_vals.get(part["_MeatGuidCustom1"]),
                        "hzv_misc2": meat_vals.get(part["_MeatGuidCustom2"]),
                        "hzv_misc3": meat_vals.get(part["_MeatGuidCustom3"]),
                        "part_type": part["_PartsType"],
                }

            for weak in parts_raw["_WeakPointArray"]["_DataArray"]:
                if guid := weak.get("_LinkParsGuid"):
                    parts[guid]["is_weak_point"] = [x["_Value"] for x in weak["_Vital"]]
            
            for scar in parts_raw["_ScarPointArray"]["_DataArray"]:
                if guid := scar.get("_LinkParsGuid"):
                    parts[guid]["scar_points"] = {
                            "size_rate": scar["SizeRate"],
                            "num": scar["_Num"],
                            "normal_vital": [x["_Value"] for x in scar["_NormalVital"]],
                            "tear_vital": [x["_Value"] for x in scar["_TearVital"]],
                            "raw_scar_vital": [x["_Value"] for x in scar["_RawScarVital"]],
                    }
            parts["legendary_scar_nums"] = parts_raw["_LegendaryScarNumArray"]


            # get thigns that can be cut off
            file_path = os.path.join(base_path, f"Em{emid}", subid, f"Data/Em{emid}_{subid}_Param_PartsLost.user.3.json")
            parts_lost = {}
            if os.path.exists(file_path):
                f = open(file_path)
                parts_lost_raw = json.load(f)[0]["rsz"]["_PartsLostArray"]["_DataArray"]
                for part in parts_lost_raw:
                    if guid := part.get("_TargetDataGuid"):
                        parts_lost[guid] = part

            # part breaks
            for part in parts_raw["_PartsBreakArray"]["_DataArray"]:
                guid = part["_TargetDataGuid"]
                if parts.get(guid):
                    parts[guid]["break_data"] = {
                            "execute_count": part["_ExcuteCount"],
                            "max_count": part["_MaxCount"],
                            "condition": part["_Condition"]
                    }
                    if part_lost := parts_lost.get(part["_InstanceGuid"]):
                        parts[guid]["break_data"]["carve_count"] = part_lost["_HagitoriNum"] 


            enemies[id]["part_datas"] = {
                    "base_health": base_health,
                    "parts": parts,
            }

    return enemies

def get_enemies():
    enemies = Parser2(parse_enemies, MSG_FILES, base, msg_ext="").parse()
    with open('wilds/data/enemies.json', 'w') as f:
        json.dump(enemies, f, ensure_ascii=False, indent=4)
    return enemies

if __name__ == "__main__":
    get_enemies()
