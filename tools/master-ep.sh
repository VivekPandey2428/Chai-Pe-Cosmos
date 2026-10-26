#!/usr/bin/env bash
# Mixes an episode's dialogue + sfx bed onto its silent render, then two-pass loudnorm to -14 LUFS / -1 dBTP
# (the same targets as master.sh), video copied untouched, trimmed to the episode length.
# Usage: tools/master-ep.sh <episode-dir> <silent.mp4> <out.mp4> [premixed.wav]
#   with a premixed (e.g. edited) track, that audio is used as is and the length follows the video
set -euo pipefail
ep="$1"; in="$2"; out="$3"; pre="${4:-}"
tmp=$(mktemp -d)
if [[ -n "$pre" ]]; then
  cp "$pre" "$tmp/mix.wav"
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
else
  dur=$(python3 -c "import json;print(json.load(open('$ep/story.json'))['duration'])")
  ffmpeg -hide_banner -loglevel error -y -i "$ep/assets/audio/dialogue.wav" -i "$ep/assets/audio/sfx-bed.wav" \
    -filter_complex "amix=inputs=2:normalize=0:dropout_transition=0" -ar 48000 -ac 2 "$tmp/mix.wav"
fi
m=$(ffmpeg -hide_banner -nostats -i "$tmp/mix.wav" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$m" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i "$in" -i "$tmp/mix.wav" -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -t "$dur" -movflags +faststart "$out"
ffmpeg -hide_banner -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
