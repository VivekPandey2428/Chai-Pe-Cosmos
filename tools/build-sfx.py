"""Builds assets/audio/sfx-bed.wav for Challan, every cue level-matched under the dialogue.

Each cue's peak lands one frame after its picture. Gains are set against the dialogue's peak momentary
loudness (`under` LU below it); short clicks are matched by sample peak instead.
"""
import os, re, subprocess, tempfile

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = "/home/user/.agents/skills/media-use/audio/assets/sfx"
A = os.path.join(PROJ, "assets/audio")
SR, FRAME, DUR = 48000, 1 / 30, 31.3


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def momentary_max(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", path, "-af", "ebur128=framelog=verbose", "-f", "null", "-"]).stderr
    vals = [float(m) for m in re.findall(r"M:\s*(-?[\d.]+)", err) if float(m) > -120]
    return max(vals) if vals else -70.0


def peak_db(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "astats=measure_perchannel=none", "-f", "null", "-"]).stderr
    return float(re.findall(r"Peak level dB:\s*(-?[\d.]+)", err)[-1])


voice = os.path.join(A, "dialogue.wav")
v_m, v_peak = momentary_max(voice), peak_db(voice)
lib = lambda f: os.path.join(LIB, f)
own = lambda f: os.path.join(A, f)
# (name, source, filter, peak time inside the processed clip, picture time, LU under the dialogue)
cues = [
    ("whistle", own("whistle.mp3"), "atrim=0:1.3,afade=t=out:st=1.15:d=0.15", 0.05, 0.0, 6),       # the hook, before anyone speaks
    ("zap", own("radar.mp3"), "anull", 0.6, 8.7, 9),                                               # beam into the sky
    ("whoosh1", lib("whoosh.mp3"), "anull", 0.162, 8.88, 10),
    ("whoosh2", lib("whoosh-cinematic.mp3"), "atrim=1.7:3.6,asetpts=PTS-STARTPTS,afade=t=in:d=0.12,afade=t=out:st=1.5:d=0.4", 0.9, 12.47, 10),
    ("riser", lib("riser.mp3"), "atrim=0.8:3.45,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=2.5:d=0.15", 2.45, 16.15, 11),
    ("whoosh3", lib("whoosh.mp3"), f"asetrate={int(44100*0.85)},aresample=44100", 0.162 / 0.85, 16.15, 10),
    ("whoosh4", lib("whoosh.mp3"), f"asetrate={int(44100*1.25)},aresample=44100", 0.162 / 1.25, 20.3, 8),  # snap back
    ("selfbeep", own("radar.mp3"), "atrim=0:0.5,afade=t=out:st=0.4:d=0.1", 0.12, 21.0, 10),         # gun turns on himself
    ("trombone", own("trombone.mp3"), "afade=t=out:st=2.15:d=0.4", 0.2, 24.45, 9),                  # after "मैं भी?"
    ("pop1", lib("pop.mp3"), "anull", 0.12, 26.8, 11),                                              # kulhad out of the pocket
    ("pop2", lib("pop.mp3"), "asetrate=52920,aresample=44100", 0.1, 27.9, 12),                      # the hand-off
    ("endboom", lib("impact-bass-1.mp3"), "asetrate=48510,aresample=44100,lowpass=f=220", 0.066, 29.05, 9),
]
for i, (t, rate) in enumerate(zip([10.52, 14.1, 18.27, 21.25], [1.0, 0.9, 0.8, 0.95])):
    cues.append((f"boom{i+1}", lib("impact-bass-1.mp3"), f"asetrate={int(44100*rate)},aresample=44100,lowpass=f=220", 0.073 / rate, t, 9))
for n, (a, b) in enumerate([(10.17, 11.16), (13.75, 15.22), (17.9, 19.55), (20.95, 21.25)]):
    k, t = 0, a + 0.04
    while t < b - 0.04:
        f = "key-press.mp3" if k % 2 == 0 else "click-soft.mp3"
        cues.append((f"tick{n}_{k}", lib(f), "atrim=0:0.12,afade=t=out:st=0.08:d=0.04,highpass=f=900", 0.02, t, 16))
        k += 1
        t += 0.065

tmp = tempfile.mkdtemp()
inputs, chains = [], []
for i, (name, src, pre, peak, pic, under) in enumerate(cues):
    clip = os.path.join(tmp, f"{name}.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", src, "-af", f"{pre},aresample={SR},apad=pad_dur=0.5", "-ac", "2", clip])
    gain = (v_peak - under) - peak_db(clip) if name.startswith("tick") else (v_m - under) - momentary_max(clip)
    start = max(0.0, pic + FRAME - peak)
    inputs += ["-i", clip]
    chains.append(f"[{i}:a]volume={gain:.2f}dB,adelay={int(start*1000)}|{int(start*1000)}[c{i}]")
    if not name.startswith("tick"):
        print(f"{name:9s} at {start:6.3f}s  picture {pic:6.3f}s  gain {gain:+6.1f} dB")
graph = ";".join(chains) + ";" + "".join(f"[c{i}]" for i in range(len(cues))) + \
    f"amix=inputs={len(cues)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR},atrim=0:{DUR}[out]"
run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", str(SR), "-ac", "2", os.path.join(A, "sfx-bed.wav")])
print("dialogue momentary max %.1f, peak %.1f dB" % (v_m, v_peak))
