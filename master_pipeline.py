"""
MASTER PIPELINE (v2 - with vector graphics fallback)
USAGE: python master_pipeline.py "path/to/your.pdf"
"""
import sys
import os
import re
import subprocess
import fitz
from PIL import Image
import io
import shutil

# Dynamic lookup for nougat executable
env_nougat = os.path.join(os.path.dirname(sys.executable), "nougat.exe" if os.name == "nt" else "nougat")
if os.path.exists(env_nougat):
    NOUGAT_EXE = env_nougat
else:
    NOUGAT_EXE = shutil.which("nougat") or "nougat"

def run_pipeline(pdf_path):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_root = f"pipeline_output_{base_name}"
    nougat_out_dir = os.path.join(output_root, "nougat_text")
    images_dir = os.path.join(output_root, "images")
    os.makedirs(nougat_out_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # ---- STEP 1: Nougat ----
    print(f"[1/5] Running Nougat on: {pdf_path}")
    subprocess.run(
        [NOUGAT_EXE, pdf_path, "-o", nougat_out_dir, "--model", "0.1.0-base"],
        check=True
    )
    mmd_path = os.path.join(nougat_out_dir, base_name + ".mmd")
    if not os.path.exists(mmd_path):
        print(f"ERROR: Nougat output missing: {mmd_path}")
        sys.exit(1)
    print(f"    Done. Text saved: {mmd_path}")

    # ---- STEP 2: Embedded (raster) images extract karo ----
    print("[2/5] Extracting embedded images from PDF...")
    doc = fitz.open(pdf_path)
    page_images = {}
    for page_num in range(len(doc)):
        images = doc[page_num].get_images(full=True)
        if images:
            page_images[page_num] = [doc.extract_image(img[0])["image"] for img in images]
    print(f"    Pages with embedded images found: {list(page_images.keys())}")

    # ---- STEP 3: Stitch embedded images (per page) ----
    print("[3/5] Stitching multi-part embedded images...")
    stitched_paths = []
    for page_num, img_bytes_list in page_images.items():
        imgs = [Image.open(io.BytesIO(b)) for b in img_bytes_list]
        width = max(im.width for im in imgs)
        total_height = sum(im.height for im in imgs)
        combined = Image.new("RGB", (width, total_height), "white")
        y = 0
        for im in imgs:
            combined.paste(im, (0, y))
            y += im.height
        save_path = os.path.join(images_dir, f"page{page_num+1}_figure.png")
        combined.save(save_path)
        stitched_paths.append(save_path)
        print(f"    Saved: {save_path}")

    # ---- STEP 3.5: Vector-graphics fallback ----
    print("[3.5/5] Checking for vector-graphics pages (fallback)...")
    for page_num in range(len(doc)):
        if page_num in page_images:
            continue
        page = doc[page_num]
        drawings = page.get_drawings()
        if len(drawings) > 5:
            print(f"    Page {page_num+1}: {len(drawings)} vector shapes found, rendering full page...")
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            fallback_path = os.path.join(images_dir, f"page{page_num+1}_vector_render.png")
            pix.save(fallback_path)
            stitched_paths.append(fallback_path)
            print(f"    Saved: {fallback_path}")
    doc.close()

    print(f"    Total figures/images collected: {len(stitched_paths)}")

    # ---- STEP 4: Merge text + images ----
    print("[4/5] Merging text and images...")
    with open(mmd_path, "r", encoding="utf-8") as f:
        text = f.read()

    fig_pattern = re.compile(
        r"((?:Figure\s+\d+|maximum value of Z|feasible region).*?(?:is\s*:|\.))",
        re.IGNORECASE
    )
    img_idx = [0]

    def replacer(match):
        line = match.group(1)
        if img_idx[0] < len(stitched_paths):
            rel_path = os.path.relpath(stitched_paths[img_idx[0]], output_root)
            img_idx[0] += 1
            return line + f"\n\n![figure]({rel_path.replace(os.sep, '/')})\n\n"
        return line

    merged_text = fig_pattern.sub(replacer, text, count=len(stitched_paths))

    final_path = os.path.join(output_root, "FINAL_OUTPUT.md")
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(merged_text)

    print(f"\n[5/5] COMPLETE! Final file: {final_path}")
    print(f"   Images inserted: {img_idx[0]} / {len(stitched_paths)}")
    print(f"\nKholne ke liye: code {output_root}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python master_pipeline.py "path/to/your.pdf"')
        sys.exit(1)
    run_pipeline(sys.argv[1])