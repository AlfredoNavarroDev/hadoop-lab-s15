"""Render a terminal-style transcript (prompt + command + output) into a PNG image.
Used to produce 'imagen de los codigos y salidas' evidence for the lab PDF.
"""
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_SIZE = 16
PADDING = 22
LINE_SPACING = 6
BG = (12, 14, 18)
FG = (214, 222, 230)
PROMPT_COLOR = (98, 209, 150)
TITLE_BG = (30, 34, 40)
TITLE_FG = (255, 255, 255)
MAX_WIDTH = 980

def wrap_line(line, font, draw, max_width):
    if draw.textlength(line, font=font) <= max_width:
        return [line]
    words = line.split(" ")
    out, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out or [""]

def render(title, blocks, out_path):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    title_font = ImageFont.truetype(FONT_PATH, FONT_SIZE + 2)

    tmp_img = Image.new("RGB", (10, 10))
    tmp_draw = ImageDraw.Draw(tmp_img)

    content_w = MAX_WIDTH - 2 * PADDING
    rendered_lines = []  # (text, color, is_prompt)
    for block in blocks:
        cmd = block.get("cmd")
        out = block.get("out", "")
        if cmd:
            for wl in wrap_line("$ " + cmd, font, tmp_draw, content_w):
                rendered_lines.append((wl, PROMPT_COLOR))
        for raw_line in out.splitlines():
            for wl in wrap_line(raw_line, font, tmp_draw, content_w):
                rendered_lines.append((wl, FG))
        rendered_lines.append(("", FG))

    line_h = FONT_SIZE + LINE_SPACING
    title_h = 46
    img_h = title_h + PADDING * 2 + line_h * len(rendered_lines)
    img = Image.new("RGB", (MAX_WIDTH, img_h), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, MAX_WIDTH, title_h], fill=TITLE_BG)
    draw.ellipse([16, 15, 32, 31], fill=(237, 106, 94))
    draw.ellipse([38, 15, 54, 31], fill=(245, 191, 79))
    draw.ellipse([60, 15, 76, 31], fill=(97, 194, 83))
    draw.text((92, 13), title, font=title_font, fill=TITLE_FG)

    y = title_h + PADDING
    for text, color in rendered_lines:
        draw.text((PADDING, y), text, font=font, fill=color)
        y += line_h

    img.save(out_path)
    print(f"saved {out_path} ({img.width}x{img.height})")

if __name__ == "__main__":
    spec_path = sys.argv[1]
    out_path = sys.argv[2]
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    render(spec["title"], spec["blocks"], out_path)
