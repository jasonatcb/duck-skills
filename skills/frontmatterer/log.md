# Change Log: frontmatterer (Frontmatter 更新器)

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-03-26 | 1.0.9 | Feature | 更新 GMC 文件 frontmatter：重新排序符合 schema，新增 related 文件連結（Google Ads、GA4），修正 sites 值為 TW。 | 完整 GMC 文件 frontmatter。 |
| 2026-03-25 | 1.0.8 | Fix | 更新 SKILL.md 與 reference.md：明確說明 prerequisites 無相關文檔時使用純字串格式 `- 文字` 而非 wikilink。 | 確保技能文件與實際行為一致。 |
| 2026-03-25 | 1.0.7 | Feature | 新增 prerequisites 進階規則：有特定標題用 `[[filename#heading]]`，無則用 `[[doc title]]`，無相關文檔時用純字串。 | 更靈活的先備知識引用方式。 |
| 2026-03-25 | 1.0.6 | Fix | 修正 paths 規則：外部服務（如 GA4）路徑需加上服務名稱前綴以區分 CYBERBIZ 後台路徑。 | 避免路徑混淆。 |
| 2026-03-25 | 1.0.5 | Fix | 修正 paths 規則：應使用文檔內容中提及的導航路徑，而非 zensical.toml 選單名稱。 | 更準確反映路徑欄位用途。 |
| 2026-03-25 | 1.0.4 | Fix | 新增規則：新增 related/prerequisites 前必須驗證文檔確實存在，並說明 paths 應參照 zensical.toml 確認正確選單名稱。 | 避免引用不存在的文檔與錯誤路徑。 |
| 2026-03-25 | 1.0.3 | Fix | 將 paths 纳入 essential content fields 規則。 | 確保路徑欄位不遺漏。 |
| 2026-03-25 | 1.0.2 | Fix | 新增 essential content fields 規則（intents, features, prerequisites, related, tags 不應為空），並說明 status 欄位預設為空字串。 | 確保文件完整性与一致性。 |
| 2026-03-18 | 1.0.1 | Fix | 修正多個文件 frontmatter，包括 Google Tag Assistant 與 Google 商家檔案。 | 新增 intents、features、tags、acoiv、paths 等欄位。 |
| 2026-03-18 | 1.0.0 | Init | 初始技能建立。 | 建立基線。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
