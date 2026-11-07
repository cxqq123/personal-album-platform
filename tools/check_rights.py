#!/usr/bin/env python3
"""校验图像版权清单 content/rights/artworks.csv。

用法：
    python3 tools/check_rights.py            # 日常校验（格式 + 矛盾）
    python3 tools/check_rights.py --strict   # 发布前（必须全部 ready 且可商用）

只依赖标准库。
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "content" / "rights" / "artworks.csv"

# 所有行都必须有的字段
BASE_REQUIRED = ["status", "id", "title_zh", "museum", "source_url", "license"]

# status=ready 的行必须完整填写
READY_REQUIRED = ["figure", "commercial_ok", "credit_line", "checked_date", "checked_by"]

STATUSES = {"draft", "ready"}

LICENSES = {
    "PD", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0",
    "CC-BY-NC-4.0", "CC-BY-ND-4.0", "ARR", "UNKNOWN",
}

# 允许商用的协议
COMMERCIAL_LICENSES = {"PD", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0"}

COMMERCIAL_FLAGS = {"yes", "no", "unknown"}


def main() -> int:
    strict = "--strict" in sys.argv

    if not CSV_PATH.exists():
        print(f"✗ 找不到清单：{CSV_PATH}")
        return 1

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    errors: list[str] = []
    warnings: list[str] = []

    missing_cols = [c for c in BASE_REQUIRED if c not in header]
    if missing_cols:
        print(f"✗ 缺少必需列：{', '.join(missing_cols)}")
        return 1

    seen: dict[str, int] = {}
    counts = {"yes": 0, "no": 0, "unknown": 0}
    ready = 0

    for i, row in enumerate(rows, start=2):  # 行号从表格第 2 行算起（含表头）
        rid = (row.get("id") or "").strip()
        where = f"第 {i} 行" + (f"（{rid}）" if rid else "")
        status = (row.get("status") or "").strip().lower()

        for col in BASE_REQUIRED:
            if not (row.get(col) or "").strip():
                errors.append(f"{where}: 必填字段 {col} 为空")

        if status and status not in STATUSES:
            errors.append(f"{where}: status 只能是 draft / ready")
        if status == "ready":
            ready += 1
            for col in READY_REQUIRED:
                if not (row.get(col) or "").strip():
                    errors.append(f"{where}: ready 状态缺少 {col}")
        elif status == "draft":
            warnings.append(f"{where}: 草稿，不得出现在已发布内容中")

        if rid:
            if rid != rid.lower():
                errors.append(f"{where}: id 必须全小写")
            if rid in seen:
                errors.append(f"{where}: id 与第 {seen[rid]} 行重复")
            else:
                seen[rid] = i

        lic = (row.get("license") or "").strip()
        if lic and lic not in LICENSES:
            errors.append(f"{where}: license '{lic}' 不在枚举内")

        ok = (row.get("commercial_ok") or "").strip().lower()
        if ok and ok not in COMMERCIAL_FLAGS:
            errors.append(f"{where}: commercial_ok 只能是 yes / no / unknown")
        elif ok:
            counts[ok] += 1

        url = (row.get("source_url") or "").strip()
        if url and not url.startswith("https://"):
            errors.append(f"{where}: source_url 必须是 https 链接")

        # 矛盾检测：声称可商用，协议却不允许
        if ok == "yes" and lic and lic not in COMMERCIAL_LICENSES:
            errors.append(f"{where}: commercial_ok=yes 但 {lic} 不允许商用")

        # 提示：协议允许但没标 yes
        if lic in COMMERCIAL_LICENSES and ok in {"", "unknown"}:
            warnings.append(f"{where}: 协议 {lic} 可商用，但 commercial_ok 未标 yes")

        if lic == "UNKNOWN" and status == "ready":
            errors.append(f"{where}: ready 状态不允许 UNKNOWN 协议")

    total = len(rows)
    print(f"清单：content/rights/artworks.csv")
    print(
        f"共 {total} 条｜ready {ready}｜可商用 {counts['yes']}"
        f"｜不可商用 {counts['no']}｜未核实 {counts['unknown']}"
    )

    if warnings:
        print(f"\n⚠ {len(warnings)} 条提示：")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n✗ {len(errors)} 个错误：")
        for e in errors:
            print(f"  - {e}")
        return 1

    if strict:
        blockers = [
            r for r in rows
            if (r.get("status") or "").strip().lower() != "ready"
            or (r.get("commercial_ok") or "").strip().lower() != "yes"
        ]
        if blockers:
            print(f"\n✗ 严格模式：{len(blockers)} 条未就绪或不可商用，禁止发布：")
            for r in blockers[:20]:
                print(
                    f"  - {r.get('id')}｜status={(r.get('status') or '?')}"
                    f"｜license={(r.get('license') or '?')}"
                    f"｜commercial_ok={(r.get('commercial_ok') or '?')}"
                )
            return 1
        print("\n✓ 严格模式通过：全部条目已核实且可商用")

    print("\n✓ 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
