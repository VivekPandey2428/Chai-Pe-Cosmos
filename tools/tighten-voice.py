"""Shortens the pauses between sentences in the Hinglish take (never the words, never the speed).

Cuts the middle of each detected silence down to a target length and writes the new word timings
(shifted by every cut before them, plus the 0.2 s lead-in on the timeline) to assets/audio/words-hi.json.
"""
import json, re, subprocess, sys

SRC, OUT, WORDS_IN, WORDS_OUT = sys.argv[1:5]
VO_OFFSET = 0.2
# (silence start, silence end, kept length) from silencedetect on the raw take
PAUSES = [
    (1.00726, 1.38678, 0.20),  # after "बैठे हो?"
    (2.12429, 2.48381, 0.20),  # after "फिर से!"
    (3.75678, 3.98703, 0.16),
    (5.3666, 5.66703, 0.18),   # before "Sun"
    (6.98862, 7.22324, 0.16),
    (8.62757, 8.89918, 0.16),
    (13.0491, 13.398, 0.25),   # beat before "Coffee"
]
cuts = []  # (cut start, cut end) in source time
for a, b, keep in PAUSES:
    d = b - a
    if d > keep:
        mid = (a + b) / 2
        cuts.append((mid - (d - keep) / 2, mid + (d - keep) / 2))

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                           capture_output=True, text=True).stdout)
segs, t = [], 0.0
for a, b in cuts:
    segs.append((t, a))
    t = b
segs.append((t, dur))
parts = []
for i, (a, b) in enumerate(segs):
    parts.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={max(0, b - a - 0.006):.4f}:d=0.006[s{i}]")
graph = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", SRC, "-filter_complex", graph, "-map", "[out]", OUT], check=True)

def shift(x):
    return x - sum(min(b, x) - a for a, b in cuts if x > a)

words = json.load(open(WORDS_IN))
out = [{"text": w["text"], "start": round(shift(w["start"]) + VO_OFFSET, 3), "end": round(shift(w["end"]) + VO_OFFSET, 3)} for w in words]
json.dump(out, open(WORDS_OUT, "w"), ensure_ascii=False, indent=1)
print("removed %.3f s; new voice length %.3f s" % (sum(b - a for a, b in cuts), dur - sum(b - a for a, b in cuts)))
for w in out:
    print(f'{w["start"]:6.3f} {w["end"]:6.3f}  {w["text"]}')
