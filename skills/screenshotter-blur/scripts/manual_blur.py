#!/usr/bin/env python3
"""
手動模糊腳本 - 透過指定座標模糊圖片中的特定區域

用法:
    python manual_blur.py --input input.png --regions "x,y,w,h x,y,w,h" --output output.png
    python manual_blur.py --input input.png --regions "100,50,200,30" --output output.png

參數:
    --input: 輸入圖片路徑
    --regions: 模糊區域座標 (x,y,w,h)，多個區域用空格分隔
    --output: 輸出圖片路徑 (預設: input-blurred.png)
    --method: 模糊方法 (solid/pixelate)，預設: solid
"""

import argparse
import cv2
import numpy as np
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
    for x, y, w, h in regions:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    return img


def apply_pixelation(img, regions, block_size=10):
    """套用像素化效果"""
    for x, y, w, h in regions:
        roi = img[y : y + h, x : x + w]
        if roi.size == 0:
            continue
        small = cv2.resize(roi, (block_size, block_size), interpolation=cv2.INTER_AREA)
        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
        img[y : y + h, x : x + w] = pixelated
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

    # 驗證輸入檔案
    if not os.path.exists(args.input):
        print(f"錯誤: 找不到輸入檔案 '{args.input}'", file=sys.stderr)
        sys.exit(1)

    # 讀取圖片
    img = cv2.imread(args.input)
    if img is None:
        print(f"錯誤: 無法讀取圖片 '{args.input}'", file=sys.stderr)
        sys.exit(1)

    # 解析座標
    regions = parse_regions(args.regions)
    if not regions:
        print("錯誤: 沒有有效的模糊區域", file=sys.stderr)
        sys.exit(1)

    # 套用模糊
    if args.method == "solid":
        img = apply_solid_redaction(img, regions)
    else:
        img = apply_pixelation(img, regions, args.block_size)

    # 設定輸出路徑
    if args.output is None:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}-blurred{ext}"

    # 儲存結果
    cv2.imwrite(args.output, img)
    print(f"已儲存模糊後的圖片: {args.output}")
    print(f"模糊區域數量: {len(regions)}")
    print(f"模糊方法: {args.method}")


if __name__ == "__main__":
    main()
