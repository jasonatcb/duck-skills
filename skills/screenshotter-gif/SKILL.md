---
name: screenshotter-gif
description: 自動將多張截圖合併為 GIF 動畫。使用 ImageMagick 建立技術文件用的 GIF，適用於展示多步驟操作流程、對話框操作、狀態變化等場景。當截圖數量 ≥ 2 張且涉及操作流程時，會由 screenshotter 技能自動呼叫。
version: 1.0.0
last_updated: 2026-03-23
compatibility:
  tools:
    - ImageMagick (magick command - v7+)
    - Bash
  environment: macOS/Linux with ImageMagick installed
  note: "In ImageMagick 7+, use `magick` instead of `convert`. Alternatively, `magick mogrify` replaces `mogrify`."
---

# Screenshot to GIF Skill

此技能使用 ImageMagick 將多張截圖合併為 GIF 動畫。

## 自動呼叫時機

**由 screenshotter 技能自動呼叫**，當：
- 截圖數量 ≥ 2 張
- 文檔描述多步驟操作流程（如 Step 1, Step 2...）
- 操作涉及對話框、彈窗或狀態變化
- 用戶明確要求建立 GIF 或動畫

## 手動使用時機

手動呼叫此技能當：
- 用戶說「合併為 GIF」、「建立動畫」
- 需要將現有截圖組合成 GIF
- 需要調整現有 GIF 的參數

## 觸發範例

| 用戶輸入 | 是否觸發 |
|---------|---------|
| 「為 @doc.md 的 Step 1, 2, 3 截圖」 | ✅ 自動呼叫 |
| 「把這些圖做成 GIF」 | ✅ 呼叫 |
| 「建立帳戶流程的 GIF」 | ✅ 呼叫 |
| 「截圖這篇文章的示意圖」 | ❌ 單張靜態圖 |
| 「更新某個設定頁面的截圖」 | ❌ 單張靜態圖 |

## Prerequisites

Ensure ImageMagick is installed:
```bash
brew install imagemagick
```

## Basic Usage

### Single Command (Inline)

```bash
magick -delay 100 -loop 0 frame1.png frame2.png frame3.png output.gif
```

### With Image Resizing and Optimization

```bash
magick -resize 1280x800 -delay 100 -loop 0 -quality 85 \
  frame1.png frame2.png frame3.png output.gif
```

!!! note "ImageMagick 7+"
    In ImageMagick 7+, use `magick` instead of `convert`. The `magick` command provides better performance and more consistent behavior.

## Command Options Explained

| Option | Description | Recommended Value |
|--------|-------------|------------------|
| `-resize WxH` | Scale images to fixed width (height auto) | 1280px width |
| `-delay N` | Time between frames in hundredths of a second | **200 = 2 seconds** (default for docs) |
| `-loop 0` | Loop forever | 0 = infinite |
| `-quality N` | Compression quality (1-100) | 85 |
| `-coalesce` | Merge animated layers | For GIFs with transparency |

### Delay Values Reference

| Delay | FPS | Use Case |
|-------|-----|----------|
| 100 | 1s | Fast transitions only |
| **200** | **2s** | **Standard documentation (DEFAULT)** |
| 300 | 3s | Complex steps needing more reading time |

## Creating GIF from Prefix-Named Files

When screenshots are named with sequential prefixes (e.g., `screenshot-01.png`, `screenshot-02.png`):

```bash
magick screenshot-*.png -resize 1280x800 -delay 100 -loop 0 output.gif
```

## GIF Optimization

### Remove Extra Frames

If you have intermediate frames that are just scrolling (not meaningful state changes), remove them before creating the GIF.

### Palette Optimization

For smaller file sizes, generate a custom palette:

```bash
magick frame1.png frame2.png frame3.png \
  -resize 1280x800 \
  -coalesce \
  -duplicate 1,-2 \
  -layers Optimize \
  -delay 100 -loop 0 \
  output.gif
```

## Example Workflow

1. **Capture screenshots** with screenshotter skill (numbered: `step-01.png`, `step-02.png`, etc.)
2. **Blur sensitive info** with screenshotter-blur skill if needed
3. **Create GIF** using this skill
4. **Reference in document** with Markdown syntax

### Example Command

```bash
# Create GIF from step-by-step screenshots
magick docs/assets/images/ec-feature-01.png \
       docs/assets/images/ec-feature-02.png \
       docs/assets/images/ec-feature-03.png \
       docs/assets/images/ec-feature-04.png \
       -resize 1280x800 \
       -delay 100 \
       -loop 0 \
       docs/assets/images/ec-feature-demo.gif
```

## Output Location

Save GIFs to `docs/assets/images/` directory and reference with relative paths:

```markdown
![Feature demonstration](assets/images/feature-demo.gif){ .screenshot }
```

## Best Practices

- **Limit frame count**: Keep GIFs to 6-10 frames maximum
- **Remove redundant frames**: Delete frames that only show scrolling
- **Consistent timing**: Use same delay between all frames
- **Purposeful animation**: Only animate meaningful state changes
- **File size**: Aim for < 2MB per GIF for fast loading

## Troubleshooting

### "Not a valid image file" Error
- Check that all input files exist and are valid images
- Use `file frame.png` to verify file types

### GIF is too large
- Reduce resize dimensions
- Lower quality setting
- Remove unnecessary frames
- Use `-layers Optimize` flag

### Images not in order
- Use explicit file list instead of glob patterns
- Name files with zero-padded numbers (01, 02, 03...)

### Command Not Found
- In ImageMagick 7, use `magick` instead of `convert`
- For backward compatibility, ImageMagick 7 may have an alias: `convert` -> `magick`
