# Change Log: evaluator (文件品質檢查)

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-04-09 | 1.0.6 | Fix | QA 檢查時發現 related 欄位若引用已存在的檔案，應使用 Obsidian wikilink 格式 `"[[filename]]"` 而非純字串。 | 修正 SKILL.md 中的 wikilink 格式說明，確保 related/prerequisites 使用正確格式。 |
| 2026-03-26 | 1.0.5 | Fix | QA 檢查並修正 GMC 文件：移除重複的 `---` 分隔符號，驗證 related wikilinks 指向的檔案存在。 | 確保文件格式正確。 |
| 2026-03-18 | 1.0.4 | Feature | 新增 subtitle 自動修正：若 description 有值但 { .subtitle } 前無文字，自動提取 description 填入。 | 確保 subtitle 與 description 一致。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
