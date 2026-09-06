#!/usr/bin/env python3
"""Render the world atlas: a top-down plan of every world, drawn from the data.

    python3 scripts/gen_atlas.py [output.html]

Every plan on the page is generated from world_data.py — the same source the
Blender blockout builds from — so what you see is genuinely what gets built,
not an illustration of it.
"""

import html
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "blender"))

from world_data import WORLDS  # noqa: E402

# One hue per world, so sixteen plans never read as the same place twice.
ACCENT = {
    "trailer":         ("#FFB44D", "amber"),
    "portal_hub":      ("#C69BFF", "violet"),
    "living_city":     ("#FF3DCB", "magenta"),
    "the_deep":        ("#2FD9D2", "teal"),
    "the_garden":      ("#7BE86A", "green"),
    "the_void":        ("#8A7BFF", "indigo"),
    "thought_world":   ("#FF8FA8", "rose"),
    "the_dreaming":    ("#B98CFF", "lilac"),
    "the_wasteland":   ("#E88A3D", "rust"),
    "pet_sanctuary":   ("#A8D96B", "moss"),
    "bio_metropolis":  ("#4FE0A0", "jade"),
    "plasma_strait":   ("#4FA8FF", "electric blue"),
    "ruins_labyrinth": ("#D8C48A", "bone"),
    "gravity_ring":    ("#66D8FF", "cyan"),
    "the_arcade":      ("#FF5FA0", "hot pink"),
    "crystal_shatter": ("#9FE8FF", "ice"),
    "portal_glade":    ("#6FD98C", "forest"),
    "the_cascades":    ("#5FD4E8", "spray"),
    "the_bazaar":      ("#FFC96B", "lantern"),
}

ROUND = {"island", "dome", "stalk", "cap", "core", "cabinet", "shard", "rock",
         "spire", "bed", "crate", "trunk", "boulder", "lantern", "parasol",
         "firepit"}


def extent(world):
    xs, ys = [], []
    for s in world["structures"]:
        xs += [s["loc"][0] - s["size"][0], s["loc"][0] + s["size"][0]]
        ys += [s["loc"][1] - s["size"][1], s["loc"][1] + s["size"][1]]
    for t in world["interactables"]:
        xs.append(t["at"][0]); ys.append(t["at"][1])
    if world.get("ground"):
        gx, gy = world["ground"]["size"]
        xs += [-gx / 2, gx / 2]; ys += [-gy / 2, gy / 2]
    if not xs:
        xs, ys = [-8, 8], [-8, 8]
    span = max(max(xs) - min(xs), max(ys) - min(ys), 12.0)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return cx, cy, span * 1.06


def plan_svg(key, world, size=460):
    """Top-down plan. +Y is up on the page, as on a map."""
    accent, _ = ACCENT[key]
    cx, cy, span = extent(world)
    k = size / span

    def px(x): return round((x - cx) * k + size / 2, 1)
    def py(y): return round(size / 2 - (y - cy) * k, 1)

    parts = [f'<svg viewBox="0 0 {size} {size}" role="img" '
             f'aria-label="Top-down plan of {html.escape(world["name"])}">']
    parts.append(f'<rect x="0" y="0" width="{size}" height="{size}" fill="#0C0B17"/>')

    # grid, 20 m
    step = 20 * k
    if step > 8:
        n = int(size / step) + 2
        for i in range(-n, n):
            gx = round(size / 2 + i * step, 1)
            parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{size}" '
                         f'stroke="#1C1A2E" stroke-width="1"/>')
            parts.append(f'<line x1="0" y1="{gx}" x2="{size}" y2="{gx}" '
                         f'stroke="#1C1A2E" stroke-width="1"/>')

    if world.get("ground"):
        gx, gy = world["ground"]["size"]
        parts.append(f'<rect x="{px(-gx / 2)}" y="{py(gy / 2)}" '
                     f'width="{round(gx * k, 1)}" height="{round(gy * k, 1)}" '
                     f'fill="{accent}" fill-opacity="0.045" '
                     f'stroke="{accent}" stroke-opacity="0.22" stroke-width="1"/>')

    heights = [s["size"][2] for s in world["structures"]] or [1.0]
    hmax = max(heights)
    for s in world["structures"]:
        x, y = s["loc"][0], s["loc"][1]
        w, d = max(s["size"][0] * k, 1.4), max(s["size"][1] * k, 1.4)
        # taller things read brighter, so height shows in a flat plan
        op = round(0.20 + 0.55 * (s["size"][2] / hmax), 3)
        if s["kind"] in ROUND:
            parts.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="{round(max(w, d) / 2, 1)}" '
                         f'fill="{accent}" fill-opacity="{op}"/>')
        else:
            parts.append(
                f'<g transform="rotate({-s.get("rot", 0)} {px(x)} {py(y)})">'
                f'<rect x="{round(px(x) - w / 2, 1)}" y="{round(py(y) - d / 2, 1)}" '
                f'width="{round(w, 1)}" height="{round(d, 1)}" '
                f'fill="{accent}" fill-opacity="{op}"/></g>')

    # interactables
    for t in world["interactables"]:
        x, y = px(t["at"][0]), py(t["at"][1])
        if t.get("coop"):
            parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="none" '
                         f'stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="1"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#FFFFFF" '
                     f'fill-opacity="0.92"/>')

    # arrival portal
    p = world["portal"]
    parts.append(f'<circle cx="{px(p[0])}" cy="{py(p[1])}" r="11" fill="none" '
                 f'stroke="{accent}" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{px(p[0])}" cy="{py(p[1])}" r="4" fill="{accent}"/>')

    # scale bar
    bar = 50 * k
    if bar < size * 0.6:
        parts.append(f'<line x1="16" y1="{size - 16}" x2="{round(16 + bar, 1)}" '
                     f'y2="{size - 16}" stroke="#8F88AD" stroke-width="2"/>')
        parts.append(f'<text x="16" y="{size - 24}" fill="#8F88AD" '
                     f'font-family="ui-monospace,monospace" font-size="12">50 m</text>')
    parts.append("</svg>")
    return "".join(parts)


def vocab(world):
    counts = {}
    for s in world["structures"]:
        counts[s["kind"]] = counts.get(s["kind"], 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def chips(world):
    r = world["rules"]
    out = [("gravity", str(r.get("gravity", 1.0)))]
    out.append(("combat", "yes" if r.get("combat") else "none"))
    pvp = r.get("pvp")
    out.append(("pvp", pvp if isinstance(pvp, str) else ("yes" if pvp else "none")))
    out.append(("vehicles", "yes" if r.get("vehicles") else "no"))
    if r.get("swim"):
        out.append(("swim", "yes"))
    g = world.get("ground")
    out.append(("ground", f'{g["size"][0]}×{g["size"][1]} m' if g else "open space"))
    return out


def plate(index, key, world):
    accent, hue = ACCENT[key]
    e = html.escape
    rows = []
    for t in world["interactables"]:
        extra = t.get("secret") or t.get("repeat") or ""
        tag = ' <span class="two-p">2P</span>' if t.get("coop") else ""
        rows.append(
            f'<tr><th scope="row">{e(t["name"])}{tag}</th>'
            f'<td class="prompt">{e(t["prompt"])}</td>'
            f'<td>{e(t["does"])}{f"<em>{e(extra)}</em>" if extra else ""}</td></tr>')
    vocab_html = "".join(
        f'<li><span class="n">{n}</span>{e(k.replace("_", " "))}</li>'
        for k, n in vocab(world)[:6]) or '<li><span class="n">1</span>hand-built room</li>'
    chip_html = "".join(f'<div class="chip"><span>{e(a)}</span><b>{e(b)}</b></div>'
                        for a, b in chips(world))
    return f'''
<section class="plate" id="{e(key)}" style="--accent:{accent}">
  <div class="plan">{plan_svg(key, world)}</div>
  <div class="detail">
    <p class="eyebrow"><span class="idx">{index:02d}</span> {e(world["kind"])} · {e(hue)}</p>
    <h2>{e(world["name"])}</h2>
    <p class="tagline">{e(world["tagline"])}</p>
    <p class="source">{e(world.get("source", "GDD Part I"))}</p>
    <div class="chips">{chip_html}</div>
    <p class="vocab-label">Built from</p>
    <ul class="vocab">{vocab_html}</ul>
    <p class="vocab-label">{len(world["interactables"])} things to find</p>
    <div class="table-wrap">
      <table><tbody>{"".join(rows)}</tbody></table>
    </div>
  </div>
</section>'''


def build(out_path):
    e = html.escape
    total_i = sum(len(w["interactables"]) for w in WORLDS.values())
    total_s = sum(len(w["structures"]) for w in WORLDS.values())
    coop = sum(1 for w in WORLDS.values() for t in w["interactables"] if t.get("coop"))
    secrets = sum(1 for w in WORLDS.values() for t in w["interactables"]
                  if t.get("secret") or t.get("repeat"))
    plates = "".join(plate(i + 1, k, w) for i, (k, w) in enumerate(WORLDS.items()))
    nav = "".join(
        f'<a href="#{e(k)}" style="--accent:{ACCENT[k][0]}">{e(w["name"])}</a>'
        for k, w in WORLDS.items())

    doc = f'''<title>Reality Machine Atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;800&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Single-theme by intent: this is a neon multiverse seen on a dark screen.
   Every colour is painted explicitly so the page holds on any host ground. */
:root {{
  --ground:#0B0A14; --plate:#131126; --edge:#241F3D;
  --ink:#EDE9FA; --muted:#948CB4; --faint:#635C82;
  --accent:#FF3DCB;
  --f-display:"Syne","Trebuchet MS",sans-serif;
  --f-body:"IBM Plex Sans",system-ui,sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,monospace;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--f-body); font-size:15px; line-height:1.6;
  -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:1180px; margin:0 auto; padding:0 24px 96px; }}

header.top {{ padding:72px 0 40px; border-bottom:1px solid var(--edge); }}
h1 {{ font-family:var(--f-display); font-weight:800; font-size:clamp(38px,6vw,68px);
  line-height:0.98; letter-spacing:-0.02em; margin:0 0 18px; text-wrap:balance;
  background:linear-gradient(96deg,#FF3DCB 0%,#C69BFF 42%,#3DE8FF 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent; }}
.lede {{ max-width:62ch; color:var(--muted); font-size:17px; margin:0 0 8px; }}
.lede strong {{ color:var(--ink); font-weight:600; }}

.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(132px,1fr));
  gap:1px; background:var(--edge); border:1px solid var(--edge); margin:36px 0 0; }}
.stats div {{ background:var(--ground); padding:16px 18px; }}
.stats b {{ display:block; font-family:var(--f-display); font-weight:800;
  font-size:30px; line-height:1; letter-spacing:-0.02em; }}
.stats span {{ font-family:var(--f-mono); font-size:11px; text-transform:uppercase;
  letter-spacing:0.12em; color:var(--faint); }}

nav.jump {{ display:flex; flex-wrap:wrap; gap:6px; padding:26px 0 0; }}
nav.jump a {{ font-family:var(--f-mono); font-size:11.5px; letter-spacing:0.04em;
  text-decoration:none; color:var(--muted); border:1px solid var(--edge);
  padding:5px 10px; transition:color .15s,border-color .15s; }}
nav.jump a:hover, nav.jump a:focus-visible {{ color:var(--accent);
  border-color:var(--accent); outline:none; }}

.plate {{ display:grid; grid-template-columns:460px minmax(0,1fr); gap:44px;
  padding:64px 0; border-bottom:1px solid var(--edge); align-items:start; }}
.plan {{ position:sticky; top:24px; border:1px solid var(--edge); line-height:0; }}
.plan svg {{ width:100%; height:auto; display:block; }}

.eyebrow {{ font-family:var(--f-mono); font-size:11px; text-transform:uppercase;
  letter-spacing:0.14em; color:var(--faint); margin:0 0 10px; }}
.idx {{ color:var(--accent); font-weight:500; }}
.plate h2 {{ font-family:var(--f-display); font-weight:800;
  font-size:clamp(28px,3.4vw,40px); line-height:1.02; letter-spacing:-0.02em;
  margin:0 0 10px; color:var(--accent); text-wrap:balance; }}
.tagline {{ font-size:17px; margin:0 0 6px; max-width:60ch; }}
.source {{ font-family:var(--f-mono); font-size:11.5px; color:var(--faint);
  margin:0 0 22px; max-width:60ch; }}

.chips {{ display:flex; flex-wrap:wrap; gap:1px; background:var(--edge);
  border:1px solid var(--edge); margin:0 0 26px; }}
.chip {{ background:var(--ground); padding:9px 13px; flex:1 1 auto; }}
.chip span {{ display:block; font-family:var(--f-mono); font-size:10px;
  text-transform:uppercase; letter-spacing:0.1em; color:var(--faint); }}
.chip b {{ font-weight:600; font-size:14px; font-variant-numeric:tabular-nums; }}

.vocab-label {{ font-family:var(--f-mono); font-size:10.5px; text-transform:uppercase;
  letter-spacing:0.14em; color:var(--faint); margin:0 0 10px;
  padding-bottom:8px; border-bottom:1px solid var(--edge); }}
ul.vocab {{ list-style:none; display:flex; flex-wrap:wrap; gap:8px;
  margin:0 0 30px; padding:0; }}
ul.vocab li {{ font-family:var(--f-mono); font-size:12px; color:var(--muted);
  border:1px solid var(--edge); padding:4px 9px; }}
ul.vocab .n {{ color:var(--accent); margin-right:7px;
  font-variant-numeric:tabular-nums; }}

.table-wrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; }}
tbody tr {{ border-bottom:1px solid var(--edge); }}
tbody tr:last-child {{ border-bottom:none; }}
th, td {{ text-align:left; vertical-align:top; padding:11px 14px 11px 0;
  font-weight:400; }}
th {{ font-weight:600; width:23%; min-width:150px; }}
td.prompt {{ font-family:var(--f-mono); font-size:12px; color:var(--accent);
  width:20%; min-width:130px; white-space:nowrap; }}
td em {{ display:block; font-style:normal; color:var(--faint); font-size:13.5px;
  margin-top:3px; }}
.two-p {{ font-family:var(--f-mono); font-size:9.5px; letter-spacing:0.08em;
  border:1px solid var(--accent); color:var(--accent); padding:1px 4px;
  vertical-align:middle; margin-left:6px; }}

footer {{ padding:56px 0 0; color:var(--faint); font-size:13.5px; max-width:66ch; }}
footer code {{ font-family:var(--f-mono); font-size:12.5px; color:var(--muted); }}

@media (max-width:900px) {{
  .plate {{ grid-template-columns:1fr; gap:28px; }}
  .plan {{ position:static; }}
  th {{ width:auto; }}
}}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<div class="wrap">
<header class="top">
  <h1>Sixteen places,<br>no two alike</h1>
  <p class="lede">Every world in <strong>The Reality Machine</strong>, drawn from the
  project's actual world data — the same file the Blender blockout and the Unreal
  data tables are generated from. These plans are not illustrations of the design.
  They <strong>are</strong> the design.</p>
  <p class="lede">Each plan is top down, north up, to scale. Filled shapes are
  blockout structures, brighter where they are taller. White dots are things you
  can walk up to and touch; a ring around a dot means it takes two players. The
  large ring is where you arrive, and where the portal throws you home from.</p>
  <div class="stats">
    <div><b>{len(WORLDS)}</b><span>spaces</span></div>
    <div><b>{total_i}</b><span>things to find</span></div>
    <div><b>{total_s}</b><span>structures</span></div>
    <div><b>{coop}</b><span>need two players</span></div>
    <div><b>{secrets}</b><span>reward a second look</span></div>
  </div>
  <nav class="jump">{nav}</nav>
</header>
{plates}
<footer>
  <p>Generated by <code>scripts/gen_atlas.py</code> from
  <code>blender/world_data.py</code>. Change a world in that file
  and the plan, the Blender blockout, the Unreal data tables and this page all
  change together.</p>
  <p>Grey boxes at true scale, on purpose: the blockout is the level design, and it
  gets walked and timed before anything is sculpted. Art comes after the space works.</p>
</footer>
</div>'''
    with open(out_path, "w") as handle:
        handle.write(doc)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "build", "atlas.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    print(f"[rm] wrote {build(out)}")
