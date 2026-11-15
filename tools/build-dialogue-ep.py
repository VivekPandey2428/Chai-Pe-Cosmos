"""Lays an episode's per-line takes on one dialogue track (generalised from build-dialogue.py).

Reads <episode>/dialogue.json: [{id, speaker, gap}] where gap is the silence (s) between the previous line's last word
and this line's first word (the first line's gap is measured from 0). Word times come from <episode>/audio/words.json
({id: [{text, start, end}]}, times inside each take). Every take is loudness-matched to -19 LUFS, never sped up or cut
inside. Writes <episode>/assets/audio/dialogue.wav and lines.json (absolute word times) and prints the duration.
"""
import json, os, subprocess, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
ep = os.path.abspath(args[0])
tail = float(args[1]) if len(args) > 1 else 1.2   # silence after the last word
# optional Shorts pacing: --tempo=1.08 speeds every take (pitch kept); --pause=0.18 caps the pauses between the phrases
# inside a take (phrases are the entries of words.json, cut out with a little padding and re-joined)
tempo = float(opts.get("tempo", 1))
pause = float(opts["pause"]) if "pause" in opts else None


def tighten(w):
    """filter graph (input [0:a] after tempo) and new phrase times for a take with capped inner pauses"""
    parts, nw, t = [], [], 0.0
    for k, x in enumerate(w):
        a = 0.0 if k == 0 else x["start"] - 0.04
        b = x["end"] + 0.4 if k == len(w) - 1 else x["end"] + 0.06
        if k:
            sil = max(0.0, min(pause, x["start"] - w[k - 1]["end"]) - 0.10)
            parts.append(("sil", sil))
            t += sil
        parts.append(("cut", a, b))
        nw.append({**x, "start": t + (x["start"] - a), "end": t + (x["end"] - a)})
        t += b - a
    n = len(parts)
    g = f"[0:a]asplit={len(w)}" + "".join(f"[p{k}]" for k in range(len(w))) + ";"
    labels, k = [], 0
    for i, p in enumerate(parts):
        if p[0] == "cut":
            g += f"[p{k}]atrim={p[1]:.3f}:{p[2]:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=mono[c{i}];"
            k += 1
        else:
            g += f"aevalsrc=0:s=44100:d={max(p[1], 0.001):.3f},aformat=sample_rates=44100:channel_layouts=mono[c{i}];"
        labels.append(f"[c{i}]")
    g += "".join(labels) + f"concat=n={n}:v=0:a=1[m]"
    return g, nw
plan = json.load(open(os.path.join(ep, "dialogue.json")))
words = json.load(open(os.path.join(ep, "audio/words.json")))
A = os.path.join(ep, "assets/audio")
os.makedirs(A, exist_ok=True)

def run(args):
    subprocess.run(args, check=True, capture_output=True)

inputs, chains, out = [], [], []
t_end = 0.0
for i, line in enumerate(plan):
    w = words[line["id"]]
    src = os.path.join(ep, "audio", f"{line['id']}-raw.mp3")
    if tempo != 1:
        tmp = os.path.join(A, f"{line['id']}-tempo.wav")
        run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-af", f"atempo={tempo}", "-ac", "1", "-ar", "44100", tmp])
        src = tmp
        w = [{**x, "start": x["start"] / tempo, "end": x["end"] / tempo} for x in w]
    if pause is not None and len(w) > 1:
        g, w = tighten(w)
        tmp = os.path.join(A, f"{line['id']}-tight.wav")
        run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-filter_complex", g, "-map", "[m]", tmp])
        src = tmp
    first = w[0]["start"]
    slot = round(t_end + line["gap"] - first, 3)
    norm = os.path.join(A, f"{line['id']}-norm.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-af",
         "loudnorm=I=-19:TP=-3:LRA=11,aresample=48000", "-ac", "2", norm])
    inputs += ["-i", norm]
    ms = int(round(slot * 1000))
    chains.append(f"[{i}:a]adelay={ms}|{ms}[l{i}]")
    out.append({"id": line["id"], "speaker": line["speaker"], "start": slot,
                "words": [{"text": x["text"], "start": round(slot + x["start"], 3), "end": round(slot + x["end"], 3)} for x in w]})
    t_end = slot + w[-1]["end"]
dur = round(t_end + tail, 2)
graph = ";".join(chains) + ";" + "".join(f"[l{i}]" for i in range(len(plan))) + \
    f"amix=inputs={len(plan)}:normalize=0:dropout_transition=0,apad=whole_dur={dur},atrim=0:{dur}[out]"
run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "2",
     os.path.join(A, "dialogue.wav")])
json.dump(out, open(os.path.join(A, "lines.json"), "w"), ensure_ascii=False, indent=1)
for l in out:
    print(f'{l["id"]:3s} {l["speaker"]:3s} {l["words"][0]["start"]:6.2f}-{l["words"][-1]["end"]:6.2f}  ' + " ".join(x["text"] for x in l["words"]))
print("duration", dur)
