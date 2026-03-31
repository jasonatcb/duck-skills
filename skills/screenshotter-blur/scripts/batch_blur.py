#!/usr/bin/env python3
"""
批次模糊腳本 - 一次處理多張圖片

用法:
    python batch_blur.py --input-dir images/ --pattern "*.png" --output-dir images/
    python batch_blur.py --input-dir images/ --pattern "ec-*.png" --type personal

參數:
    --input-dir: 輸入圖片目錄
    --pattern: 檔案匹配模式 (預設: *.png)
    --output-dir: 輸出圖片目錄 (預設: 與輸入相同)
    --type: PII 類型 (personal/financial/api/all)
    --method: 模糊方法 (solid/pixelate)
"""

import argparse
import cv2
import numpy as np
import os
import sys
from pathlib import Path
import fnmatch

# 預設 PII 類型的區域模板 (x, y, w, h) - 需根據具體圖片調整
# 這些是常見 CYBERBIZ 截圖中需要模糊的位置
PII_TEMPLATES = {
    "personal": [
        (50, 100, 200, 30),  # 姓名欄位
        (50, 140, 200, 30),  # 電話欄位
        (50, 180, 250, 30),  # Email 欄位
        (50, 220, 300, 30),  # 地址欄位
    ],
    "financial": [
        (50, 100, 200, 30),  # 信用卡號
        (50, 140, 150, 30),  # 有效日期
        (50, 180, 100, 30),  # CVV
        (50, 220, 200, 30),  # 銀行帳號
    ],
    "api": [
        (50, 100, 400, 30),  # API Key
        (50, 140, 400, 30),  # API Secret
        (50, 180, 300, 30),  # Token
    ],
    "order": [
        (50, 100, 200, 30),  # 訂單編號
        (50, 140, 200, 30),  # 客戶編號
    ],
}


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


def get_regions_for_type(pii_type):
    """取得指定類型的預設區域"""
    if pii_type == "all":
        regions = []
        for regions_list in PII_TEMPLATES.values():
            regions.extend(regions_list)
        return regions
    return PII_TEMPLATES.get(pii_type, [])


def main():
    parser = argparse.ArgumentParser(description="批次模糊圖片")
    parser.add_argument("--input-dir", "-i", required=True, help="輸入圖片目錄")
    parser.add_argument("--pattern", "-p", default="*.png", help="檔案匹配模式")
    parser.add_argument("--output-dir", "-o", default=None, help="輸出圖片目錄")
    parser.add_argument(
        "--type",
        "-t",
        default="all",
        choices=["personal", "financial", "api", "order", "all"],
        help="PII 類型",
    )
    parser.add_argument(
        "--method", "-m", default="solid", choices=["solid", "pixelate"]
    )
    parser.add_argument("--regions", "-r", default=None, help="自訂區域座標 (x,y,w,h)")

    args = parser.parse_args()

    # 設定輸出目錄
    output_dir = args.output_dir or args.input_dir

    # 找出圖片
    images = find_images(args.input_dir, args.pattern)
    if not images:
        print(f"找不到符合模式的圖片: {args.pattern}")
        sys.exit(1)

    print(f"找到 {len(images)} 張圖片")

    # 解析自訂區域
    regions = None
    if args.regions:
        regions = []
        for region in args.regions.split():
            coords = list(map(int, region.split(",")))
            if len(coords) == 4:
                regions.append(tuple(coords))
    else:
        regions = get_regions_for_type(args.type)

    if not regions:
        print("警告: 沒有指定模糊區域")
        regions = []

    # 處理每張圖片
    for img_path in images:
        print(f"處理: {img_path.name}")

        img = cv2.imread(str(img_path))
        if img is None:
            print(f"  錯誤: 無法讀取圖片")
            continue

        if args.method == "solid":
            img = apply_solid_redaction(img, regions)
        else:
            img = apply_pixelation(img, regions)

        # 儲存輸出
        output_path = Path(output_dir) / f"{img_path.stem}-blurred{img_path.suffix}"
        cv2.imwrite(str(output_path), img)
        print(f"  已儲存: {output_path.name}")


if __name__ == "__main__":
    main()
