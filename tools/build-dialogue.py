"""Places the seven dialogue takes on one track at their planned start times.

Each line is loudness-matched (-19 LUFS, leaving headroom for the -14 LUFS master), never sped up or
trimmed inside. Writes assets/audio/dialogue.wav and assets/audio/lines.json (absolute word times
for the scene: a line's words start at its slot + the word's time in its own take).
"""
import json, os, subprocess

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(PROJ, "assets/audio")
DUR = 31.3
# line id, speaker, slot start (s), words from the ElevenLabs transcript of that take
LINES = [
    ("c1", "cop", 1.20, [("ऐ", .08, .24), ("हीरो!", .32, .72), ("रुको!", .96, 1.44), ("Speeding", 1.76, 2.16), ("कर", 2.24, 2.32), ("रहे", 2.4, 2.56), ("हो!", 2.64, 3.2)]),
    ("g1", "guy", 4.35, [("hmm?", 0, .5), ("मैं?", 1.04, 1.76), ("मैं", 1.84, 2), ("तो", 2.08, 2.16), ("बैठ", 2.2, 2.36), ("के", 2.4, 2.56), ("chai", 2.6, 2.8), ("पी", 2.88, 2.96), ("रहा", 3, 3.16), ("हूँ!", 3.2, 3.68)]),
    # c2 was re-recorded with the exact number ("सोलह सौ सत्तर"); 0.28 s is cut from its pause after "हो?" (CUTS below),
    # and these word times are already shifted to match the cut take
    ("c2", "cop", 8.08, [("बैठे", 0, .4), ("हो?", .44, .64), ("Earth", .84, 1.16), ("घूम", 1.24, 1.48), ("रही", 1.52, 1.72), ("है,", 1.8, 2.36), ("सोलह", 2.44, 2.76), ("सौ", 2.84, 3.027), ("सत्तर", 3.08, 3.44), ("की", 3.48, 3.6), ("speed", 3.64, 3.88), ("से!", 3.96, 4.18)]),
    ("c3", "cop", 12.50, [("Sun", 0, .32), ("के", .4, .48), ("चक्कर", .56, .88), ("में,", .96, 1.52), ("एक", 1.6, 1.84), ("लाख", 2, 2.32), ("सात", 2.4, 2.64), ("हज़ार!", 2.72, 3.36)]),
    ("c4", "cop", 15.95, [("और", 0, .2), ("galaxy", .24, .72), ("में,", .8, 1.36), ("कम", 1.44, 1.6), ("से", 1.68, 1.787), ("कम", 1.84, 2), ("सात", 2.32, 2.64), ("लाख", 2.8, 3.12), ("बीस", 3.28, 3.52), ("हज़ार!", 3.6, 4.24)]),
    ("c5", "cop", 21.40, [("(gulp)", 0, .64), ("एक", .8, .96), ("minute...", 1.04, 1.92), ("मैं", 2.16, 2.32), ("भी?", 2.4, 2.96)]),
    ("g2", "guy", 26.00, [("(laughs)", 0, .4), ("बैठ", .96, 1.2), ("जाओ", 1.28, 1.44), ("भाई,", 1.48, 2.08), ("chai", 2.16, 2.32), ("पियो।", 2.4, 2.96)]),
]

# per-line cuts (start, end) in the take's own time, made inside silences only
CUTS = {"c2": [(0.73, 1.01)]}


def run(args):
    subprocess.run(args, check=True, capture_output=True)

inputs, chains, out = [], [], []
for i, (lid, who, at, words) in enumerate(LINES):
    norm = os.path.join(A, f"{lid}-norm.wav")
    src = os.path.join(A, f"{lid}-raw.mp3")
    pre = "anull"
    if lid in CUTS:
        keep, t0 = [], 0.0
        for a, b in CUTS[lid]:
            keep.append(f"between(t,{t0},{a})")
            t0 = b
        keep.append(f"gte(t,{t0})")
        pre = f"aselect='{'+'.join(keep)}',asetpts=N/SR/TB"
    run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-af",
         f"{pre},loudnorm=I=-19:TP=-3:LRA=11,aresample=48000", "-ac", "2", norm])
    inputs += ["-i", norm]
    ms = int(round(at * 1000))
    chains.append(f"[{i}:a]adelay={ms}|{ms}[l{i}]")
    out.append({"id": lid, "speaker": who, "start": at,
                "words": [{"text": w, "start": round(at + s, 3), "end": round(at + e, 3)} for w, s, e in words]})
graph = ";".join(chains) + ";" + "".join(f"[l{i}]" for i in range(len(LINES))) + \
    f"amix=inputs={len(LINES)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR},atrim=0:{DUR}[out]"
run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "2",
     os.path.join(A, "dialogue.wav")])
json.dump(out, open(os.path.join(A, "lines.json"), "w"), ensure_ascii=False, indent=1)
for l in out:
    print(l["id"], l["speaker"], l["start"], " ".join(f'{w["text"]}@{w["start"]}' for w in l["words"]))
