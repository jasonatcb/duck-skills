#!/bin/bash

# create-gif.sh - 標準化 GIF 產生腳本
# 用法: ./create-gif.sh <輸入前綴> [輸出檔名] [速度]
# 
# 範例:
#   ./create-gif.sh "ec-功能-建立帳戶-"           # 使用預設速度 (1fps)
#   ./create-gif.sh "ec-功能-建立帳戶-" "輸出.gif" 2  # 2fps
#
# 預設輸出: 輸入前綴.gif (去掉結尾編號)

set -e

INPUT_PREFIX="${1:?請輸入圖片前綴，如 ec-功能-01}"
OUTPUT_NAME="${2:-}"
FPS="${3:-1}"

if [[ -z "$OUTPUT_NAME" ]]; then
    OUTPUT_NAME="${INPUT_PREFIX%.png}.gif"
fi

echo "建立 GIF: $OUTPUT_NAME"
echo "輸入: ${INPUT_PREFIX}%02d.png"
echo "速度: ${FPS} fps"

ffmpeg -y -framerate "$FPS" \
    -i "${INPUT_PREFIX}%02d.png" \
    -vf "scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 \
    "$OUTPUT_NAME"

echo "完成: $OUTPUT_NAME"
ls -lh "$OUTPUT_NAME"
