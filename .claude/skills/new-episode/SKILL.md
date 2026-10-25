---
name: new-episode
description: Make a new Chai Pe Cosmos YouTube Short with the recurring characters (the guy and Hawaldar sahab). Use when the person asks for a new episode, a new video, the next Short, or invokes /new-episode with a topic or fact (e.g. "/new-episode why the sky is blue").
---

# New Chai Pe Cosmos episode

The person gives a topic or a fact (it may be loose: "something about the Moon"). You run the whole production,
stopping only at the gates marked **STOP**.

## 0. Load the memory and the environment
1. Read `SERIES.md` completely (characters, voices, look, story formula, rules, pipeline, episode log, lessons)
   and `thumbs/README.md`. Episode 1 (`compositions/world.html`, `assets/challan-scene.js`, `tools/`) is the
   working reference for every step below: reuse its code, do not rebuild from scratch.
2. Check the tools in this container and fix what is missing:
   - HyperFrames skills: if `/hyperframes` is not available, run `npx skills add heygen-com/hyperframes -y`.
   - `ffmpeg -version` (install if missing); `npm install` in the project if `node_modules` is missing.
   - ElevenLabs connector: list voices (`creative_list_voices`) to confirm it is connected; the two series voices
     are in `SERIES.md`.
3. Next episode number = last row of the episode log + 1. Work in a new folder `episodes/epNN/` (copy the
   project skeleton: `index.html`, `compositions/`, `assets/` incl. `vendor/` and `fonts/`, `tools/`), so earlier
   episodes keep rendering.

## 1. Research
- Find the real numbers for the topic from several sources; keep only what they agree on. If they disagree,
  use a defensible floor with "+" and "kam se kam" / "at least", and say so. Note the sources.

## 2. Story and plan: STOP
- Write three storylines in a few lines each, using the series formula (hook → absurd-but-true accusation or
  situation → evidence that lands as numbers on spoken words → reversal → comic beat → chai together → end card
  "Sab ___ mein hain"-style moral → **subscribe-challan sign-off**, see the Growth playbook in `SERIES.md`). Build in
  one comment question, a teaser of the next episode and, when possible, a loop-friendly ending. Reuse the guy and the cop; a new character is allowed only if the story needs it,
  and is built in the same vinyl-toy style and added to `SERIES.md`.
- Recommend one. For it, give: the Hinglish dialogue line by line (mostly Hindi; Hindi in Devanagari for the
  voice engine), who speaks each line, the spoken numbers matching the on-screen numbers exactly, the English
  subtitles, the on-screen labels (Roman Hinglish), the scene list with times, sound effects, and an ElevenLabs
  credit estimate (`estimate_only` calls cost nothing).
- **STOP: wait for the person's OK** before spending credits, unless they said they give you a free hand.

## 3. Voice
- One take per line, `eleven_v4`, the series voices, audio tags as needed (`[shouting]`, `[laughs]`...).
- Word timings with ElevenLabs Scribe (`creative_transcribe_audio`, connect_from the generation node; 0 credits).
- Lay the dialogue with `tools/build-dialogue.py` (loudness-matched, slots, cuts only inside silences).
  Never speed a voice up.

## 4. Picture
- Build the scene by reusing `makeGuy`, `makeCop`, `makeKulhad`, `makeDuo`, the worlds, the 3D numbers, the whips,
  the speed lines, the camera shot list and the keyed acting from `assets/challan-scene.js`.
- Every number lands on its spoken word; captions are English, colour by speaker, inside the safe band.
- `npx hyperframes check`, then snapshots of every beat; look at them and fix before rendering.

## 5. Sound and renders
- `tools/build-sfx.py` with this episode's cues (generate missing effects with ElevenLabs sfx, 50 credits each,
  only when the bundled library has nothing fitting). Effects 8–12 dB under the dialogue.
- 720×1280 draft → `tools/master.sh` → send it with one frame per scene. **STOP: wait for OK** before the final.
- Final 1080×1920 (and 4K with `--resolution portrait-4k` if asked) → master → verify −14 LUFS → send.

## 6. Publishing kit
- Thumbnail: copy `thumbs/ep01.json` to `thumbs/epNN.json`, follow the five rules in `thumbs/README.md`,
  render both sizes, check them at 168 px wide.
- Title, description (with sources) and hashtags in the episode-1 style from `SERIES.md`.
- The Growth playbook's upload checklist: pinned-comment text, the comment question, the related-video link to the
  previous episode, the "Challan #N" thumbnail tag and playlist, and the suggested posting time.

## 7. Remember
- Add the episode to the log in `SERIES.md`, plus any new running joke, character or lesson.
- Remind the person to push the project to their repository so the next session has it.
