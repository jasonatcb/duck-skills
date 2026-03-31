# Change Log: screenshotter

All notable changes to this skill will be documented in this file.

| Date | Version | Type | Change Description | Impact/Notes |
| :--- | :--- | :--- | :--- | :--- |
| 2026-03-26 | 1.0.8 | Feature | 完成 GMC 文件完整流程截圖：建立帳戶 → 設定商家資訊 → 驗證網站 → 同步商品 → 設定運送退貨 → 串接 Google Ads。學習並更新 PII 模糊處理流程與座標。 | 完整 GMC 文件。 |
| 2026-03-26 | 1.0.7 | Feature | 新增完整 PII 模糊處理流程：截圖 → 模糊處理 → 驗證 → 建立 GIF。加入常見模糊區域座標參考表（Google GMC 右上角 header）。 | 確保敏感資訊不外洩。 |
| 2026-03-26 | 1.0.5 | Feature | 新增 PII 模糊處理規則：當截圖包含帳號 ID、Email 等敏感資訊時，必須呼叫 screenshotter-blur 技能進行模糊處理。新增 Tabs 使用時機說明（僅複雜步驟）。新增截圖時需提示用戶輸入表單資訊。 | 更完善的隱私保護與 UX。 |
| 2026-03-23 | 1.0.4 | Feature | 新增自動判斷是否需要 GIF 的邏輯。當文檔包含多步驟流程時，自動呼叫 screenshotter-gif 技能。改用 ImageMagick (magick) 替代 ffmpeg。 | screenshotter 與 screenshotter-gif 自動協作。 |
| 2026-03-23 | 1.0.3 | Fix | 更新 GIF 製作原則：只捕捉關鍵狀態，移除多餘的捲動幀，避免來回捲動。新增標準化 create-gif.sh 腳本。 | 技術文件 GIF 更清晰易讀。 |
| 2026-03-23 | 1.0.2 | Feature | 新增瀏覽器缩放 125% 功能以提升截圖解析度。 | 截圖更清晰。 |
| 2026-03-23 | 1.0.1 | Feature | 新增 GIF 合併功能。當單一步驟有多張圖片時，使用 ffmpeg 合併為 GIF。 | 支援連續動作展示。 |
| 2026-03-23 | 1.0.0 | Init | 初始技能建立。 | 建立基線。 |

> **Note:** Versions follow [Semantic Versioning](https://semver.org/): 
> **Major** (breaking changes), **Minor** (new features), **Patch** (bug fixes).

## 版本類型說明
- **Init**: 初始版本
- **Fix**: 錯誤修正
- **Feature**: 新功能
- **Breaking**: 破壞性變更