# Change Log: zh-punct-fixer

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-05-25 | 1.0.0 | Init | 初始技能建立。 | 建立基線。 |
| 2026-06-04 | 1.1.0 | Fix | 補上 `;` 的「後接 CJK」lookahead 規則 (`(?<!CJK);(?=CJK)`)。修正 `**「公開」**;設為` 這類情境。 | 原規則僅處理「前綴 CJK」，遺漏 `}`、`*`、`)` 等非 CJK 文字後的 `;`。 |
| 2026-06-04 | 1.1.0 | Fix | 修正 nested placeholder 還原順序 (reverse insertion order)，避免 lucide icon 嵌入 markdown link 時 placeholder 未正確還原。 | 還原改為由外而內 (`reversed(list(placeholders.keys()))`)。 |
| 2026-06-04 | 1.2.0 | Feature | 新增第三道「廣義上下文」規則：對剩餘的 ASCII `:` `,` `;`，檢查 ±5 字元內雙邊是否都有 CJK。捕獲 `(選填):**`、`(見上方):**` 等模式。 | 需要雙邊都有 CJK 才替換，避免誤觸英文句子。 |
| 2026-06-04 | 1.3.0 | Feature | 新增 `?` → `？` 與 `!` → `！` 支援，套用三層規則（前綴 CJK / 後綴 CJK / 廣義上下文）。 | 涵蓋 FAQ 提問句與驚嘆句。 |
| 2026-06-04 | 1.3.0 | Fix | 移除 admonition early-return（`^!!!\s+`、`^\?\?\?\s+` 的行級略過），讓 `??? quote` 和 `!!! note` 標題內文也能被修正。 | 之前 `??? quote "設定條件，卻?"` 整行被跳過不處理。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/):
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
