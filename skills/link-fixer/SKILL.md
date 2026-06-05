---
name: link-fixer
description: >
  修復 Zensical 文檔中的連結問題。檢測並修正失效連結（目標檔案不存在）、
  將 `{ data-preview }` 替換為 `{ title="..." }`（從目標頁面 frontmatter
  自動擷取標題）。當用戶說「修復連結」、「連結壞掉」、「連結不正確」、
  「修正連結路徑」、「fix links」、「links not working」、「fix broken links」、
  「fix 參考資料」或類似意圖時觸發。也用於任何情境下用戶指出文檔中的
  markdown 連結目標路徑錯誤或需要移除 `{ data-preview }` 屬性時。
version: "1.0.0"
last_updated: 2026-05-26
---

# Link Fixer (連結修復技能)

修復 Zensical 文檔中的連結問題，包含失效路徑修正與 `{ data-preview }` 屬性替換。

## 觸發時機

用戶說「修復連結」、「連結壞掉」、「fix links」、「links not working」、
「修正 參考資料」、「fix 參考資料」等，或明確指出某個文檔的連結路徑錯誤、
`{ data-preview }` 需要移除時。

## 工作流程

### 1. 讀取目標文件

使用 Read 工具完整讀取文件內容。紀錄文件所在目錄（用於解析相對路徑）。

### 2. 掃描與檢測

從文件中擷取所有 markdown 連結 `[text](path){ attributes }`，檢查以下問題：

#### 問題類型 A：連結目標不存在（Broken Link）

- 找出所有相對路徑的 markdown 連結（指向 `.md` 檔案的）
- 以文件所在目錄為基準解析絕對路徑
- 使用 Glob 確認目標檔案是否存在
- 若不存在，標記為「連結目標不存在」

#### 問題類型 B：`{ data-preview }` 未替換為 `{ title }`

- 找出所有帶 `{ data-preview }` 屬性的連結
- 若未搭配 `title` 屬性，標記為「data-preview 需替換為 title」

#### 問題類型 C：連結文字與目標不符（選擇性）

- 比對連結顯示文字與目標頁面的 `title` frontmatter
- 若明顯不符（例如連結文字是「計費方式」但目標頁面標題是「物流中心」），標記為「連結文字可能錯誤」

### 3. 呈現檢測結果

列出所有發現的問題，格式如下：

```
在「檔案名稱.md」中發現以下問題：

[1] 🔗 連結目標不存在
    原始路徑: docs/ec/payments-and-logistics/references/cvs-b2c-logistics-centers.md
    所在行數: 223
    建議修正: docs/ec/payments-and-logistics/references/超商大宗寄倉 B2C 物流中心對照.md

[2] 🏷️  data-preview 需替換為 title
    原始連結: [物流中心收貨資訊](...){ data-preview }
    所在行數: 223
    建議修正: [物流中心收貨資訊](...){ title="超商大宗寄倉 B2C 物流中心對照" }

請問要修復哪些問題？(可以說「全部」或列出編號，如「1,2」)
```

### 4. 執行修復

依用戶選擇，逐一執行修復。

#### 4.1 修復連結目標不存在

**尋找正確檔案：**

1. 取得原始路徑的目錄部分（例如 `docs/ec/payments-and-logistics/references/`）
2. 使用 Glob 列出該目錄下所有 `.md` 檔案
3. 透過比對關鍵字找出最匹配的檔案：

   常見的關鍵字對應：
   - `cvs` / `convenience-store` → `超商`
   - `logistics-centers` / `centers` → `物流中心`
   - `channels` / `specs` → `通路規格` / `規格`
   - `plans` / `billing` → `方案` / `計費`
   - `b2c` → `B2C`
   - `guide` → `指南` / `使用`
   - `reference` → `對照` / `參考`

4. 若只有一個高度匹配的結果，直接採用；若有多個或無匹配，詢問用戶確認
5. 使用 Read 讀取正確檔案的 frontmatter，取得 `title` 欄位

**更新連結語法：**

```markdown
# 舊（目標不存在 + data-preview）
[連結文字](../references/old-broken-path.md){ data-preview }

# 新（正確路徑 + title 屬性）
[連結文字](../references/正確路徑.md){ title="目標頁面 frontmatter 的 title" }
```

#### 4.2 替換 data-preview 為 title

對於目標已存在的連結：

1. 使用 Read 讀取目標檔案的 frontmatter，取得 `title` 欄位
2. 將 `{ data-preview }` 替換為 `{ title="<目標頁面的 title>" }`

```markdown
# 舊
[連結文字](path/to/file.md){ data-preview }

# 新
[連結文字](path/to/file.md){ title="目標頁面標題" }
```

#### 4.3 修復連結文字不符

將連結顯示文字更新為目標頁面的 `title` frontmatter 值。

### 5. 更新時間

修復後更新 `last_modified` 為當前時間 `YYYY-MM-DD HH:mm`。

### 6. 回報結果

向用戶簡要說明修復了哪些問題：

```
已修復 3 個問題：
✓ 修正 2 個連結路徑（cvs-b2c-centers → 超商大宗寄倉...）
✓ 替換 3 個 data-preview 為 title
```

## 注意事項

- 始終先確認目標檔案是否存在再讀取 frontmatter
- 如果目標檔案不存在也無法自動找到替代檔案：
  - 優先詢問用戶是否要 **直接註解掉整行／整張 grid card**（使用 `<!-- -->`）
  - 若用戶同意，移除 `{ data-preview }` 後用 `<!-- -->` 包裹整段連結
- **參考資料區段的連結**：通常不需要 `{ title="..." }` 屬性，直接使用純連結即可（除非用戶明確要求補上 title）
- 不要在 code blocks 或 frontmatter 中搜尋連結
- 外部 URL（`https://`、`http://`）不需檢查目標是否存在
- 圖片連結（`![alt](path)`）不屬於本技能處理範圍，除非是 `{ data-preview }` 誤用在圖片上
