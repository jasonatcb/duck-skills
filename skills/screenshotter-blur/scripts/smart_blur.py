#!/usr/bin/env python3
"""
智慧模糊腳本 - 使用 OCR 自動偵測 PII 並模糊

用法:
    python smart_blur.py --input screenshot.png --type ga
    python smart_blur.py --input screenshot.png --type email
    python smart_blur.py --input screenshot.png --type all

依賴:
    pip install pillow pytesseract
    # macOS 還需安裝: brew install tesseract
"""

import argparse
from PIL import Image, ImageDraw
import os
import sys
from pathlib import Path

# 安裝提醒
try:
    import pytesseract
except ImportError:
    print("錯誤: 請先安裝 pytesseract")
    print("  pip install pytesseract")
    print("  # macOS 還需安裝 tesseract:")
    print("  brew install tesseract")
    sys.exit(1)

# PII 類型的辨識模式
PII_PATTERNS = {
    "ga": [
        r"G-[A-Z0-9]{6,}",  # GA4 ID 如 G-XXXXXXXX
    ],
    "email": [
        r"[\w.-]+@[\w.-]+\.\w+",  # Email
    ],
    "phone": [
        r"\d{4}-\d{3,4}-\d{3,4}",  # 電話格式
        r"\d{10,}",  # 純數字電話
    ],
    "url": [
        r"https?://[^\s]+",  # URL
        r"www\.[^\s]+",
    ],
    "api": [
        r"sk-[a-zA-Z0-9]+",  # API Key
        r"api[_-]?key",  # api_key
    ],
    "order": [
        r"ORD\d{6,}",  # 訂單編號
        r"#\d{6,}",
    ],
    "account_id": [
        r"^\d{7,}$",  # 純數字帳號 ID (如 5753408045) - 需獨立數字
        r"\d{3,}-\d{3,}-\d{4,}",  # 破折號格式 (如 898-903-6088)
        r"om-\d{16,}",  # om- 前綴格式 (如 om-1958562190358733320)
    ],
    "gmc_header": [
        r"Duck, \d+",  # GMC 帳戶名稱格式 (如 "Duck, 5753408045")
        r"Duck · \d{3,}-\d{3,}-\d{4,}",  # 選帳戶頁面 (如 "Duck · 898-903-6088")
    ],
    "ads_id": [
        r"\d{3,}-\d{3,}-\d{4,}",  # Google Ads ID (如 898-903-6088)
    ],
    "mc_id": [
        r"om-\d{16,}",  # Merchant Center ID (如 om-1958562190358733320)
    ],
}


def detect_pii_regions(image_path, pii_types=None):
    """使用 OCR 偵測圖片中的 PII 區域"""
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size

    # OCR 取得所有文字及其位置
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    regions = []
    n = len(data["text"])

    # 如果沒有指定類型，偵測所有類型
    if pii_types is None:
        pii_types = list(PII_PATTERNS.keys())

    all_patterns = []
    for pii_type in pii_types:
        all_patterns.extend(PII_PATTERNS.get(pii_type, []))

    import re

    # 檢查每個偵測到的文字
    for i in range(n):
        text = data["text"][i].strip()
        if not text:
            continue

        # 檢查是否符合任何 PII 模式
        for pattern in all_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                # 加入一些邊距
                padding = 5
                regions.append(
                    (
                        max(0, x - padding),
                        max(0, y - padding),
                        w + padding * 2,
                        h + padding * 2,
                    )
                )
                break

    return regions


def apply_blur(img, regions, method="solid"):
    """套用模糊"""
    draw = ImageDraw.Draw(img)

    for x, y, w, h in regions:
        if method == "solid":
            draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
        else:
            # 像素化
            roi = img.crop((x, y, x + w, y + h))
            small = roi.resize((10, 10), Image.Resampling.NEAREST)
            pixelated = small.resize((w, h), Image.Resampling.NEAREST)
            img.paste(pixelated, (x, y))

    return img


def main():
    parser = argparse.ArgumentParser(description="智慧模糊 - 自動偵測並模糊 PII")
    parser.add_argument("--input", "-i", required=True, help="輸入圖片路徑")
    parser.add_argument(
        "--type",
        "-t",
        default="all",
        help=f"PII 類型: {', '.join(PII_PATTERNS.keys())}, all",
    )
    parser.add_argument("--output", "-o", default=None, help="輸出圖片路徑")
    parser.add_argument(
        "--method", "-m", default="solid", choices=["solid", "pixelate"]
    )
    parser.add_argument(
        "--show", "-s", action="store_true", help="顯示偵測到的區域 (除錯用)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"錯誤: 找不到輸入檔案 '{args.input}'")
        sys.exit(1)

    # 決定要偵測的類型
    if args.type == "all":
        pii_types = list(PII_PATTERNS.keys())
    else:
        pii_types = [args.type]

    print(f"偵測類型: {pii_types}")

    # 偵測 PII 區域
    regions = detect_pii_regions(args.input, pii_types)

    if not regions:
        print("警告: 找不到任何 PII 區域")
        sys.exit(1)

    print(f"找到 {len(regions)} 個 PII 區域")

    # 顯示偵測到的區域 (除錯用)
    if args.show:
        img = Image.open(args.input)
        draw = ImageDraw.Draw(img)
        for i, (x, y, w, h) in enumerate(regions):
            draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
            print(f"  區域 {i + 1}: x={x}, y={y}, w={w}, h={h}")
        debug_path = args.input.replace(".png", "-debug.png")
        img.save(debug_path)
        print(f"除錯圖片已儲存: {debug_path}")
        return

    # 模糊處理
    img = Image.open(args.input)
    if img.mode != "RGB":
        img = img.convert("RGB")

    img = apply_blur(img, regions, args.method)

    # 儲存
    if args.output is None:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}-blurred{ext}"

    img.save(args.output)
    print(f"已儲存模糊後的圖片: {args.output}")
    print(f"模糊方法: {args.method}")


if __name__ == "__main__":
    main()
