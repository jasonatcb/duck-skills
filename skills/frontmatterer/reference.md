---
title: frontmatter
created: 2026-03-05 10:50
last-modified: 2026-03-05 11:45
type:
tags: []
last_modified: 2026-03-05 14:56
aliases: []
id: reference
---

## Frontmatter Schema

```yaml
title: { type: String, required: true, desc: "H1 Title / SEO Title" }
description: { type: String, max_length: 160, desc: "Meta description for Zensical social card" }
created: { type: Date, format: "YYYY-MM-DD HH:mm" }
last_modified: { type: Date, format: "YYYY-MM-DD HH:mm" }
lang: { type: String, enum: ["zh-TW", "en-US", "ja-JP"] }
type: { type: String, enum: ["tutorial", "guide", "reference", "concept"] }
status: { type: String, enum: ["new", "update", "deprecated"] }
version: { type: String, desc: "Semantic versioning or change type" }
author: { type: String, default: "Jase" }
reviewers: { type: Array, default: [] }
notes: { type: Array, desc: "Internal editor notes" }
ga_views: { type: Integer, default: 0, desc: "GA4 total page views" }
feedback: { type: Integer, default: 0, desc: "Net feedback score (Up minus Down) from zensical feedback widge" }
products: { type: Array, enum: ["EC", "POS", "WMS"] }
modules: { type: Array, desc: "Matching CYB admin console leftsidebar menu" }
sites: { type: Array, enum: ["TW", "JP", "US"] }
audiences: { type: Array, enum: ["admin", "developer", "clerk"] }
difficulty: { type: String, enum: ["beginner", "intermediate", "advanced"] }
tnb: { type: String, enum: ["trunk", "branch"] }
plans: { type: Array, enum: ["專業", "進階", "高手", "專業 PLUS", "進階 PLUS", "高手 PLUS", "企業"] }
cyb_extensions: { type: Array, default: ["APP MARKET", "AUTOMATION", "CHANNEL BRIDGE", "CHAT BOX", "EXPRESS", "NOW!", "STORE PAL", "TICKET"] }
intents: { type: Array, desc: "Search intent/User goal" } 
features: { type: Array, desc: "Specific system features mentioned" } 
prerequisites: { type: Array, desc: "Required reading/tasks/documents" }
related: { type: Array, desc: "Related documents" }
tags: { type: Array, desc: "SEO internal keywords" }
acoiv: { type: String, enum: ["activate", "configure", "operation", "integration", "venture"] }
apis: { type: Array, desc: "List of API endpoints" }
devices: { type: Array, enum: ["desktop", "mobile", "tablet"] }
ui_components: { type: Array, desc: "UI elements mentioned" }
paths: { type: Array, desc: "admin console navigation routes mentioned" }
layouts: { type: Array, enum: ["classic", "draggable"] }
wp_url: { type: Array, desc: WordPress docs urls } 
permalink: { type: String, desc: "Slug for Zensical URL" }
comments: { type: Boolean, default: false }
search:
  exclude: { type: Boolean, default: false }
icon: { type: String, desc: "Lucide icon (e.g., lucide/braces)" }
hide: { type: Array, enum: ["navigation", "toc", "feedback"] desc: "Visual elements to hide on the page"
```

## Field Specification & Taxonomy

### 1. 標誌與語系 (Identity & Localization)

| **Key**         | **Type** | **Required** | **Description**                              |
| --------------- | -------- | ------------ | -------------------------------------------- |
| `title`         | String   | ✅            | **文件標題**：SEO 與 H1 的主要來源。                     |
| `description`   | String   | ✅            | **內容摘要**：用於 Zensical Social Cards，建議 160 字內。 |
| `created`       | Date/Time| ✅           | **建立日期**：文件最初產生的時間。由核心模板於建立時填入，後續**不應更改**。|
| `last_modified` | Date     | ✅            | **最後更新**：格式必須為 `YYYY-MM-DD HH:mm`。                 |
| `lang`          | Enum     | ✅            | **語系**：`zh-TW`, `en-US`, `ja-JP`。            |
| `permalink`     | String   | ✅            | **固定連結**：Zensical 產出的 URL Slug。              |

### 2. 文件生產流程 (DDLC)

|**Key**|**Type**|**Default**|**Description**|
|---|---|---|---|
|`type`|Enum|-|`tutorial`, `guide`, `reference`, `concept`。|
|`status`|Enum|-|`new`, `update`, `deprecated`。|
|`version`|String|-|語義化版本或變更類型 (如: Refactor, Rewrite, Revise)。|
|`author`|String||文件主要負責人。|
|`reviewers`|Array|`[]`|審核者清單。|
|`notes`|Array|`[]`|**內部筆記**：僅供編輯者閱讀，不對外發佈。|

### 3. 數據統計 (Metrics & Performance)

|**Key**|**Type**|**Default**|**Description**|
|---|---|---|---|
|`ga_views`|**Integer**|`0`|**累積瀏覽量**：由系統定期從 GA4 同步，代表該頁面總點擊整數。|
|`feedback`|**Integer**|`0`|**回饋淨值**：正負評抵銷後的整數得分 (Upvotes - Downvotes)。|

### 4. 產品與商業範疇 (Product & Commercial)

|**Key**|**Type**|**Description**|
|---|---|---|
|`products`|Array|產品線：`EC`, `POS`, `WMS`。|
|`modules`|Array|功能模組：須對照 **CYB 後台左側選單** 名稱。|
|`sites`|Array|適用站點：`TW`, `JP`, `US`。|
|`tnb`|Enum|`trunk` (全方案適用) 或 `branch` (特定方案)。|
|`plans`|Array|**方案限制**：`專業`, `進階`, `高手`, `專業 PLUS`, `進階 PLUS`, `高手 PLUS`, `企業`。|
|`cyb_extensions`|Array|**官方外掛**：`APP MARKET`, `AUTOMATION`, `CHANNEL BRIDGE`, `CHAT BOX`, `EXPRESS`, `NOW!`, `STORE PAL`, `TICKET`。|

### 5. 使用者情境 (User Context)

|**Key**|**Type**|**Description**|
|---|---|---|
|`audiences`|Array|目標對象：`admin` (商家/管理員), `developer` (開發人員), `clerk`(店員)。|
|`difficulty`|Enum|難易度：`beginner`, `intermediate`, `advanced`。|
|`intents`|Array|**搜尋意圖**：使用者想解決什麼問題？(例如：如何退貨)。|
|`features`|Array|**功能特性**：文中提到的特定系統功能。|

### 6. 內容關聯 (Content Relations)

|**Key**|**Type**|**Description**|
|---|---|---|
|`prerequisites`|Array|**前置作業**：開始此教學前必須先完成的事項或閱讀的文檔。|
|`related`|Array|**延伸閱讀**：相關文件。|
|`tags`|Array|**標籤**：SEO 與搜尋引擎內部的輔助關鍵字。|
|`acoiv`|Enum|**維度分類**：`activate`, `configure`, `operation`, `integration`, `venture`。|

### 7. 技術架構 (Technical Metadata)

|**Key**|**Type**|**Description**|
|---|---|---|
|`apis`|Array|文件中調用的 **API Endpoints** 列表。|
|`devices`|Array|適用設備：`desktop`, `mobile`, `tablet`。|
|`ui_components`|Array|文中提到的介面元素名稱。|
|`paths`|Array|**後台路徑**：文中提到的後台介面操作路徑。|
|`layouts`|Enum|頁面佈局：`classic` (一般版型), `draggable`（拖拉版型）。|

### 8. 外部整合與系統 (Zensical / WP)

|**Key**|**Type**|**Default**|**Description**|
|---|---|---|---|
|`wp_url`|Array|-|對應 WordPress 的原始文件網址。|
|`comments`|Boolean|`false`|是否開啟頁面評論功能。|
|`search.exclude`|Boolean|`false`|是否從搜尋結果中排除此頁。|
|`icon`|String|-|**Lucide 圖示**：格式如 `lucide/braces` 或 `lucide/book`。|
|hide|Array|-|隱藏頁面元素：可選擇 `navigation` (左側選單) 或 `toc` (右側大綱) `feedback（回饋工具）`。|
