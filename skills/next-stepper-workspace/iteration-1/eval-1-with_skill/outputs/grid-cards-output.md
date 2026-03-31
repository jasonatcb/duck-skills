## 串接後建議調整項目

為確保數據準確性，建議完成串接後進行以下調整：

<div class="grid cards" markdown>

:lucide-shield:[排除內部流量]{ .card-title }
---
在 GA4 管理介面的「資料串流」中定義公司 IP，避免開發或行銷人員的瀏覽行為干擾分析。

:lucide-link:[列出不適用的參照連結]{ .card-title }
---
將金物流服務商（如 `cyberbizpay.com`、`pay.ecpay.com.tw`、`web-pay.line.me` 等）加入排除名單，以免轉換來源被誤判為第三方金流頁面。

:lucide-clock:[延長資料保留期限]{ .card-title }
---
GA4 預設資料僅保留 2 個月，建議至「資料收集與修改」→「資料保留」中手動改為 **14 個月**。

:lucide-users:[啟用 Google 信號]{ .card-title }
---
開啟此功能可取得跨裝置的使用行為資料與更精確的使用者輪廓。

</div>
