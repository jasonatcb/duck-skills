---
name: screenshotter-blur
description: 模糊處理圖片中的敏感資訊 (PII)。當用戶說「模糊」、「遮蔽」、「馬賽克」、「隱藏個資」、「blur」、「redact」或使用 @docfile.md 語法並指定圖片時觸發此技能。此技能會分析圖片或文檔中的圖片參照，識別需要遮蔽的區域並套用安全的不透明遮罩。與 screenshotter 技能搭配使用。
version: "1.0.5"
last_updated: 2026-03-27
compatibility:
  requires: ["pillow", "pytesseract", "tesseract"]
  install: |
    # 安裝依賴
    uv venv .venv && source .venv/bin/activate
    uv pip install pillow pytesseract
    
    # macOS 還需安裝 OCR 引擎
    brew install tesseract tesseract-lang
---

# 截圖模糊技能

此技能用於模糊處理截圖中的敏感資訊（PII），以確保文件中不會洩露個人識別資訊。

## 使用情境

- 與 screenshotter 技能搭配，在截圖後立即模糊敏感資訊
- 用戶提供圖片路徑要求模糊處理
- 用戶提供文檔並指定需要模糊的圖片章節

## ⚠️ 重要：必須先詢問用戶

**每次截圖後，必須先詢問用戶要模糊的文字內容，再執行模糊處理。**

流程：
1. 截圖完成後，**必須問**：「請問需要模糊哪些文字或區域？」
2. 用戶提供要模糊的文字（如「Jason Ke」）
3. 使用 pytesseract OCR 自動偵測該文字的座標
4. 確認模糊位置後再執行
5. 顯示模糊後的圖片讓用戶確認

**禁止**：
- ❌ 在未詢問用戶的情況下自行猜測座標模糊
- ❌ 自行判斷哪些是 PII 而不詢問用戶

## 輸入方式

用戶可透過以下方式提供圖片：
- **直接指定**：`docs/assets/images/screenshot.png`
- **文檔引用**：提供 `@docfile.md`，技能會解析文檔找出圖片路徑
- **模糊區域說明**：描述需要模糊的位置（如「訂單編號欄位」、「客戶 email」）

## 執行步驟

### 1. 詢問用戶要模糊的內容

截圖後，**必須**問：
```
請問需要模糊哪些文字或區域？
```

用戶回覆後，記錄要模糊的文字內容。

### 2. 使用 OCR 偵測座標

使用 pytesseract 自動找出文字座標：

```python
from PIL import Image
import pytesseract

img = Image.open('screenshot.png')
# 使用中英文語言包
data = pytesseract.image_to_data(img, lang='chi_tra+eng', output_type=pytesseract.Output.DICT)

# 搜尋目標文字
target_text = "Jason Ke"  # 用戶提供的文字
for i, text in enumerate(data['text']):
    if target_text.lower() in text.lower():
        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]
        print(f"Found '{text}' at x={x}, y={y}, w={w}, h={h}")
```

**注意**：
- 使用 `lang='chi_tra+eng'` 支援中文和英文
- 搜尋時將用戶輸入轉為小寫比對
- 如果搜尋不到，嘗試搜尋部分文字（如用戶說「頻道名稱」，搜尋「頻道」或「Jason」）

### 3. 驗證位置再模糊

在執行模糊前，先顯示偵測到的座標給用戶確認：
```
偵測到「XXX」位於座標 (x, y, w, h)：xxx, xxx, xxx, xxx
請確認是否正確？
```

只有確認後才執行模糊。

### 4. 如果 OCR 失敗

如果 pytesseract 無法偵測到文字：
1. **詢問用戶提供座標**：「抱歉無法自動偵測，請問能提供精確的座標嗎？」
2. 或者請用戶在圖片上標記後回傳

**千萬不要自行猜測座標！**

### 5. 執行模糊

確認座標後，使用 PIL 套用黑色方塊：

```python
from PIL import Image, ImageDraw

img = Image.open('screenshot.png')
draw = ImageDraw.Draw(img)
# 座標格式：x1, y1, x2, y2 (左上、右下)
draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
img.save('screenshot-blurred.png')
```

### 6. 顯示結果確認

模糊完成後，顯示圖片讓用戶最終確認：
- 模糊區域是否正確？
- 是否需要調整？
- 其他區域是否也需要模糊？

常見需要模糊的類型：

| 類型 | 範例 | 優先級 |
|------|------|--------|
| 個人資訊 | 姓名、電話、Email、地址 | 高 |
| 金融資料 | 信用卡號、银行帳號、交易金額 | 高 |
| 身份證明 | 身份證字號、駕照號碼 | 高 |
| API 金鑰 | API Key、Secret、Token | 高 |
| 訂單資訊 | 訂單編號、客戶編號 | 中 |
| 位置資訊 | IP 地址、GPS 座標 | 中 |

### 3. 套用模糊處理

**首選方法：solid black block（不透明黑色方塊）**

此方法最安全，無法被 AI 工具還原。使用 PIL：
```python
from PIL import Image, ImageDraw

def redact_region(image_path, regions, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    for x, y, w, h in regions:
        draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
    img.save(output_path)
```

**次選方法：pixelation（像素化）**
```python
def pixelate_region(image_path, regions, output_path):
    img = Image.open(image_path)
    for x, y, w, h in regions:
        roi = img.crop((x, y, x + w, y + h))
        small = roi.resize((10, 10), Image.Resampling.NEAREST)
        pixelated = small.resize((w, h), Image.Resampling.NEAREST)
        img.paste(pixelated, (x, y))
    img.save(output_path)
```

**不建議使用：Gaussian blur**
- 可被 AI 工具部分還原
- 安全性較低

### 4. 輸出檔案

**命名規範：**
- 原始檔：`原始檔名.png`
- 模糊後：`原始檔名-blurred.png` 或 `原始檔名-redacted.png`

**存放位置：**
- 與原始圖片相同目錄
- 或覆蓋原始檔案（如果用戶明確要求）

### 5. 驗證結果

1. 確認模糊區域已正確套用
2. 確認其他資訊仍然清晰可讀
3. 產生處理報告

## 模糊腳本使用

### 智慧模式（推薦）

使用 OCR 自動偵測並模糊，無需指定座標：
```bash
# 使用系統 Python（需先安裝依賴）
python3 scripts/smart_blur.py --input "screenshot.png" --type all

# 或使用 venv
.venv/bin/python scripts/smart_blur.py --input "screenshot.png" --type ga
```

**參數：**
- `--input/-i`: 輸入圖片路徑（必填）
- `--type/-t`: PII 類型 (ga/email/phone/url/api/order/all)，預設 all
- `--output/-o`: 輸出圖片路徑（預設 input-blurred.png）
- `--show/-s`: 顯示偵測到的區域（除錯用）
- `--method/-m`: solid 或 pixelate，預設 solid

### 手動模式

當 OCR 無法偵測時（如帳號名稱不是標準 email 格式），需使用手動模式指定座標：
```bash
# 格式：x,y,w,h（座標）
python3 scripts/manual_blur_pil.py -i "screenshot.png" -r "2470,65,160,30" -o "screenshot-blurred.png"
```

**常見模糊區域（Google GMC 範例）：**
| 區域 | 座標 (x, y, w, h) | 說明 |
|------|-------------------|------|
| 右上角header | 2470, 65, 160, 30 | 帳號名稱 + Email |

**支援的 PII 類型：**
| 類型 | 範例 | pattern |
|------|------|----------|
| ga | G-XXXXXXXX | `G-[A-Z0-9]{6,}` |
| email | test@mail.com | `[\w.-]+@[\w.-]+` |
| phone | 0912-345-678 | `\d{4}-\d{3,4}-\d{3,4}` |
| url | https://... | `https?://[^\s]+` |
| api | sk-xxx | `sk-[a-zA-Z0-9]+` |
| order | ORD123456 | `ORD\d{6,}` |
| account_id | 5753408045 | `\d{7,}` 或 `\d{3,}-\d{3,}-\d{4,}` |
| gmc_header | Duck, 5753408045 | `Duck, \d+` 或 `Duck · \d{3,}-\d{3,}-\d{4,}` |
| ads_id | 898-903-6088 | `\d{3,}-\d{3,}-\d{4,}` |
| mc_id | om-1958562190358733320 | `om-\d{16,}` |

### 手動模式

指定座標進行模糊：
```bash
.venv/bin/python scripts/manual_blur_pil.py --input "screenshot.png" \
    --regions "100,50,200,30" \
    --output "screenshot-blurred.png"
```

### 批次處理

一次模糊多張圖片：
```bash
.venv/bin/python scripts/batch_blur_pil.py --input-dir "images/" \
    --pattern "*.png" \
    --regions "100,50,200,30"
```

## 與 screenshotter 技能整合

screenshotter-blur 應在 screenshotter 之後使用：

1. **screenshotter**：產生截圖
2. **screenshotter-blur**：識別並模糊截圖中的 PII
3. 更新文檔引用模糊後的圖片

### 建議工作流程

```markdown
1. 用戶請求截圖並模糊
2. screenshotter 產生截圖
3. 分析截圖內容，識別 PII 區域
4. 套用模糊處理
5. 儲存模糊後的圖片
6. 更新文檔中的圖片引用
```

## 注意事項

- **預設使用 solid black block**：這是最安全的模糊方式，無法被 AI 還原
- **避免 Gaussian blur**：除非用戶明確要求
- **保持上下文可讀**：模糊時不要過度遮蔽，造成文件難以理解
- **先備份原始圖片**：避免覆蓋無法復原
- **提供模糊前後對照**：讓用戶確認效果

## 錯誤處理

- 圖片不存在：回報錯誤並列出可用圖片
- 格式不支援：僅支援 PNG, JPG, JPEG, WEBP
- 座標無效：回報錯誤並建議使用自動偵測
