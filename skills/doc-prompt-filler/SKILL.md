---
name: doc-prompt-filler
description: >-
  引導使用者填寫 doc-generator.md 中的各文件變數（情境、category、module、頁面、主題、檔案路徑），產出完整的提示詞供複製到 Firebase CYBERBIZ 後端專案的 Claude Code 中使用。
  當使用者提及「要寫文件」、「產生文件提示詞」、「填 doc-generator 變數」、「幫我填提示詞」、「準備 doc prompt」、「要產生訂單相關文件」、「幫我產出 doc prompt」或類似意圖時觸發。也用於任何需要從 doc-generator.md 模板產生 CYBERBIZ 商家教學文件 prompt 的情境。
version: 1.0.0
last_updated: 2025-05-25
---

# Doc Prompt Filler

## 任務

使用者想要產生一份 CYBERBIZ 商家教學文件的 prompt，以便複製到 Firebase CYBERBIZ 後端專案的 Claude Code 中執行。你的工作是：

1. **讀取** `reference/prompts/doc-generator.md` 模板
2. **引導使用者**填寫各文件變數（各文件變數區塊中的值）
3. **產出完整提示詞**（code block），讓使用者可以直接複製貼上

## 流程

### 第一步：讀取模板

首先使用 `read` 工具讀取專案中的 `reference/prompts/doc-generator.md`，取得完整模板內容。

此時可向使用者說明：「我已讀取 doc-generator.md 模板，接下來我會引導你填寫變數。」

### 第二步：詢問情境

使用 `question` 工具詢問使用者本次的文件情境是 `single`（單一文件）還是 `series`（系列文件）。

### 第三步：詢問關聯文件（僅 series）

若為 `series`，再詢問關聯文件的順序鏈，例如：`宅配通出貨流程 → 宅配通託運單設定 → 配送尺寸對照表`。

### 第四步：逐一詢問各文件變數

對每份文件，依序詢問下列變數：

1. **category** — 產品/功能的 kebab-case 名稱，用於錨點前綴與檔名，例如 `pelican-shipping`、`search-and-filter`
2. **module** — 所屬模組目錄，例如 `orders`、`payments-and-logistics`
3. **頁面** — 後台頁面路徑或 URL，例如 `/admin/orders_v2` 或 `https://demo005.cyberbiz.co/admin/orders_v2`
4. **主題** — 文件的主題（商家使用視角），例如「使用超商大宗寄倉（B2C）出貨」

自動計算 **檔案路徑**：`docs/{module}/{category}.md`

此外，再詢問使用者是否有：
- **參考既有文件**：若有，讀取其內容一併納入 prompt
- **特別要求**：例如只補某段落、重寫整篇、只產對照表等

為簡化互動流程，建議在同一次 `question` 呼叫中同時詢問多個變數（例如一次問 category、module、頁面、主題），僅在需要時才分開追問。

### 第五步：產出完整提示詞

將所有收集到的變數填入模板，產出完整的 prompt。產出時：

- 將各文件的 **頁面** 填入任務描述區的 `{{頁面路徑}}`（single 時使用該文件的值，series 時填寫整體系列範圍）
- 將各文件的 **主題** 填入任務描述區的 `{{主題}}`（同上的邏輯）
- 填入 `{{情境}}`（`single` 或 `series`）
- 填入 `{{關聯文件}}`（series 專用）
- 填入各文件變數區塊（category、module、頁面、主題、檔案路徑）
- 填入 `{{參考既有文件}}` 和 `{{特別要求}}` 的值
- 移除未使用的 placeholder 如 `{{若有}}`、`{{...}}`（但保留模板中原有的範例文字作為說明）
- **不要修改** doc-generator.md 模板的內容結構和格式本身

**重要：務必替換所有 `{category}` 出現處。** 模板中的 `{category}` 是錨點 placeholder，出現在：
- 文件結構（1-9 項）heading anchor：`{ #intro-{category} }` → `{ #intro-search-and-filter }`
- FAQ 標題、FAQ 內部連結、FAQ 變數說明表
- 自查清單第 9 項說明
- 範例路徑和說明文字中的 `{category}`

替換時注意區分：那些**用來展示格式的範例**（如反引號內的 `{primary}-{category}-{subtopic}`）應當保留原樣；但**實際的 placeholder 用法**（如 `{ #intro-{category} }` 在文件結構清單中）應當替換。

#### 範例（single）

```
使用者給的 category: order-tags, module: orders, 頁面: /admin/orders_v2, 主題: 使用訂單標籤管理訂單

任務描述區 → {{頁面路徑}} = /admin/orders_v2, {{主題}} = 使用訂單標籤管理訂單

各文件變數區塊 → 文件 A: category: order-tags, module: orders, 頁面: /admin/orders_v2, 主題: 使用訂單標籤管理訂單, 檔案路徑: docs/orders/order-tags.md

Heading 錨點 → { #intro-order-tags }、{ #operate-order-tags }、{ #faq-order-tags } 等
```

### 第六步：輸出

用三個反引號包住完整 prompt 輸出，方便使用者複製。

在 prompt 之後，簡短說明：
- 這是給 Firebase CYBERBIZ 後端專案的 **Claude Code** 使用的 doc-generator prompt
- 提醒使用者複製後到該專案中貼上執行即可開始研究程式碼並產出文件

## 注意事項

- **不要修改 doc-generator.md 模板本身**，只產出填好變數的副本
- category 必須是 kebab-case 格式（全小寫、連字號分隔），這會影響錨點和檔名
- 使用者若對某個變數不確定，可以提供該專案常見的 module 和 category 範例供參考
- **不要遺漏 `{category}` 的替換**：模板中多處使用 `{category}` 作為錨點和路徑的 placeholder，必須全部替換為使用者提供的實際 category 值。這包括文件結構清單（1-9 項）、FAQ 區塊、自查清單第 9 項等處的 heading anchor ID
