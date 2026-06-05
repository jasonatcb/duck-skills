---
name: glossary-sync
description: Maintain and synchronize `includes/abbreviations.md` with `docs/resources/glossary.md` for the zensical-zh-tw documentation project. This skill provides multiple subcommands (sync, format, cleanup, check, add) to manage glossary content. Use this whenever the user mentions syncing abbreviations and glossary, updating/refreshing glossary entries, reformatting glossary.md, cleaning up abbreviations.md, adding new glossary terms, checking glossary consistency, or improving glossary SEO. Triggers on phrases like "同步詞彙表", "更新詞彙表", "修正 glossary", "glossary 格式", "新增詞彙", "檢查 glossary". Always offer this skill when glossary-related work is discussed.
version: "1.0.2"
last_updated: 2026-06-01
---

# Glossary Sync for Zensical Documentation

## Overview

Maintain the relationship between `includes/abbreviations.md` (MkDocs abbreviation definitions used for inline tooltips) and `docs/resources/glossary.md` (resource center glossary page). The skill is structured as a set of subcommands — tell it which task you want and it handles the rest.

## Usage

```
glossary-sync <command> [options]
```

### Commands

| Command | Description |
| :--- | :--- |
| `sync` | Convert abbreviations.md entries into glossary.md format, categorize, add 參閱 links. Also cleans up abbreviations.md. |
| `format` | Reformat existing glossary.md to use H3 headings, English annotations, and 參閱 links (without pulling in new terms). |
| `cleanup` | Remove English-only plan entries from abbreviations.md. |
| `check` | Compare abbreviations.md vs glossary.md, report missing/different entries. |
| `add <term>` | Add a new term to both files: insert abbreviation entry + create glossary entry in correct section. |

### Options (apply to all commands)

| Flag | Description |
| :--- | :--- |
| `--dry-run` | Preview changes without modifying files |
| `--verbose` | Show detailed progress for each entry |
| `--source <path>` | Path to abbreviations file (default: `includes/abbreviations.md`) |
| `--target <path>` | Path to glossary file (default: `docs/resources/glossary.md`) |

### Examples

```
glossary-sync sync                       # Full sync
glossary-sync sync --dry-run             # Preview changes only
glossary-sync format --target docs/resources/glossary.md
glossary-sync cleanup --source includes/abbreviations.md
glossary-sync check
glossary-sync add "電子發票" --verbose
```

---

## Glossary Format Standard (applies to all commands that write glossary.md)

Every glossary entry must follow this H3 heading format. **Do not use MkDocs definition lists (`term` + `:`) — always use H3 headings.**

### Template

**English acronym:**

```markdown
### SKU

**Stock Keeping Unit（存貨單位）**，用於識別商品的唯一代碼或編號，用於追蹤庫存、管理商品資料與銷售統計。

- **參閱**：[商品管理操作指南](../../resources/商品管理操作指南.md)
```

**English acronym with counterpart entry (anchor cross-link):**

```markdown
### WMS

**Warehouse Management System（倉儲管理系統）**，用於管理、控制與最佳化倉儲作業，涵蓋入庫、出庫、庫存管理、訂單揀貨與配送流程。

- **參閱**：[串倉](#串倉) | [訂單與物流操作指南](../../resources/訂單物流操作指南.md)
```

**Pure Chinese term (no English annotation):**

```markdown
### 退貨期限

商家規定顧客可申請退貨的最長時間範圍，自顧客收到商品起算。在此期限內，顧客可依退貨政策提出退貨申請；逾期將無法透過系統申請退貨。

- **參閱**：[訂單與物流操作指南](../../resources/訂單物流操作指南.md)
```

### Rules

| Rule | Why |
| :--- | :--- |
| Use `###` (H3) for every term — never `####` or other levels | Each term gets its own auto-generated anchor (`#term`) for direct linking from other pages |
| Only English acronyms/brand names get bold English annotation (**bold**). Pure Chinese terms start directly with the definition, no bold prefix. | Users need English for acronyms they encounter in the UI, but not for Chinese-native terms where English adds no value. |
| Keep definitions to 1–2 sentences, ~30–50 chars max | Readable at a glance; matches the glossary's concise style |
| Abbreviation version wins over existing glossary version | Abbreviation definitions are richer; summarize them to glossary conciseness |
| "參閱" links use relative paths from `docs/resources/glossary.md` | Works with mkdocs-autorefs validation |
| Search `docs/` for the most specific relevant page for each 參閱 link | More useful than generic links |
| If a related term exists in the glossary, link with `[term](#term)` anchor syntax | Creates internal cross-reference network |
| If no relevant doc is found, omit the 參閱 section entirely | Better than dead links |

---

## Command Details

### `sync` — Full Sync

Parses every entry in `includes/abbreviations.md`, converts them to the Glossary Format Standard, and rewrites `docs/resources/glossary.md`.

**Also:** removes English-only plan entries from `abbreviations.md` (see `cleanup`).

**Steps:**

1. Read both files
2. Parse each `*[term]: definition` line
3. Categorize each term using the [Categorization Reference](#categorization-reference)
4. Generate each entry following the [Glossary Format Standard](#glossary-format-standard-applies-to-all-commands-that-write-glossarymd)
5. Assemble glossary.md with frontmatter preserved
6. Sort terms alphabetically within each section (Chinese by stroke, English alphabetically)
7. Clean up abbreviations.md
8. Verify: check all entries accounted for, 參閱 links point to existing files

### `format` — Reformat Only

Reformats the existing `docs/resources/glossary.md` content into H3 headings without pulling in new terms from abbreviations.md.

**Use this when:** you already have the right content but want to improve the format/SEO.

**Steps:**

1. Read existing glossary.md
2. Extract all current entries (both definition list and any pre-existing H3 entries)
3. For each entry, determine the English annotation (search abbreviations.md or infer from context)
4. Rewrite each entry in H3 format
5. Add 參閱 links by searching `docs/` for relevant pages

### `cleanup` — Clean Up abbreviations.md

Removes English-only subscription plan entries from `includes/abbreviations.md`.

**Entries removed:**

- `Regular Plans`
- `PLUS Plans`
- `Professional Plan`
- `Professional PLUS Plan`
- `Advanced Plan`
- `Advanced PLUS Plan`
- `Master Plan`
- `Master PLUS Plan`
- `Enterprise Plan`

**Steps:**

1. Read abbreviations.md
2. Remove the lines matching the entries above
3. Preserve all other entries and their order
4. Write the cleaned file

### `check` — Audit and Compare

Compares `abbreviations.md` against `glossary.md` and reports inconsistencies.

**Reports three categories:**
- **Missing from glossary** — Terms in abbreviations.md that have no matching entry in glossary.md
- **Missing from abbreviations** — Terms in glossary.md that have no matching entry in abbreviations.md
- **Different definitions** — Terms that exist in both but have significantly different definitions

Outputs a summary, not file modifications.

### `add <term>` — Add New Term

Adds a new term to both files.

**Steps:**

1. Determine the correct H2 section from the Categorization Reference (or infer from context if new term)
2. Add a `*[term]: definition` entry to abbreviations.md (insert alphabetically)
3. Add a formatted H3 entry to the correct section in glossary.md (insert alphabetically)
4. If the term doesn't fit any existing H2 section, ask the user where to put it rather than guessing

---

## Categorization Reference

All terms go under one of these H2 section headers. Use this table when categorizing terms.

### 商品

Product display and basic product information.

| Term | English |
| :--- | :--- |
| 商品資訊 | Product Information |
| 商品名稱 | Product Name |
| 商品標語 | Product Slogan |
| 商品簡述 | Product Description |
| 商品頁面 | Product Page |
| 商品網址 | Product URL |
| 商品連結 | Product Link |
| 圖床 | Image Hosting |

### 商品結構與規格

Product structure, bundles, variants, and categories.

| Term | English |
| :--- | :--- |
| 組合商品 | Bundle Product |
| 子商品 | Child Product |
| 指定組合商品 | Fixed Bundle |
| 任選組合商品 | Pick & Mix Bundle |
| 任選組合總數 | Pick & Mix Total |
| 組合品價差 | Bundle Price Difference |
| 加購價格 | Upsell Price |
| 規格 | Specification |
| 規格項目 | Specification Option |
| 款式 | Variant |
| SKU | Stock Keeping Unit |
| 商品通路 | Product Channel |
| 商品通路設定 | Product Channel Setting |
| 商品關聯群組 | Product Relation Group |
| Google 產品類別 | Google Product Category |

### 訂單、付款與物流

Order management, payment processing, and shipping/logistics.

| Term | English |
| :--- | :--- |
| 信用卡一次付清 | Credit Card One-Time Payment |
| 3D 驗證 | 3D Secure |
| OTP | One-Time Password |
| COD | Cash on Delivery |
| 配送條件 | Shipping Condition |
| 配送條件綁定 | Shipping Condition Binding |
| 配送溫層設定 | Delivery Temperature Setting |
| 物流運費設定 | Shipping Fee Setting |
| 正物流 | Forward Logistics |
| 逆物流 | Reverse Logistics |
| 退貨期限 | Return Period |
| 上收服務 | Pickup Service |
| 大宗寄倉 | Bulk Drop-off |
| WMS | Warehouse Management System |
| 串倉 | Warehouse Connection |
| POS | Point of Sale |

### 行銷與成長

Marketing, analytics, advertising, and growth.

| Term | English |
| :--- | :--- |
| 優惠券 | Coupon |
| 優惠碼 | Promo Code |
| EDM | Electronic Direct Mail |
| SEO | Search Engine Optimization |
| GA | Google Analytics |
| GA4 | Google Analytics 4 |
| GSC | Google Search Console |
| GMC | Google Merchant Center |
| MBE | Meta Business Extension |
| FBE | Facebook Business Extension |
| 分潤 | Revenue Share |
| CTR | Click-Through Rate |
| SERP | Search Engine Results Page |
| OG image | Open Graph Image |
| LAP | LINE Ads Platform |
| GTM | Google Tag Manager |
| CPA | Cost Per Action |
| UTM | Urchin Tracking Module |
| ROAS | Return on Ad Spend |
| LINE OA | LINE Official Account |
| LIFF | LINE Front-end Framework |

### 平台、方案與其他

Platform plans, business models, and miscellaneous.

| Term | English |
| :--- | :--- |
| 一般版 | Standard Plan |
| PLUS版 | PLUS Plan |
| Cyber幣 | Cyber Coin |
| EC | E-commerce |
| B2C | Business to Consumer |
| C2C | Consumer to Consumer |
| 分票 | Ticket Splitting |
| 註解程式碼 | Code Commenting |
| UID | Unique Identifier |
| 2FA | Two-Factor Authentication |

---

## abbreviations.md Cleanup (used by `sync` and `cleanup`)

When cleaning up `includes/abbreviations.md`, remove these English-only subscription plan entries:

- `Regular Plans`
- `PLUS Plans`
- `Professional Plan`
- `Professional PLUS Plan`
- `Advanced Plan`
- `Advanced PLUS Plan`
- `Master Plan`
- `Master PLUS Plan`
- `Enterprise Plan`

Keep all other entries — they are used for MkDocs inline abbreviation tooltips.
