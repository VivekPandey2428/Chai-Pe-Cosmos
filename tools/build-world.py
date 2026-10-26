"""Writes an episode's compositions/world.html and index.html from <episode>/story.json, in Episode 1's type styles.

story.json: {title, duration, scene_note, caps: [{unit, label, in, out}] (labels under the 3D numbers),
tags: [{top, text, sub?, in, out, color?}] (text-only callouts), captions: [{who: cop|guy, text, in, out}],
end: {lines: [[word, ...], ...], at, size}}. Captions longer than ~20 characters wrap into two lines.
"""
import html, json, os, sys

ep = os.path.abspath(sys.argv[1])
S = json.load(open(os.path.join(ep, "story.json"), encoding="utf-8"))
D = S["duration"]


def wrap(text):
    if len(text) <= 20 or "<br" in text:
        return html.escape(text), "<br" in text
    words = text.split()
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return html.escape(" ".join(words[:best])) + "<br />" + html.escape(" ".join(words[best:])), True


caps_html, caps_js = [], []
for i, c in enumerate(S["caps"], 1):
    caps_html.append(f'        <div class="w-cap" id="w-cap{i}">\n          <span class="w-unit" id="w-unit{i}">{html.escape(c["unit"])}</span>\n'
                     f'          <span class="w-label" id="w-label{i}">{html.escape(c["label"])}</span>\n        </div>')
    caps_js.append({"cap": f"#w-cap{i}", "unit": f"#w-unit{i}", "label": f"#w-label{i}", "inAt": c["in"], "outAt": c["out"]})
tags_html, tags_js = [], []
for i, t in enumerate(S.get("tags", []), 1):
    sub = f'<span class="w-tag-sub">{html.escape(t["sub"])}</span>' if t.get("sub") else ""
    style = f'top: {t["top"]}px;' + (f' color: {t["color"]};' if t.get("color") else "") + (f' font-size: {t["size"]}px;' if t.get("size") else "")
    tags_html.append(f'        <div class="w-tag" id="w-tag{i}" style="{style}"><span class="w-tag-main">{html.escape(t["text"])}</span>{sub}</div>')
    tags_js.append({"id": f"#w-tag{i}", "in": t["in"], "out": t["out"]})
cc_html, cc_js = [], []
for i, c in enumerate(S["captions"], 1):
    txt, two = wrap(c["text"])
    cc_html.append(f'        <div class="cc cc-{c["who"]}{" cc-2" if two else ""}" id="w-cc{i}">{txt}</div>')
    cc_js.append({"id": f"#w-cc{i}", "in": c["in"], "out": c["out"]})
end = S["end"]
end_ids, end_lines = [], []
for line in end["lines"]:
    spans = []
    for w in line:
        end_ids.append(f"#w-end{len(end_ids) + 1}")
        spans.append(f'<span id="w-end{len(end_ids)}">{html.escape(w)}</span>')
    end_lines.append(" ".join(spans))
end_out = end.get("out", D)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "compositions", "world.html"), encoding="utf-8").read()
head = tpl[: tpl.index("    </style>")]
head = head.replace("<title>Challan</title>", f"<title>{html.escape(S['title'])}</title>")
head = head.replace("font-size: 150px;\n        line-height: 1;", f"font-size: {end.get('size', 150)}px;\n        line-height: 1.02;")
head = head.replace("<!--\n  Challan (9:16)", f"<!--\n  {S['title']} (9:16). {S.get('scene_note', '')}\n  Built on Episode 1, Challan (9:16)")
extra_css = """      /* text-only callouts (no 3D number): a big word with an optional line under it */
      .w-tag {
        position: absolute;
        font-size: 84px;
        left: 60px;
        width: 960px;
        text-align: center;
        opacity: 0;
        color: #ffffff;
        text-shadow: 0 0 4px #2a1530, 3px 3px 0 #2a1530, -3px 3px 0 #2a1530, 3px -3px 0 #2a1530, -3px -3px 0 #2a1530, 0 8px 18px rgba(0, 0, 0, 0.35);
      }
      .w-tag-main {
        display: block;
        font-weight: 700;
        font-size: 1em;
        line-height: 1.05;
        text-transform: uppercase;
      }
      .w-tag-sub {
        display: block;
        margin-top: 12px;
        font-weight: 600;
        font-size: 0.64em;
        line-height: 1.1;
        text-transform: uppercase;
      }
"""
out = head + extra_css + f"""    </style>
  </head>
  <body>
    <div id="root" data-composition-id="world" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="w-bg"></div>
      <div id="w-police"></div>
      <canvas id="w-canvas" width="1080" height="1920"></canvas>
      <canvas id="w-lines" width="1080" height="1920"></canvas>
      <div id="w-stage" data-layout-allow-overflow>
{chr(10).join(caps_html)}
{chr(10).join(tags_html)}
{chr(10).join(cc_html)}
        <div id="w-end">{"<br />".join(end_lines)}</div>
      </div>
    </div>

    <script>
      (function () {{
        var root = document.getElementById("root");
        var duration = parseFloat(root.dataset.duration) || {D};
        var clock = {{ t: 0 }};
        var host = {{ duration: duration, clock: clock, render: null }};
        window.__world = host;
        window.__hf = window.__hf || {{}};
        window.__hf.buildReady = window.__hf.buildReady || {{}};
        window.__hf.buildReady["world"] = new Promise(function (resolve) {{
          host.ready = resolve;
        }});

        // scale the 1080x1920 type stage to whatever size the root renders at (720p draft or 1080p master)
        var stage = document.getElementById("w-stage");
        stage.style.transform = "scale(" + (window.innerWidth || 1080) / 1080 + ")";

        var tl = gsap.timeline({{ paused: true }});
        tl.to(clock, {{ t: duration, duration: duration, ease: "none", onUpdate: function () {{ if (host.render) host.render(clock.t); }} }}, 0);
        // number labels: unit pops as the number lands, label follows, both leave on the next whip
        {json.dumps(caps_js)}.forEach(function (c) {{
          tl.fromTo(c.cap, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, c.inAt - 0.01);
          tl.fromTo(c.unit, {{ y: 40, scale: 0.6 }}, {{ y: 0, scale: 1, duration: 0.32, ease: "back.out(2.2)" }}, c.inAt);
          tl.fromTo(c.label, {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, c.inAt + 0.1);
          tl.to(c.cap, {{ opacity: 0, scale: 0.7, duration: 0.14, ease: "power3.in" }}, c.outAt);
        }});
        // text callouts: slam in like the number labels, leave fast
        {json.dumps(tags_js)}.forEach(function (c) {{
          tl.fromTo(c.id, {{ opacity: 0, scale: 1.5, y: -20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2.2)" }}, c.in);
          tl.to(c.id, {{ opacity: 0, scale: 0.7, duration: 0.14, ease: "power3.in" }}, c.out - 0.14);
        }});
        // dialogue captions: pop in on the first word, cut out when the phrase ends
        {json.dumps(cc_js)}.forEach(function (c) {{
          tl.fromTo(c.id, {{ opacity: 0, scale: 0.86, y: 14 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "back.out(2)" }}, c.in);
          tl.to(c.id, {{ opacity: 0, duration: 0.06 }}, c.out - 0.06);
        }});
        // end card: words slam in, one per beat, and clear before the sign-off
        {json.dumps(end_ids)}.forEach(function (id, i) {{
          tl.fromTo(id, {{ opacity: 0, scale: 1.8, y: -30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.24, ease: "back.out(2.4)" }}, {end["at"]} + i * 0.16);
          tl.to(id, {{ opacity: 0, duration: 0.12 }}, {end_out} - 0.12);
        }});
        window.__timelines = window.__timelines || {{}};
        window.__timelines["world"] = tl;
      }})();
    </script>

    <script type="module" src="assets/challan-scene.js"></script>
  </body>
</html>
"""
os.makedirs(os.path.join(ep, "compositions"), exist_ok=True)
open(os.path.join(ep, "compositions/world.html"), "w", encoding="utf-8").write(out)
idx = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html"), encoding="utf-8").read()
idx = idx.replace('data-duration="31.3"', f'data-duration="{D}"')
open(os.path.join(ep, "index.html"), "w", encoding="utf-8").write(idx)
print("wrote", os.path.join(ep, "compositions/world.html"), len(cc_js), "captions,", len(caps_js), "number labels,", len(tags_js), "tags")
