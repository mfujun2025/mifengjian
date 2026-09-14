# -*- coding: utf-8 -*-
"""
生成 密封件.cn 站点的数据文件。
数据来源：GB/T 3452.1-2005《液压气动用O形橡胶密封圈 第1部分：尺寸系列及公差》
（等同采用 ISO 3601-1）G 系列（一般应用）。

输出：
  data/o-ring-specs.json      O 型圈规格全集
  data/materials.json         材质参数与耐介质矩阵
  data/media.json             介质清单
  data/selection-rules.json   选型规则（温度档 / 硬度推荐 / 工况修正）
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

# ---------------------------------------------------------------- 截面系列
# GB/T 3452.1-2005 G 系列的 5 个截面（线径）尺寸
CS_TOL = {1.8: 0.08, 2.65: 0.09, 3.55: 0.10, 5.3: 0.13, 7.0: 0.15}

# ---------------------------------------------------------------- 内径系列
# (内径 d1, 该内径在标准中包含的截面组合)
ID_SERIES = [
    (1.8, [1.8]), (2.0, [1.8]), (2.24, [1.8]), (2.5, [1.8]), (2.8, [1.8]),
    (3.15, [1.8]), (3.55, [1.8]), (3.75, [1.8]), (4.0, [1.8]), (4.5, [1.8]),
    (4.87, [1.8]), (5.0, [1.8]), (5.15, [1.8]), (5.3, [1.8]), (5.6, [1.8]),
    (6.0, [1.8]), (6.3, [1.8]), (6.7, [1.8]), (6.9, [1.8]),
    (7.1, [1.8, 2.65]), (7.5, [1.8, 2.65]), (8.0, [1.8, 2.65]), (8.5, [1.8, 2.65]),
    (8.75, [1.8, 2.65]), (9.0, [1.8, 2.65]), (9.5, [1.8, 2.65]), (10.0, [1.8, 2.65]),
    (10.6, [1.8, 2.65]), (11.2, [1.8, 2.65]), (11.8, [1.8, 2.65]), (12.5, [1.8, 2.65]),
    (13.2, [1.8, 2.65]), (14.0, [1.8, 2.65]), (15.0, [1.8, 2.65]), (16.0, [1.8, 2.65]),
    (17.0, [1.8, 2.65]),
    (18.0, [1.8, 2.65, 3.55]), (19.0, [1.8, 2.65, 3.55]), (20.0, [1.8, 2.65, 3.55]),
    (21.0, [1.8, 2.65, 3.55]), (22.4, [1.8, 2.65, 3.55]), (23.6, [1.8, 2.65, 3.55]),
    (25.0, [1.8, 2.65, 3.55]), (25.8, [1.8, 2.65, 3.55]), (26.5, [1.8, 2.65, 3.55]),
    (28.0, [1.8, 2.65, 3.55]), (30.0, [1.8, 2.65, 3.55]),
    (31.5, [2.65, 3.55, 5.3]), (32.5, [2.65, 3.55, 5.3]), (33.5, [2.65, 3.55, 5.3]),
    (34.5, [2.65, 3.55, 5.3]), (35.5, [2.65, 3.55, 5.3]), (36.5, [2.65, 3.55, 5.3]),
    (37.5, [2.65, 3.55, 5.3]), (38.7, [2.65, 3.55, 5.3]),
    (40.0, [2.65, 3.55, 5.3, 7.0]), (41.2, [2.65, 3.55, 5.3, 7.0]),
    (42.5, [2.65, 3.55, 5.3, 7.0]), (43.7, [2.65, 3.55, 5.3, 7.0]),
    (45.0, [2.65, 3.55, 5.3, 7.0]), (46.2, [2.65, 3.55, 5.3, 7.0]),
    (47.5, [2.65, 3.55, 5.3, 7.0]), (48.7, [2.65, 3.55, 5.3, 7.0]),
    (50.0, [2.65, 3.55, 5.3, 7.0]),
    (51.5, [3.55, 5.3, 7.0]), (53.0, [3.55, 5.3, 7.0]), (54.5, [3.55, 5.3, 7.0]),
    (56.0, [3.55, 5.3, 7.0]), (58.0, [3.55, 5.3, 7.0]), (60.0, [3.55, 5.3, 7.0]),
    (61.5, [3.55, 5.3, 7.0]), (63.0, [3.55, 5.3, 7.0]), (65.0, [3.55, 5.3, 7.0]),
    (67.0, [3.55, 5.3, 7.0]), (69.0, [3.55, 5.3, 7.0]), (71.0, [3.55, 5.3, 7.0]),
    (73.0, [3.55, 5.3, 7.0]), (75.0, [3.55, 5.3, 7.0]), (77.5, [3.55, 5.3, 7.0]),
    (80.0, [3.55, 5.3, 7.0]), (82.5, [3.55, 5.3]), (85.0, [3.55, 5.3, 7.0]),
    (87.5, [3.55, 5.3]), (90.0, [3.55, 5.3, 7.0]), (92.5, [3.55, 5.3]),
    (95.0, [3.55, 5.3, 7.0]), (97.5, [3.55, 5.3]), (100.0, [3.55, 5.3, 7.0]),
    (103.0, [3.55, 5.3]), (106.0, [3.55, 5.3, 7.0]), (109.0, [3.55, 5.3, 7.0]),
    (112.0, [3.55, 5.3, 7.0]),
    (115.0, [5.3, 7.0]), (118.0, [5.3, 7.0]), (122.0, [5.3, 7.0]),
    (125.0, [5.3, 7.0]), (128.0, [5.3, 7.0]), (132.0, [5.3, 7.0]),
    (136.0, [5.3, 7.0]), (140.0, [5.3, 7.0]), (145.0, [5.3, 7.0]),
    (150.0, [5.3, 7.0]), (155.0, [5.3, 7.0]), (160.0, [5.3, 7.0]),
    (165.0, [5.3, 7.0]), (170.0, [5.3, 7.0]), (175.0, [5.3, 7.0]),
    (180.0, [5.3, 7.0]),
    (185.0, [5.3, 7.0]), (190.0, [5.3, 7.0]), (195.0, [5.3, 7.0]),
    (200.0, [5.3, 7.0]), (206.0, [5.3, 7.0]), (212.0, [5.3, 7.0]),
    (218.0, [5.3, 7.0]), (224.0, [5.3, 7.0]), (230.0, [5.3, 7.0]),
    (236.0, [5.3, 7.0]), (243.0, [5.3, 7.0]), (250.0, [5.3, 7.0]),
    (258.0, [5.3, 7.0]), (265.0, [5.3, 7.0]), (272.0, [5.3, 7.0]),
    (280.0, [5.3, 7.0]), (290.0, [5.3, 7.0]), (300.0, [5.3, 7.0]),
    (307.0, [5.3, 7.0]), (315.0, [5.3, 7.0]), (325.0, [7.0]),
    (335.0, [7.0]), (345.0, [7.0]), (355.0, [7.0]), (365.0, [7.0]),
    (375.0, [7.0]), (387.0, [7.0]), (400.0, [7.0]),
]

# 内径公差分档（按 GB/T 3452.1-2005，单位 mm）
def id_tol(d1):
    if d1 <= 6.3:
        return 0.13
    if d1 <= 10.0:
        return 0.14
    if d1 <= 18.0:
        return 0.17
    if d1 <= 30.0:
        return 0.22
    if d1 <= 50.0:
        return 0.30
    if d1 <= 80.0:
        return 0.45
    if d1 <= 118.0:
        return 0.65
    if d1 <= 180.0:
        return 0.90
    if d1 <= 280.0:
        return 1.20
    if d1 <= 400.0:
        return 1.60
    return 2.10


def fmt(x):
    """去掉多余小数零：2.0 -> 2，2.65 -> 2.65"""
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s if s else "0"


def build_specs():
    rows = []
    for d1, css in ID_SERIES:
        for d2 in css:
            d3 = round(d1 + 2 * d2, 2)          # 外径 = 内径 + 2×截面
            rows.append({
                "id": "%sx%s" % (fmt(d1), fmt(d2)),
                "d1": d1,                        # 内径 mm
                "d2": d2,                        # 截面直径 mm
                "d3": d3,                        # 外径 mm
                "tol_d1": id_tol(d1),            # 内径公差 ±mm
                "tol_d2": CS_TOL[d2],            # 截面公差 ±mm
                "std": "GB/T 3452.1-2005",
                "series": "G",
            })
    rows.sort(key=lambda r: (r["d2"], r["d1"]))
    return rows


# ---------------------------------------------------------------- 介质清单
MEDIA = [
    {"id": "hydraulic_mineral", "name": "液压油（矿物型）", "cat": "油类", "note": "最常见的液压系统工作介质"},
    {"id": "engine_oil",        "name": "机油 / 润滑油",     "cat": "油类", "note": "发动机、齿轮箱用油"},
    {"id": "gasoline",          "name": "汽油",              "cat": "油类", "note": "含芳香烃，溶胀性强"},
    {"id": "diesel",            "name": "柴油",              "cat": "油类", "note": "含芳香烃，溶胀性强"},
    {"id": "aromatic",          "name": "芳香烃（苯/甲苯/二甲苯）", "cat": "溶剂", "note": "强溶剂，对多数橡胶溶胀明显"},
    {"id": "ketone",            "name": "酮类（丙酮/丁酮）",  "cat": "溶剂", "note": "极性溶剂，溶胀极强"},
    {"id": "ester",             "name": "酯类（合成酯油/酯型溶剂）", "cat": "溶剂", "note": "合成酯液压油、酯类清洗剂"},
    {"id": "alcohol",           "name": "醇类（乙醇/甲醇）",  "cat": "溶剂", "note": "甲醇汽油、酒精类介质"},
    {"id": "phosphate_ester",   "name": "磷酸酯液压油",      "cat": "油类", "note": "航空、电厂抗燃液压油"},
    {"id": "brake_fluid",       "name": "刹车油（DOT3/DOT4 醇醚型）", "cat": "油类", "note": "汽车制动系统"},
    {"id": "water_cold",        "name": "水（常温）",        "cat": "水/汽", "note": "自来水、冷却水"},
    {"id": "steam_hot_water",   "name": "热水 / 蒸汽",       "cat": "水/汽", "note": "≥100℃ 热水或饱和蒸汽"},
    {"id": "air",               "name": "空气 / 压缩空气",   "cat": "气体", "note": "气动系统、真空场合"},
    {"id": "ozone",             "name": "臭氧",              "cat": "气体", "note": "户外老化、电气环境"},
    {"id": "glycol",            "name": "乙二醇冷却液 / 防冻液", "cat": "水/汽", "note": "发动机冷却系统"},
    {"id": "hfc",               "name": "HFC 制冷剂（R134a 等）", "cat": "气体", "note": "汽车空调、制冷设备"},
    {"id": "acid_dilute",       "name": "稀酸",              "cat": "酸碱", "note": "稀硫酸、稀盐酸等"},
    {"id": "alkali_strong",     "name": "强碱（氢氧化钠等）",  "cat": "酸碱", "note": "碱洗、脱脂工序"},
    {"id": "ammonia",           "name": "氨 / 胺类",          "cat": "酸碱", "note": "制冷氨、胺类添加剂"},
    {"id": "perfluoro_solvent", "name": "全氟溶剂",          "cat": "溶剂", "note": "氟化溶剂、部分清洗剂"},
]

# ---------------------------------------------------------------- 材质数据
# temp: 长期工作温度区间（℃）；peak: 短时可承受上限
# good: 耐（推荐）；bad: 不耐（排除并给出原因）；mid: 未列入时按"需验证"处理
MATERIALS = [
    {
        "code": "NBR", "name": "丁腈橡胶", "en": "Nitrile Rubber",
        "temp_min": -30, "temp_max": 100, "peak": 120,
        "hardness_range": "70~90 Shore A",
        "color": "黑色（亦可配色）",
        "price_level": "低",
        "good": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "water_cold", "air", "glycol", "hfc"],
        "bad": ["ketone", "ester", "phosphate_ester", "brake_fluid", "ozone", "steam_hot_water", "acid_dilute", "alkali_strong"],
        "bad_reason": {
            "ketone": "酮类对丁腈溶胀极强，体积膨胀可达 20% 以上",
            "ester": "酯类会显著溶胀丁腈，导致硬度与强度下降",
            "phosphate_ester": "磷酸酯液压油会溶解丁腈，属典型不兼容组合",
            "brake_fluid": "醇醚型刹车油会溶胀丁腈，必须改用 EPDM",
            "ozone": "丁腈双键含量高，极易被臭氧老化开裂",
            "steam_hot_water": "高温水/蒸汽会使丁腈快速水解老化",
            "acid_dilute": "耐酸性差，长期接触会硬化开裂",
            "alkali_strong": "耐碱性差，强碱环境下迅速劣化",
        },
        "summary": "性价比最高的通用耐油橡胶。耐矿物油、汽油、柴油性能优异，是液压与燃油系统的主力材质；缺点是耐臭氧、耐候性差，不耐酮酯类溶剂，高温上限仅约 100℃。",
    },
    {
        "code": "HNBR", "name": "氢化丁腈橡胶", "en": "Hydrogenated Nitrile",
        "temp_min": -40, "temp_max": 150, "peak": 165,
        "hardness_range": "70~90 Shore A",
        "color": "黑色 / 绿色",
        "price_level": "中高",
        "good": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "water_cold", "air", "ozone", "glycol", "hfc", "acid_dilute"],
        "bad": ["ketone", "ester", "phosphate_ester", "brake_fluid", "steam_hot_water"],
        "bad_reason": {
            "ketone": "酮类为极性强溶剂，会溶胀氢化丁腈",
            "ester": "酯类会造成明显溶胀",
            "phosphate_ester": "与磷酸酯液压油不兼容",
            "brake_fluid": "醇醚型刹车油会溶胀，应改用 EPDM",
            "steam_hot_water": "长期高温水/蒸汽会导致水解老化",
        },
        "summary": "丁腈的升级版。把丁腈分子链上的双键加氢饱和后，耐臭氧、耐候、耐热性大幅提升，工作温度可达 150℃，同时保留了对矿物油、燃油的良好耐受，是汽车动力总成与油田设备的高性价比选择。",
    },
    {
        "code": "EPDM", "name": "三元乙丙橡胶", "en": "EPDM",
        "temp_min": -50, "temp_max": 150, "peak": 180,
        "hardness_range": "60~90 Shore A",
        "color": "黑色 / 彩色",
        "price_level": "低",
        "good": ["water_cold", "steam_hot_water", "ozone", "alcohol", "ketone", "acid_dilute", "alkali_strong", "glycol", "hfc", "phosphate_ester", "brake_fluid", "air"],
        "bad": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "aromatic", "ester"],
        "bad_reason": {
            "hydraulic_mineral": "乙丙橡胶属非极性橡胶，遇矿物油迅速溶胀失效——这是最常见的选型错误",
            "engine_oil": "机油等矿物系油品会造成严重溶胀",
            "gasoline": "汽油溶胀极强，不可用于燃油系统",
            "diesel": "柴油会造成严重溶胀",
            "aromatic": "芳香烃溶剂会剧烈溶胀乙丙橡胶",
            "ester": "酯类介质会造成溶胀",
        },
        "summary": "耐水、耐蒸汽、耐候之王。户外使用寿命长，耐臭氧、耐老化性能在所有通用橡胶中最好，同时耐醇类、酮类、酸碱与磷酸酯液压油；唯一致命短板是绝不耐矿物油，选型时务必确认介质类型。",
    },
    {
        "code": "SI", "name": "硅橡胶（VMQ）", "en": "Silicone Rubber",
        "temp_min": -60, "temp_max": 200, "peak": 230,
        "hardness_range": "40~80 Shore A",
        "color": "红色 / 透明 / 白色",
        "price_level": "中",
        "good": ["air", "ozone", "water_cold", "alcohol", "hfc", "glycol"],
        "bad": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "aromatic", "ester", "steam_hot_water", "acid_dilute", "alkali_strong", "phosphate_ester"],
        "bad_reason": {
            "hydraulic_mineral": "硅橡胶耐矿物油性差，会明显溶胀且强度下降——高温液压场合切忌选硅橡胶",
            "engine_oil": "机油会造成溶胀、力学性能下降",
            "gasoline": "汽油溶胀严重",
            "diesel": "柴油溶胀严重",
            "aromatic": "芳香烃会溶胀并破坏强度",
            "ester": "酯类会造成溶胀",
            "steam_hot_water": "高温蒸汽会使硅橡胶迅速降解",
            "acid_dilute": "耐酸性差",
            "alkali_strong": "耐碱性差",
            "phosphate_ester": "与磷酸酯液压油不兼容",
        },
        "summary": "温域最宽的通用橡胶（-60~200℃），弹性好、耐臭氧耐候、无毒无味，广泛用于食品医疗与电气密封；但机械强度低、耐油性差，绝不能用在与矿物油、燃油接触的场合。",
    },
    {
        "code": "FVMQ", "name": "氟硅橡胶", "en": "Fluorosilicone",
        "temp_min": -60, "temp_max": 200, "peak": 225,
        "hardness_range": "60~80 Shore A",
        "color": "蓝色 / 黑色",
        "price_level": "高",
        "good": ["gasoline", "diesel", "aromatic", "air", "ozone", "hfc"],
        "bad": ["ketone", "ester", "brake_fluid", "steam_hot_water", "alkali_strong", "ammonia"],
        "bad_reason": {
            "ketone": "酮类会溶胀氟硅橡胶",
            "ester": "酯类会造成溶胀",
            "brake_fluid": "醇醚型刹车油不兼容",
            "steam_hot_water": "高温水/蒸汽会破坏氟硅结构",
            "alkali_strong": "强碱会侵蚀氟硅橡胶",
            "ammonia": "氨/胺类会造成劣化",
        },
        "summary": "兼顾低温与耐油。把硅橡胶的部分甲基换成三氟丙基后，耐油性明显改善，同时保留 -60℃ 的低温弹性，常用于航空燃油系统与低温液压场合；价格高、耐酮酯性仍不足。",
    },
    {
        "code": "FKM", "name": "氟橡胶（Viton）", "en": "Fluoroelastomer / Viton",
        "temp_min": -20, "temp_max": 200, "peak": 230,
        "hardness_range": "70~90 Shore A",
        "color": "黑色 / 棕色 / 绿色",
        "price_level": "高",
        "good": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "aromatic", "air", "ozone", "acid_dilute", "hfc"],
        "bad": ["ketone", "ester", "brake_fluid", "steam_hot_water", "alkali_strong", "ammonia", "phosphate_ester"],
        "bad_reason": {
            "ketone": "酮类是氟橡胶的典型不兼容介质，会造成溶胀降解",
            "ester": "低分子酯类会侵蚀氟橡胶",
            "brake_fluid": "DOT3/DOT4 醇醚型刹车油不兼容，应改用 EPDM",
            "steam_hot_water": "高温水/蒸汽会使氟橡胶脱氟降解",
            "alkali_strong": "强碱会侵蚀氟橡胶",
            "ammonia": "氨/胺类会造成氟橡胶劣化",
            "phosphate_ester": "与磷酸酯液压油不兼容",
        },
        "summary": "高温耐油的标准答案。耐 200℃、耐几乎所有矿物油与燃油、耐芳香烃与多数化学品，耐候与耐臭氧优异，被广泛用于发动机、液压、化工密封；但对酮类、酯类、热水蒸汽、强碱与氨类不兼容，低温弹性也一般（约 -20℃）。",
    },
    {
        "code": "FFKM", "name": "全氟醚橡胶", "en": "Perfluoroelastomer",
        "temp_min": -20, "temp_max": 300, "peak": 320,
        "hardness_range": "70~90 Shore A",
        "color": "黑色 / 白色",
        "price_level": "极高",
        "good": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "aromatic", "ketone", "ester", "acid_dilute", "alkali_strong", "steam_hot_water", "ammonia", "hfc", "ozone", "air", "alcohol", "glycol", "brake_fluid", "phosphate_ester", "perfluoro_solvent"],
        "bad": [],
        "bad_reason": {},
        "summary": "耐介质性天花板。几乎耐受所有已知化学品与溶剂，工作温度可达 300℃，弹性与密封性远优于聚四氟乙烯，是半导体、化工、制药与航空航天极端工况的首选；唯一的问题是价格，通常是氟橡胶的十倍以上。",
    },
    {
        "code": "PTFE", "name": "聚四氟乙烯（包覆圈）", "en": "PTFE",
        "temp_min": -60, "temp_max": 260, "peak": 280,
        "hardness_range": "—（塑料，靠内芯提供弹性）",
        "color": "白色 / 本色",
        "price_level": "高",
        "good": ["hydraulic_mineral", "engine_oil", "gasoline", "diesel", "aromatic", "ketone", "ester", "acid_dilute", "alkali_strong", "steam_hot_water", "ammonia", "hfc", "ozone", "air", "alcohol", "glycol", "brake_fluid", "phosphate_ester", "perfluoro_solvent"],
        "bad": [],
        "bad_reason": {},
        "summary": "化学惰性极强、摩擦系数极低，几乎耐所有介质，常见形式是「PTFE 包覆 O 型圈」（外覆 PTFE 薄膜、内嵌氟橡胶或硅橡胶芯，兼顾耐介质与弹性）。注意 PTFE 本身是塑料、无弹性、存在冷流变形，纯 PTFE 圈只适用于静密封。",
    },
    {
        "code": "PU", "name": "聚氨酯橡胶", "en": "Polyurethane",
        "temp_min": -30, "temp_max": 80, "peak": 100,
        "hardness_range": "80~95 Shore A",
        "color": "琥珀色 / 透明",
        "price_level": "中",
        "good": ["hydraulic_mineral", "engine_oil", "air", "ozone", "glycol"],
        "bad": ["water_cold", "steam_hot_water", "ketone", "ester", "acid_dilute", "alkali_strong", "alcohol", "aromatic", "brake_fluid", "phosphate_ester"],
        "bad_reason": {
            "water_cold": "聚氨酯会水解，长期泡水会发软强度下降（耐水解牌号可短期应对）",
            "steam_hot_water": "高温水/蒸汽会迅速水解降解",
            "ketone": "酮类会溶解聚氨酯",
            "ester": "酯类会造成溶胀降解",
            "acid_dilute": "耐酸性差，会水解",
            "alkali_strong": "强碱会加速水解",
            "alcohol": "醇类会造成溶胀",
            "aromatic": "芳香烃会造成溶胀",
            "brake_fluid": "与醇醚型刹车油不兼容",
            "phosphate_ester": "与磷酸酯液压油不兼容",
        },
        "summary": "耐磨与抗挤出性能最强，机械强度、撕裂强度远高于普通橡胶，耐磨性是丁腈的 3 倍以上，广泛用于高压液压、气动与往复运动密封（如 Y 形圈、防尘圈）。短板是耐水解性差、耐温上限低（约 80℃），不适合热水、蒸汽与酸碱环境。",
    },
    {
        "code": "CR", "name": "氯丁橡胶", "en": "Neoprene / CR",
        "temp_min": -40, "temp_max": 120, "peak": 130,
        "hardness_range": "60~90 Shore A",
        "color": "黑色",
        "price_level": "低",
        "good": ["hydraulic_mineral", "engine_oil", "water_cold", "air", "ozone", "hfc", "glycol", "alcohol"],
        "bad": ["ketone", "ester", "aromatic", "phosphate_ester", "brake_fluid", "steam_hot_water"],
        "bad_reason": {
            "ketone": "酮类会溶胀氯丁橡胶",
            "ester": "酯类会造成溶胀",
            "aromatic": "芳香烃溶剂会显著溶胀",
            "phosphate_ester": "与磷酸酯液压油不兼容",
            "brake_fluid": "醇醚型刹车油不兼容",
            "steam_hot_water": "长期高温水/蒸汽会老化开裂",
        },
        "summary": "耐候耐臭氧性能仅次于乙丙橡胶，同时耐一般矿物油、耐制冷剂与耐燃性较好，常用于户外密封、制冷设备与胶管；耐低温性一般，对酮酯类溶剂不兼容。",
    },
]


def build_materials():
    media_ids = {m["id"] for m in MEDIA}
    out = []
    for m in MATERIALS:
        miss = [x for x in (m["good"] + m["bad"]) if x not in media_ids]
        assert not miss, "%s 引用了未知介质: %s" % (m["code"], miss)
        ov = set(m["good"]) & set(m["bad"])
        assert not ov, "%s 耐/不耐清单冲突: %s" % (m["code"], ov)
        mm = dict(m)
        mm["temp_span"] = "%d ~ %d ℃" % (m["temp_min"], m["temp_max"])
        out.append(mm)
    return out


# ---------------------------------------------------------------- 选型规则
RULES = {
    "note": "温度优先过滤，介质黑名单一票否决，无记录组合标注为「需实测验证」。",
    "hardness_guide": [
        {"scene": "静态密封（径向/端面静密封）", "hardness": "70 Shore A", "why": "压缩量大、贴合性好，密封可靠性高"},
        {"scene": "一般动态密封（往复速度 <0.5 m/s）", "hardness": "80 Shore A", "why": "兼顾弹性与耐磨"},
        {"scene": "高压液压动态密封（>16 MPa）", "hardness": "90 Shore A", "why": "抗挤出能力强，避免间隙挤出破坏"},
        {"scene": "真空 / 低压气动", "hardness": "60~70 Shore A", "why": "低硬度更容易在低压差下变形贴合"},
    ],
    "compression_guide": [
        {"scene": "静态端面密封", "rate": "20% ~ 25%"},
        {"scene": "静态径向密封", "rate": "15% ~ 20%"},
        {"scene": "往复动态密封", "rate": "12% ~ 18%"},
        {"scene": "旋转动态密封", "rate": "8% ~ 12%"},
    ],
    "temperature_bands": [
        {"band": "-60 ~ -20 ℃", "first": "SI / FVMQ", "alt": "PTFE 包覆圈", "note": "此温区可用材质极少，硅系是主力"},
        {"band": "-20 ~ 100 ℃", "first": "NBR", "alt": "HNBR / CR / PU", "note": "常规工业温区，丁腈性价比最优"},
        {"band": "100 ~ 150 ℃", "first": "HNBR", "alt": "FKM / EPDM（非油介质）", "note": "丁腈已到极限，需升级材质"},
        {"band": "150 ~ 200 ℃", "first": "FKM", "alt": "SI / FVMQ（非油介质）", "note": "氟橡胶的主场"},
        {"band": "200 ~ 300 ℃", "first": "FFKM", "alt": "PTFE 包覆圈", "note": "可选材质急剧收窄，成本大幅上升"},
    ],
    "selection_order": [
        "1. 先定介质：确认是否接触矿物油系油品（这一步排除掉一半材质）",
        "2. 再定温度：用长期工作温度而非峰值温度，峰值仅作短时参考",
        "3. 再看运动方式：静态、往复、旋转对硬度与压缩率要求不同",
        "4. 最后看压力与间隙：高压工况需提高硬度或加装挡圈防挤出",
        "5. 仍有两个以上候选时，按成本从低到高择优",
    ],
}


def main():
    os.makedirs(DATA, exist_ok=True)
    specs = build_specs()
    materials = build_materials()

    payload_specs = {
        "meta": {
            "title": "O 型圈规格尺寸表",
            "standard": "GB/T 3452.1-2005",
            "standard_full": "液压气动用O形橡胶密封圈 第1部分：尺寸系列及公差（等同 ISO 3601-1）",
            "series": "G 系列（一般应用）",
            "unit": "mm",
            "count": len(specs),
            "note": "外径 d3 = 内径 d1 + 2 × 截面直径 d2。公差为标称值，实际以标准原文与厂家实测为准。",
        },
        "specs": specs,
    }
    payload_materials = {"meta": {"count": len(materials), "updated": "2026-09"}, "materials": materials}
    payload_media = {"media": MEDIA}

    def dump(name, obj):
        p = os.path.join(DATA, name)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=1)
        print("  %-26s %6.1f KB" % (name, os.path.getsize(p) / 1024.0))

    dump("o-ring-specs.json", payload_specs)
    dump("materials.json", payload_materials)
    dump("media.json", payload_media)
    dump("selection-rules.json", RULES)

    ids = [s["id"] for s in specs]
    assert len(ids) == len(set(ids)), "存在重复规格"
    print("\n规格总数：%d 条" % len(specs))
    by_cs = {}
    for s in specs:
        by_cs[s["d2"]] = by_cs.get(s["d2"], 0) + 1
    print("按截面分布：" + "，".join("%smm=%d条" % (fmt(k), v) for k, v in sorted(by_cs.items())))
    print("材质：%d 种，介质：%d 种" % (len(materials), len(MEDIA)))


if __name__ == "__main__":
    main()
