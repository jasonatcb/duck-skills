```markdown
# CYBERBIZ 商家教學文件產生器

## 任務

為 CYBERBIZ 後台 **/admin/orders** 撰寫一份**末端商家**使用的教學文件。

主題:**宅配通出貨流程**

---

## 撰寫前置研究(必做，不得憑空捏造)

請依序閱讀以下程式碼來源，並以實際程式碼內容為準撰寫文件。

### 1. 後端

* Controller:`app/controllers/admin/{{controller}}.rb`(舊版頁面)
* Controller:`app/controllers/api_internal/v2/admin/{{controller}}.rb` 或 `app/features/admin_context/{{feature}}/`(新版頁面)
* Model / Service:相關業務邏輯檔案(例如 `app/services/orders_searcher.rb`、`app/models/order.rb`)
* KeyValues 定義:`app/models/key_values/{{...}}.rb`(列舉所有可選值)

### 2. 前端

* 舊版 View:`app/views/admin/{{page}}/`(haml / erb)
* 新版前端:`frontend/admin/src/features/{{feature}}/`,含 `components/`、`slices/`、`domain/models/`

### 3. i18n(取得實際商家看到的中文字面)

* 主檔:`config/locales/zh-TW.yml`
* KeyValues 字典:`config/locales/key_values/{{model}}/zh-TW.yml`
* 前端 i18n:`frontend/admin/src/locale/res/payments-and-logistics/zh.json`
* ⚠ 字面務必抓自 i18n,不要自行翻譯英文 code 為中文

### 4. Plugin / 方案開通條件(三張關鍵檔案)

* `app/models/key_values/plan/type_plugin.rb` — 各版本功能定義
* `app/services/shop_rake/plan/plan_upgrader.rb` — 商店升級時自動安裝的功能
* `app/services/shop_default_datas.rb` — 新店家預設功能

針對每個篩選器 / 欄位 / 動作,確認:

* 它是否有 `shop.has_plugin?('xxx')` / `shop.is_enterprise?` / `shop.add_on?` 等條件判斷
* 對應的 plugin 中文名與哪些方案會預設安裝

---

## 錨點命名規則

所有 heading 錨點遵循 `{primary}-{category}-{subtopic}` 格式。

### Primary 類別(H2 層級)

| Primary | 對應標題 | 必/選 | 說明 |
|---------|----------|-------|------|
| `intro` | 功能介紹 | 必 | 頁面用途、核心價值 |
| `overview` | 頁面功能總覽 | 選 | 僅頁面有多區塊/多入口時使用 |
| `prerequisites` | 使用前提與限制 | 選 | 開通條件、方案、前置設定 |
| `pricing` | 計費規則 | 選 | 僅當有計費/扣款規則時使用 |
| `configure` | 設定類步驟 | 選 | 僅當內容為首次設定（非日常操作） |
| `operate` | 操作步驟 | 必 | 日常操作流程 |
| `specs` | 重要規範與限制 | 選 | 取代模糊的 `rules`，語意更精準 |
| `next-steps` | 後續操作 | 選 | 完成後可進行的相關操作 |
| `faq` | 常見問題 | 必 | FAQ accordion |
| `reference` | 參考資料 | 必 | 對照表、外部連結 |

### 子層級規則

- **H3**: `{primary}-{category}-{subtopic}`
  範例：`operate-pelican-bulk-download`、`prerequisites-pelican-billing-mode`、`configure-pelican-management-sender`
- **H4 以上**: 繼續 append
  範例：`operate-pelican-bulk-download-confirm`
- **FAQ 內部**: `faq-{category}-{keyword}`
  範例：`faq-pelican-insufficient-points`

---

## A. 寫操作步驟前的強制驗證(防止幻覺)

每個「操作步驟」小節在動筆前,**必須**先在內部備註(不放進文件)寫出下列三項。未通過此檢查,不得描述任何點擊路徑 / 按鈕名 / 視窗名。

* **觸發 UI 元件**:具體檔案路徑與行號(例:`OrdersTagsModal.tsx:26`)
* **入口位置**:此元件由哪個 component 觸發、按鈕文字對應的 i18n key
* **使用的 i18n keys**:列出所有會出現在文件中的中文文案,逐一對到 yml / json 行號

### 範例(內部備註,不放進文件)

```text
標籤註記操作步驟:
- 元件:OrdersTagsModal.tsx (line 26)
- 觸發:OrdersTableField.tsx (line 859)經由「更多操作」下拉
- i18n:
  - orders_index_more_action → 「更多操作」
  - orders_index_action_add_tags → 「新增訂單標籤」
  - orders_index_add_tags_placeholder → 「請選擇標籤或輸入以建立新標籤」
```

寧可空著段落請使用者補充,也不要憑印象描述操作流程。

---

## 文件規格

| 項目 | 規定 |
| :-- | :-- |
| 語言 | 繁體中文(zh-TW),不使用簡體 / 英文混雜 |
| 標點 | 使用全形中文標點:**，。「」、():；!？**,不使用半形 `,.""():;!?`(規則細節見 §B) |
| 對象 | 末端商家(end-merchant),非開發者 — 不要露出 plugin code、欄位英文 code、表名 |
| 格式 | Markdown(Material for MkDocs / Zensical 風格) |
| 文件類型 | User tutorial(使用指南) |
| divider | only between h3 headings not and further down |

---

## 文件結構(依序)

1. **功能介紹** — 這個頁面是什麼、用途 { #intro-tcat-shipping }
2. **頁面功能總覽**(若有,以表格呈現) { #overview-tcat-shipping }
3. **計費或規則說明**(若有) { #pricing-tcat-shipping }
4. **使用前提與限制**(若有) { #prerequisites-tcat-shipping }
5. **操作步驟** — Step-by-step,依**使用情境**分段 { #operate-tcat-shipping }
6. **重要規範與限制**(若有) { #specs-tcat-shipping }
7. **後續操作** — 完成主要操作後商家可能接著做的事 { #next-steps-tcat-shipping }
8. **常見問題(FAQ)** { #faq-tcat-shipping }
9. **參考資料** { #reference-tcat-shipping }

跳轉 headings 應使用 `{primary}-{category}-{subtopic}` 格式的錨點：

```markdown
## 自訂物流出貨說明 { #intro-custom-logistics-shipping }
## 使用前提與限制 { #prerequisites-custom-logistics-shipping }
```

步驟的格式需為 task-oriented procedure writing style，參考以下：

```text
二、 操作步驟教學

以下以黑貓託運單為例，其他物流商（如宅配通、順豐、新竹物流或自訂出貨）的操作步驟皆相同：

1. **進入訂單詳情：** 前往後台路徑：「訂單」→「所有訂單」，點選欲執行部分出貨的「訂單編號」進入明細頁。
2. **勾選出貨商品：** 在訂單頁面右側的「出貨」欄位中，勾選本次要優先出貨的商品品項。
3. **選擇出貨方式與運費：** 勾選商品後，於下方選單選擇出貨方式(例如「黑貓託運單」)並選擇運費計算標準，最後點擊**「確認出貨」**。
4. **確認出貨紀錄：** 操作完成後，該項商品下方會顯示出貨的日期及時間。
5. **後續出貨：** 若日後要繼續寄送剩餘尚未出貨的商品，重複上述步驟即可。
```

> **進階範例：避免步驟文字過長**
>
> 步驟中若出現方案差異、系統錯誤提示原文或技術細節而導致文字過長時，**不要全部塞在內文**，改用 `[^n]` 腳註將次要資訊移出步驟流程，讓步驟保持簡潔可掃讀：
>
> ```text
> 4. 點擊 **「確認下載」**，系統彈出二次確認視窗，按 **「確認」** 即會：
>     * 扣除 Cyber 幣或列入對帳單[^1]
>     * 呼叫順豐[^2] 取得新單號
>     * 自動下載託運單 PDF
>     * 將該訂單與單號寫入下方的「單號使用紀錄」表格
>
> [^1]: 一般版立即扣除(單價×張數)；PLUS版/企業版列入對帳單。
> [^2]: 順豐 OpenAPI
> ```
>
> 腳註定義寫在所屬小節結尾、`---` 分隔線之前，不需要集中放到文末。

FAQ 格式範例：

```markdown
## 常見問題 { #faq-tcat-shipping }
??? quote "{問題文字}"
    [](){ #faq-tcat-shipping-{keyword} }
    {答案內容}
    - {列表項目}
    - {列表項目}
```

**FAQ 變數說明：**
| 變數 | 說明 | 範例 |
|------|------|------|
| `{category}` | 產品/功能 kebab-case | `pelican`, `pelican-management`, `tcat` |
| `{keyword}` | 問題 kebab-case | `download-no-response` |
| `{問題文字}` | 問題內容 | `下載沒反應 / 無法下載託運單` |

**格式規則：**
- 答案中的列表前需空行
- 錨點 slug 前綴為 `faq-{category}`
- 答案中專有名詞加 `{ data-preview }` 連結

---

## 檔案組織

* **主文**:`docs/payments-and-logistics/tcat-shipping.md`
* **對照表**:`docs/payments-and-logistics/references/tcat-shipping-columns.md`、`docs/payments-and-logistics/references/tcat-shipping-statuses.md` 等,**每張對照表獨立一個檔案**
* 對照表檔案內僅放錨點標題 + 表格 + 註釋,不重複主文敘述

理由:對照表會被多份主文(搜尋篩選、匯出、報表)共用;集中於 `references/` 可避免重複維護,且 data-preview 跳轉跨檔案仍可運作。

---

## B. 標點符號強制規則(可機械檢查)

文件中**禁止出現**的半形字元在 CJK 上下文中。送出前用下列 regex 自我搜尋,有 hit 即修。

### 對照表

| 半形 | 應改為全形 |
| :-- | :-- |
| `,`(中文句中) | `，` |
| `.`(中文句末) | `。` |
| `(` `)` | `(` `)` |
| `:`(中文標題或敘述後) | `：` |
| `;`(中文句中) | `；` |
| `?` `!` | `？` `！` |
| `"..."` `'...'`(引述) | `「...」` |

### 例外(允許半形)

* 程式碼區塊內(三反引號之間)
* 行內程式碼(單反引號包住)
* URL / 檔案路徑 / API 端點
* 數字千分位(`1,000`)與小數點(`3.14`)
* 英文段落內

### 自查 regex

```text
[\u4e00-\u9fff],          ← 中文後接半形逗號
[\u4e00-\u9fff]\.          ← 中文後接半形句號
[\u4e00-\u9fff]\(          ← 中文後接半形左括號
\][\u4e00-\u9fff]          ← 半形右括號接中文
[\u4e00-\u9fff]:           ← 中文後接半形冒號
[\u4e00-\u9fff];           ← 中文後接半形分號
```

---

## C. 換行與粗體規則(可機械檢查)

### C-1. 段落與列表項目「不可在中間換行」

每個段落、每個列表項目寫成**單一物理行**,**不在 markdown 原始檔中按 Enter 斷行**。即使一行很長,也讓編輯器自行 word-wrap。

理由:Zensical / MkDocs 在 CJK 環境下,把單一換行 render 為空白或斷行,造成輸出跑版。寫成單行可避開所有渲染器差異。

```markdown
❌ 錯誤(貼上後會跑版)
* 訂單標籤是商家內部使用的分類工具,
  不會顯示給顧客。

✅ 正確(一整行,讓編輯器自行 word-wrap)
* 訂單標籤是商家內部使用的分類工具,不會顯示給顧客。
```

**自查方式**:列表項目(`*` 或 `1.` 開頭)後面,若下一行開頭是中文且無項目符號,即為違規。

### C-2. 粗體前後留空格

`**...**` 緊貼 CJK 字元時,Zensical 不會 render 為粗體。一律加空格。

```markdown
❌ 錯誤
請點選**儲存**按鈕。

✅ 正確
請點選 **儲存** 按鈕。
```

**例外**:當 `**` 緊接全形標點(`,。「」(`)時不需空格,因為全形標點具有 CJK 寬度,Zensical 可以正確識別邊界。

**自查 regex**:

```text
[\u4e00-\u9fff]\*\*        ← CJK 緊接 ** 開頭(違規)
\*\*[\u4e00-\u9fff]        ← ** 結尾緊接 CJK(違規)
```

### C-3. 列表縮排用 4 個空格

巢狀列表、列表項目下的延續段落 / admonition,延續行縮排 **4 格**(對齊列表內容的開始位置),不是 2 格。

### C-4. 表格內不換行

Markdown 表格的單一儲存格內容必須保持一行,不要為了原始檔好讀就在儲存格內手動換行。需要分行時用 `<br>` 或拆成多列。

### C-5. Admonition 內容縮排 4 格

```markdown
!!! tip "技巧"
    內容寫一整行,不在中間換行。
    若有多段,空行後再寫一行,同樣縮排 4 格。
```

---

## 樣式約定(Material for MkDocs / Zensical)

### 內容分頁(新舊版並陳時必用)

```markdown
=== "新版訂單列表"
    內容...

=== "舊版訂單列表"
    內容...
```

### Admonition

```markdown
!!! info "提示"
!!! tip "技巧"
!!! note "註釋"
!!! plan "方案 / 開通條件"      ← 自定 class,方案差異一律用這個
??? plan "可折疊的方案對照"      ← 內容多時用 ??? 折疊
```

全部範例參考 [zensical 官方文件](https://zensical.org/docs/authoring/admonitions/?h=adm)

### 錨點與 data-preview 跳轉

* 對照表用 `### 標題 { #anchor-name }` 建錨點
* 引用其他段落時用 `[顯示文字][anchor-name]{ data-preview }`
* 對照表獨立檔案時,跨檔案 data-preview 仍可運作,錨點需全站唯一

### 鍵盤鍵

* 用 `++enter++`、`++ctrl+s++`,不要寫 `Enter`、`Ctrl+S`

### 前提條件 checkbox 格式

使用 `- [x]` 搭配粗體標題，讓前提條件一目瞭然：

```markdown
- [x] **公司物流地址**：至「一般設定」>「公司物流地址」設定寄件地址。
- [x] **公司統一編號**：至「一般設定」>「公司聯絡資訊」輸入統編。
```

### Hero 圖片與 Subtitle

```markdown
頁面用途的簡短摘要。
{ .subtitle }

![Alt 文字](../../assets/images/路徑-hero.png){ .hero-page }
```

### 後續操作 grid cards

後續操作區塊使用 Material for MkDocs 的 grid cards 格式，搭配 Lucide icons：

```markdown
<div class="grid cards" markdown>

- :lucide-package:{ .lg }  
  [__顯示文字__](../path/to/page.md){ data-preview }  
  簡短說明文字。

- :lucide-settings:{ .lg }  
  [__顯示文字__](../path/to/page.md){ data-preview }  
  簡短說明文字。

</div>
```

---

## 篩選 / 列表類功能必含的內容

當主題是「搜尋與篩選」這類功能,**至少**要交代:

### 區塊一. 關鍵字搜尋

* 搜尋框比對哪些欄位(訂單編號、客戶 Email、商品 SKU 等)
* 模糊比對 vs 完全比對(若有開關)
* 新舊版差異(若有)

### 區塊二. 條件篩選 — 包含三段

1. **篩選的組合邏輯**(獨立小節,新功能容易漏)
   * 同一篩選器多選 → OR / AND?
   * 不同篩選器疊加 → OR / AND?
   * 搜尋 + 篩選 → 怎麼疊?
   * 是否可切換邏輯?
2. **操作方式**(依新舊版用 `===` 分頁)
   * 新版:新增條件 → 設值 → 清除 → 儲存為檢視群組
   * 舊版:固定下拉的操作流程
3. **方案 / 加值功能差異** — 用 `??? plan` 折疊區呈現對照

### 區塊三. 對照表(獨立檔案放 `references/`)

每個多值篩選器 / 狀態欄位 / 列表欄位都應有獨立對照表,**檔案獨立**,主文以 `data-preview` 引用。統一格式:

```markdown
### {{篩選器中文名}}對照表 { #anchor-id }

| {{欄位名}} | 說明 | 開通條件 |
| :-- | :-- | :-- |
| 值 1 | 從商家視角描述這個值代表的業務情境 | — 或具體加值功能名 |
| 值 2 | ... | ... |

!!! note "註釋"
    * 整體 / 個別選項的開通條件
    * 動態 vs 靜態選項的說明
```

#### 對照表撰寫原則

* **欄位設計**:基本款是「值 / 說明」兩欄;當 plugin 條件多時擴充為「值 / 說明 / 開通條件」三欄
* **說明欄位**從**商家視角**寫,不寫 code 或內部術語
   * ❌ "shipping with `branch_store_pickup` plugin"
   * ✅ 「由顧客至超商門市取貨」
* **動態選項**不要硬列舉(避免清單過時),用「依商家設定動態顯示」+ 範例帶過
* **混合 / 邊界情境**要明確說明(例「混合訂單」是什麼、「不需出貨」適用什麼商品)

### 區塊四. 總覽表(新版有 chip-based 篩選時必加)

所有可用篩選器 + 類型(多選 / 日期區間)+ 簡短說明 + 開通條件,讓商家一眼看完。

### 區塊五. 常見組合範例(tip admonition)

給 3-5 個典型業務情境的「篩選組合配方」,把抽象規則變成可套用的場景:

* 「找今天要出貨的訂單」 → 配送狀態 = 未出貨 + 訂單成立日期 = 過去 7 天
* 「特定門市的當月業績」 → 訂單來源 = 某 POS 門市 + 訂單成立日期 = 介於 X ~ Y

---

## D. 提交前最終檢核(必跑)

寫完文件後,**送出前**心中跑完這份清單,任一項未通過則回頭修。**未過任一項,不得交付。**

1. ☐ 每個操作步驟對應到具體 component 檔案 + 觸發位置(已完成 §A 內部備註)
2. ☐ 每個中文按鈕 / 文案能對到 i18n key 與行號
3. ☐ 每個 plugin 條件能對到 `type_plugin.rb` / `plan_upgrader.rb` / `shop_default_datas.rb`
4. ☐ 全文無半形 `,` `.` `(` `)` `:` `;` `?` `!` 在 CJK 上下文中(§B regex 跑過)
5. ☐ 全文無 CJK 與 `**` 直接相鄰的情況(§C-2 regex 跑過)
6. ☐ 列表項目皆為單一物理行(§C-1)
7. ☐ 對照表已拆檔到 `docs/{{module}}/references/`,主文用 `data-preview` 跳轉
8. ☐ 新舊版差異(若適用)已用 `=== "..."` 分頁呈現
9. ☐ 所有 heading 錨點符合 `{primary}-{category}-{subtopic}` 格式，無 `{category}-{primary}` 這類 category-first 的舊命名
10. ☐ 步驟中無過長文字，方案差異、錯誤提示、技術細節等已使用 `[^n]` 腳註分離(原則見 §F)
11. ☐ 後續操作使用 `<div class="grid cards">` 搭配 Lucide icons(非普通列表)

---

## E. 嚴禁事項

1. **不憑空捏造** — 任何選項、文案、條件都必須能在程式碼或 i18n 中找到出處
2. **不洩漏內部術語** — 商家文件不出現 plugin code、欄位英文 code、表名、`has_plugin?` 之類
3. **不羅列全部商家不會碰到的細節** — 例如顯示用 column toggle 不要混進「篩選器」段落
4. **不把舊版獨有功能寫進新版章節**(反之亦然)
5. **不用過度技術性的描述** — 「API 回傳 401」 → 「登入過期請重新登入」
6. **不在段落 / 列表內手動換行** — 違反 §C-1,貼上後會跑版
7. **粗體前後缺空格** — `**xxx**` 緊貼 CJK 字元時不會 render(§C-2) 正確格式` **xxx** `
8. **未驗證 UI 元件就寫操作步驟** — 不知道按鈕在哪、Modal 是哪個檔案,就不要描述操作流程。寧可空著請使用者補充,也不要憑印象寫(§A)
9. **CJK 句中使用半形標點** — 違反 §B,影響可讀性與專業度

---

## F. 腳註使用原則

### 為什麼要使用腳註

步驟流程中若混入方案差異、系統錯誤提示、技術細節等次要資訊，會讓步驟變得密密麻麻、難以掃讀。使用 `[^n]` 腳註可將這些「非主線資訊」移出步驟流程，讓每一步驟維持單一動作、一氣呵成。

### 使用時機（僅供參考，非強制規範）

當步驟文字因為以下原因變得過長時，考慮用腳註分離：

* **方案差異**：同一個步驟中對不同方案（一般版 vs PLUS版 vs 企業版）有不同行為描述
* **系統錯誤提示**：步驟中提及的系統擋下訊息或驗證提示原文
* **技術細節**：呼叫後端 API、第三方服務等商家不需要關注的實作細節
* **注意事項展開**：步驟中附帶的多項注意事項清單

此原則是保持步驟可讀性，不要為了用腳註而用腳註。只要步驟本身簡潔清晰，不需要硬拆。

### 格式範例

```markdown
4. 點擊 **「確認下載」**，按 **「確認」** 即會[^1]：
    * 扣除 CYBER 幣或列入對帳單[^2]
    * 呼叫順豐取得新單號
    * 自動下載託運單 PDF

[^1]: 一般版若餘額不足會直接擋下。
[^2]: 一般版立即扣除(單價×張數)；PLUS版/企業版列入對帳單。
```

### 定義位置

腳註定義**不集中放在文末**，而是放在所屬小節結尾、`---` 分隔線之前。這讓閱讀和維護更容易。

---

## 工作流程建議

1. 先用 Explore agent 並行研究:後端篩選定義、前端 UI 元件與觸發點、i18n、plugin 條件(各派一支 agent,單一訊息平行送出)
2. 完成 §A 內部備註:每個操作步驟先列出元件路徑、觸發位置、i18n keys
3. 確認所有可選值的字面與開通條件
4. 列出文件骨架(七大段),向使用者確認結構
5. 撰寫,並對每個對照表標註程式碼出處(內部備註用,不放進文件)
6. 寫完後跑 §D 提交前檢核清單,逐項打勾才交付

---

## 預設交付格式

直接輸出 Markdown 內容(用三個反引號包起來方便複製),並在末尾用簡短文字說明:

* 設計重點(為什麼這樣寫)
* 與既有文件的整合建議(放哪個位置、和哪個段落呼應)
* 若新增了對照表,提供對照表的目標檔案路徑(`docs/{{module}}/references/{{file}}.md`)

---

## 本次任務變數

### 文件情境

| 情境 | 說明 |
|:--|:--|
| `single` | 單一文件，獨立主題（預設） |
| `series` | 多份文件，彼此相關、共用同一套程式碼研究，需一次性產出 |

若為 `series` 情境，請先理解完整主題範圍，再按關聯性分篇撰寫，確保各篇之間用 `data-preview` 互相參照。

### 變數填寫

* **情境**:single

#### 各文件變數

依文件數量重複下列區塊，每份文件一個區塊。單一文件時僅需一組。

```yaml
文件 A:
  category: tcat-shipping
  module: payments-and-logistics
  頁面: /admin/orders
  主題: 宅配通出貨流程
  檔案路徑: docs/payments-and-logistics/tcat-shipping.md
```

**範例（single）：**

```yaml
category: tcat-shipping
module: payments-and-logistics
頁面: /admin/orders
主題: 宅配通出貨流程
檔案路徑: docs/payments-and-logistics/tcat-shipping.md
```

### 其他

* **參考既有文件**:無
* **特別要求**:只需要補操作步驟段落就好，其他部分不用
```
