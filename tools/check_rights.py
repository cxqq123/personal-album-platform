#!/usr/bin/env python3
"""校验图像版权清单 content/rights/artworks.csv（并交叉校验 sources.csv）。

用法：
    python3 tools/check_rights.py            # 日常校验
    python3 tools/check_rights.py --strict   # 发布前（必须全部 ready + 可商用）
    python3 tools/check_rights.py --episode E01   # 只看某一期

只依赖标准库。
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "content" / "rights" / "artworks.csv"
SRC_PATH = ROOT / "content" / "rights" / "sources.csv"

# 所有行都必须有的字段
BASE_REQUIRED = [
    "status", "id", "episode", "artist", "title_zh",
    "museum", "source", "license",
]

# ready 行必须完整（对应上架四个要件）
READY_REQUIRED = [
    "license_marker",    # ③ 页面授权标识
    "source_page_url",   # ② 图片直接来源
    "image_url",         # ② 图片直链
    "license_url",       # ③ 页面授权标识
    "credit_line",       # 永久署名
    "accessed_date",     # ④ 获取日期
    "checked_by",
    "commercial_ok",
]

STATUSES = {"draft", "ready"}

LICENSES = {
    "PD", "PDM", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0",
    "CC-BY-NC-4.0", "CC-BY-ND-4.0", "ARR", "UNKNOWN",
}

# 页面授权标识（第 ③ 项）
MARKERS = {
    "CC0",            # 馆方明确标注 CC0
    "PDM",            # Public Domain Mark
    "CC-BY-4.0",      # 需署名
    "FAITHFUL_REPRO", # 忠实摄影副本（PD-Art）
    "INSTITUTIONAL",  # 馆方自有条款
    "NONE",           # 无标识
}

COMMERCIAL_LICENSES = {"PD", "PDM", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0"}
COMMERCIAL_FLAGS = {"yes", "no", "unknown"}

# 标识与协议必须自洽
MARKER_TO_LICENSE = {
    "CC0": {"CC0-1.0"},
    "PDM": {"PD", "PDM"},
    "CC-BY-4.0": {"CC-BY-4.0", "CC-BY-SA-4.0"},
    "FAITHFUL_REPRO": {"PD", "PDM", "UNKNOWN"},
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EPISODE_RE = re.compile(r"^E\d{2}$")


def load_sources() -> dict[str, dict]:
    if not SRC_PATH.exists():
        return {}
    with SRC_PATH.open(encoding="utf-8-sig", newline="") as fh:
        return {r["code"].strip(): r for r in csv.DictReader(fh) if r.get("code")}


def main() -> int:
    strict = "--strict" in sys.argv
    episode = None
    if "--episode" in sys.argv:
        episode = sys.argv[sys.argv.index("--episode") + 1].upper()

    if not CSV_PATH.exists():
        print(f"✗ 找不到清单：{CSV_PATH}")
        return 1

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    sources = load_sources()
    errors: list[str] = []
    warnings: list[str] = []

    missing_cols = [c for c in BASE_REQUIRED if c not in header]
    if missing_cols:
        print(f"✗ 缺少必需列：{', '.join(missing_cols)}")
        return 1

    seen: dict[str, int] = {}
    counts = {"yes": 0, "no": 0, "unknown": 0}
    ready = 0
    per_episode: dict[str, int] = {}

    for i, row in enumerate(rows, start=2):
        rid = (row.get("id") or "").strip()
        where = f"第 {i} 行" + (f"（{rid}）" if rid else "")
        status = (row.get("status") or "").strip().lower()
        ep = (row.get("episode") or "").strip().upper()

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

        if ep:
            per_episode[ep] = per_episode.get(ep, 0) + 1
            if not EPISODE_RE.match(ep):
                errors.append(f"{where}: episode 应形如 E01")

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

        marker = (row.get("license_marker") or "").strip()
        if marker and marker not in MARKERS:
            errors.append(f"{where}: license_marker '{marker}' 不在枚举内")
        elif marker in MARKER_TO_LICENSE and lic:
            if lic not in MARKER_TO_LICENSE[marker]:
                errors.append(
                    f"{where}: license_marker={marker} 与 license={lic} 不匹配"
                )

        src = (row.get("source") or "").strip()
        if src and sources and src not in sources:
            errors.append(f"{where}: source '{src}' 未在 sources.csv 登记")
        elif src in sources and sources[src].get("commercial_default") == "no":
            warnings.append(f"{where}: 来源 {src} 默认不可商用，需替代来源")

        ok = (row.get("commercial_ok") or "").strip().lower()
        if ok and ok not in COMMERCIAL_FLAGS:
            errors.append(f"{where}: commercial_ok 只能是 yes / no / unknown")
        elif ok:
            counts[ok] += 1

        if ok == "yes" and lic and lic not in COMMERCIAL_LICENSES:
            errors.append(f"{where}: commercial_ok=yes 但 {lic} 不允许商用")

        for col in ("source_page_url", "image_url", "license_url"):
            val = (row.get(col) or "").strip()
            if val and not val.startswith("https://"):
                errors.append(f"{where}: {col} 必须是 https 链接")

        for col in ("accessed_date",):
            val = (row.get(col) or "").strip()
            if val and not DATE_RE.match(val):
                errors.append(f"{where}: {col} 应为 YYYY-MM-DD")

        if status == "ready" and lic == "UNKNOWN":
            errors.append(f"{where}: ready 状态不允许 UNKNOWN 协议")
        if status == "draft":
            warnings.append(f"{where}: 草稿，不得出现在已发布内容中")

    if episode:
        rows = [r for r in rows if (r.get("episode") or "").upper() == episode]
        print(f"（筛选：{episode}）")

    print("清单：content/rights/artworks.csv")
    print(
        f"共 {len(rows if episode else seen)} 件｜ready {ready}｜可商用 {counts['yes']}"
        f"｜不可商用 {counts['no']}｜未核实 {counts['unknown']}"
    )
    if per_episode and not episode:
        print("分期：" + "　".join(f"{k} {v} 件" for k, v in sorted(per_episode.items())))

    if warnings:
        print(f"\n⚠ {len(warnings)} 条提示：")
        for w in warnings[:15]:
            print(f"  - {w}")
        if len(warnings) > 15:
            print(f"  … 另有 {len(warnings) - 15} 条")

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
            print(f"\n✗ 严格模式：{len(blockers)} 件未就绪或不可商用，禁止发布：")
            for r in blockers[:20]:
                print(
                    f"  - {r.get('id')}｜status={(r.get('status') or '?')}"
                    f"｜license={(r.get('license') or '?')}"
                )
            return 1
        print("\n✓ 严格模式通过：全部条目已核实且可商用")

    print("\n✓ 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
