"""Standard acting and camera beats for a Cycle 2 episode, generated from its dialogue (for tools/cycle2_patch.py).

Every Cycle 2 episode runs the same shape: hook line (the cop aims at something) -> explanation, with trips to the
episode's space world -> the punchline, after which the cop is crushed (shock, trombone, sad, the guy hands him a kulhad,
the end card) -> comment question to camera -> 1 s subscribe callout -> teaser (the cop aims at the next suspect) ->
the guy's loop line -> last shot matches frame 0. `standard(ep_dir, spec)` returns (act, shots, nums-free timing dict)
from assets/audio/lines.json and lines-voice.json; an episode can then edit any of it before calling build().

spec = {dur, space: [[in, out]], hook: target, tease: target, home_start: bool, screen: {hook, punch, cam, sub, tease},
        smug_lines: [ids], extra_shots: [...]}  Targets name points returned by the episode's skyAt(t).
"""
import json, os, re

SKY = {"guy": "AIM", "cam": "AIM", "down": "LOW"}  # anything else is a sky target: hand UP
CU_COP_AIM = {"look": [0.9, 2.75, 0.5], "dir": [-0.35, 0.02, 1]}
CU_COP = {"look": [1.0, 2.75, 0.5], "dir": [-0.35, 0.08, 1]}
CU_GUY = {"look": [-0.45, 2.3, 0.2], "dir": [0.3, 0.1, 1]}
TWO = {"look": [0.2, 2.2, 0.3], "dir": [0.04, 0.22, 1]}
SKY_WIDE = {"look": [0.3, 3.6, -0.5], "dir": [0.06, -0.1, 1]}


def in_space(t, space):
    return any(a <= t < b for a, b in space)


def standard(ep, spec):
    lines = json.load(open(os.path.join(ep, "assets/audio/lines.json"), encoding="utf-8"))
    voice = {l["id"]: l["prompt"] for l in json.load(open(os.path.join(ep, "lines-voice.json"), encoding="utf-8"))}
    D, space = spec["dur"], spec["space"]
    L = [{"id": l["id"], "who": l["speaker"], "a": l["words"][0]["start"], "b": l["words"][-1]["end"],
          "tag": re.match(r"\[(\w+)\]", voice[l["id"]]).group(1), "text": voice[l["id"]]} for l in lines]
    comment = next(l for l in L if "Comment" in l["text"])
    ci = L.index(comment)
    punch = L[ci - 1]
    tease = next(l for l in L if l["tag"] == "mysterious")
    loop = L[-1]
    first = L[0]
    T = round(punch["b"] + 0.08, 2)  # trombone
    C = round(comment["a"] - 0.1, 2)  # to camera
    S = round(comment["b"] + 0.05, 2)  # subscribe callout
    Z = round(tease["a"] - 0.05, 2)  # teaser
    P = round(loop["a"] - 0.05, 2)  # loop line
    k2 = {"pop": round(T + 0.2, 2), "give": round(T + 0.8, 2), "sipA": round(T + 1.12, 2), "sipB": round(min(T + 1.42, comment["a"] - 0.08), 2),
          "end": round(D - 1.0, 2)}
    home = lambda t: not in_space(t, space)
    hs = spec.get("home_start", True)
    low = set(spec.get("low", []))  # targets near the ground: hand LOW, no looking at the sky
    isSky = lambda n: n not in SKY and n not in low

    # ---- the cop: aim, hands, moods
    aim = [[0, spec["hook"]]]
    for l in L[1:ci - 1]:
        if not home(l["a"]):
            continue
        aim.append([round(l["a"] - 0.1, 2), "guy" if l["who"] == "guy" else spec["hook"]])
    aim += [[round(punch["a"] - 0.1, 2), "guy" if punch["who"] == "guy" else spec["hook"]], [T, "down"], [C, "cam"], [Z, spec["tease"]], [P, spec["hook"]]]
    clean = []
    for t, n in aim:  # drop repeats
        if not clean or clean[-1][1] != n:
            clean.append([t, n])
    aim = clean
    handR = []
    for t, n in aim:
        pos = "LOW" if n in low else SKY.get(n, "UP")
        if not handR:
            handR.append([0, pos])
        elif handR[-1][1] != pos:
            handR += [[round(t - 0.01, 2), handR[-1][1]], [round(t + 0.25, 2), pos, "back"]]
    handR.append([D, handR[-1][1]])
    fa = first["a"] if first["who"] == "cop" else 0.6
    handL = [[0, "HIP"]]
    if first["who"] == "cop" and home(first["a"]):
        handL += [[fa + 0.25, "HIP"], [fa + 0.4, "STOP", "back"], [min(first["b"], fa + 1.8), "STOP"], [min(first["b"], fa + 1.8) + 0.3, "HIP"]]
    handL += [[k2["give"] - 0.2, "HIP"], [k2["give"] - 0.05, "TAKE", "back"], [k2["give"] + 0.05, "TAKE"], [k2["sipA"] - 0.12, "HOLD"],
              [k2["sipA"], "SIP"], [k2["sipB"] - 0.1, "SIP"], [k2["sipB"], "HOLD"], [k2["end"], "HOLD"], [k2["end"] + 0.4, "HIP"]]
    shock0 = round(max(punch["a"] + 0.3, T - 1.3), 2)
    lid = [[0, -0.75], [shock0 - 0.1, -0.75], [shock0, -1.8, "snap"], [T, -1.8], [T + 0.3, 0.35], [k2["give"] - 0.2, 0.35], [k2["give"] - 0.05, -0.9],
           [k2["sipA"] - 0.05, -0.9], [k2["sipA"], 1.1], [k2["sipB"] - 0.1, 1.1], [k2["sipB"], -0.75], [D, -0.75]]
    mood = {"shout": [first["a"]] if first["who"] == "cop" else [], "shock": [[shock0, T]], "sad": [[T, k2["give"] - 0.15]],
            "sheepish": [[k2["give"] - 0.15, C]], "sip": [[k2["sipA"], k2["sipB"]]], "toCam": [[C, Z]],
            "confused": [], "suspicious": [], "smug": [], "lookSky": []}
    for l in L[1:ci]:
        if l["who"] != "cop" or not home(l["a"]):
            continue
        key = {"confused": "confused", "curious": "confused", "surprised": "confused", "suspicious": "suspicious", "smug": "smug", "stern": "smug"}.get(l["tag"])
        if key:
            mood[key].append([round(l["a"] - 0.1, 2), round(l["b"] + 0.1, 2)])
    first_guy = next(l for l in L if l["who"] == "guy")
    if isSky(spec["hook"]):
        mood["lookSky"].append([-1, round(first_guy["a"] - 0.1, 2)])
    if isSky(spec["tease"]):
        mood["lookSky"].append([Z + 0.1, round(tease["b"] + 0.2, 2)])
    if isSky(spec["hook"]):
        mood["lookSky"].append([round(D - 1.4, 2), 99])
    duty = [[0, round(min(first_guy["a"] - 0.1, space[0][0] if space and space[0][0] > 0.01 else 99), 2)], [C, round(Z, 2)], [round(D - 1.4, 2), 99]]
    beam = [[0, round(first["b"], 2)], [Z + 0.3, round(tease["b"], 2)], [round(D - 1.4, 2), 99]] if spec["hook"] not in SKY and spec.get("beam", True) else []
    sc = spec["screen"]
    screen = [[0, sc["hook"], 1], [shock0, sc.get("shock", "ERROR"), 1], [T, sc["punch"], 0], [C, "COMMENT", 0], [S, "SUBSCRIBE?", 1],
              [Z, sc["tease"], 0], [P, sc["hook"], 1]]
    cop = {"handR": handR, "handL": handL, "lid": lid, "aim": aim, "beam": beam, "screen": screen, "duty": duty, "lazyFrom": k2["give"],
           "sweat": [shock0 + 0.1, T], "mood": mood}

    # ---- the guy: sips, gestures on his lines, laughs, the hand-off, the loop line
    gR = [[0, "SIP_R"], [0.85, "SIP_R"], [1.1, "REST_R", "back"]] if hs else [[0, "REST_R"]]
    gest = ["RAISE_R", "TOAST_R", "SKY_R"]
    gi = 0
    for l in L[1:]:
        if l["who"] != "guy" or not home(l["a"]) or l is loop or l["b"] - l["a"] < 1.2:
            continue
        g = gest[gi % len(gest)]
        gi += 1
        gR += [[round(l["a"] + 0.1, 2), "REST_R"], [round(l["a"] + 0.35, 2), g, "back"], [round(l["b"] - 0.2, 2), g], [round(l["b"] + 0.1, 2), "REST_R"]]
    sip2 = k2["sipB"] + 0.3
    gR += [[sip2, "REST_R"], [sip2 + 0.2, "SIP_R"], [sip2 + 0.8, "SIP_R"], [sip2 + 1.1, "REST_R"]]
    gR += [[P, "REST_R"], [P + 0.25, "RAISE_R", "back"], [round(D - 0.65, 2), "RAISE_R"], [round(D - 0.3, 2), "SIP_R" if hs else "REST_R"]]
    gR.sort(key=lambda k: k[0])
    gL = [[0, "REST_L"], [k2["pop"] - 0.05, "REST_L"], [k2["pop"] + 0.05, "POCKET"], [k2["pop"] + 0.12, "POCKET"],
          [k2["pop"] + 0.32, "OFFER", "back"], [k2["give"] - 0.1, "OFFER"], [k2["give"] + 0.15, "REST_L"]]
    glid = [[0, 1.1 if hs else -0.85], [0.85, 1.1 if hs else -0.85], [0.95, -1.75 if hs else -0.85, "snap"], [1.5, -1.3 if hs else -0.85],
            [max(1.6, first_guy["a"] - 0.3), -0.85]]
    gmood = {"startle": [first["a"]] if hs else [], "smug": [], "laugh": [[T, T + 0.35]], "sip": [[sip2 + 0.2, sip2 + 0.8]], "lookUp": [], "confused": []}
    if hs:
        gmood["sip"] = [[-1, 0.9]] + gmood["sip"] + [[round(D - 0.3, 2), 99]]
    for l in L[1:]:
        if l["who"] != "guy":
            continue
        if l["tag"] in ("amused", "casual", "smug"):
            gmood["smug"].append([round(l["a"] - 0.1, 2), round(l["b"] + 0.1, 2)])
        if l["tag"] == "laughs":
            gmood["laugh"].append([round(l["a"] - 0.05, 2), round(l["a"] + 0.75, 2)])
    lt = sorted([(w[0], w[0] + 0.75) for w in gmood["laugh"]])
    for a, b in lt:
        glid += [[round(a - 0.05, 2), -0.85], [round(a + 0.05, 2), 0.05], [round(b - 0.1, 2), 0.05], [round(b, 2), -0.85]]
    glid += [[round(sip2 + 0.15, 2), -0.85], [round(sip2 + 0.25, 2), 1.1], [round(sip2 + 0.75, 2), 1.1], [round(sip2 + 0.9, 2), -0.85]]
    if hs:
        glid += [[round(D - 0.35, 2), -0.85], [round(D - 0.25, 2), 1.1]]
    glid.sort(key=lambda k: k[0])
    if first["who"] == "cop" and isSky(spec["hook"]) and hs:
        gmood["lookUp"].append([1.5, round(first["b"], 2)])
    if isSky(spec["tease"]):
        gmood["lookUp"].append([Z + 0.2, round(tease["b"], 2)])
    yaw = [[0, 0], [0.95, 0], [1.15, 0.55, "back"], [round(D - 0.6, 2), 0.55], [round(D - 0.2, 2), 0]] if hs else [[0, 0.55], [D, 0.55]]
    guy = {"handR": gR, "handL": gL, "lid": glid, "yaw": yaw, "mood": gmood}

    # ---- camera: hook CU, speaker close-ups at home, punch push-in, trombone, end card, to camera, teaser, loop
    shots = []
    if hs:
        shots.append({"t": 0, **CU_COP_AIM, "dist": 5.2, "to": {"dist": 4.6}})
    for a, b in space:
        if b < D:
            shots.append({"t": b, **TWO, "dist": 9.6})
    for l in L[1:ci - 1]:
        if not home(l["a"]) or l["a"] >= shock0:
            continue
        t0 = round(l["a"] - 0.15, 2)
        if any(a - 0.01 <= t0 < a + 0.4 for a, b in space) or any(abs(t0 - b) < 0.45 for a, b in space):
            t0 = round(l["a"] + 0.35, 2)
        cu = CU_GUY if l["who"] == "guy" else CU_COP
        shots.append({"t": t0, "blend": 0.45, **cu, "dist": 4.8})
    if home(punch["a"]):
        cu = CU_GUY if punch["who"] == "guy" else CU_COP
        shots.append({"t": round(punch["a"] - 0.15, 2), **cu, "dist": 4.9})
    shots += [{"t": shock0, "blend": 0.5, "look": [1.0, 3.0, 0.5], "dir": [-0.35, 0.08, 1], "dist": 4.6},
              {"t": T, "blend": 0.35, "look": [1.0, 2.6, 0.5], "dir": [-0.3, 0.05, 1], "dist": 3.6},
              {"t": round(T + 0.2, 2), "look": [0.15, 2.4, 0.2], "dir": [0.06, 0.3, 1], "dist": 11.0},
              {"t": C, "look": [1.05, 2.75, 0.75], "dir": [0.12, 0.1, 1], "dist": 4.4, "to": {"dist": 4.0}},
              {"t": Z, **SKY_WIDE, "dist": 12.0},
              {"t": P, **CU_GUY, "dist": 5.0, "to": {"dist": 4.7}}]
    if hs:
        shots.append({"t": round(D - 1.4, 2), **CU_COP_AIM, "dist": 5.6, "to": {"dist": 5.2}})
    shots += spec.get("extra_shots", [])
    shots.sort(key=lambda s: s["t"])
    if not shots or shots[0]["t"] > 0:
        shots.insert(0, {"t": 0, **CU_GUY, "dist": 5.0})
    times = {"T": T, "C": C, "S": S, "Z": Z, "P": P, "shock": shock0, "k2": k2, "punch": punch, "comment": comment, "tease": tease, "loop": loop, "L": L}
    return {"guy": guy, "cop": cop, "k2": k2, "alt": spec.get("alt", [])}, shots, times
