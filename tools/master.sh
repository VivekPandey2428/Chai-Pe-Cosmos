#!/usr/bin/env bash
# Two-pass loudnorm of a rendered video's audio to -14 LUFS / -1 dBTP; video stream is copied untouched.
set -euo pipefail
in="$1"; out="$2"
m=$(ffmpeg -hide_banner -nostats -i "$in" -vn -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$m" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i "$in" -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true,aresample=48000" -c:a aac -b:a 256k -t 31.3 -shortest -movflags +faststart "$out"
