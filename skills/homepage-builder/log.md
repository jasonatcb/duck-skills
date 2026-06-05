# Change Log: Homepage Builder

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-05-31 | 1.0.0 | Init | 初始技能建立。從 homepage_ec.html 開發過程中提取的 Zensical 自訂首頁模板模式。 | 建立基線。涵蓋 Jinja2 區塊合約、CSS 架構、深色模式策略、JS 模式、SPA 繞過繼承。 |
| 2026-05-31 | 1.1.0 | Feature | 新增 homepage_resources.html 模式：highlight section、large card variant、zero-invention 原則。 | 新增 `ec-highlight`、`ec-card.large` 模式。記錄「先重用、後發明」原則。修正 hero background 顏色不一致（gradient → 統一 solid primary-container）。移除 17 個未使用的 :root 變數。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
