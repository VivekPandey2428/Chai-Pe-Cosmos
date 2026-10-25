"""Builds <episode>/assets/audio/sfx-bed.wav from <episode>/sfx.json, every cue level-matched under the dialogue.

Generalised from build-sfx.py (Episode 1). sfx.json: {"duration": s, "cues": [[name, source, filter, peak, picture, under], ...],
"ticks": [[from, to], ...], "booms": [[time, rate], ...]}. Sources: "own:<file>" (the episode's assets/audio),
"lib:<file>" (assets/audio/local-sfx). Each cue's peak lands one frame after its picture; gains are set against the
dialogue's peak momentary loudness (`under` LU below it); ticks are matched by sample peak.
"""
import json, os, re, subprocess, sys, tempfile

ep = os.path.abspath(sys.argv[1])
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ep, "assets/audio")
LIB = os.path.join(PROJ, "assets/audio/local-sfx")
SR, FRAME = 48000, 1 / 30
cfg = json.load(open(os.path.join(ep, "sfx.json")))
DUR = cfg["duration"]


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def momentary_max(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", path, "-af", "ebur128=framelog=verbose", "-f", "null", "-"]).stderr
    vals = [float(m) for m in re.findall(r"M:\s*(-?[\d.]+)", err) if float(m) > -120]
    return max(vals) if vals else -70.0


def peak_db(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "astats=measure_perchannel=none", "-f", "null", "-"]).stderr
    return float(re.findall(r"Peak level dB:\s*(-?[\d.]+)", err)[-1])


def source(s):
    kind, f = s.split(":", 1)
    return os.path.join(A if kind == "own" else LIB, f)


voice = os.path.join(A, "dialogue.wav")
v_m, v_peak = momentary_max(voice), peak_db(voice)
cues = [tuple(c) for c in cfg["cues"]]
for i, (t, rate) in enumerate(cfg.get("booms", [])):
    cues.append((f"boom{i+1}", "lib:impact.wav", f"asetrate={int(44100*rate)},aresample=44100,lowpass=f=220", 0.01 / rate, t, 9))
for n, (a, b) in enumerate(cfg.get("ticks", [])):
    k, t = 0, a + 0.04
    while t < b - 0.04:
        cues.append((f"tick{n}_{k}", "lib:tick.wav", f"asetrate={int(44100*(1.0 if k % 2 else 0.8))},aresample=44100", 0.002, t, 16))
        k += 1
        t += 0.065

tmp = tempfile.mkdtemp()
inputs, chains = [], []
for i, (name, src, pre, peak, pic, under) in enumerate(cues):
    clip = os.path.join(tmp, f"{name}.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", source(src), "-af", f"{pre},aresample={SR},apad=pad_dur=0.5", "-ac", "2", clip])
    gain = (v_peak - under) - peak_db(clip) if name.startswith("tick") else (v_m - under) - momentary_max(clip)
    start = max(0.0, pic + FRAME - peak)
    inputs += ["-i", clip]
    chains.append(f"[{i}:a]volume={gain:.2f}dB,adelay={int(start*1000)}|{int(start*1000)}[c{i}]")
    if not name.startswith("tick"):
        print(f"{name:10s} at {start:6.3f}s  picture {pic:6.3f}s  gain {gain:+6.1f} dB")
graph = ";".join(chains) + ";" + "".join(f"[c{i}]" for i in range(len(cues))) + \
    f"amix=inputs={len(cues)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR},atrim=0:{DUR}[out]"
run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", str(SR), "-ac", "2", os.path.join(A, "sfx-bed.wav")])
print("dialogue momentary max %.1f, peak %.1f dB" % (v_m, v_peak))
