# Chai Pe Cosmos: thumbnail system

Every episode's thumbnail follows the same five rules, so the channel page reads as one series:

1. **One giant number** (or a 1–2 word answer): white, extruded, rim in the episode's accent colour.
2. **The heroes, big and reacting.** Faces at least a quarter of the frame height. A clear emotion beats a pretty pose.
3. **A yellow sticker hook**, 2–3 Hinglish words, tilted like a stamp. It never repeats the video title.
4. **The episode's colour world** (the film's background gradient) with a light burst behind the heroes.
5. **The brand chip** bottom-left: mascot face + CHAI PE COSMOS. Never bottom-right: YouTube puts the timestamp there.

Optional, per episode: a red radar **reticle** locked on a face, and colour **glows** (episode 1 uses police red/blue).

## Files
- `thumb-hero.html`: renders the film's characters at one moment, on a transparent background, from the camera in the episode file.
  Still-only flags: `gunScreen` (radar readout), `hideSteam`, `copShout`.
- `thumb.html`: the layout template (number, sticker, reticle, glows, chip).
- `thumbs/epNN.json`: everything episode-specific: words, colours, scene moment, cameras, positions.
- `tools/render-thumbs.cjs`: renders both sizes to `thumbs/out/` as PNG and JPG.

## A new episode
1. Copy `thumbs/ep01.json` to `thumbs/ep02.json`.
2. Change `number`, `unit`, `plus`, `hook`, `accent` / `accentDeep`, `world` and `glows`.
3. Point `scene.t` at the frame with the strongest reaction, and move the cameras until faces are big.
   For a new film, render its own hero PNG the same way (or any transparent PNG) and pass it as `hero`.
4. Render:
   ```bash
   python3 -m http.server 8765 --bind 127.0.0.1 &
   node tools/render-thumbs.cjs http://127.0.0.1:8765 thumbs/ep02.json
   ```
5. Check it at 168 px wide (sidebar size). If the number and faces don't read, make them bigger. Never add more words.

## Sizes
- `16x9` = 1280×720: the standard YouTube thumbnail (JPG, under 2 MB).
- `9x16` = 1080×1920: Shorts cover. Keep words between y 280 and 1640 so a 4:5 crop never cuts them.
