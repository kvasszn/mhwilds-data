import os
import sys

from icon_map import *
from colors import *
from images import *
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
from parser import Parser2
import json
import struct

BASE = os.environ["BASE"]

MSG_FILES = ["combined_msgs.json"]

def getpog():
    f = open(os.path.join(BASE, "natives/STM/GameDesign/Stage/st101/Layout/Loaded/Gimmick/PointGraph/st101_PointList_Gimmick.poglst.0.json"))
    poglist = json.load(f)["paths"]
    pog_ver = 10
    base = os.path.join(BASE, "natives/STM/")

    points = []
    names = []
    weathers = []
    for pogpath in poglist:
        f = open(os.path.join(base, pogpath) + f".{pog_ver}.json")
        pog = json.load(f)['nodes']
        if pog[0][0]["type"] != "app.point_graph_data.ContextLayoutGimmick":
            continue
        for val in pog[0]:
            point = val["rsz"]["v1"]
            gmid = val["rsz"]["_GmID"]
            weather = val["rsz"]["_WeatherAdaptedType"]
            #if "GM003" not in gmid:
            #    continue
            point = struct.unpack('<4f', bytes(point))
            points.append(point[0:3])
            names.append(gmid)
            weathers.append(weather)
    return (points, names, weathers)


def parse_gimmicks(self):
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Gimmick/GimmickTextData.user.3.json"))
    textdata = json.load(f)[0]["rsz"]["_Values"]
    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Gimmick/GimmickBasicData.user.3.json"))
    basicdata = json.load(f)[0]["rsz"]["_Values"]

    gimmicks = {}
    for gimmick in textdata:
        id = gimmick["_GimmickId"]
        name = self.get_msg_by_guid(gimmick["_Name"])
        expl = self.get_msg_by_guid(gimmick["_Explain"])
        name_langs = self.get_msg_by_guid_all_langs(gimmick["_Name"])
        expl_langs = self.get_msg_by_guid_all_langs(gimmick["_Explain"])
        gimmicks[id] = {
            "name": name,
            "name_langs": name_langs,
            "explain": expl,
            "explain_langs": expl_langs,
            "icon": "Question Mark",
            "color": "none",
            "map_icon": None,
            "map_filtering_type": None,
            "points": [],
        }
    for gimmick in basicdata:
        id = gimmick["_GimmickId"]

        icon = gimmick["_IconType"]
        icon_idx = None
        tex_name = ""
        color = ""
        color_id = gimmick["_IconColor"]
        if "INVALID" not in icon:
            icon_idx = int(icon.strip("ITEM_"))
            icon = ICONS_WILDS[icon_idx]
            color = color_id.replace("I_", "").lower().capitalize()
            tex_name = f"MHWilds-{icon} Icon {color}.png"
        map_icon_id = gimmick["_MapIconType"]
        map_icon_idx = None
        if map_icon_id != "INVALID":
            map_icon_idx = int(map_icon_id.split("_")[-1]) + 16 * 20

        name = None
        explain = None
        name_langs = None
        explain_langs = None
        if gim := gimmicks.get(id):
            name = gim["name"]
            name_langs = gim["name_langs"]
            explain = gim["explain"]
            explain_langs = gim["explain_langs"]
        gimmicks[id] = {
            "name": name,
            "name_langs": name_langs,
            "explain": explain,
            "explain_langs": explain_langs,
            "icon": icon,
            "color": color,
            "map_icon": gimmick["_MapIconType"],
            "map_filtering_type": gimmick["_MapFilteringType"],
            "points": [],
        }

        if "GM800" in id:
            param_path = os.path.join(BASE, f"natives/STM/GameDesign/Gimmick/Gm800/Gm800{id[5:]}/Gm800{id[5:]}_AaaUniqueParam.user.3.json")
            if os.path.exists(param_path):
                f = open(param_path)
                params = json.load(f)[0]["rsz"]
                point = params["_IconPos"]
                if params["_IsEnableCampSet"]:
                    point = params["_TentPoint"]["_Position"]
                gimmicks[id]["points"].append(point)

    f = open(os.path.join(base, "natives/STM/GameDesign/Common/Gimmick/GimmickControlData.user.3.json"))
    controldata = json.load(f)[0]["rsz"]["_Values"]
    for gim in controldata:
        id = gim["_GimmickId"]
        if gimmicks.get(id) is None:
            continue
        gimmicks[id]["repop_time"] = gim["_RepopTime"]
        gimmicks[id]["pop_type"] = gim["_PopType"]
        gimmicks[id]["continuous"] = gim["_Continuous"]
        gimmicks[id]["continuous_quest"] = gim["_ContinuousKeepQuest"]

    f = open(os.path.join(base, "natives/STM/GameDesign/Gimmick/Common/GimmickRewardData.user.3.json"))
    rewarddata = json.load(f)[0]["rsz"]["_Values"]
    for reward in rewarddata:
        id = reward["_gimmickId"]
        print(id)
        stage = reward["_stageId"]
        if gimmicks.get(id) is None:
            continue
        if gimmicks[id].get(stage) is None:
            gimmicks[id][stage] = []
        gimmicks[id][stage].append({
                "data_id": reward["_dataId"],
                "items": reward["_itemId"],
                "normal_num": reward["_normalRewardNum"],
                "normal_prob": reward["_normalProbability"],
                "rare_num": reward["_rareRewardNum"],
                "rare_prob": reward["_rareProbability"],
            })

        out_dir = "wilds/data/gimmick_icons"
        icon_path = os.path.join(out_dir, tex_name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        # if not os.path.exists(icon_path):
        if icon_idx is not None:
            icon_tex_base = ICONS_TEX[icon_idx].copy()
            color = COLORS[WILDS_COLOR_IDX_MAP[color_id]]
            icon_tex = multiply_image_by_color(icon_tex_base, color[:3])
            icon_tex.save(icon_path)

        if map_icon_idx is not None:
            map_tex_name = f"MHWilds-{id} Map Icon.png"
            map_icon_path = os.path.join(out_dir, map_tex_name)
            color = COLORS[WILDS_COLOR_IDX_MAP[color_id]]
            map_tex = ICONS_TEX[map_icon_idx].copy()
            map_tex = multiply_image_by_color(map_tex, color[:3])
            map_tex.save(map_icon_path)

    pog_data = getpog()
    for point, name, weather in zip(*pog_data):
        if not gimmicks.get(name):
            gimmicks[name] = {
                "name": name,
                "name_lang": None,
                "explain": None,
                "explain_lang": None,
                "icon": "Question Mark",
                "color": "None",
                "map_icon": None,
                "map_filtering_type": None,
                "points": [],
                "weather_environments": None,
                "weather_event": None,
            }
        gimmicks[name]["points"].append(point)
        gimmicks[name]["weather_environments"] = weather["_EnvironmentFlags"].split("|")
        gimmicks[name]["weather_repop"] = weather["_IsEnableEnvironmentRepop"]

    return gimmicks

gimmick_data = Parser2(parse_gimmicks, MSG_FILES, base, msg_ext="").parse()
with open('wilds/data/gimmickdata.json', 'w') as f:
    json.dump(gimmick_data, f, ensure_ascii=False, indent=4)

