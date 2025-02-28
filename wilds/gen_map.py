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

VERSIONS = {
    "poglst": 0,
    "pog": 10,
}

STAGE_COLORS = {
    "ST101": [0xe8, 0xe0, 0x89],
    "ST102": [0x68, 0xd9, 0x75],
    "ST103": [0xeb, 0x81, 0x44],
    "ST104": [0x75, 0xc7, 0xe0],
    "ST105": [0xff, 0xff, 0xff],
    "ST201": [0xff, 0xff, 0xff],
}

def save_map_area_number(stagearea_id, stage="ST101"):
    num = stagearea_id.split('_')[-1]
    if num == "INVALID":
        return
    digits = [int(d) for d in str(int(num))]
    texs = [MAP_NUMS[d] for d in digits]
    #texs = [tex.crop((50, 0, tex.width - 50, tex.height)) for tex in texs]
    tex = combine_images_horz(texs, 0)
    tex = multiply_image_by_color(tex, STAGE_COLORS[stage])
    tex.save(os.path.join("wilds/data/map_nums", stagearea_id + ".png"))

def get_stage_area():
    f = open(os.path.join(BASE, "natives/STM/GameDesign/GUI/GUI060000/Model/_UserData/MapStageDrawData.user.3.json"))
    data = json.load(f)
    points = {}

    for map in data[0]["rsz"]["_DrawDatas"]:
        areas = map["_AreaIconPosList"]
        label = map["_StageFixedID"]
        if points.get(label) is None:
            points[label] = {}
        for area in areas:
            pos = area["_AreaIconPos"]
            #name = area['_AreaID']
            num = area['_DrawAreaNum']
            name = label.lower() + "_" + str(num).rjust(2, '0')
            points[label][name] = pos
            save_map_area_number(name, stage=label)
    return points


def get_stage_area_pog(stage_id):
    path = os.path.join(BASE, f"natives/STM/GameDesign/Stage/{stage_id}/Layout/Loaded/Stage/PointGraph/{stage_id}_ZoneAreaFeild_poglst.poglst.{VERSIONS["poglst"]}.json")

    if not os.path.exists(path):
        return [], []
    f = open(path)
    poglist = json.load(f)["paths"]
    base = os.path.join(BASE, "natives/STM/")
    points = {}
    if not os.path.exists("wilds/data/map_nums"):
        os.makedirs("wilds/data/map_nums")
    for pogpath in poglist:
        f = open(os.path.join(base, pogpath) + f".{VERSIONS["pog"]}.json")
        pog = json.load(f)['nodes']
        for val in pog[0]:
            point = val["rsz"]["v1"]
            id = val["rsz"]["_AreaIdSerializable"]
            point = struct.unpack('<4f', bytes(point))
            points[id] = point[0:3]
            #points.append(point[0:3])
            #names.append(id)
            save_map_area_number(id)
    return points

def save_map():
    #points = get_stage_area_pog(stage_id)
    points = get_stage_area()
    with open(f"wilds/data/map_area_points.json", 'w') as f:
        json.dump(points, f, indent=4)


#points, names = get_stage_area_pog("st101")
#points, names = get_stage_area_pog("st201")
#points, names = get_stage_area_pog("st503")
save_map()
