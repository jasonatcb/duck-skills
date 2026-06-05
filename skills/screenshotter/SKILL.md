---
name: screenshotter
description: 截圖技能。根據文檔內容分析目標頁面，使用 chrome-devtools-mcp 導航並截圖，將截圖存放到正確位置並更新文檔。當用戶說「截圖」、「截圖功能畫面」或使用 @docfile.md 語法並指定功能時觸發。
version: "1.0.0"
last_updated: 2026-03-31
---

# 截圖技能

此技能根據文檔內容分析目標頁面，使用 chrome-devtools-mcp 導航並截圖，將截圖存放到正確位置並更新文檔。

## 使用方式

用戶提供文檔路徑作為輸入：
- `@路徑/文檔.md` 提供完整文檔
- 附加說明需要截圖的具體頁面或功能

## 執行步驟

### 1. 分析文檔內容

讀取用戶提供的文檔並找出：
- **目標 URL**：文檔中明確提及的網址（如 `https://admin.cyberbiz.co/...`）
- **功能名稱**：需要截圖的功能頁面（如「商品列表」、「訂單管理」）
- **操作步驟**：文檔描述的操作流程，以確定需要截圖的畫面

### 2. 推斷目標頁面

如果文檔未提供明確 URL：
- 對於 CYBERBIZ 相關文檔，預設使用 `https://admin.cyberbiz.co`
- 根據功能名稱推斷路徑（如「商品列表」→ `/products`）
- 如果無法確定禮貌地詢問用戶需要截圖的具體 URL

### 3. 導航並截圖

使用 chrome-devtools-mcp：

```javascript
// 導航到目標頁面
await chrome_devtools_navigate_page({type: "url", url: "目標URL"})

// 等待頁面載入完成
await chrome_devtools_wait_for({text: ["載入完成標記", "loading"]})

// 調整 viewport（如需要）
await chrome_devtools_resize_page({width: 1280, height: 800})

// 設定瀏覽器縮放為 125% 以獲得更高解析度
await chrome_devtools_evaluate_script({
  function: "() => { document.body.style.zoom = '125%'; }"
})

// 截圖
await chrome_devtools_take_screenshot({filePath: "截圖路徑"})
```

### 4. 截圖命名規範

截圖檔名格式：`{產品線}-{功能}-{畫面描述}.png`

**產品線前綴：**
- `ec-` = 品牌官網 (E-Commerce)
- `pos-` = 智能 POS
- `wms-` = 智慧倉儲

**範例：**
- `ec-商品列表-新增商品.png`
- `ec-訂單管理-篩選功能.png`
- `pos-門市管理-結帳畫面.png`

### 5. 自動判斷是否需要 GIF

**自動偵測時機：**
在截圖前，分析文檔內容判斷是否適合用 GIF：

| 適合 GIF | 適合靜態圖 |
|---------|-----------|
| 多步驟操作流程 | 單一設定頁面 |
| 有對話框/彈窗的場景 | 說明性截圖 |
| 狀態變化過程 | 不需要操作說明的畫面 |
| 點擊→結果的對比 | 只需要一張圖示意的內容 |

**主動建議：**
如果文檔包含多個連續步驟（如 Step 1, Step 2...）或操作流程，主動建議使用 GIF 並諮詢用戶。

**使用 screenshotter-gif 技能：**
當需要 GIF 時，**自動載入並使用 `screenshotter-gif` 技能**，使用 ImageMagick 合併截圖為 GIF。

### 6. 合併多張圖片為 GIF

當一個步驟需要多張圖片展示連續動作時，使用 ImageMagick (magick) 合併為 GIF。

**優先使用 ImageMagick（screenshotter-gif 技能）：**
```bash
# 基本用法
magick frame1.png frame2.png frame3.png -resize 1280x800 -delay 250 -loop 0 output.gif

# 批次處理（前綴命名）
magick screenshot-*.png -resize 1280x800 -delay 250 -loop 0 output.gif
```

**參數說明：**
- `-delay 250`：每幀間隔 250 厘秒（2.5 秒，推薦用於教學文件）
- `-resize 1280x800`：寬度 1280，高度自動
- `-loop 0`：無限循環

**執行流程：**
1. 連續截圖時使用編號命名：`ec-功能-01.png`, `ec-功能-02.png`, `ec-功能-03.png`
2. **（重要）檢查所有幀是否有 PII**
3. **詢問用戶要模糊的內容**
4. 調用 `screenshotter-blur` 模糊 PII
5. 使用 magick 合併為 GIF
6. 在文檔中引用 GIF：`![說明](../../../assets/images/功能.gif){ .screenshot }`

**參數說明：**
- `framerate 1`：每秒 1 幀（建議用於技術文件）
- `scale=1280:-1`：寬度 1280，高度自動維持比例
- `loop 0`：無限循環

**GIF 製作原則（重要）：**
- **只捕捉關鍵狀態**：每個截圖應該代表一個有意義的步驟，避免只因捲動而產生的重複畫面
- **移除多餘的捲動幀**：如果從 A 狀態捲動到 B 狀態，中間的過度幀應刪除，只保留 A 和 B
- **避免來回捲動**：如果同一個畫面需要展示上半部和下半部，應該分成兩個獨立的截圖點，而非來回捲動
- **不顯示捲動過程**：技術文件的 GIF 應該是靜態畫面之間的跳躍，而非動畫式的捲動
- **範例**：建立帳戶流程只需 6 幀：(1) 帳戶頁面 → (2) 輸入帳戶名稱 → (3) 資源頁面 → (4) 輸入屬性名稱 → (5) 商家詳細資料 → (6) 業務目標

**GIF 幀延遲參考：**

| 延遲值 | 時間 | 用途 |
|--------|------|------|
| 150 | 1.5秒 | 快速過渡動畫 |
| **250** | **2.5秒** | **教學文件（推薦）** |
| 300 | 3秒 | 複雜步驟需要更多閱讀時間 |
| 400 | 4秒 | 很複雜的流程 |

### 7. 存放位置

所有截圖存放於：`docs/assets/images/`

### 8. 更新文檔 - 相對路徑格式（重要）

在文檔中插入截圖時，必須使用正確的相對路徑。路徑計算方式：
- 從文檔位置計算到 `docs/assets/images/` 的相對路徑

**相對路徑格式：**

| 文檔位置 | 圖片位置 | 相對路徑 |
|---------|---------|---------|
| `docs/ec/products/建立商品.md` | `docs/assets/images/ec-建立商品.png` | `../../assets/images/ec-建立商品.png` |
| `docs/ec/integrations/google/設定GA.md` | `docs/assets/images/ga-設定.png` | `../../../assets/images/ga-設定.png` |
| `docs/pos/門市通訊/基本設定.md` | `docs/assets/images/pos-基本設定.png` | `../../assets/images/pos-基本設定.png` |

使用 zensical Markdown 語法：

```markdown
![功能說明](../..//assets/images/圖檔名.png){ .screenshot }
```

或（根據檔案深度）：
```markdown
![功能說明](../../../assets/images/圖檔名.png){ .screenshot }
```

**截圖擺放位置原則：**
- 截圖應放置於**一系列步驟完成後**（展示結果畫面），或**步驟之間**（過渡畫面）
- 路徑說明後應先有步驟，截圖置於步驟之後，**勿將截圖放在路徑與步驟之間**
- 截圖上下方需有空白行
- 縮排需與步驟內容一致（通常為 4 空格）
- 嚴禁只放截圖而無文字說明
- 詳細規則參考：[截圖擺放位置參考指南](reference.md)

### 9. 更新 frontmatter

如果文檔有 frontmatter，請更新 `last_modified` 欄位為當前時間。

## 範例

**輸入：** 用戶提供 `docs/ec/products/建立商品.md` 文檔，要求截圖

**處理流程：**
1. 讀取文檔，找出目標 URL 是 CYBERBIZ 後台商品頁面
2. 導航到 `https://admin.cyberbiz.co/products/new`
3. 截圖並命名為 `ec-建立商品-基本資料.png`
4. 存放至 `docs/assets/images/ec-建立商品-基本資料.png`
5. 在文檔中插入 `![新增商品](../../assets/images/ec-建立商品-基本資料.png){ .screenshot }`

## 注意事項

- 截圖前確保頁面已完全載入，使用 `chrome_devtools_wait_for` 確認
- 如果頁面需要登入，先導航到登入頁面並處理登入流程
- 回傳截圖時提供清晰的截圖說明
- 截圖尺寸預設為 1280x800，若需不同尺寸可調整
- 確保截圖清晰，必要时先调整 viewport

## 本地預覽

- **不要執行 `uv run zensical build` 或 `uv run zensical serve`**
- 用戶會自己執行 `uv run zensical serve` 進行本地預覽
- Build 只在用戶要求驗證最終結果時執行

## 複雜步驟的格式優先順序

**優先使用子標題 (####)**：
- 當步驟有多個階段時，先用 `###` 建立主要標題，再用 `####` 建立各階段的子標題
- 這讓使用者可以掃描目錄並跳到特定階段
- 子標題層級的文章更容易閱讀和維護
- **嚴禁跳過標題層級**：不要從 `##` 直接跳到 `####`，或從 `###` 直接跳到 `=== tabs`（沒有 `####`）

**僅在最複雜的情況下使用 Tabs（在子標題內）**：
- 每個子標題內的內容本身非常複雜（各自有 3+ 個子步驟且包含多種變體）
- 使用者需要頻繁在不同變體間切換比較
- 也就是說：**子標題 alone 就足夠了，subheading + tabs 只保留給最複雜的流程**

**如果無法確定格式**：請詢問用戶以下選項：
- A) 子標題 (####)
- B) Tabs (===)
- C) 子標題 + Tabs

**正確的層級結構**：
```markdown
## H2 主標題

### H3 子標題

#### H4 階段標題

=== "Tab 1"
    內容...
=== "Tab 2"
    內容...
```

**錯誤的層級結構（禁止）**：
```markdown
## H2 主標題

### H3 子標題

=== "Tab 1"  <!-- 跳過了 #### -->
    內容...
```

## 截圖時需要用戶輸入

當需要填寫表單欄位時，**必須提示用戶輸入**：
- 詢問網址（如商店網站）
- 詢問商家名稱
- 詢問其他必要資訊

**範例prompt**：
```
需要填寫「商店網站」欄位，請問要使用哪個網址？（例如：www.cyberbiz.co）
```

## PII 模糊處理

截圖完成後，**必須**詢問用戶要模糊的內容：
```
請問需要模糊哪些文字或區域？
```

只有在用戶確認要模糊的內容後，才呼叫 `screenshotter-blur` 技能進行處理。

**禁止**：自行判斷哪些是 PII 而不詢問用戶。

### 模糊處理流程

1. **截圖完成後詢問用戶**：「請問需要模糊哪些文字或區域？」
2. 用戶回覆要模糊的內容（如「Jason Ke」）
3. 呼叫 `screenshotter-blur` 技能，該技能會使用 pytesseract OCR 自動偵測座標
4. 驗證結果

### 常見模糊區域座標參考

| 應用程式 | 區域 | 座標 (x, y, w, h) |
|---------|------|-------------------|
| Google GMC | 右上角 header（帳號名稱+Email） | 2470, 65, 160, 30 |
| Google GMC | 選取帳戶頁面（帳戶名稱+ID） | 896, 825, 165, 35 |
| Google GMC | 連結確認頁面（帳戶名稱+ID） | 896, 830, 170, 35 |

**重要**：模糊後必須讀取圖片驗證效果，確認敏感資訊已完全遮蔽。
