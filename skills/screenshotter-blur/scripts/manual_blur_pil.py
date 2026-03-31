#!/usr/bin/env python3
"""
手動模糊腳本 - 使用 PIL/Pillow 模糊圖片中的特定區域

用法:
    python manual_blur_pil.py --input input.png --regions "x,y,w,h x,y,w,h" --output output.png

依賴:
    pip install pillow
"""

import argparse
from PIL import Image, ImageDraw
import os
import sys


def parse_regions(regions_str):
    """解析區域字串為座標列表"""
    regions = []
    for region in regions_str.split():
        coords = region.split(",")
        if len(coords) != 4:
            print(f"警告: 跳過無效座標 '{region}'", file=sys.stderr)
            continue
        try:
            x, y, w, h = map(int, coords)
            regions.append((x, y, w, h))
        except ValueError:
            print(f"警告: 跳過無效座標 '{region}'", file=sys.stderr)
    return regions


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


def main():
    parser = argparse.ArgumentParser(description="手動模糊圖片中的特定區域")
    parser.add_argument("--input", "-i", required=True, help="輸入圖片路徑")
    parser.add_argument(
        "--regions",
        "-r",
        required=True,
        help="模糊區域座標 (x,y,w,h)，多個區域用空格分隔",
    )
    parser.add_argument(
        "--output", "-o", default=None, help="輸出圖片路徑 (預設: input-blurred.png)"
    )
    parser.add_argument(
        "--method",
        "-m",
        default="solid",
        choices=["solid", "pixelate"],
        help="模糊方法",
    )
    parser.add_argument(
        "--block-size", "-b", type=int, default=10, help="像素化區塊大小 (預設: 10)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"錯誤: 找不到輸入檔案 '{args.input}'", file=sys.stderr)
        sys.exit(1)

    img = Image.open(args.input)
    if img.mode != "RGB":
        img = img.convert("RGB")

    regions = parse_regions(args.regions)
    if not regions:
        print("錯誤: 沒有有效的模糊區域", file=sys.stderr)
        sys.exit(1)

    if args.method == "solid":
        img = apply_solid_redaction(img, regions)
    else:
        img = apply_pixelation(img, regions, args.block_size)

    if args.output is None:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}-blurred{ext}"

    img.save(args.output)
    print(f"已儲存模糊後的圖片: {args.output}")
    print(f"模糊區域數量: {len(regions)}")
    print(f"模糊方法: {args.method}")


if __name__ == "__main__":
    main()
