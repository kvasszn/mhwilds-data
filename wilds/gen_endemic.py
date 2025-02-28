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
from gen_em import *

BASE = os.environ["BASE"]

MSG_FILES = ["combined_msgs.json"]

VERSIONS = {
    "poglst": 0,
    "pog": 10,
}

def get_stage_endemic_pop(stage_id):
    path = os.path.join(BASE, f"natives/STM/GameDesign/Stage/{stage_id}/Layout/Loaded/Animal/PointGraph/{stage_id}_AnimalPopAreaLayoutList.poglst.{VERSIONS["poglst"]}.json")

    if not os.path.exists(path):
        return [], []
    f = open(path)
    poglist = json.load(f)["paths"]
    points = {}
    if not os.path.exists("wilds/data/map_nums"):
        os.makedirs("wilds/data/map_nums")
    for pogpath in poglist:
        pogpath = os.path.join(BASE, "natives/STM/", pogpath) + f".{VERSIONS["pog"]}.json"
        if not os.path.exists(pogpath):
            continue
        f = open(pogpath)
        pog = json.load(f)['nodes']
        info = pog[1][0]
        id = info["rsz"]["_EmId"]
        points[id] = {
            "target": info["rsz"]["_TargetInfo"],
            "points": [],
        }
        for val in pog[0]:
            point = val["rsz"]["v1"]
            point = struct.unpack('<4f', bytes(point))
            points[id]["points"].append(point[0:3])
    return points


def get_stage_endemic_context(stage_id):
    path = os.path.join(BASE, f"natives/STM/GameDesign/Stage/{stage_id}/Layout/Loaded/Animal/PointGraph/{stage_id}_AnimalContextLayoutList.poglst.{VERSIONS["poglst"]}.json")

    if not os.path.exists(path):
        return {}
    f = open(path)
    poglist = json.load(f)["paths"]
    points = {}
    if not os.path.exists("wilds/data/map_nums"):
        os.makedirs("wilds/data/map_nums")
    for pogpath in poglist:
        f = open(os.path.join(BASE, "natives/STM/", pogpath) + f".{VERSIONS["pog"]}.json")
        pog = json.load(f)['nodes']
        info = pog[1][0]
        id = info["rsz"]["_EmId"]
        points[id] = []
        for val in pog[0]:
            point = val["rsz"]["v1"]
            point = struct.unpack('<4f', bytes(point))
            points[id].append(point[0:3])
    return points

def get_endemic_pog(stage_id):
    pop_points = get_stage_endemic_pop(stage_id)
    context_points = get_stage_endemic_context(stage_id)
    return pop_points, context_points


def save_endemic():
    endemic = {}
    enemies = get_enemies()
    stages = ["st101"]
    stage_endemic = {}
    for stage in stages:
        pop_points, context_points = get_endemic_pog(stage)
        for e, v in pop_points.items():
            if not enemies.get(e):
                continue

            # initialize endemic life if its not already in
            enemy = enemies[e]
            if not endemic.get(e):
                endemic[e] = {
                        "name": enemy["name"],
                        "explain": enemy["explain"],
                        "memo": enemy["memo"],
                        "name_langs": enemy["name_langs"],
                        "explain_langs": enemy["explain_langs"],
                        "memo_langs": enemy["memo_langs"],
                        "color": enemy["color"],
                        "item_icon": enemy["item_icon"],
                        "map_icon": enemy["map_icon"],
                        "animal_icon": enemy["animal_icon"],
                        "reward_data": enemy["reward_data"],
                    }

            # add stage data
            if not endemic[e].get(stage):
                endemic[e][stage] = {}
            category = v["target"]["_Category"]
            endemic[e][stage] = {
                "target": {
                    "category": category,
                },
                "points": v["points"],
            }
            if category == "GIMMICK":
                endemic[e][stage]["target"]["gimmicks"] = v["target"]["_Param"]["_GmIds"]

        for e, v in context_points.items():
            if not enemies.get(e):
                continue
            enemy = enemies[e]
            params = None
            if not endemic.get(e):
                endemic[e] = {
                        "name": enemy["name"],
                        "explain": enemy["explain"],
                        "memo": enemy["memo"],
                        "name_langs": enemy["name_langs"],
                        "explain_langs": enemy["explain_langs"],
                        "memo_langs": enemy["memo_langs"],
                        "color": enemy["color"],
                        "item_icon": enemy["item_icon"],
                        "map_icon": enemy["map_icon"],
                        "animal_icon": enemy["animal_icon"],
                        "reward_data": enemy["reward_data"],
                    }
            if not endemic[e].get(stage):
                endemic[e][stage] = {"points": []}
            endemic[e][stage]["points"] += v
        
    with open(f"wilds/data/endemic.json", 'w') as f:
        json.dump(endemic, f, indent=4)

save_endemic()
