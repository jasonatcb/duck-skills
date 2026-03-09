# duck-skills

一個專為 Duck Center AI 編碼助手操作設計的技能倉庫。

## 概述

此 repo 包含可由 AI 編碼助手加载的可重用技能。每個技能提供領域特定的指令、工作流程和附帶的資源訪問權限。

## 可用技能

### frontmatterer

將 Markdown 文件的 frontmatter 更新為符合標準化的 zensical-zh-tw 結構描述。

**功能說明：**
- 保留已設置的現有欄位值
- 添加缺失的必填和可選欄位
- 重新排序 frontmatter 以符合參考結構描述
- 在變更時更新 `last_modified` 時間戳
- 確保欄位類型和格式符合規範

**主要特點：**
- 語言感知的欄位驗證（內容欄位必須與文檔的 `lang` 匹配）
- 基於結構描述參考的嚴格欄位順序
- 支持多種語言：`zh-TW`、`en-US`、`ja-JP`

**使用方式：**
```
加載 frontmatterer 技能並提供文件路徑以更新其 frontmatter。
```

## 安裝與設定

### 使用 openskills 安裝

openskills 是 2026 年最通用的技能管理工具，支援所有基於 $SKILL.md$ 規範的 AI 代理（如 Claude Code, Cursor, OpenCode）。


``` bash
# 從 GitHub 安裝技能
npx openskills install jasonatcb/duck-skills
```


```bash
# 同步至 AGENTS.md (讓 AI 能夠偵測到新技能)
npx openskills sync
```

### 使用 npx skills add

```bash
# 使用 npx 安裝技能
npx skills add jasonatcb/duck-skills
```

### 手動安裝

```bash
# 複製此倉庫
git clone https://github.com/your-org/duck-skills.git ~/.config/opencode/skills/duck-skills
```

## 使用方式

安裝後，可以通過名稱調用技能：

```
使用 frontmatterer 技能更新 docs/article.md 的 frontmatter
```
## 目錄結構

```
duck-skills/
├── README.md
└── skills/
    └── frontmatterer/
        ├── SKILL.md        # 技能定義和說明
        ├── reference.md    # 完整結構描述規範
        └── example.md      # 轉換前後範例
```

