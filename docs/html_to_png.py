#!/usr/bin/env python3
"""Convert the guide HTML to a PNG image using WeasyPrint + CairoSVG + Pillow."""

from pathlib import Path
from weasyprint import HTML
from PIL import Image
from io import BytesIO
import subprocess

html_path = Path(__file__).parent / "claude-computer-use-guide.html"
html_text = html_path.read_text(encoding="utf-8")
html_text = html_text.replace(
    "font-family: -apple-system",
    "font-family: 'IPAGothic', 'WenQuanYi Zen Hei'"
)

out_dir = Path(__file__).parent
out_pdf = out_dir / "claude-computer-use-guide.pdf"
out_png = out_dir / "claude-computer-use-guide.png"

# Step 1: Generate PDF
html = HTML(string=html_text, base_url=str(html_path.parent))
html.write_pdf(str(out_pdf))
print(f"PDF written to {out_pdf}")

# Step 2: Convert PDF pages to PNG images using pdftoppm if available
import shutil
if shutil.which("pdftoppm"):
    prefix = str(out_dir / "page")
    subprocess.run(["pdftoppm", "-png", "-r", "200", str(out_pdf), prefix], check=True)

    page_files = sorted(out_dir.glob("page-*.png"))
    if not page_files:
        print("No page images generated")
        exit(1)

    images = [Image.open(p) for p in page_files]
    total_h = sum(img.height for img in images)
    max_w = max(img.width for img in images)

    stitched = Image.new("RGB", (max_w, total_h), (255, 255, 255))
    y = 0
    for img in images:
        stitched.paste(img, (0, y))
        y += img.height

    stitched.save(str(out_png), "PNG")
    print(f"PNG written to {out_png} ({stitched.width}x{stitched.height})")

    # Cleanup temp page files
    for p in page_files:
        p.unlink()
else:
    print(f"pdftoppm not found. PDF is at {out_pdf}")
    print("Install poppler-utils for PNG conversion: apt install poppler-utils")
