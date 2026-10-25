"""Lays an episode's per-line takes on one dialogue track (generalised from build-dialogue.py).

Reads <episode>/dialogue.json: [{id, speaker, gap}] where gap is the silence (s) between the previous line's last word
and this line's first word (the first line's gap is measured from 0). Word times come from <episode>/audio/words.json
({id: [{text, start, end}]}, times inside each take). Every take is loudness-matched to -19 LUFS, never sped up or cut
inside. Writes <episode>/assets/audio/dialogue.wav and lines.json (absolute word times) and prints the duration.
"""
import json, os, subprocess, sys

ep = os.path.abspath(sys.argv[1])
tail = float(sys.argv[2]) if len(sys.argv) > 2 else 1.2   # silence after the last word
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
    first = w[0]["start"]
    slot = round(t_end + line["gap"] - first, 3)
    norm = os.path.join(A, f"{line['id']}-norm.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", os.path.join(ep, "audio", f"{line['id']}-raw.mp3"), "-af",
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
