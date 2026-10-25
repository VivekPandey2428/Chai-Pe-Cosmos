"""Builds assets/audio/voice-norm.wav and assets/audio/sfx-bed.wav.

Every cue's peak lands one frame (0.033 s) after its picture. Each effect is level-matched to
sit a set number of LU under the voice's peak momentary loudness.
"""
import json, os, re, subprocess, sys, tempfile

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = "/home/user/.agents/skills/media-use/audio/assets/sfx"
OUT = os.path.join(PROJ, "assets/audio")
SR = 48000
FRAME = 1 / 30
VO_OFFSET = 0.2
VOICE_TARGET = -19.0  # integrated LUFS; leaves headroom, the final master pass brings the mix to -14 LUFS


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def momentary_max(path):
    # max 400 ms momentary loudness: works for clips shorter than the 3 s short-term window
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", path, "-af", "ebur128=framelog=verbose", "-f", "null", "-"]).stderr
    vals = [float(m) for m in re.findall(r"M:\s*(-?[\d.]+)", err) if float(m) > -120]
    return max(vals) if vals else -70.0


def peak_db(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "astats=measure_perchannel=none", "-f", "null", "-"]).stderr
    return float(re.findall(r"Peak level dB:\s*(-?[\d.]+)", err)[-1])


tmp = tempfile.mkdtemp()
# 1. voice: loudness-normalised, no time stretch
voice = os.path.join(OUT, "voice-norm.wav")
run(["ffmpeg", "-y", "-hide_banner", "-i", os.path.join(OUT, "voice-hi.wav"), "-af",
     f"loudnorm=I={VOICE_TARGET}:TP=-2:LRA=11,aresample={SR}", "-ac", "2", voice])
v_st = momentary_max(voice)
v_peak = peak_db(voice)

# 2. cues: (name, file, pre-filter, peak time inside the processed clip, picture time, LU under voice)
W = [2.28, 5.37, 9.42, 12.68]            # camera whips (12.68 = snap back)
BOOM = [3.91, 6.88, 11.08]               # number landings
COUNT = [(3.55, 4.35), (6.52, 7.28), (10.72, 11.56)]
GALAXY = 9.42
PLOP = 14.24

cues = [
    ("whoosh1", "whoosh.mp3", "anull", 0.162, W[0], 10),
    ("whoosh2", "whoosh-cinematic.mp3", "atrim=1.7:3.6,asetpts=PTS-STARTPTS,afade=t=in:d=0.12,afade=t=out:st=1.5:d=0.4", 0.9, W[1], 10),
    ("whoosh3", "whoosh.mp3", f"asetrate={int(44100*0.85)},aresample=44100", 0.162 / 0.85, W[2], 10),
    ("whoosh4", "whoosh.mp3", f"asetrate={int(44100*1.25)},aresample=44100", 0.162 / 1.25, W[3], 8),
    ("riser", "riser.mp3", "atrim=0.8:3.45,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=2.5:d=0.15", 2.45, GALAXY, 11),
    ("pop", "pop.mp3", "anull", 0.12, PLOP, 9),
]
for i, (t, rate) in enumerate(zip(BOOM, [1.0, 0.9, 0.8])):
    cues.append((f"boom{i+1}", "impact-bass-1.mp3",
                 f"asetrate={int(44100*rate)},aresample=44100,lowpass=f=220", 0.073 / rate, t, 9))
for n, (a, b) in enumerate(COUNT):
    k, t = 0, a + 0.04
    while t < b - 0.04:
        f = "key-press.mp3" if k % 2 == 0 else "click-soft.mp3"
        cues.append((f"tick{n}_{k}", f, f"atrim=0:0.12,afade=t=out:st=0.08:d=0.04,highpass=f=900", 0.02, t, 16))
        k += 1
        t += 0.065

inputs, chains = [], []
for i, (name, f, pre, peak, pic, under) in enumerate(cues):
    clip = os.path.join(tmp, f"{name}.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", os.path.join(SFX, f), "-af", f"{pre},aresample={SR},apad=pad_dur=0.5", "-ac", "2", clip])
    if name.startswith("tick"):
        # clicks are shorter than the 400 ms loudness window: match their peak to the voice's peak instead
        gain = (v_peak - under) - peak_db(clip)
    else:
        gain = (v_st - under) - momentary_max(clip)
    start = max(0.0, pic + FRAME - peak)
    inputs += ["-i", clip]
    chains.append(f"[{i}:a]volume={gain:.2f}dB,adelay={int(start*1000)}|{int(start*1000)}[c{i}]")
    print(f"{name:10s} at {start:6.3f}s  picture {pic:6.3f}s  gain {gain:+6.1f} dB")

graph = ";".join(chains) + ";" + "".join(f"[c{i}]" for i in range(len(cues))) + \
    f"amix=inputs={len(cues)}:normalize=0:dropout_transition=0,apad=whole_dur=15,atrim=0:15[out]"
run(["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", str(SR), "-ac", "2",
     os.path.join(OUT, "sfx-bed.wav")])
print("voice momentary max", v_st)
