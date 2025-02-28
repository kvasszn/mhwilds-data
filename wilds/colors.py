import os
import io

WILDS_COLOR_IDX_MAP = {
        "I_NONE": 0,
        "I_WHITE": 1,
        "I_GRAY": 2,
        "I_ROSE": 3,
        "I_PINK": 4,
        "I_RED": 5,
        "I_VERMILION": 6,
        "I_ORANGE": 7,
        "I_BROWN": 8,
        "I_IVORY": 9,
        "I_YELLOW": 10,
        "I_LEMON": 11,
        "I_SGREEN": 12,
        "I_MOS": 13,
        "I_GREEN": 14,
        "I_EMERALD": 15,
        "I_SKY": 16,
        "I_BLUE": 17,
        "I_ULTRAMARINE": 18,
        "I_BPURPLE": 19,
        "I_PURPLE": 20,
        "I_DPURPLE": 21,
        "RARE_01": 22,
        "RARE_02": 23,
        "RARE_03": 24,
        "RARE_04": 25,
        "RARE_05": 26,
        "RARE_06": 27,
        "RARE_07": 28,
        "RARE_08": 29,
        "RARE_09": 30,
        "RARE_10": 31,
        "RARE_11": 32,
        "RARE_12": 33,
        "Rank_Prog00": 34,
        "Rank_Prog01": 35,
        "Rank_Prog02": 36,
        "Rank_Prog03": 37,
        "TXT_White01": 38,
        "TXT_White02": 39,
        "TXT_White03": 40,
        "TXT_Gray01": 41,
        "TXT_Black01": 42,
        "TXT_Safe": 43,
        "TXT_Danger": 44,
        "TXT_Accent": 45,
        "TXT_Accent2": 46,
        "TXT_Accent3": 47,
        "TXT_Sub": 48,
        "TXT_Max": 49,
        "TXT_CharaName": 50,
        "TXT_Choice_01": 51,
        "TXT_Choice_02": 52,
        "TXT_Title": 53,
        "TXT_currency00num": 54,
        "TXT_currency00unit": 55,
        "TXT_currency01num": 56,
        "TXT_currency01unit": 57,
        "TXT_currency02num": 58,
        "TXT_currency02unit": 59,
        "TXT_currency03num": 60,
        "TXT_currency03unit": 61,
        "GUI_White": 62,
        "GUI_Black": 63,
        "GUI_Disable": 64,
        "GUI_Safe": 65,
        "GUI_Danger": 66,
        "GUI_Acrtive01": 67,
        "GUI_Acrtive02": 68,
        "GUI_DShadow": 69,
        "GUI_Psolo": 70,
        "GUI_P1": 71,
        "GUI_P2": 72,
        "GUI_P3": 73,
        "GUI_P4": 74,
        "GUI_PNPC": 75,
        "GUI_PStealth": 76,
        "GUI_Tab00": 77,
        "GUI_Tab01": 78,
        "GUI_Tab02": 79,
        "GUI_Tab03": 80,
        "GUI_Tab04": 81,
        "GUI_Tab05": 82,
        "GUI_Tab06": 83,
        "GUI_MapEmWarningLv1": 84,
        "GUI_MapEmWarningLv2": 85,
        "GUI_MapEmWarningLv3": 86,
        "GUI_MapEmWarningLv4": 87,
        "GUI_MapEmWarningLv5": 88,
        "GUI_Sharp00": 89,
        "GUI_Sharp01": 90,
        "GUI_Sharp02": 91,
        "GUI_Sharp03": 92,
        "GUI_Sharp04": 93,
        "GUI_Sharp05": 94,
        "GUI_Sharp06": 95,
        "GUI_LSword_Spr00": 96,
        "GUI_LSword_Spr01": 97,
        "GUI_LSword_Spr02": 98,
        "GUI_Insect_Ext00": 99,
        "GUI_Insect_Ext01": 100,
        "GUI_Insect_Ext02": 101,
        "GUI_Insect_Ext03": 102,
        "GUI_Insect_Ext02_2": 103,
        "GUI_Horn_Note00": 104,
        "GUI_Horn_Note01": 105,
        "GUI_Horn_Note02": 106,
        "GUI_Horn_Note03": 107,
        "GUI_Horn_Note04": 108,
        "GUI_Horn_Note05": 109,
        "GUI_Horn_Note06": 110,
        "GUI_Horn_Note07": 111,
        "GUI_Horn_Activation": 112,
        "GUI_Horn_ActivationAdd": 113,
        "MAX": 114
}

def read_colors(base):
    path = "natives/STM/GUI/colorPreset.gcp.2"
    f = open(os.path.join(base, path), 'rb')
    colors = []
    data = io.BytesIO(f.read())
    ver = data.read(4)
    magic = data.read(4)
    n = int.from_bytes(data.read(8)[::-1])

    for _ in range(1, n):
        sub_colors = [
                (
                int.from_bytes(data.read(1)),
                int.from_bytes(data.read(1)),
                int.from_bytes(data.read(1)),
                int.from_bytes(data.read(1))
                )
                for _ in range(4)]
        unk = data.read(4)
        null = data.read(4)

        guid = data.read(16)
        colors.append(sub_colors[0])
    return colors

base = os.environ["BASE"]
COLORS = read_colors(base)
