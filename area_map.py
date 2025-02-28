import matplotlib.pyplot as plt
import numpy as np
import json
from mpl_toolkits.mplot3d import Axes3D
import os
import struct

from vispy.visuals.visual import VisualShare

BASE = os.environ["BASE"]

def get_landmarks():
    f = open(os.path.join(BASE, "../wilds_bench/natives/STM/GameDesign/NPC/Partner/CommonData/SituationSpeech/NPCLandmarkPointData.user.3.json"))
    landmarks = json.load(f)["app.user_data.NpcLandMarkPointData"]["_DataList"]
    lm_points = []
    lm_names = []
    for l in landmarks:
        point = l["_Point"]
        lm_points.append((point[0], point[1],point[2]))
        lm_names.append(l["_LandMarkType"])
    return lm_points, lm_names

def area_map():
    do_3d = True
    fig = None
    ax = None
    if do_3d:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig, ax = plt.subplots(figsize=(10, 10))


    label="npc landmarks"
    points, names = get_landmarks()
    plot_points(points, names, ax, do_3d, label)

    f = open(os.path.join(BASE, "natives/STM/GameDesign/gui/gui060000/model/_userdata/mapstagedrawdata.user.3.json"))
    data = json.load(f)
    positions = []
    names = []

    for map in data["app.user_data.MapStageDrawData"]["_DrawDatas"]:
        areas = map["_AreaIconPosList"]
        positions.append([])
        names.append([])
        label = map["_StageFixedID"]
        for area in areas:
            pos = area["_AreaIconPos"]
            name = area['_AreaID'].split('_')
            #positions[-1].append(( pos[0], pos[1], pos[2]))
            names[-1].append(name[-1])
        for area in map["_BorderIconSetList"]:
            pos = area["_IconPos"]
            #positions[-1].append((pos[0], pos[1], pos[2]))
            names[-1].append(label + "-to-" +area["_ConnectStage"])
        if positions[-1] != []:
            x, y, z = zip(*positions[-1])
            if do_3d:
                points=(x, y, z)
            else:
                points=(z, x)
            ax.scatter(*points, s=100, label=label)
            for i, p in enumerate(zip(*points)):
                if names[-1][i] != "INVALID":
                    ax.text(*p, s=f"{names[-1][i]}", fontsize=6, ha='center', va='center')
                else:
                    ax.text(*p, s=f"{i + 1}", fontsize=6, ha='center', va='center')

    points = []
    names = []
    for root, paths, files in os.walk(os.path.join(BASE, "../wilds_bench/natives/STM/GameDesign/Player/Layout")):
        for file in files:
            print(file)
            if "Quest" in file or "Return" in file or "poglst" in file:
                continue
            f = open(os.path.join(root, file))
            data = json.load(f)
            #point = data["points"][0]["a"]#[0][0]["rsz"]["v1"]
            point = data["nodes"][0][0]["rsz"]["v1"]
            point = struct.unpack('<4f', bytes(point))
            points.append(point[0:3])
            names.append(data["nodes"][1][0]["rsz"]["_LayoutID"])
    #print(points, names)
    plot_points(points, names, ax, do_3d, label)

    points, names = getpog()
    plot_points(points, names, ax, do_3d, label)


    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    if do_3d:
        ax.set_zlabel("Z Axis")
        ax.view_init(elev=0, azim=-90)
    ax.legend()
    plt.show()


def getpog():
    f = open(os.path.join(BASE, "natives/STM/GameDesign/Stage/st101/Layout/Loaded/Gimmick/PointGraph/st101_Pointlist_Gimmick.poglst.0.json"))
    poglist = json.load(f)["paths"]
    pog_ver = 10
    base = os.path.join(BASE, "natives/STM/")
    points = []
    names = []
    for pogpath in poglist:
        f = open(os.path.join(base, pogpath.lower()) + f".{pog_ver}.json")
        pog = json.load(f)
        if pog[0][0]["type"] != "app.point_graph_data.ContextLayoutGimmick":
            continue
        for val in pog[0]:
            point = val["rsz"]["v1"]
            gmid = val["rsz"]["_GmID"]
            #if "GM003" not in gmid:
            #    continue
            point = struct.unpack('<4f', bytes(point))
            points.append(point[0:3])
            names.append(gmid)
    return points, names

def plot_points(points, names, ax, do_3d, label):
    x, y, z = zip(*points)
    if do_3d:
        points=(x, y, z)
    else:
        points=(z, x)
    ax.scatter(*points, s=100, label=label)
    for i, p in enumerate(zip(*points)):
        ax.text(*p, s=f"{names[i]}", fontsize=8, ha='center', va='center')

import vispy
from vispy import app, scene, io
from vispy.visuals.transforms import STTransform
from vispy.io import load_data_file, read_png

def pog():
    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    cam = scene.cameras.TurntableCamera(
        parent=view.scene, fov=60.0, azimuth=-42.0, elevation=30.0
    )
    view.camera = cam

    axis = scene.visuals.XYZAxis(parent=view)
    s = STTransform(translate=(50, 50), scale=(50, 50, 50, 1))
    affine = s.as_matrix()
    axis.transform = affine

    f = open("wilds/data/gimmickdata.json")
    gimmick_data = json.load(f)
    points, names = getpog()

    for i in range(len(points)):
        tex = f"wilds/data/gimmick_icons/MHWilds-{names[i]} Map Icon.png"
        point = points[i]
        if os.path.exists(tex):
            img_data = read_png(tex)
            image = scene.visuals.Image(img_data, interpolation='nearest', parent=view.scene, method='subdivide')
            transform = scene.transforms.STTransform(translate=(point[0], point[2], point[1]), scale=(0.35, 0.35, 1))
            rotation = scene.transforms.MatrixTransform()
            rotation.rotate(90, (0, 0, 1))
            image.transform = rotation * transform
            continue

        if gimmick := gimmick_data.get(names[i]):
            if not gimmick.get("icon"):
                continue
            tex = f"wilds/data/gimmick_icons/MHWilds-{gimmick["icon"]} Icon {gimmick["color"]}.png"
            if os.path.exists(tex):
                img_data = read_png(tex)
                image = scene.visuals.Image(img_data, interpolation='nearest', parent=view.scene, method='subdivide')
                transform = scene.transforms.STTransform(translate=(point[0], point[2], point[1]), scale=(0.2, 0.2, 1))
                rotation = scene.transforms.MatrixTransform()
                rotation.rotate(90, (0, 0, 1))
                image.transform = rotation * transform
                continue

            # Set 2D camera (the camera will scale to the contents in the scene)

    view.camera = scene.cameras.TurntableCamera()
# flip y-axis to have correct aligment
    #view.camera.flip = (0, 1, 0)
    #view.camera.set_range()
    #view.camera.zoom(0.1, (800, 800))

    canvas.show()
    app.run()


#pog()
area_map()

points, names = getpog()
with open("./gimmick_points.json", 'w') as f:
    json.dump({"points": points, "names": names}, f)
