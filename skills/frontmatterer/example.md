# Frontmatter Transformation Examples

## Example 1: Minimal frontmatter → Complete

**Before:**
```yaml
---
title: 設定電子票券
created: 2026-03-01 10:00
products: ["EC"]
---
```

**After:**
```yaml
---
title: 設定電子票券
description:
created: 2026-03-01 10:00
last_modified: 2026-03-07 14:30
lang: zh-TW
type:
status:
version:
author:
reviewers: []
notes: []
ga_views: 0
feedback: 0
products: ["EC"]
modules: []
sites: []
audiences: []
difficulty:
tnb:
plans: []
cyb_extensions: []
intents: []
features: []
prerequisites: []
related: []
tags: []
acoiv:
apis: []
devices: []
ui_components: []
paths: []
layouts: []
wp_url: []
permalink:
comments: false
search:
  exclude: false
icon:
hide: []
---
```

## Example 2: Out-of-order fields → Reordered

**Before:**
```yaml
---
products: ["EC", "POS"]
title: 智能 POS 設定指南
permalink: /pos/setup-guide
created: 2026-02-15 09:30
type: guide
lang: zh-TW
description: 完整的 POS 系統設定教學
audiences: ["merchant", "clerk"]
---
```

**After:**
```yaml
---
title: 智能 POS 設定指南
description: 完整的 POS 系統設定教學
created: 2026-02-15 09:30
last_modified: 2026-03-07 14:30
lang: zh-TW
type: guide
status:
version:
author:
reviewers: []
notes: []
ga_views: 0
feedback: 0
products: ["EC", "POS"]
modules: []
sites: []
audiences: ["merchant", "clerk"]
difficulty:
tnb:
plans: []
cyb_extensions: []
intents: []
features: []
prerequisites: []
related: []
tags: []
acoiv:
apis: []
devices: []
ui_components: []
paths: []
layouts: []
wp_url: []
permalink:
comments: false
search:
  exclude: false
icon:
hide: []
---
```

## Example 3: Complete frontmatter with all fields

**After (fully populated):**
```yaml
---
title: 電子票券核銷完整指南
description: 詳細說明如何使用 CYBERBIZ POS 系統核銷電子票券，包含各種核銷場景與常見問題排解
created: 2026-01-10 14:00
last_modified: 2026-03-07 14:30
lang: zh-TW
type: tutorial
status: update
version: v2.1
author: Jase
reviewers: ["Amy", "Kevin"]
notes: ["需要更新截圖", "等待產品確認新流程"]
ga_views: 1250
feedback: 42
products: ["EC", "POS"]
modules: ["票券管理", "POS 核銷"]
sites: ["TW", "JP"]
audiences: ["merchant", "clerk"]
difficulty: beginner
tnb: trunk
plans: ["進階", "高手", "企業"]
cyb_extensions: ["STORE PAL"]
intents: ["如何核銷票券", "票券核銷失敗怎麼辦"]
features: ["票券掃碼核銷", "手動輸入核銷碼", "批次核銷"]
prerequisites:
  - "[[設定電子票券]]"
related:
  - "[[設定網站安全性]]"
  - "[[新增網站管理員並設定權限]]"
  - "[[POS 報表列表與功能說明]]"
tags: ["電子票券", "核銷", "POS", "STORE PAL"]
acoiv: operation
apis: ["/api/v1/tickets/verify", "/api/v1/tickets/redeem"]
devices: ["mobile", "tablet"]
ui_components: ["掃碼器", "核銷按鈕", "票券詳情彈窗"]
paths: ["票券管理 > 核銷記錄", "POS > 核銷"]
layouts: ["classic"]
wp_url: ["https://www.cyberbiz.io/support/ticket-redemption"]
permalink:
comments: true
search:
  exclude: false
icon: lucide/ticket-check
hide: []
---
```

## Notes

- All existing values are preserved
- Missing fields are added with appropriate defaults
- Field order matches `reference.md` exactly
- `last_modified` is always updated to current timestamp
- `created` is never changed
