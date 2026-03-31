# Change Log: screenshotter-blur

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-03-26 | 1.0.4 | Feature | 新增 OCR 自動偵測 patterns：account_id、gmc_header、ads_id、mc_id，可自動模糊 GMC 帳號名稱與 ID。 | 減少手動模糊需求。 |
| 2026-03-26 | 1.0.3 | Fix | 修正模糊座標學習：當 OCR 無法偵測非標準格式的帳號名稱（如 "Duck, 5753408045"）時，需使用手動模式並指定正確座標區域。更新 SKILL.md 加入常見模糊區域參考表。 | 解決 GMC 帳號模糊失敗問題。 |
| 2026-03-26 | 1.0.2 | Feature | 新增與 screenshotter 技能整合時機：PII 模糊處理必須在建立 GIF **之前**執行，確保最終輸出不含敏感資訊。 | 確保 GIF 輸出不包含 PII。 |
| 2026-03-23 | 1.0.1 | Feature | 新增 smart_blur.py - 使用 OCR 自動偵測 PII 並模糊，無需手動座標。 | 無需指定座標即可模糊。 |
| 2026-03-23 | 1.0.0 | Init | 初始技能建立 - 模糊圖片中的 PII 資訊。 | 與 screenshotter 技能搭配使用。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更
