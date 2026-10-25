# Chai Pe Cosmos: series bible

Read this first in every session about this channel. It is the memory of how the channel looks, sounds and is made.
Update the **Episode log** and **Lessons** at the end of every episode.

**To make the next video:** open this project in Claude Code and type `/new-episode <topic>`
(skill: `.claude/skills/new-episode/SKILL.md`).

## The channel
- **Name:** Chai Pe Cosmos · handle **@ChaiPeCosmos** (confirm availability when claiming).
- **Promise:** "Science, Hinglish mein. Ek chai ke saath." Funny 3D animated Shorts that make space and physics easy.
- **Format:** YouTube Shorts, 9:16 (1080×1920 master, 4K 2160×3840 available), ~30 s, 30 fps.
- **Language:** dialogue in Hinglish, mostly Hindi (Hindi words written in Devanagari for the voice engine, English words in Latin:
  "Earth", "speed", "galaxy", "chai"). **Subtitles in English.** On-screen labels and end cards in Roman Hinglish
  ("EARTH KA SPIN", "SAB SPEEDING MEIN HAIN").
- **Tone:** a situation every Indian viewer knows (chai, traffic police, challan) colliding with a real science fact.
  Comedy comes from characters reacting, never from a narrator lecturing.
- **Brand assets:** `brand/avatar-800x800.png` (the mascot with his kulhad), `brand/cover-2560x1440.png` (banner),
  rendered by `still.html` + `tools/render-stills.cjs`. Channel description, title/description/hashtag style: see "Publishing".

## Recurring characters
All are designer-vinyl toys: chibi proportions (head about one third of the height), **matte clay** materials
(no glossy plastic, no blush stickers), lit by the same studio key light + cool rim light as the planets.
Models live in `assets/challan-scene.js` (`makeGuy`, `makeCop`, `makeFace`, `makeKulhad`, `makeDuo`).

### The guy (the mascot): unnamed so far
- Relaxed young Indian guy. Warm skin `#E8A87C`, short dark-brown hair `#3B2416` with a front **quiff**.
- Dark oval eyes with a small white glint, eyebrows, small smile. Resting face: relaxed half-closed eyes.
- Orange hoodie `#FF8A3D` (deep `#EE7428`, white drawstrings, kangaroo pocket), navy joggers `#1E3A8A`,
  white sneakers with green `#34C759` soles, charcoal headphones around his neck.
- Always has a **terracotta kulhad of chai** (`#B5562F`, chai `#C68E5E`), with steam.
- Sits in a **sand `#E8C07D` mid-century armchair with walnut legs**, on top of a **tiny low-poly planet**
  (navy ocean, green land, sand deserts) under a coral sky.
- Personality: unbothered, cheeky, generous (offers chai). Voice: **Bobby, "Energetic natural voiceover"**
  (ElevenLabs voice_id `YgpoWAqBbWpygO1YiIEI`), model `eleven_v4`, tags like `[confused]`, `[laughs]`.
- Acting range built so far: blissful sip (eyes closed), startle (eyes wide + "o" mouth), confused (tilted brows),
  smug (one raised brow, smirk), laugh, offering a second kulhad from his hoodie pocket.

### The cop: Hawaldar sahab
- Chubby Indian traffic policeman: khaki shirt `#C9A66B`, trousers `#9C7A45`, **pot belly**, brown belt with gold
  buckle, gold badge, epaulettes, black shoes. Skin `#C98B5E`.
- **Big curled black moustache**, thick brows, bigger nose.
- Khaki peaked cap with a **red band**, black visor, gold badge and a **red/blue police beacon** on top that flashes
  (and lights the scene red/blue) while he is on duty.
- Carries a **radar speed gun** with a green LCD screen that can show a live readout ("SPEED?", "720000+").
- Personality: stern and loud, then deflates comically when the facts turn on him; ends up sharing chai.
  Voice: **Ranga, "Authoritative and Deep Hindi Voice"** (voice_id `d0grukerEzs069eKIauC`), `eleven_v4`,
  tags like `[shouting]`, `[nervous]`.
- Acting range built so far: stern V-brows, shout with STOP palm, smug, gunslinger blow on the gun, shock
  (huge eyes + sweat drop), sad (droopy moustache, cap askew, beacon dies), sheepish smile, sip.

## The look
- Worlds, each with its own gradient: home sky coral `#FF6B6B` → apricot `#FFD6A5`; Earth deep blue `#0B3D91` → cyan
  `#00B4D8`; orbit midnight `#14213D`, Sun gold `#FFB703` → orange `#FB5607`, orbit line magenta `#FF006E`;
  galaxy violet `#240046` → purple `#5A189A`, stars pink `#FF4D9E` and teal `#4CC9F0`.
- Earth: low-poly, real continent outlines, navy ocean `#1E3A8A`, green land `#34C759`, sand deserts `#E8C07D`.
- Numbers: big extruded 3D digits, glossy white face, rim in the world's colour; they fly in, spin once, lock with
  a small overshoot, while a counter races up. Label under them: unit + max 4-word Roman Hinglish label.
- Type: **Fredoka** (npm `@fontsource/fredoka`; 3D digits from `assets/fonts/fredoka-700.typeface.json`).
- Captions: English, Fredoka 700 with a dark outline, at the bottom of the 9:16 safe band (≤1330 px),
  colour by speaker (cop white, guy peach `#FFC896`), max ~5 words a line, two lines allowed.
- Motion: fast in with a soft overshoot; camera whips with speed lines between scales; the snap back is the
  fastest move; nothing holds still longer than ~1 s; acting goes through a take (anticipation, squash, new face, settle).
- Render budget: no real-time shadows (baked blob shadows), no glass transmission, ≤5,000 particles.

## Story formula (what worked in episode 1)
1. **Hook (0–2 s):** frame 0 is a thumbnail: a face, a situation, a sound (police whistle).
2. **Conflict:** the cop accuses the guy of something absurd but true.
3. **Evidence, scale by scale:** each fact lands as a big number on its spoken word, with a whip to a new world.
4. **Reversal:** the fact turns on the accuser (the radar reads the cop too).
5. **Beat:** a comic sound (sad trombone) on the loser's face.
6. **Resolution:** chai together. **End card** with the moral in Roman Hinglish, held ~2 s.

## Rules that are not negotiable
- **Facts:** research every number, keep only what sources agree on; if they disagree, show a defensible floor
  with "+" and say "kam se kam" / "at least". The spoken number must match the on-screen number exactly
  (episode 1 re-recorded "सत्रह सौ" → "सोलह सौ सत्तर" for 1,670).
- **Voice:** never sped up. Tighten pauses inside silences instead, or re-record.
- **Credits:** before spending ElevenLabs credits on a new video, show the plan and wait for OK, unless the person
  gives a free hand for that video.
- **Libraries/fonts via npm only, never a CDN.** Vendored copies live in `assets/vendor/`.
- **Sound:** effects 8–12 dB under the dialogue, never covering a word; master −14 LUFS, true peak about −1 dBTP.
- Show frames before the final render; draft at 720 first.

## Pipeline (how episode 1 was made)
- HyperFrames project; the whole film is one three.js scene (`assets/challan-scene.js`) driven by
  `compositions/world.html` (type, captions, number labels, end card). `render(t)` is a pure function of time.
- Voice: one ElevenLabs take per line → `tools/build-dialogue.py` loudness-matches (−19 LUFS) and places lines
  at slot times, applies cuts inside silences, writes `assets/audio/dialogue.wav` + `lines.json` (word times).
- Word timings: **ElevenLabs Scribe** (`creative_transcribe_audio`, 0 credits). Local whisper cannot download
  models here (huggingface.co is blocked).
- Sound effects: `tools/build-sfx.py` (bundled HyperFrames SFX + ElevenLabs-generated whistle, radar zap,
  sad trombone, 50 credits each). Openverse is blocked here.
- Mastering: `tools/master.sh` (two-pass loudnorm to −14 LUFS, video copied, trimmed to length).
- Renders: draft `-c draft.html` at 720×1280 (~5.5 min); final 1080×1920 (~10 min);
  4K `--resolution portrait-4k` (~33 min; the scene follows `devicePixelRatio`).
- Thumbnails: `thumb-hero.html` + `thumb.html` + `thumbs/epNN.json` + `tools/render-thumbs.cjs`
  (rules in `thumbs/README.md`). Stills need a local server: `python3 -m http.server 8765 --bind 127.0.0.1`.

## Publishing (episode 1 style)
- Title: story first + number, e.g. "Chai Peete Hue Challan Kat Gaya! 😂 720,000 km/h Speeding #Shorts".
- Description: Hinglish hook line, the facts as emoji bullets, a comment prompt, subscribe line, sources,
  first 3 hashtags `#Shorts #ChaiPeCosmos #ScienceInHindi`.
- Pin a comment that invites replies. Thumbnail: the 9:16 cover in the mobile app.

## Growth playbook (every episode)
Shorts grow on watch-through, rewatches and comments; likes and subscribers follow. Earn attention first,
ask in character only after the payoff, never at the start.
- **Subscribe challan sign-off (~2 s, after the end card beat):** the cop turns to camera, beacon flashing:
  "Aur aap? Subscribe nahi kiya? Challan katega!"; the guy raises his kulhad: "Chai pe milte hain!".
  Rotate the wording every episode; record it with the series voices.
- **One comment question inside the story**, answerable with a number or a pick
  ("Aapka wazan Jupiter pe kitna hoga? Comment karo!"). Also put it in the pinned comment.
- **Teaser of the next episode** in the last beat ("Agla challan: Chand ki FIR…").
- **Loop-friendly ending** when the story allows: the last frame flows into the first.
- **Series name:** "Hawaldar Sahab ke Challan": playlist + a small "Challan #N" tag on the thumbnail.
- **Schedule:** 2–3 Shorts a week, same time (evenings, 7–9 pm IST).
- **Upload checklist:** pinned comment with a playful question; reply to and heart comments in the first hour;
  "Related video" link to the previous episode; subscribe watermark (avatar) set in YouTube Studio → Branding;
  community poll for the next topic once available.
- **Measure:** "Viewed vs. swiped away" (aim 70%+) and subscribers gained per Short; keep what works and log it
  under Lessons.

## Episode log
| # | Title | Fact(s) | Characters | Files |
|---|-------|---------|------------|-------|
| 1 | Chai Peete Hue Challan Kat Gaya! (Challan) | Earth spin 1,670 km/h; orbit 107,000 km/h; around the Milky Way 720,000+ km/h | guy, cop | `renders/challan_9x16_1080x1920.mp4`, `renders/challan_9x16_4K_2160x3840.mp4`, `thumbs/out/ep01-*` |

Running jokes to reuse: "same to same", the cop's radar gun, the second kulhad from the hoodie pocket,
"Sab ___ mein hain" end cards, the beacon dying when the cop loses.

## Lessons
- Clay colours wash out under the bright key light: the home world renders at exposure 0.85 (others 1.05),
  clay has low specular (0.25) and no sheen.
- Raised land faces on the low-poly Earth leave cracks; colour faces only, never lift them.
- Short captions (<1 s) fail the reading check: merge them into two-line captions.
- Thumbnail at 168 px wide is the real test: one number, one sticker, big faces.
