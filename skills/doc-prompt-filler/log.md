# Change Log: Doc Prompt Filler

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2025-05-25 | 1.0.0 | Init | 初始技能建立。引導使用者填寫 doc-generator.md 的各文件變數，產出完整的提示詞供複製到 Firebase CYBERBIZ 後端專案的 Claude Code 中使用。 | 建立基線。 |
| 2025-05-25 | 1.0.1 | Fix | 明確指示替換 heading anchors 中的 `{category}` placeholder。 | 修復 with-skill 產出中 heading anchor 仍殘留 `{category}` 的問題。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
