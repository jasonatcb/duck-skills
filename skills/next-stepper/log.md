# Change Log: next-stepper

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-03-23 | 1.0.0 | Init | 初始技能建立。 | 建立基線。將敘述形式建議轉換為 zensical grid card 布局。 |
| 2026-03-23 | 1.0.1 | Fix | 強化格式規範說明。 | 明確要求 `- :lucide-xxx:{ .lg }` 和 `[__標題__](連結)` 格式。 |
| 2026-03-23 | 1.0.2 | Fix | 新增圖示選擇範例。 | 修正圖示選擇邏輯，禁止使用 `-off`/`-check` 結尾圖示。 |
| 2026-03-23 | 1.0.3 | Fix | 修正卡片開頭符號與屬性格式。 | 明確要求使用 `- ` 開頭，屬性使用 `{ .lg }`。 |
| 2026-03-23 | 1.0.4 | Fix | 修正空連結格式。 | 無論是否有連結，都必須使用 `[__標題__](連結)` 格式。 |
| 2026-03-23 | 1.0.5 | Fix | 修正空連結不帶屬性。 | 空連結 `[__標題__]()` 不加 `{ data-preview }`。 |
| 2026-03-23 | 1.0.6 | Fix | 嚴格規範格式並禁止 Material icons。 | 在檔案開頭新增正確/錯誤格式範例對比，明確禁止使用 Material icons（`:material-xxx:`）、`*` 開頭、`**粗體**`、單行圖示+標題。 |
| 2026-03-23 | 1.0.7 | Feature | 新增 @ 檔案引用輸入方式。 | 現在支援兩種輸入方式：1) @檔案路徑 的 ##章節名稱  2) 直接貼上文字。 |
| 2026-03-26 | 1.0.8 | Feature | 為 GMC 文件更新 後續操作 grid cards：Google Ads 轉換追蹤、Google Analytics 追蹤。修正相對路徑。 | 完善 GMC 後續操作區塊。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
