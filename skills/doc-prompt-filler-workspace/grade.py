"""Grade doc-prompt-filler test outputs."""
import json, re, sys, os
from pathlib import Path

BASE = Path("/Users/jason.ke/.config/opencode/skills/doc-prompt-filler-workspace/iteration-1")

D = {
    "eval-1-single-search-and-filter": {
        "with_skill": BASE / "eval-1-single-search-and-filter/with_skill/outputs/prompt-output.md",
        "without_skill": BASE / "eval-1-single-search-and-filter/without_skill/outputs/prompt-output.md",
        "assertions": [
            ("Task has /admin/orders_v2 and 訂單搜尋與篩選", lambda t: "/admin/orders_v2" in t and "訂單搜尋與篩選" in t),
            ("情境 set to single", lambda t: bool(re.search(r'\*\*情境\*\*[：:]\s*single', t) or re.search(r'\*[\s\*]*情境[\s\*]*[：:]\s*single', t))),
            ("category is search-and-filter", lambda t: "search-and-filter" in t),
            ("module is orders", lambda t: "module: orders" in t or "module: orders" in t),
            ("檔案路徑: docs/orders/search-and-filter.md", lambda t: "docs/orders/search-and-filter.md" in t),
            ("Heading anchors use search-and-filter", lambda t: "intro-search-and-filter" in t or "operate-search-and-filter" in t),
        ]
    },
    "eval-2-single-tcat-shipping": {
        "with_skill": BASE / "eval-2-single-tcat-shipping/with_skill/outputs/prompt-output.md",
        "without_skill": BASE / "eval-2-single-tcat-shipping/without_skill/outputs/prompt-output.md",
        "assertions": [
            ("Task has /admin/orders and 宅配通出貨流程", lambda t: "/admin/orders" in t and "宅配通出貨流程" in t),
            ("情境 set to single", lambda t: bool(re.search(r'\*[\s\*]*情境[\s\*]*[：:]\s*single', t))),
            ("category is tcat-shipping", lambda t: "tcat-shipping" in t),
            ("module is payments-and-logistics", lambda t: "payments-and-logistics" in t),
            ("檔案路徑: docs/payments-and-logistics/tcat-shipping.md", lambda t: "docs/payments-and-logistics/tcat-shipping.md" in t),
            ("Heading anchors use tcat-shipping", lambda t: "intro-tcat-shipping" in t or "operate-tcat-shipping" in t),
            ("特別要求 included", lambda t: "只需要補操作步驟段落" in t),
        ]
    },
    "eval-3-series-cvs-delivery": {
        "with_skill": BASE / "eval-3-series-cvs-delivery/with_skill/outputs/prompt-output.md",
        "without_skill": BASE / "eval-3-series-cvs-delivery/without_skill/outputs/prompt-output.md",
        "assertions": [
            ("情境 set to series", lambda t: bool(re.search(r'\*[\s\*]*情境[\s\*]*[：:]\s*`?series`?', t))),
            ("關聯文件 chain included", lambda t: "超商取貨設定" in t and "超商出貨流程" in t and "配送狀態對照表" in t),
            ("文件 A: cvs-pickup-setting", lambda t: "cvs-pickup-setting" in t),
            ("文件 A 頁面 /admin/logistics/cvs", lambda t: "/admin/logistics/cvs" in t),
            ("文件 B: cvs-shipping", lambda t: "cvs-shipping" in t),
            ("文件 C: delivery-status", lambda t: "delivery-status" in t),
            ("All three file paths distinct", lambda t: len(set(re.findall(r'docs/payments-and-logistics/[a-z-]+\.md', t))) >= 3),
        ]
    }
}

for eval_name, config in D.items():
    for cond, path in [("with_skill", config["with_skill"]), ("without_skill", config["without_skill"])]:
        if not path.exists():
            print(f"MISSING: {path}")
            continue
        text = path.read_text()
        results = []
        passed = 0
        for i, (desc, check_fn) in enumerate(config["assertions"]):
            ok = check_fn(text)
            results.append({
                "text": desc,
                "passed": ok,
                "evidence": f"Found in output" if ok else "Not found in output"
            })
            if ok:
                passed += 1
        grading = {
            "expectations": results,
            "summary": {
                "passed": passed,
                "failed": len(results) - passed,
                "total": len(results),
                "pass_rate": round(passed / len(results), 2)
            }
        }
        grading_path = path.parent.parent / "grading.json"
        grading_path.write_text(json.dumps(grading, ensure_ascii=False, indent=2))
        print(f"{eval_name}/{cond}: {passed}/{len(results)} passed ({grading['summary']['pass_rate']:.0%})")
