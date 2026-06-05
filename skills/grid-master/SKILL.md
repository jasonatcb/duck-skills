---
name: grid-master
description: |
  建立 Zensical grid cards 佈局的專家技能。當用戶說「建立 grid cards」、「新增卡片區塊」、「轉換為 grid cards」、「什麼情況用什麼 grid card」、「grid card 樣式」、「後續操作 grid cards」或類似意圖時觸發。此技能整合了 Zensical 的完整 grid 系統，透過互動式引導讓用戶選擇樣式與放置位置，快速建立專業的 grid 佈局。
version: 1.1.0
last_updated: 2026-04-27
---

# Grid Master 技能

為 Zensical 文件建立專業的 grid 佈局，透過互動式引導選擇最適合的樣式與放置位置。

## Grid 類型總覽

Zensical 提供三種主要的 grid 類型：

| Grid 類型 | 使用情境 | 語法 |
| :--- | :--- | :--- |
| [Card Grids (List)](#card-grids-list-語法) | 標準卡片列表 | `<div class="grid cards" markdown>` |
| [Card Grids (Block)](#card-grids-block-語法) | 混合格局 | `<div class="grid" markdown>` + `{ .card }` |
| [Generic Grids](#generic-grids) | 任意區塊組合 | `<div class="grid" markdown>` |

---

## Card Grids (List 語法)

標準卡片網格，每個卡片有悬停效果。最適合用於導航、功能說明、後續操作等場景。

### 放置位置與樣式對照表

| 放置位置 | 樣式名稱 | 圖示 Class | 特點 |
| :--- | :--- | :--- | :--- |
| [輕量導航](#輕量導航-lightweight-navigation) | 入口導航 | `{ .ig .middle }` | 僅標題+連結 |
| [步驟導航 + 詳述](#步驟導航--詳述-step-navigation-with-details) | Step Nav + Details | `{ .lg .middle }` | 步驟內簡單導航 + 後續詳細說明 |
| [後續操作](#後續操作-next-steps) | Next Steps | `{ .lg }` | 圖示+標題+說明+連結 |
| [功能說明 (單卡片)](#功能說明-feature-cards) | Feature | `{ .lg .middle }` + `---` | 圖示+標題+分隔線+描述+連結 |
| [功能說明 (多卡片)](#功能說明-多卡片-feature-cards-multi) | Feature Multi | `{ .lg .middle }` + `---` | 多項功能各自獨立卡片 |

---

### 輕量導航 (Lightweight Navigation)

用於「全站共同設定」、「章節入口」等輕量導航場景。

```markdown
## 全站共用設定

<div class="grid cards" markdown>

- :lucide-menu:{ .ig .middle }
  [__導覽列__](#導覽列){ data-preview }
- :lucide-arrow-down-to-line:{ .ig .middle }
  [__頁腳__](#頁腳){ data-preview }
- :lucide-megaphone:{ .ig .middle }
  [__彈窗廣告__](#彈窗廣告){ data-preview }
- :lucide-palette:{ .ig .middle }
  [__顏色與圖示設定__](#顏色與圖示設定){ data-preview }

</div>
```

**格式規則**：
- 圖示：`{ .ig .middle }`（中等尺寸、置中）
- 標題：`[__標題__](#錨點){ data-preview }`
- 每個卡片佔一列，無需說明文字
- 卡片間不需空行

---

### 步驟導航 + 詳述 (Step Navigation with Details)

用於步驟說明中，先在步驟下提供簡單的無描述 grid card 作為導航，接著在後續內容中以 `###` 標題 + 詳細說明展開每個項目。

```markdown
3.  **執行修改**：在訂單編輯頁中，你可以執行以下操作：

    <div class="grid cards" markdown>

    - :lucide-minus-circle:{ .lg .middle }
      [增減或移除商品](#edit-order-adjust-remove){ data-preview }

    - :lucide-plus-circle:{ .lg .middle }
      [新增商品](#edit-order-add-product){ data-preview }

    - :lucide-settings:{ .lg .middle }
      [自訂品項/折扣](#edit-order-custom){ data-preview }

    </div>

4.  **確認儲存**：操作完成後點擊「確認編輯」，並在二次彈窗中點選「確認並送出」即可完成。

---

### 增減或移除商品 {#edit-order-adjust-remove}

可直接調整原有商品的數量或將其移除。

![增減或移除商品](../../assets/images/EC-訂單詳情頁-編輯訂單-增減或移除商品.png)

---

### 新增商品 {#edit-order-add-product}

點選「新增商品」，從彈窗中搜尋（[搜尋機制][product-filter-backend]{ data-preview }）並加入品項（僅限溫層與通路相同的商品）。

![新增商品](../../assets/images/EC-訂單詳情頁-編輯訂單-新增商品.png)

??? tip "已新增商品標籤"
    新增商品會以「已新增」標籤註記，以利辨識區分。

    ![新增商品標籤](../../assets/images/EC-訂單詳情頁-編輯訂單-已新增標籤.png)

---

### 自訂品項/折扣 {#edit-order-custom}

若需補收運費或提供額外優惠，可點選「新增自訂品項」或「新增自訂折扣」手動輸入名稱與金額。
```

**格式規則**：
- **步驟內 grid card**：
  - 圖示：`{ .lg .middle }`（大尺寸、置中）
  - 僅標題+錨點連結，無描述文字
  - 連結格式：`[標題](#錨點){ data-preview }`
- **詳述區塊**：
  - 使用 `###` 標題 + `{#錨點}` 作為錨點目標
  - 標題與內容間用 `---` 分隔線
  - 可包含圖片、admonitions、連結等完整內容
- **流程**：步驟 N → 簡單 grid card → 步驟 N+1 → `###` 詳述區塊

**使用時機**：
- 步驟說明中有多個子操作需要展開詳述
- 需要在步驟中提供快速導航，同時保留詳細說明空間
- 避免步驟內容過長影響可讀性

---

### 後續操作 (Next Steps)

用於文件末尾的「後續操作」或「延伸閱讀」區塊。

```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-user-plus:{ .lg }   
  [__LINE 加入好友工具__](../line/設定拖拉版型網站的 LINE 加入好友工具.md){ data-preview }       
  在拖拉版型官網設定工具，引導商家加入 LINE 官方帳號好友。

- :lucide-ban:{ .lg }     
  [__物流限制與排除選項__](設定超商配送限制與物流排除.md)  
  設定商品的配送物流條件，限制特定物流方式於結帳流程中的顯示與使用。

</div>
```

**格式規則**：
- 圖示：`{ .lg }`（大尺寸）
- 結構：圖示 → 標題+連結 → 說明文字
- 標題使用 `__雙底線__`
- 連結後加 `{ data-preview }`（若文件存在）
- 說明文字 1-2 行

---

### 功能說明 (Feature Cards)

用於詳細的功能介紹，每項包含標題、描述與操作連結。

```markdown
<div class="grid cards" markdown>

-   :lucide-tags:{ .lg .middle } __建立並驗證 GMC 帳號__

    ---

    進入 Google Merchant Center 完成商家基本資訊設定，並確認商店所有權完成驗證。

    [:lucide-arrow-right: 設定教學](設定 Google Merchant Center 並同步 CYBERBIZ 商品.md){ data-preview }

-   :lucide-chart-no-axes-column-increasing:{ .lg .middle } __建立並串接 GA4 帳號__

    ---

    在 Google Analytics 後台取得「評估 ID」，前往 CYBERBIZ 後台填入評估 ID 完成串接。

    [:lucide-arrow-right: 設定教學](建立並串接 Google Analytics.md){ data-preview }

</div>
```

**格式規則**：
- 圖示：`{ .lg .middle }`（大尺寸、置中）
- 標題在圖示同一行，使用 `__雙底線__`
- 分隔線：`---`（單獨一行）
- 描述文字（可多行）
- 連結格式：`[:lucide-arrow-right: 操作名稱](連結.md){ data-preview }`

---

### 功能說明 (多卡片) (Feature Cards Multi)

用於多個子功能或設定項目的詳細說明。與單卡片版本的差別在於每個項目各自成為一張獨立的卡片，適合需要強調多個不同功能點的場景。

```markdown
## 簡訊通知樣板管理

商家可以設定系統在特定情境下（如訂單成立、出貨、密碼變更）自動發送簡訊給顧客。

<div class="grid cards" markdown>

-   :lucide-map-pin:{ .lg .middle } __設定路徑__

    ---

    後台路徑：**「訊息推播」>「簡訊通知樣板」**。

-   :lucide-layout-grid:{ .lg .middle } __樣板類別__

    ---

    包含訂單相關、退貨相關、物流相關（如貨物到店提醒）、顧客相關（如註冊驗證碼、密碼更改通知）以及 POS 相關通知。

-   :lucide-pencil:{ .lg .middle } __編輯內容__

    ---

    點擊樣板標題即可自訂文字。請注意 `{{...}}` 內的代碼為系統自動抓取的參數（如商店名稱或訂單編號），不可隨意更動。

-   :lucide-link:{ .lg .middle } __短網址功能__

    ---

    可開啟短網址功能，自動將簡訊中的連結縮短以節省字數。

    [:lucide-arrow-right: 詳細設定](設定與管理簡訊通知樣板.md){ data-preview }

</div>
```

**格式規則**：
- 圖示：`{ .lg .middle }`（大尺寸、置中）
- 每個功能點佔一張卡片
- 標題使用 `__雙底線__`
- 分隔線：`---`（單獨一行）
- 描述文字
- 最後一張卡片通常包含 `[:lucide-arrow-right: 操作名稱](連結.md){ data-preview }`

**使用時機**：
- 需要說明多個子功能或設定項目時
- 當內容不適合用簡單的 bullet points 呈現時
- 強調每個功能點的獨立性

**與單卡片版本的差別**：
| 單卡片 | 多卡片 |
|--------|--------|
| 一個功能主題 | 多個獨立功能點 |
| 適合概覽性介紹 | 適合詳細說明 |
| 說明文字在卡片內 | 每張卡片各自獨立 |

---

## Card Grids (Block 語法)

允許卡片與其他元素混合排列在同一个 grid 中。使用 `{ .card }` 來標記卡片元素。

```markdown
<div class="grid" markdown>

:fontawesome-brands-html5: __HTML__ for content and structure
{ .card }

:fontawesome-brands-js: __JavaScript__ for interactivity
{ .card }

:fontawesome-brands-css3: __CSS__ for text running out of boxes
{ .card }

> :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

</div>
```

**使用情境**：當需要將卡片與其他非卡片元素（如 admonitions、程式碼區塊）混合排列時使用。

---

## Generic Grids

通用網格，允許排列任意區塊元素（admonitions、程式碼區塊、內容分頁等）。

```markdown
<div class="grid" markdown>

=== "未排序列表"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "已排序列表"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

</div>
```

**使用情境**：
- 比較不同類型的內容
- 並排顯示程式碼範例
- 混合 admonitions 和其他元素

**注意**：Generic Grids **不使用** `cards` class，因此沒有悬停卡片效果。

---

## Lucide 圖示選擇指南

根據功能類型選擇最適合的圖示：

| 類型 | 推薦圖示 |
| :--- | :--- |
| 設定/配置 | `:lucide-settings:`, `:lucide-cog:`, `:lucide-sliders:` |
| 導覽/頁面 | `:lucide-menu:`, `:lucide-navigation:`, `:lucide-sitemap:` |
| 搜尋/查找 | `:lucide-search:`, `:lucide-binoculars:` |
| 新增/建立 | `:lucide-plus:`, `:lucide-file-plus:`, `:lucide-circle-plus:` |
| 編輯/修改 | `:lucide-pencil:`, `:lucide-edit:`, `:lucide-pen:` |
| 刪除/移除 | `:lucide-trash:`, `:lucide-x:`, `:lucide-minus:` |
| 匯入/匯出 | `:lucide-download:`, `:lucide-upload:`, `:lucide-import:` |
| 串接/整合 | `:lucide-plug:`, `:lucide-link:`, `:lucide-connection-points:` |
| 訊息/通知 | `:lucide-bell:`, `:lucide-message:`, `:lucide-mail:`, `:lucide-megaphone:` |
| 會員/用戶 | `:lucide-users:`, `:lucide-user-plus:`, `:lucide-user:` |
| 商品/產品 | `:lucide-package:`, `:lucide-box:`, `:lucide-tag:` |
| 訂單/交易 | `:lucide-shopping-cart:`, `:lucide-receipt:`, `:lucide-dollar-sign:` |
| 金流/付款 | `:lucide-credit-card:`, `:lucide-wallet:`, `:lucide-payments:` |
| 物流/配送 | `:lucide-truck:`, `:lucide-package-check:` |
| 庫存/倉儲 | `:lucide-warehouse:`, `:lucide-archive:` |
| 顏色/外觀 | `:lucide-palette:`, `:lucide-swatchbook:` |
| 分析/數據 | `:lucide-bar-chart:`, `:lucide-chart-line:`, `:lucide-analytics:` |
| 優化/效能 | `:lucide-rocket:`, `:lucide-zap:`, `:lucide-speed:` |
| 安全/驗證 | `:lucide-shield:`, `:lucide-lock:`, `:lucide-check-circle:` |
| 時間/排程 | `:lucide-clock:`, `:lucide-calendar:`, `:lucide-timer:` |
| 影片/多媒體 | `:lucide-play:`, `:lucide-video:`, `:lucide-film:` |
| 折扣/優惠 | `:lucide-percent:`, `:lucide-badge-percent:`, `:lucide-circle-percent:` |
| LINE 相關 | `:lucide-message-circle:`, `:lucide-send:` |
| 下一步/流程 | `:lucide-arrow-right:`, `:lucide-chevron-right:`, `:lucide-arrow-right-from-line:` |
| 部落格/文章 | `:lucide-file-text:`, `:lucide-newspaper:`, `:lucide-book-open:` |
| 評論/反饋 | `:lucide-star:`, `:lucide-message-square:`, `:lucide-feedback:` |

---

## 互動式執行流程

### Step 1: 選擇 Grid 樣式

使用 `question` 工具詢問用戶要使用哪種樣式：

```
請選擇要建立的 Grid 樣式：

A) 輕量導航 (入口導航) — 僅標題+連結，適合章節入口
B) 後續操作 (Next Steps) — 圖示+標題+說明+連結，適合文件末尾的操作建議
C) 功能說明 (單卡片) — 圖示+標題+分隔線+描述+連結，適合單一功能介紹
D) 功能說明 (多卡片) — 多項功能各自獨立卡片，適合多個設定項目詳細說明
E) 入口按鈕 (Extension Buttons) — 大膠囊按鈕樣式，適合功能入口展示
F) Block 語法 — 卡片與其他元素混合排列
G) Generic Grids — 任意區塊（比較、程式碼範例）
```
請選擇要建立的 Grid 樣式：

A) 輕量導航 (入口導航) — 僅標題+連結，適合章節入口
B) 後續操作 (Next Steps) — 圖示+標題+說明+連結，適合文件末尾的操作建議
C) 功能說明 (Feature Cards) — 圖示+標題+分隔線+描述+連結，適合詳細功能介紹
D) 入口按鈕 (Extension Buttons) — 大膠囊按鈕樣式，適合功能入口展示
E) Block 語法 — 卡片與其他元素混合排列
F) Generic Grids — 任意區塊（比較、程式碼範例）
```

### Step 2: 選擇放置位置

根據選擇的樣式，提供對應的放置位置選項：

**輕量導航**：
- 章節頂部的設定項目導覽
- 功能分類入口

**後續操作**：
- 文件末尾的延伸閱讀
- 操作建議區塊

**功能說明**：
- 產品功能介紹
- 設定項目說明

**入口按鈕**：
- 擴充功能展示
- 應用程式入口

### Step 3: 輸入內容

詢問用戶要轉換的內容：
- 直接貼上文字內容
- 或提供檔案路徑
- 說明每個項目的標題、說明、連結

### Step 4: 生成 Grid

根據前三步的選擇，生成正確的 Markdown 格式。

---

## 常見問題

### Q: 如何選擇適合的樣式？

**A**: 參考「放置位置與樣式對照表」：

| 如果你的文件需要... | 使用這個樣式 |
| :--- | :--- |
| 輕量導航，僅標題+連結 | 輕量導航 (`{ .ig .middle }`) |
| 具體操作建議，含說明 | 後續操作 (`{ .lg }`) |
| 單一功能詳細說明 | 功能說明 (單卡片) (`{ .lg .middle }` + `---`) |
| 多個設定項目詳細說明 | 功能說明 (多卡片) |
| 卡片與其他元素混合 | Block 語法 (`{ .card }`) |
| 任意區塊（admonitions、程式碼） | Generic Grids |

### Q: 什麼時候加 `{ data-preview }`？

**A**:
- **有相關文件**：`[__標題__](doc.md){ data-preview }`
- **僅為錨點**：`[__標題__](#錨點){ data-preview }`
- **文件尚未建立**：`[__標題__]()`
- **autoref 交叉引用** (新啟用)：`[顯示文字][標題文字]{ data-preview }`
  - 格式：`[顯示文字][目標標題]{ data-preview }`
  - 目標標題需與目標文件中的標題（如 `### 商家手動取消訂單`）完全一致
  - 範例：`[取消訂單][商家手動取消訂單]{ data-preview }`
  - **此語法由 mkdocs-autorefs 插件自動解析，無需定義參考連結**
- **autoref 交叉引用** (新啟用)：`[顯示文字][參考標籤]{ data-preview }`
    - 格式：`[顯示文字][目標標題]{ data-preview }`
    - 目標標題需與文件中某個標題（如 `### 商家手動取消訂單`）完全一致
    - 範例：`[取消訂單][商家手動取消訂單]{ data-preview }`
    - **此語法由 mkdocs-autorefs 插件自動解析，無需定義參考連結**
- **autoref 交叉引用** (新啟用)：`[顯示文字][標題文字]{ data-preview }`
    - 格式：`[顯示文字][目標標題]{ data-preview }`
    - 目標標題需與文件中某個標題（如 `### 商家手動取消訂單`）完全一致
    - 範例：`[取消訂單][商家手動取消訂單]{ data-preview }`
    - **此語法由 mkdocs-autorefs 插件自動解析，無需定義參考連結**

### Q: List 語法 vs Block 語法？

**A**: 
- **List 語法** (`class="grid cards"`)：標準用法，列表項自動變成卡片
- **Block 語法** (`class="grid"` + `{ .card }` )：當需要與其他元素混合時使用

### Q: Cards vs Generic？

**A**: 
- **Cards** (`class="grid cards"`）：有悬停卡片效果，適合連結導航
- **Generic** (`class="grid"`）：無卡片效果，適合比較、程式碼等場景

---

## 範例

### 範例 1：輕量導航

**輸入**：
```
在「全站共用設定」中，有以下設定項目：導覽列、頁腳、彈窗廣告、顏色與圖示設定。
```

**輸出**：
```markdown
## 全站共用設定

<div class="grid cards" markdown>

- :lucide-menu:{ .ig .middle }
  [__導覽列__](#導覽列){ data-preview }
- :lucide-arrow-down-to-line:{ .ig .middle }
  [__頁腳__](#頁腳){ data-preview }
- :lucide-megaphone:{ .ig .middle }
  [__彈窗廣告__](#彈窗廣告){ data-preview }
- :lucide-palette:{ .ig .middle }
  [__顏色與圖示設定__](#顏色與圖示設定){ data-preview }

</div>
```

### 範例 2：後續操作

**輸入**：
```
將以下文字轉換為 grid cards：
完成設定後，建議進行以下操作：
1. **LINE 加入好友工具**：引導商家加入 LINE 官方帳號好友。
2. **物流限制**：設定商品的配送物流條件。
假設相關文件為「設定拖拉版型網站的 LINE 加入好友工具.md」和「設定超商配送限制與物流排除.md」。
```

**輸出**：
```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-user-plus:{ .lg }   
  [__LINE 加入好友工具__](../integrations/line/設定拖拉版型網站的 LINE 加入好友工具.md){ data-preview }       
  在拖拉版型官網設定工具，引導商家加入 LINE 官方帳號好友。

- :lucide-ban:{ .lg }     
  [__物流限制與排除選項__](設定超商配送限制與物流排除.md)  
  設定商品的配送物流條件，限制特定物流方式於結帳流程中的顯示與使用。

</div>
```

### 範例 3：功能說明 (單卡片)

**輸入**：
```
將以下功能說明轉換為 grid cards：
- **GMC 帳號設定**：進入 Google Merchant Center 完成商家基本資訊設定，並確認商店所有權完成驗證。
- **GA4 串接**：在 Google Analytics 後台取得「評估 ID」，前往 CYBERBIZ 後台填入評估 ID 完成串接。
```

**輸出**：
```markdown
<div class="grid cards" markdown>

-   :lucide-tags:{ .lg .middle } __建立並驗證 GMC 帳號__

    ---

    進入 Google Merchant Center 完成商家基本資訊設定，並確認商店所有權完成驗證。

    [:lucide-arrow-right: 設定教學](設定 Google Merchant Center 並同步 CYBERBIZ 商品.md){ data-preview }

-   :lucide-chart-no-axes-column-increasing:{ .lg .middle } __建立並串接 GA4 帳號__

    ---

    在 Google Analytics 後台取得「評估 ID」，前往 CYBERBIZ 後台填入評估 ID 完成串接。

    [:lucide-arrow-right: 設定教學](建立並串接 Google Analytics.md){ data-preview }

</div>
```

### 範例 4：功能說明 (多卡片)

**輸入**：
```
將以下設定項目轉換為多卡片 grid：
- **設定路徑**：後台路徑：「訊息推播」→「簡訊通知樣板」。
- **樣板類別**：包含訂單相關、退貨相關、物流相關、顧客相關以及 POS 相關通知。
- **編輯內容**：點擊樣板標題即可自訂文字。請注意 {{...}} 內的代碼為系統自動抓取的參數。
- **短網址功能**：可開啟短網址功能，自動將簡訊中的連結縮短以節省字數。
```

**輸出**：
```markdown
## 簡訊通知樣板管理

<div class="grid cards" markdown>

-   :lucide-map-pin:{ .lg .middle } __設定路徑__

    ---

    後台路徑：**「訊息推播」>「簡訊通知樣板」**。

-   :lucide-layout-grid:{ .lg .middle } __樣板類別__

    ---

    包含訂單相關、退貨相關、物流相關、顧客相關以及 POS 相關通知。

-   :lucide-pencil:{ .lg .middle } __編輯內容__

    ---

    點擊樣板標題即可自訂文字。請注意 `{{...}}` 內的代碼為系統自動抓取的參數。

-   :lucide-link:{ .lg .middle } __短網址功能__

    ---

    可開啟短網址功能，自動將簡訊中的連結縮短以節省字數。

    [:lucide-arrow-right: 詳細設定](設定與管理簡訊通知樣板.md){ data-preview }

</div>
```

### 範例 5：Generic Grid 比較

**輸入**：
```
用 Generic Grid 並排顯示兩種列表範例。
```

**輸出**：
```markdown
<div class="grid" markdown>

=== "未排序列表"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "已排序列表"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

</div>
```
