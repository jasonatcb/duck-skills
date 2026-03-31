#!/usr/bin/env python3
"""
批次模糊腳本 - 使用 PIL 一次處理多張圖片

用法:
    python batch_blur_pil.py --input-dir images/ --pattern "*.png" --output-dir images/
    python batch_blur_pil.py --input-dir images/ --pattern "ec-*.png" --regions "100,50,200,30"

依賴:
    pip install pillow
"""

import argparse
from PIL import Image, ImageDraw
import os
import sys
from pathlib import Path
import fnmatch


def find_images(input_dir, pattern):
    """找出符合模式的圖片"""
    input_path = Path(input_dir)
    images = []
    for file in input_path.glob("*"):
        if file.is_file() and fnmatch.fnmatch(file.name, pattern):
            if file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
                images.append(file)
    return images


def apply_solid_redaction(img, regions):
    """套用不透明黑色遮罩"""
    draw = ImageDraw.Draw(img)
    for x, y, w, h in regions:
        draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
    return img


def apply_pixelation(img, regions, block_size=10):
    """套用像素化效果"""
    for x, y, w, h in regions:
        roi = img.crop((x, y, x + w, y + h))
        small = roi.resize((block_size, block_size), Image.Resampling.NEAREST)
        pixelated = small.resize((w, h), Image.Resampling.NEAREST)
        img.paste(pixelated, (x, y))
    return img


def parse_regions(regions_str):
    """解析區域字串"""
    if not regions_str:
        return []
    regions = []
    for region in regions_str.split():
        coords = list(map(int, region.split(",")))
        if len(coords) == 4:
            regions.append(tuple(coords))
    return regions


def main():
    parser = argparse.ArgumentParser(description="批次模糊圖片")
    parser.add_argument("--input-dir", "-i", required=True, help="輸入圖片目錄")
    parser.add_argument("--pattern", "-p", default="*.png", help="檔案匹配模式")
    parser.add_argument("--output-dir", "-o", default=None, help="輸出圖片目錄")
    parser.add_argument(
        "--regions",
        "-r",
        default=None,
        help="自訂區域座標 (x,y,w,h)，多個區域用空格分隔",
    )
    parser.add_argument(
        "--method", "-m", default="solid", choices=["solid", "pixelate"]
    )
    parser.add_argument(
        "--block-size", "-b", type=int, default=10, help="像素化區塊大小"
    )

    args = parser.parse_args()

    output_dir = args.output_dir or args.input_dir

    images = find_images(args.input_dir, args.pattern)
    if not images:
        print(f"找不到符合模式的圖片: {args.pattern}")
        sys.exit(1)

    print(f"找到 {len(images)} 張圖片")

    regions = parse_regions(args.regions) if args.regions else []
    if not regions:
        print("警告: 沒有指定模糊區域，將跳過所有圖片")
        sys.exit(1)

    for img_path in images:
        print(f"處理: {img_path.name}")

        img = Image.open(str(img_path))
        if img.mode != "RGB":
            img = img.convert("RGB")

        if args.method == "solid":
            img = apply_solid_redaction(img, regions)
        else:
            img = apply_pixelation(img, regions, args.block_size)

        output_path = Path(output_dir) / f"{img_path.stem}-blurred{img_path.suffix}"
        img.save(str(output_path))
        print(f"  已儲存: {output_path.name}")


if __name__ == "__main__":
    main()
