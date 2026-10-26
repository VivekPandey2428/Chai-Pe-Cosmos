"""Cuts an episode's dialogue + sfx mix to an edit list (the same ranges render-local.cjs --edl renders), with
10 ms fades at every join, and lays the opening whistle under the first frame.
Usage: python3 tools/edit-audio-ep.py <episode-dir> "a-b,c-d" [whistle_under_LU]
Writes <episode>/assets/audio/mix-edit.wav and prints the new duration.
"""
import os, subprocess, sys

ep = os.path.abspath(sys.argv[1])
edl = [tuple(map(float, r.split("-"))) for r in sys.argv[2].split(",")]
A = os.path.join(ep, "assets/audio")
run = lambda a: subprocess.run(a, check=True, capture_output=True)
mix = os.path.join(A, "mix-full.wav")
run(["ffmpeg", "-y", "-i", os.path.join(A, "dialogue.wav"), "-i", os.path.join(A, "sfx-bed.wav"),
     "-filter_complex", "amix=inputs=2:normalize=0:dropout_transition=0", "-ar", "48000", "-ac", "2", mix])
parts = []
for i, (a, b) in enumerate(edl):
    d = b - a
    parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d - 0.01:.3f}:d=0.01[p{i}]")
graph = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(edl))) + f"concat=n={len(edl)}:v=0:a=1[cut]"
import re
def momentary_max(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", path, "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    vals = [float(m) for m in re.findall(r"M:\s*(-?[\d.]+)", err) if float(m) > -120]
    return max(vals) if vals else -70.0
under = float(sys.argv[3]) if len(sys.argv) > 3 else 9.0
# the whistle sits under the first line (`under` LU below the dialogue's loudest moments), starting on frame 0
gain = (momentary_max(os.path.join(A, "dialogue.wav")) - under) - momentary_max(os.path.join(A, "whistle.mp3"))
graph += f";[1:a]atrim=0:1.3,afade=t=out:st=1.0:d=0.3,volume={gain:.2f}dB,aresample=48000[w];[cut][w]amix=inputs=2:normalize=0:dropout_transition=0:duration=first[out]"
out = os.path.join(A, "mix-edit.wav")
run(["ffmpeg", "-y", "-i", mix, "-i", os.path.join(A, "whistle.mp3"), "-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "2", out])
print("duration", round(sum(b - a for a, b in edl), 3), out)
