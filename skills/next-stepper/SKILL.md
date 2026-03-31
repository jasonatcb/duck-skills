---
name: next-stepper
description: 將敘述形式的後續操作建議轉換為 zensical grid card 布局。當用戶說「將下一步轉換為 grid card」、「把後續操作變成卡片」、「將步驟轉為 grid cards」或類似意圖時觸發此技能。使用方式：用戶提供文檔路徑加章節名稱（如「@docs/ga.md 的 ## 重要進階設定建議」），或直接貼上需要轉換的文字（如 bullet points 或段落），技能會解析內容，選擇適當的 Lucide 圖示，生成 grid cards 格式的 Markdown。
version: "1.0.7"
last_updated: 2026-03-23
---

# Next Stepper 技能

將敘述形式的後續操作建議轉換為 zensical grid card 布局。

## 使用方式

**輸入方式（兩種）：**

1. **引用檔案 + 章節**：@ 檔案路徑 + 指定章節名稱
   ```
   將 @docs/ec/integrations/google/ga/建立並串接 Google Analytics.md 的 ## 重要進階設定建議 轉換為 grid cards
   ```

2. **直接貼上文字**：將需要轉換的文字貼上
   ```
   將以下文字轉換為 grid cards：
   
   *   **排除內部流量**：在 GA4 管理介面的「資料串流」中定義公司 IP...
   *   **列出不適用的參照連結**：...
   ```

**輸出**：生成 grid cards 格式的 Markdown，可直接複製到文件中。

## ⚠️ 輸出格式（嚴格遵守）

**用戶提供的正確範例：**
```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-link:{ .lg }   
  [__LIFF 網址優化__](設定 LIFF 自動登入與會員綁定.md){ data-preview }       
  改用 EC 後台生成的 **LIFF 網址**。消費者點擊後可在 LINE 內自動套用帳戶資訊，實現「一鍵加入好友、註冊會員並完成綁定」，優化使用體驗。

- :lucide-search:{ .lg }     
  [__關鍵字搜尋商品__](串接 LINE Messaging API.md#line-關鍵字搜尋商品){ data-preview }    
  串接 Webhook 後，顧客可在 LINE 對話框輸入關鍵字，由系統自動回覆搜尋到的商品訊息。

</div>
```

**錯誤示範（不要這樣做）：**
```markdown
# 錯誤格式
- **標題**  # 使用粗體 ❌
- :material-xxx:  # 使用 Material icons ❌
- :lucide-xxx: **標題** { .card }  # 圖示和標題在同一行 ❌
- [:lucide-xxx: 標題](#) { .card }  # 使用方括號包圖示 ❌
```

**正確格式（必須這樣做）：**
```markdown
<div class="grid cards" markdown>

- :lucide-shield:{ .lg }   
  [__排除內部流量__]()       
  在 GA4 管理介面的「資料串流」中定義公司 IP。

- :lucide-link:{ .lg }   
  [__排除參照連結__]()    
  將金物流服務商加入排除名單。

</div>
```

## 使用方式

用戶提供敘述形式的文字（bullet points、numbered list 或段落），技能會：
1. 解析每個建議項目
2. 選擇適當的 Lucide 圖示
3. 生成 grid cards 格式的 Markdown

## 執行步驟

### 1. 解析輸入內容

**兩種輸入方式：**

**方式 A：引用檔案 + 章節**
- 用戶輸入：`@docs/path/file.md 的 ## 章節名稱`
- 解析：讀取檔案，找到指定章節（如 `## 重要進階設定建議`）
- 提取該章節下的所有 bullet points 或段落

**方式 B：直接貼上文字**
- 用戶輸入：直接貼上需要轉換的文字
- 解析：識別 bullet points（`* ` 或 `- `）、numbered list（`1. `）或段落

### 2. 解析每個建議項目
- 識別每個獨立的建議項目（每個 bullet 或段落）
- 提取標題/關鍵動作（去除 `**粗體**`）
- 提取說明文字
- 找出是否有相關文件的連結資訊

### 2. 選擇 Lucide 圖示
根據建議的類型選擇最合適的圖示：

| 類型 | 圖示 |
| :--- | :--- |
| 設定/配置 | `:lucide-settings:`, `:lucide-cog:`, `:lucide-sliders:` |
| 串接/整合 | `:lucide-plug:`, `:lucide-link:`, `:lucide-connection-points:` |
| 搜尋/查找 | `:lucide-search:`, `:lucide-binoculars:` |
| 分析/數據 | `:lucide-bar-chart:`, `:lucide-analytics:`, `:lucide-trending-up:` |
| 優化 | `:lucide-rocket:`, `:lucide-zap:`, `:lucide-speed:` |
| 通知/訊息 | `:lucide-bell:`, `:lucide-message:`, `:lucide-mail:` |
| 驗證/檢查 | `:lucide-check-circle:`, `:lucide-shield:`, `:lucide-verified:` |
| 匯入/匯出 | `:lucide-download:`, `:lucide-upload:`, `:lucide-file-export:` |
| 登入/認證 | `:lucide-log-in:`, `:lucide-key:`, `:lucide-user-check:` |
| 會員/用戶 | `:lucide-users:`, `:lucide-user-plus:`, `:lucide-user:` |
| 產品/商品 | `:lucide-package:`, `:lucide-box:`, `:lucide-tag:` |
| 訂單/交易 | `:lucide-shopping-cart:`, `:lucide-receipt:`, `:lucide-dollar-sign:` |
| 金流/付款 | `:lucide-credit-card:`, `:lucide-wallet:`, `:lucide-payments:` |
| 庫存/倉儲 | `:lucide-warehouse:`, `:lucide-package-check:` |
| LINE 相關 | `:lucide-message-circle:`, `:lucide-send:` |
| API 相關 | `:lucide-api:`, `:lucide-code:`, `:lucide-brackets:` |
| 時間/排程 | `:lucide-clock:`, `:lucide-calendar:`, `:lucide-timer:` |
| 啟用/開啟 | `:lucide-toggle-left:`, `:lucide-power:` |
| 下一步/流程 | `:lucide-arrow-right:`, `:lucide-chevron-right:` |
| 預設/預設值 | `:lucide-settings-2:`, `:lucide-sliders-horizontal:` |

### 3. 生成 Grid Cards 格式

**⚠️ 嚴格遵守以下格式，每一行都要完全正確：**

```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-shield:{ .lg }   
  [__排除內部流量__]()       
  在 GA4 管理介面的「資料串流」中定義公司 IP，避免開發或行銷人員的瀏覽行為干擾分析。

- :lucide-link:{ .lg }   
  [__排除參照連結__]()    
  將金物流服務商加入排除名單，以免轉換來源被誤判為第三方金流頁面。

</div>
```

**格式規則（每一條都要遵守）：**

1. 標題：`## 後續操作`（單獨一行）
2. 開始標籤：`<div class="grid cards" markdown>`（單獨一行）
3. **每張卡片結構**：
   - 第 1 行：`- :lucide-<name>:{ .lg }`（注意開頭是 `- `，然後是圖示）
   - 第 2 行：`  [__標題__]()`（開頭有兩個空格，然後是方括號包雙底線標題，空連結）
   - 第 3 行：`  說明文字...`（開頭有兩個空格）
4. 每張卡片之間以**空行**分隔
5. 結束標籤：`</div>`（單獨一行）

**常見錯誤（禁止發生）：**
- ❌ 不要使用 `*` 開頭，必須用 `- `
- ❌ 不要把圖示和標題寫在同一行
- ❌ 不要使用 `**粗體**`，必須用 `__雙底線__`
- ❌ 不要使用 `{ .card }`，屬性是 `{ .lg }`（用於圖示）
- ❌ 不要省略開頭的兩個空格

### 4. 處理無文件連結的情況（文件尚未建立）

當文件尚未建立時，連結為空，但仍需使用以下格式：

```markdown
- :lucide-settings:{ .lg }   
  [__設定項目名稱__]()       
  設定說明文字...
```

**注意**：
- 圖示獨立一行
- `[__標題__]()` 後面**不要加任何屬性**，直接空著
- 說明文字接在 `()` 後方

### 5. 處理多層級內容

若輸入內容有主要類別和子項目：

```markdown
<div class="grid cards" markdown>

- :lucide-settings:{ .lg }   
  [__主要設定__](doc.md)       
  主要設定的說明

  - 子項目說明

</div>
```

### 6. 圖示選擇範例

根據用戶提供的實際範例，注意以下映射關係：

| 建議項目 | 正確圖示 | 錯誤圖示 |
| :--- | :--- | :--- |
| 排除內部流量 | `:lucide-shield:` | `:lucide-shield-off:`, `:lucide-shield-check:`, `:lucide-ban:`, `:lucide-import:` |
| 排除參照連結 | `:lucide-link:` | `:lucide-link-off:`, `:lucide-ban:` |
| 延長資料保留期限 | `:lucide-clock:` | `:lucide-ban:` |
| Google 信號/用戶 | `:lucide-users:` | `:lucide-user-check:`, `:lucide-ban:` |

**嚴禁**：
- **禁止使用 Material icons**（如 `:material-xxx:`），只能使用 Lucide icons（`:lucide-xxx:`）
- 不要對不同的項目重複使用相同的圖示
- 不要使用 `-off` 結尾的圖示（如 `:lucide-shield-off:`、`:lucide-link-off:`）
- 不要使用 `-check` 結尾的圖示（如 `:lucide-shield-check:`、`:lucide-user-check:`）

### 7. 空連結格式（文件尚未建立）

當文件尚未建立時：
- **有連結**：`[__標題__](路徑.md){ data-preview }`
- **無連結（文件尚未建立）**：`[__標題__]()`

**注意**：
- 空連結寫成 `[__標題__]()`，**不要加 `{ data-preview }` 屬性**
- 說明文字直接接在 `()` 後方

## 範例

### 範例 1：Bullet points 輸入

**輸入：**
```markdown
為確保數據準確性，建議完成串接後進行以下調整：

*   **排除內部流量**：在 GA4 管理介面的「資料串流」中定義公司 IP，避免開發或行銷人員的瀏覽行為干擾分析。
*   **列出不適用的參照連結**：將金物流服務商（如 `cyberbizpay.com`、`pay.ecpay.com.tw` 等）加入排除名單。
*   **延長資料保留期限**：GA4 預設資料僅保留 2 個月，建議改為 14 個月。
```

**輸出：**
```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-users:{ .lg }   
  __排除內部流量__       
  在 GA4 管理介面的「資料串流」中定義公司 IP，避免開發或行銷人員的瀏覽行為干擾分析。

- :lucide-link:{ .lg }   
  __排除參照連結__       
  將金物流服務商（如 cyberbizpay.com、pay.ecpay.com.tw 等）加入排除名單，避免轉換來源被誤判。

- :lucide-clock:{ .lg }   
  __延長資料保留期限__       
  GA4 預設資料僅保留 2 個月，建議至「資料收集與修改」→「資料保留」改為 14 個月。

</div>
```

### 範例 2：有文件連結的輸入

**輸入：**
```markdown
完成設定後，您可以：

1. **LIFF 網址優化**：改用 EC 後台生成的 LIFF 網址，實現「一鍵加入好友、註冊會員並完成綁定」
2. **關鍵字搜尋商品**：串接 Webhook 後，顧客可在 LINE 對話框輸入關鍵字，由系統自動回覆搜尋結果
```

假設有相關文件：`設定 LIFF 自動登入與會員綁定.md` 和 `串接 LINE Messaging API.md`

**輸出：**
```markdown
## 後續操作

<div class="grid cards" markdown>

- :lucide-link:{ .lg }   
  [__LIFF 網址優化__](設定 LIFF 自動登入與會員綁定.md){ data-preview }       
  改用 EC 後台生成的 **LIFF 網址**。消費者點擊後可在 LINE 內自動套用帳戶資訊，實現「一鍵加入好友、註冊會員並完成綁定」，優化使用體驗。

- :lucide-search:{ .lg }     
  [__關鍵字搜尋商品__](串接 LINE Messaging API.md#line-關鍵字搜尋商品){ data-preview }    
  串接 Webhook 後，顧客可在 LINE 對話框輸入關鍵字，由系統自動回覆搜尋到的商品訊息。

</div>
```

## 注意事項

- 確保圖示選擇符合建議的語意
- 連結應為相對路徑，指向存在的文件
- 說明文字保持簡潔，不超過 2-3 行
- 若無法判斷合適的圖示，使用 `:lucide-arrow-right:` 作為預設
- 輸出應直接附加到文件中，或替換原有的敘述格式
