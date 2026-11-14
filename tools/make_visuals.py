"""Draw the README images: sidebar before/after (PNG + GIF), flow diagram, relative-cost chart.

python tools/make_visuals.py   ->  docs/*.png, docs/before_after.gif
The cost chart uses EXAMPLE weights (edit WEIGHTS) - not real prices.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)

def font(size, bold=False):
    for name in (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]) + ["DejaVuSans.ttf"]:
        for d in ("C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu", "/Library/Fonts"):
            p = os.path.join(d, name)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

BG, PANEL, TEXT, MUTED = (17, 19, 24), (28, 31, 38), (232, 234, 240), (140, 146, 160)
TIER_COLOR = {"Haiku": (94, 196, 140), "Sonnet": (92, 156, 230), "Opus": (176, 120, 230), "Fable": (236, 120, 86)}

BEFORE = [
    ("session-15", "Fable"), ("Continue previous work about the thing", "Fable"),
    ("fork-2", "Fable"), ("Fix stuff", "Fable"), ("new session", "Fable"),
    ("trailer edit cinematic tension beat sync v6 export", "Fable"),
    ("Untitled", "Fable"), ("check steam page and also upload clips", "Fable"),
]
AFTER = [
    ("[Bug] MLRS truck rolls over on hills", "Fable"), ("[Store] Trailer v6 — beat-synced cut", "Opus"),
    ("[Bug] Ragdoll and possession glitches", "Opus"), ("[Ops] Map split for streaming", "Opus"),
    ("[Content] Fictional vehicle names + i18n", "Sonnet"), ("[Store] Upload clips, save 22 langs", "Sonnet"),
    ("[Bug] Night glow on missiles (done)", "Sonnet"), ("Side chat", "Haiku"),
]

def sidebar(rows, title, w=560, h=520, highlight=None):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.text((24, 20), title, font=font(22, True), fill=TEXT)
    y = 70
    for i, (name, model) in enumerate(rows):
        fill = (40, 44, 54) if highlight == i else PANEL
        d.rounded_rectangle((16, y, w - 16, y + 48), 10, fill=fill)
        shown = name if len(name) <= 38 else name[:37] + "…"
        d.text((32, y + 12), shown, font=font(17), fill=TEXT)
        c = TIER_COLOR[model]
        bw = d.textlength(model, font=font(15, True)) + 20
        d.rounded_rectangle((w - 32 - bw, y + 11, w - 32, y + 37), 13, fill=c)
        d.text((w - 32 - bw + 10, y + 14), model, font=font(15, True), fill=(15, 15, 18))
        y += 56
    return img

def side_by_side():
    a = sidebar(BEFORE, "Before — every child inherits the top model")
    b = sidebar(AFTER, "After — Workspace 2.0")
    img = Image.new("RGB", (a.width * 2 + 24, a.height), BG)
    img.paste(a, (0, 0)); img.paste(b, (a.width + 24, 0))
    img.save(os.path.join(OUT, "before_after.png"))

def gif():
    frames = []
    for _ in range(6):
        frames.append(sidebar(BEFORE, "Before"))
    mixed = list(BEFORE)
    for i in range(len(AFTER)):
        mixed[i] = AFTER[i]
        for _ in range(2):
            frames.append(sidebar(mixed, "Workspace 2.0 routing…", highlight=i))
    for _ in range(10):
        frames.append(sidebar(AFTER, "After"))
    frames[0].save(os.path.join(OUT, "before_after.gif"), save_all=True, append_images=frames[1:],
                   duration=220, loop=0, optimize=True)

def flow():
    steps = ["Task", "Classify\n(route.py)", "Pick model\n(tier table)", "Clean name\n[Category] verb", "Short brief\nreport once", "Hub stays light\nno relays, /compact"]
    w, h = 1210, 200
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    bw, gap = 165, 34
    x = 20
    colors = [(60, 64, 76), (92, 156, 230), (176, 120, 230), (94, 196, 140), (236, 180, 86), (236, 120, 86)]
    for i, s in enumerate(steps):
        d.rounded_rectangle((x, 60, x + bw, 170), 14, fill=colors[i])
        lines = s.split("\n")
        for j, ln in enumerate(lines):
            f = font(19 if j == 0 else 15, j == 0)
            tw = d.textlength(ln, font=f)
            d.text((x + (bw - tw) / 2, 88 + j * 30 - (len(lines) - 1) * 6), ln, font=f, fill=(15, 15, 18))
        if i < len(steps) - 1:
            ax = x + bw + 4
            d.polygon([(ax, 105), (ax + gap - 10, 115), (ax, 125)], fill=MUTED)
        x += bw + gap
    d.text((20, 18), "What happens every time a sub-session is created", font=font(20, True), fill=TEXT)
    img.save(os.path.join(OUT, "flow.png"))

# EXAMPLE relative weights per tier. Edit to match your plan's real prices.
WEIGHTS = {"Haiku": 1, "Sonnet": 3, "Opus": 5, "Fable": 10}

def cost_chart():
    before = sum(WEIGHTS[m] for _, m in BEFORE)
    after = sum(WEIGHTS[m] for _, m in AFTER)
    fig, ax = plt.subplots(figsize=(7, 3.2), dpi=130)
    fig.patch.set_facecolor("#111318"); ax.set_facecolor("#111318")
    bars = ax.barh(["After", "Before"], [after, before], color=["#5ec48c", "#ec7856"], height=0.55)
    for b, v in zip(bars, [after, before]):
        ax.text(v + 1, b.get_y() + b.get_height() / 2, f"{v}  ({v / before:.0%})", va="center", color="#e8eaf0", fontsize=11)
    ax.set_xlim(0, before * 1.25)
    ax.set_title("Relative cost of the same 8 sessions (example weights 1 / 3 / 5 / 10)", color="#e8eaf0", fontsize=11)
    ax.tick_params(colors="#e8eaf0"); [s.set_visible(False) for s in ax.spines.values()]
    ax.set_xticks([])
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "cost_example.png"), facecolor=fig.get_facecolor())

if __name__ == "__main__":
    side_by_side(); gif(); flow(); cost_chart()
    print("written to", OUT)
